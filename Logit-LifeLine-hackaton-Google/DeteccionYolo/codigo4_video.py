import cv2
import time
import requests
import json
import os
from datetime import datetime
from ultralytics import YOLO
import numpy as np

class FallDetector:
    def __init__(self, video_path=None, camera_id="CAM-007", direccion="Av. Siempre Viva 742", 
                 api_endpoint="http://your-api-endpoint.com/api/incidents"):
        # Configuración
        self.video_path = video_path
        self.camera_id = camera_id
        self.direccion = direccion
        self.api_endpoint = api_endpoint
        
        # Cargar modelos YOLO
        self.person_model = YOLO("yolov8n.pt")  # Modelo para detectar personas
        self.furniture_model = YOLO("yolov8n.pt")  # Puedes cambiar por tu modelo personalizado
        
        # IDs de clases de muebles en COCO dataset
        self.furniture_classes = {
            56: "SILLA",      # silla
            57: "SOFA",      # sofá
            59: "CAMA",        # cama
            61: "MESA"  # mesa (opcional)
        }
        
        # Variables para seguimiento de caídas
        self.fall_detected = False
        self.fall_start_time = None
        self.fall_duration_threshold = 5.0  # Reducido a 3 segundos para pruebas más rápidas
        self.notification_sent = False
        
        # SISTEMA DE MEMORIA DE MUEBLES (solución a oclusión)
        self.furniture_memory = []  # Memoria persistente de muebles
        self.furniture_memory_timeout = 300  # 5 minutos sin detectar para olvidar mueble
        self.furniture_detection_interval = 30  # Buscar muebles cada 30 frames (más frecuente para video)
        self.frame_count = 0
        
        # SISTEMA DE ANÁLISIS DE MOVIMIENTO
        self.prev_frame = None
        self.movement_threshold = 1000  # Umbral de movimiento para considerar "caída súbita"
        
        # SISTEMA DE ALTURA RELATIVA
        self.floor_reference = None  # Referencia del "suelo" para calcular alturas
        
        # Variables visuales
        self.zone_colors = [(255, 0, 255), (255, 255, 0), (0, 255, 255), (255, 128, 0)]
        self.show_zones = True
        self.show_debug = False  # Información de debug
        
        # Crear directorio para imágenes si no existe
        self.image_dir = "fall_incidents"
        os.makedirs(self.image_dir, exist_ok=True)
        
        # Variables para control de reproducción de video
        self.paused = False
        self.playback_speed = 1.0  # Velocidad de reproducción (1.0 = normal)
        self.frame_delay = 10  # Delay en millisegundos entre frames
        
        # Configurar captura de video
        self.setup_video_capture()
        
        print("\n🏠 DETECTOR DE CAÍDAS CON ANTI-OCLUSIÓN (Modo Video)")
        print("• Sistema de memoria de muebles (persisten aunque se oculten)")
        print("• Análisis de movimiento súbito para detectar caídas reales")
        print("• Análisis de altura relativa del suelo")
        print("\n🎥 CONTROLES DE VIDEO:")
        print("• ESPACIO - Pausar/Reanudar")
        print("• 'S' - Avanzar frame por frame (cuando pausado)")
        print("• '+' / '-' - Aumentar/Disminuir velocidad")
        print("• 'R' - Reiniciar video")
        print("• Flechas ← → - Saltar 5 segundos")
        print("\n🔧 CONTROLES DEL DETECTOR:")
        print("• 'F' - Forzar escaneo de muebles")
        print("• 'T' - Alternar visualización de zonas")
        print("• 'D' - Alternar modo debug")
        print("• 'M' - Resetear memoria de muebles")
        print("• ESC - Salir\n")
    
    def setup_video_capture(self):
        """Configura la captura de video o cámara"""
        if self.video_path and os.path.exists(self.video_path):
            self.cap = cv2.VideoCapture(self.video_path)
            self.using_video = True
            
            # Obtener información del video
            self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
            self.fps = self.cap.get(cv2.CAP_PROP_FPS)
            self.duration = self.total_frames / self.fps if self.fps > 0 else 0
            
            print(f"📹 Video cargado: {self.video_path}")
            print(f"📊 Frames: {self.total_frames}, FPS: {self.fps:.1f}, Duración: {self.duration:.1f}s")
        else:
            self.cap = cv2.VideoCapture(0)
            self.using_video = False
            self.total_frames = 0
            self.fps = 30
            print("📷 Usando cámara web")
            
            if self.video_path:
                print(f"⚠️ No se pudo cargar el video: {self.video_path}")
    
    def get_video_progress(self):
        """Obtiene el progreso actual del video"""
        if not self.using_video:
            return 0, 0, "LIVE"
        
        current_frame = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
        current_time = current_frame / self.fps if self.fps > 0 else 0
        progress_percent = (current_frame / self.total_frames * 100) if self.total_frames > 0 else 0
        
        time_str = f"{current_time:.1f}s / {self.duration:.1f}s ({progress_percent:.1f}%)"
        return current_frame, current_time, time_str
    
    def seek_video(self, seconds):
        """Salta a una posición específica en el video"""
        if not self.using_video:
            return
            
        current_time = self.cap.get(cv2.CAP_PROP_POS_FRAMES) / self.fps
        new_time = max(0, min(self.duration, current_time + seconds))
        new_frame = int(new_time * self.fps)
        
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, new_frame)
        print(f"⏭️ Saltando a {new_time:.1f}s")
    
    def restart_video(self):
        """Reinicia el video desde el principio"""
        if not self.using_video:
            return
            
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        self.frame_count = 0
        self.fall_detected = False
        self.fall_start_time = None
        self.notification_sent = False
        print("🔄 Video reiniciado")
    
    def update_furniture_memory(self, frame):
        """Actualiza la memoria persistente de muebles"""
        results = self.furniture_model(frame)[0]
        current_time = time.time()
        
        # Detectar muebles actuales
        current_furniture = []
        for r in results.boxes:
            cls_id = int(r.cls[0])
            conf = float(r.conf[0])
            
            if cls_id in self.furniture_classes and conf > 0.4:  # Confianza más baja para capturar muebles parcialmente ocultos
                x1, y1, x2, y2 = map(int, r.xyxy[0])
                
                furniture_info = {
                    'bbox': (x1, y1, x2, y2),
                    'class': self.furniture_classes[cls_id],
                    'confidence': conf,
                    'class_id': cls_id,
                    'last_seen': current_time,
                    'detection_count': 1
                }
                current_furniture.append(furniture_info)
        
        # Actualizar memoria: fusionar detecciones actuales con memoria
        for current in current_furniture:
            cx1, cy1, cx2, cy2 = current['bbox']
            current_center = ((cx1 + cx2) // 2, (cy1 + cy2) // 2)
            
            # Buscar si este mueble ya existe en memoria (cerca de la misma posición)
            merged = False
            for memory_item in self.furniture_memory:
                mx1, my1, mx2, my2 = memory_item['bbox']
                memory_center = ((mx1 + mx2) // 2, (my1 + my2) // 2)
                
                # Calcular distancia entre centros
                distance = np.sqrt((current_center[0] - memory_center[0])**2 + 
                                 (current_center[1] - memory_center[1])**2)
                
                # Si están cerca y son del mismo tipo, actualizar
                if distance < 100 and current['class'] == memory_item['class']:
                    # Actualizar información (promedio ponderado para suavizar)
                    weight = 0.3  # Peso de la nueva detección
                    memory_item['bbox'] = (
                        int(mx1 * (1-weight) + cx1 * weight),
                        int(my1 * (1-weight) + cy1 * weight),
                        int(mx2 * (1-weight) + cx2 * weight),
                        int(my2 * (1-weight) + cy2 * weight)
                    )
                    memory_item['confidence'] = max(memory_item['confidence'], current['confidence'])
                    memory_item['last_seen'] = current_time
                    memory_item['detection_count'] += 1
                    merged = True
                    break
            
            # Si no se pudo fusionar, agregar como nuevo
            if not merged:
                self.furniture_memory.append(current)
        
        # Limpiar muebles que no se han visto en mucho tiempo
        self.furniture_memory = [
            item for item in self.furniture_memory 
            if current_time - item['last_seen'] < self.furniture_memory_timeout
        ]
        
        if self.show_debug:
            print(f"🏠 Memoria de muebles: {len(self.furniture_memory)} items")
    
    def analyze_movement_pattern(self, frame):
        """Analiza el patrón de movimiento para detectar caídas súbitas vs movimientos normales"""
        if self.prev_frame is None:
            self.prev_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            return False
        
        current_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Calcular diferencia de frames
        frame_diff = cv2.absdiff(self.prev_frame, current_gray)
        
        # Detectar movimiento significativo
        movement_score = np.sum(frame_diff > 30)  # Píxeles que cambiaron significativamente
        
        self.prev_frame = current_gray
        
        # Movimiento súbito indica posible caída real
        sudden_movement = movement_score > self.movement_threshold
        
        if self.show_debug and sudden_movement:
            print(f"⚡ Movimiento súbito detectado: {movement_score}")
        
        return sudden_movement
    
    def calculate_person_height_position(self, person_bbox, frame_height):
        """Calcula la posición vertical relativa de la persona"""
        x1, y1, x2, y2 = person_bbox
        
        # Calcular posición del centro vertical
        center_y = (y1 + y2) // 2
        
        # Posición relativa desde el suelo (0 = suelo, 1 = techo)
        relative_height = 1.0 - (center_y / frame_height)
        
        # Altura de la persona en píxeles
        person_height = y2 - y1
        
        return relative_height, person_height
    
    def is_in_furniture_zone_advanced(self, person_bbox, frame):
        """Verificación avanzada considerando memoria de muebles y análisis contextual"""
        px1, py1, px2, py2 = person_bbox
        person_center_x = (px1 + px2) // 2
        person_center_y = (py1 + py2) // 2
        person_area = (px2 - px1) * (py2 - py1)
        
        # Calcular altura relativa
        relative_height, person_height = self.calculate_person_height_position(person_bbox, frame.shape[0])
        
        for furniture in self.furniture_memory:
            fx1, fy1, fx2, fy2 = furniture['bbox']
            
            # Expandir zona de mueble según su tipo y confianza
            margin = 30 if furniture['class'] in ['couch', 'bed'] else 15
            
            # Zona expandida para considerar alrededores del mueble
            expanded_zone = (
                max(0, fx1 - margin),
                max(0, fy1 - margin),
                min(frame.shape[1], fx2 + margin),
                min(frame.shape[0], fy2 + margin)
            )
            
            ex1, ey1, ex2, ey2 = expanded_zone
            
            # Verificar si la persona está en la zona expandida
            center_in_expanded = (ex1 <= person_center_x <= ex2 and ey1 <= person_center_y <= ey2)
            
            # Calcular superposición con zona original
            overlap_x1 = max(px1, fx1)
            overlap_y1 = max(py1, fy1)
            overlap_x2 = min(px2, fx2)
            overlap_y2 = min(py2, fy2)
            
            overlap_area = 0
            if overlap_x1 < overlap_x2 and overlap_y1 < overlap_y2:
                overlap_area = (overlap_x2 - overlap_x1) * (overlap_y2 - overlap_y1)
            
            overlap_ratio = overlap_area / person_area if person_area > 0 else 0
            
            # LÓGICA MEJORADA DE DECISIÓN:
            # 1. Si hay superposición significativa con el mueble original
            # 2. O si está en zona expandida de cama/sofá Y está a altura apropiada
            # 3. Considerar histórico de detecciones del mueble
            
            confidence_factor = min(furniture['detection_count'] / 10, 1.0)  # Más confianza = más detecciones
            
            is_rest_furniture = furniture['class'] in ['couch', 'bed']
            appropriate_height = relative_height < 0.6  # Está en la parte baja de la imagen
            
            # Condiciones para considerar que está en zona de descanso
            if (overlap_ratio > 0.2 or 
                (center_in_expanded and is_rest_furniture and appropriate_height and confidence_factor > 0.3)):
                
                if self.show_debug:
                    print(f"🛏️  En zona de {furniture['class']}: overlap={overlap_ratio:.2f}, "
                          f"altura={relative_height:.2f}, confianza={confidence_factor:.2f}")
                
                return True, furniture['class'], confidence_factor
        
        return False, None, 0
    
    def draw_furniture_zones(self, frame):
        """Dibuja las zonas de muebles de la memoria"""
        if not self.show_zones:
            return frame
            
        overlay = frame.copy()
        current_time = time.time()
        
        for i, furniture in enumerate(self.furniture_memory):
            x1, y1, x2, y2 = furniture['bbox']
            color = self.zone_colors[i % len(self.zone_colors)]
            
            # Intensidad basada en cuándo se vio por última vez
            time_since_seen = current_time - furniture['last_seen']
            alpha_factor = max(0.3, 1.0 - (time_since_seen / 60))  # Se desvanece en 1 minuto
            
            # Zona expandida para visualización
            margin = 30 if furniture['class'] in ['couch', 'bed'] else 15
            ex1 = max(0, x1 - margin)
            ey1 = max(0, y1 - margin)
            ex2 = min(frame.shape[1], x2 + margin)
            ey2 = min(frame.shape[0], y2 + margin)
            
            # Dibujar zona expandida (más transparente)
            cv2.rectangle(overlay, (ex1, ey1), (ex2, ey2), color, -1)
            
            # Dibujar zona original (menos transparente)
            cv2.rectangle(overlay, (x1, y1), (x2, y2), color, -1)
            
            # Contorno
            line_thickness = 3 if time_since_seen < 5 else 1
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, line_thickness)
            
            # Etiqueta con información
            age_indicator = " " if time_since_seen < 5 else " " if time_since_seen < 30 else " "
            label = f"{age_indicator} {furniture['class'].upper()}"
            if self.show_debug:
                label += f" ({furniture['detection_count']}x)"
            
            label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]
            cv2.rectangle(frame, (x1, y1 - label_size[1] - 10), 
                         (x1 + label_size[0] + 10, y1), color, -1)
            cv2.putText(frame, label, (x1 + 5, y1 - 5), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
        
        # Mezclar overlay
        alpha = 0.15
        cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)
        
        return frame
    
    def detect_fall_advanced(self, frame):
        """Detección avanzada de caídas con análisis contextual"""
        results = self.person_model(frame)[0]
        
        current_fall_detected = False
        sudden_movement = self.analyze_movement_pattern(frame)
        
        for r in results.boxes:
            cls_id = int(r.cls[0])
            conf = float(r.conf[0])
            
            if cls_id != 0 or conf < 0.5:
                continue
            
            x1, y1, x2, y2 = map(int, r.xyxy[0])
            w = x2 - x1
            h = y2 - y1
            
            # Análisis de postura
            aspect_ratio = w / h if h > 0 else 0
            is_horizontal = aspect_ratio > 1.2
            
            # Verificar zona de muebles con lógica avanzada
            in_furniture_zone, furniture_type, zone_confidence = self.is_in_furniture_zone_advanced((x1, y1, x2, y2), frame)
            
            # Calcular altura relativa
            relative_height, person_height = self.calculate_person_height_position((x1, y1, x2, y2), frame.shape[0])
            
            # LÓGICA DE DECISIÓN MEJORADA
            if is_horizontal and not in_furniture_zone:
                # Persona horizontal fuera de muebles
                if sudden_movement or relative_height < 0.3:  # Movimiento súbito O muy cerca del suelo
                    current_fall_detected = True
                    color = (0, 0, 255)  # Rojo - caída real
                    label = f"CAIDA REAL ({conf:.2f})"
                else:
                    # Podría ser falso positivo, pero mantener vigilancia
                    color = (0, 165, 255)  # Naranja - sospechoso
                    label = f"Posible caída ({conf:.2f})"
                    
            elif is_horizontal and in_furniture_zone and zone_confidence > 0.5:
                # Persona en mueble con alta confianza
                color = (0, 255, 255)  # Cian - descansando
                label = f"En {furniture_type} ({conf:.2f})"
                
            elif is_horizontal and in_furniture_zone and zone_confidence <= 0.5:
                # Zona de mueble con baja confianza (podría estar oculto)
                if sudden_movement:
                    current_fall_detected = True
                    color = (128, 0, 255)  # Morado - caída cerca de mueble
                    label = f"Caída cerca de {furniture_type} ({conf:.2f})"
                else:
                    color = (255, 165, 0)  # Naranja - incierto
                    label = f"Incierto cerca de {furniture_type} ({conf:.2f})"
            else:
                # Persona de pie
                color = (0, 255, 0)
                label = f"De pie ({conf:.2f})"
            
            # Dibujar detección
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            
            # Etiqueta con fondo
            label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
            cv2.rectangle(frame, (x1, y1 - label_size[1] - 10), 
                         (x1 + label_size[0] + 5, y1), color, -1)
            cv2.putText(frame, label, (x1, y1 - 5), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            # Info de debug
            if self.show_debug:
                debug_info = f"H:{relative_height:.2f} AR:{aspect_ratio:.2f}"
                cv2.putText(frame, debug_info, (x1, y2 + 20), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)
        
        return current_fall_detected
    
    def save_incident_image(self, frame):
        """Guarda la imagen del incidente con timestamp"""
        timestamp = datetime.now()
        filename = f"incidente_{timestamp.strftime('%Y%m%d_%H%M%S')}.jpg"
        filepath = os.path.join(self.image_dir, filename)
        
        cv2.imwrite(filepath, frame)
        return filename, filepath
    
    def send_notification(self, frame):
        """Envía notificación POST cuando se detecta caída sostenida"""
        try:
            # Guardar imagen del incidente
            filename, filepath = self.save_incident_image(frame)
            
            # Preparar datos para el POST
            now = datetime.now()
            
            print(f"🚨 CAÍDA DETECTADA - Enviando notificación...")
            print(f"Archivo: {filepath}")
            print(f"Fecha: {now.strftime('%d/%m/%Y')}")
            print(f"Hora: {now.strftime('%H:%M:%S')}")
            print(f"Cámara: {self.camera_id}")
            print(f"Dirección: {self.direccion}")
            
            # Preparar datos del formulario
            form_data = {
                'echa': now.strftime("%d/%m/%Y"),     # Formato DD/MM/YYYY (como espera el webhook)
                'hora': now.strftime("%H:%M:%S"),     # Formato HH:MM:SS
                'direccion': self.direccion,
                'idCamara': self.camera_id,
            }
            
            # Preparar archivo para subir
            with open(filepath, 'rb') as image_file:
                files = {
                    'imagen': (filename, image_file, 'image/jpeg')
                }
                
                # Realizar POST request con multipart/form-data
                response = requests.post(
                    self.api_endpoint,
                    data=form_data,
                    files=files,
                    timeout=30  # Aumentado para subida de imagen
                )
            
            if response.status_code == 200:
                print("✅ Notificación enviada exitosamente")
                try:
                    response_data = response.json()
                    print(f"Respuesta del servidor: {json.dumps(response_data, indent=2)}")
                except:
                    print(f"Respuesta del servidor: {response.text}")
                return True
            else:
                print(f"❌ Error al enviar notificación: {response.status_code}")
                print(f"Respuesta: {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Error de conexión: {e}")
            return False
        except FileNotFoundError as e:
            print(f"❌ Error: No se pudo encontrar el archivo de imagen: {e}")
            return False
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            return False
    
    def update_fall_status(self, current_fall_detected, frame):
        """Actualiza el estado de la caída y maneja las notificaciones"""
        current_time = time.time()
        
        if current_fall_detected:
            if not self.fall_detected:
                self.fall_detected = True
                self.fall_start_time = current_time
                self.notification_sent = False
                print("⚠️  Caída detectada - Iniciando verificación...")
            
            elif self.fall_start_time:
                elapsed_time = current_time - self.fall_start_time
                
                if elapsed_time >= self.fall_duration_threshold and not self.notification_sent:
                    print(f"🚨 Caída confirmada después de {elapsed_time:.1f} segundos!")
                    self.send_notification(frame)
                    self.notification_sent = True
        else:
            if self.fall_detected:
                elapsed_time = current_time - self.fall_start_time if self.fall_start_time else 0
                print(f"✅ Falsa alarma o recuperación después de {elapsed_time:.1f} segundos")
                
                self.fall_detected = False
                self.fall_start_time = None
                self.notification_sent = False
    
    def draw_video_controls(self, frame):
        """Dibuja los controles de video en pantalla"""
        if not self.using_video:
            return frame
        
        # Información del video
        current_frame, current_time, time_str = self.get_video_progress()
        
        # Fondo para la información
        info_height = 80
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, frame.shape[0] - info_height), (frame.shape[1], frame.shape[0]), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        
        # Texto de información
        y_pos = frame.shape[0] - 55
        cv2.putText(frame, f"📹 {time_str}", (10, y_pos), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Estado de reproducción
        status = "PAUSADO" if self.paused else f" {self.playback_speed:.1f}x"
        cv2.putText(frame, status, (10, y_pos + 25), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Barra de progreso
        progress_width = frame.shape[1] - 20
        progress_height = 8
        progress_y = frame.shape[0] - 15
        
        # Fondo de la barra
        cv2.rectangle(frame, (10, progress_y), (10 + progress_width, progress_y + progress_height), (50, 50, 50), -1)
        
        # Progreso actual
        if self.total_frames > 0:
            progress_fill = int((current_frame / self.total_frames) * progress_width)
            cv2.rectangle(frame, (10, progress_y), (10 + progress_fill, progress_y + progress_height), (0, 255, 0), -1)
        
        return frame
    
    def run(self):
        """Ejecuta el detector principal"""
        print("🔍 Iniciando detector de caídas avanzado...")
        
        while True:
            if not self.paused:
                ret, frame = self.cap.read()
                if not ret:
                    if self.using_video:
                        print("📹 Video terminado")
                        self.restart_video()
                        continue
                    else:
                        print("❌ Error al leer frame de la cámara")
                        break
                
                self.frame_count += 1
                
                # Actualizar memoria de muebles periódicamente
                if self.frame_count % self.furniture_detection_interval == 0:
                    self.update_furniture_memory(frame)
                
                # Detectar caídas con lógica avanzada
                current_fall_detected = self.detect_fall_advanced(frame)
                
                # Actualizar estado
                self.update_fall_status(current_fall_detected, frame)
                
                # Dibujar zonas
                frame = self.draw_furniture_zones(frame)
                
                # Estado del sistema
                status_text = "SISTEMA ACTIVO"
                status_color = (0, 255, 0)
                
                if self.fall_detected:
                    if self.fall_start_time:
                        elapsed = time.time() - self.fall_start_time
                        status_text = f"VERIFICANDO CAÍDA - {elapsed:.1f}s"
                        status_color = (0, 165, 255) if elapsed < self.fall_duration_threshold else (0, 0, 255)
                
                # Mostrar estado
                status_size = cv2.getTextSize(status_text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)[0]
                cv2.rectangle(frame, (5, 5), (status_size[0] + 15, status_size[1] + 15), (0, 0, 0), -1)
                cv2.putText(frame, status_text, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, status_color, 2)
                
                # Info de memoria
                memory_info = f"Muebles en memoria: {len(self.furniture_memory)}"
                cv2.putText(frame, memory_info, (10, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                
                # Dibujar controles de video
                frame = self.draw_video_controls(frame)
            else:
                # En pausa, mantener el último frame
                ret, frame = self.cap.read()
                if not ret:
                    if self.using_video:
                        print("📹 Video terminado")
                        break
                    else:
                        print("❌ Error al leer frame de la cámara")
                        break
                
                # Regresar un frame para mantener posición
                if self.using_video:
                    current_pos = self.cap.get(cv2.CAP_PROP_POS_FRAMES)
                    self.cap.set(cv2.CAP_PROP_POS_FRAMES, max(0, current_pos - 1))
                
                # Aplicar procesamiento visual básico
                frame = self.draw_furniture_zones(frame)
                
                # Mostrar estado de pausa
                status_text = "PAUSADO"
                status_size = cv2.getTextSize(status_text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)[0]
                cv2.rectangle(frame, (5, 5), (status_size[0] + 15, status_size[1] + 15), (0, 0, 0), -1)
                cv2.putText(frame, status_text, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
                
                # Dibujar controles de video
                frame = self.draw_video_controls(frame)
            
            cv2.imshow("Detector de Caídas - YOLOv8", frame)
            
            # Calcular delay basado en velocidad de reproducción
            if self.using_video and not self.paused:
                delay = max(1, int(self.frame_delay / self.playback_speed))
            else:
                delay = 30
            
            # Manejar teclas
            key = cv2.waitKey(delay) & 0xFF
            if key == 27:  # ESC
                break
            elif key == ord(' '):  # ESPACIO - Pausar/Reanudar
                self.paused = not self.paused
                print(f"⏯️ {'Pausado' if self.paused else 'Reanudado'}")
            elif key == ord('s') or key == ord('S'):  # Avanzar frame por frame
                if self.paused and self.using_video:
                    self.paused = False
                    # Permitir un frame y luego pausar
                    cv2.waitKey(30)
                    self.paused = True
            elif key == ord('+') or key == ord('='):  # Aumentar velocidad
                self.playback_speed = min(4.0, self.playback_speed + 0.25)
                print(f"⏩ Velocidad: {self.playback_speed:.2f}x")
            elif key == ord('-'):  # Disminuir velocidad
                self.playback_speed = max(0.25, self.playback_speed - 0.25)
                print(f"⏪ Velocidad: {self.playback_speed:.2f}x")
            elif key == ord('r') or key == ord('R'):  # Reiniciar video
                self.restart_video()
            elif key == 81 or key == 2424832:  # Flecha izquierda (códigos pueden variar)
                self.seek_video(-5)  # Retroceder 5 segundos
            elif key == 83 or key == 2555904:  # Flecha derecha
                self.seek_video(5)   # Avanzar 5 segundos
            elif key == ord('f') or key == ord('F'):
                print("🔄 Escaneando muebles...")
                if not self.paused:
                    self.update_furniture_memory(frame)
            elif key == ord('t') or key == ord('T'):
                self.show_zones = not self.show_zones
                print(f"👁️  Zonas: {'Visible' if self.show_zones else 'Oculto'}")
            elif key == ord('d') or key == ord('D'):
                self.show_debug = not self.show_debug
                print(f"🐛 Debug: {'Activado' if self.show_debug else 'Desactivado'}")
            elif key == ord('m') or key == ord('M'):
                self.furniture_memory = []
                print("🗑️  Memoria de muebles reseteada")
        
        self.cleanup()
    
    def cleanup(self):
        """Limpia recursos"""
        self.cap.release()
        cv2.destroyAllWindows()
        print("🔚 Detector detenido")

# Función para facilitar el uso
def create_fall_detector(video_path=None, **kwargs):
    """
    Crea un detector de caídas configurado para video o cámara
    
    Args:
        video_path (str, optional): Ruta al archivo de video. Si es None, usa la cámara web.
        **kwargs: Otros parámetros para el FallDetector
    
    Returns:
        FallDetector: Instancia configurada del detector
    """
    return FallDetector(video_path=video_path, **kwargs)

# Ejemplos de uso
if __name__ == "__main__":
    # OPCIÓN 1: Usar con video de prueba
    # detector = create_fall_detector(
    #     video_path="path/to/your/test_video.mp4",
    #     camera_id="CAM-TEST-001",
    #     direccion="Laboratorio de Pruebas"
    # )
    
    # OPCIÓN 2: Usar con cámara web (comportamiento original)
    detector = create_fall_detector(
        video_path="C:/Users/Cuboz/Desktop/video.mp4",  # None para usar cámara web
        camera_id="CAM-Salon De Eventos",
        direccion="Avenida Universitaria",
        api_endpoint="http://192.168.43.11:8000/webhook"
    )
    
    # OPCIÓN 3: Ejemplo con video específico
    # detector = create_fall_detector(
    #     video_path="fall_test_video.mp4",
    #     camera_id="CAM-VIDEO-TEST",
    #     direccion="Video de Prueba - Detección de Caídas"
    # )
    
    try:
        detector.run()
    except KeyboardInterrupt:
        print("\n🛑 Detenido por el usuario")
        detector.cleanup()

"""
🎯 INSTRUCCIONES DE USO:

1. PREPARACIÓN:
   - Instala las dependencias: pip install ultralytics opencv-python requests numpy
   - Descarga un video de prueba o prepara tu archivo de video

2. CONFIGURACIÓN:
   - Cambia la línea de video_path por la ruta a tu archivo de video
   - Ejemplo: video_path="C:/videos/fall_test.mp4"
   - Si quieres usar la cámara web, deja video_path=None

3. CONTROLES DURANTE LA EJECUCIÓN:
   📹 CONTROLES DE VIDEO:
   - ESPACIO: Pausar/Reanudar
   - 'S': Avanzar frame por frame (cuando pausado)
   - '+'/'-': Aumentar/Disminuir velocidad (0.25x a 4.0x)
   - 'R': Reiniciar video desde el principio
   - Flechas ←/→: Saltar 5 segundos atrás/adelante

   🔧 CONTROLES DEL DETECTOR:
   - 'F': Forzar escaneo de muebles
   - 'T': Mostrar/Ocultar zonas de muebles
   - 'D': Activar/Desactivar modo debug
   - 'M': Resetear memoria de muebles
   - ESC: Salir

4. VENTAJAS DEL MODO VIDEO:
   - Pruebas repetibles y controladas
   - Análisis frame por frame
   - Control de velocidad de reproducción
   - No consume recursos de API en modo prueba
   - Fácil debugging y ajuste de parámetros

5. FORMATOS DE VIDEO SOPORTADOS:
   - MP4, AVI, MOV, MKV y otros formatos soportados por OpenCV
   - Recomendado: MP4 con codec H.264

6. TIPS PARA MEJORES PRUEBAS:
   - Usa videos con diferentes escenarios de caída
   - Prueba con videos que incluyan muebles (sofás, camas)
   - Experimenta con diferentes velocidades de reproducción
   - Usa el modo debug para entender mejor las detecciones
"""