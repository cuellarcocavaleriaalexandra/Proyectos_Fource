import cv2
import time
import requests
import json
import os
from datetime import datetime
from ultralytics import YOLO
import numpy as np

class FallDetector:
    def __init__(self, camera_id="CAM-007", direccion="Av. Siempre Viva 742", api_endpoint="http://your-api-endpoint.com/api/incidents"):
        # Configuración
        self.camera_id = camera_id
        self.direccion = direccion
        self.api_endpoint = api_endpoint
        
        # Cargar modelos YOLO
        self.person_model = YOLO("yolov8n.pt")  # Modelo para detectar personas
        self.furniture_model = YOLO("yolov8n.pt")  # Puedes cambiar por tu modelo personalizado
        
        # IDs de clases de muebles en COCO dataset
        self.furniture_classes = {
            56: "chair",      # silla
            57: "couch",      # sofá
            59: "bed",        # cama
            61: "dining_table"  # mesa (opcional)
        }
        
        # Variables para seguimiento de caídas
        self.fall_detected = False
        self.fall_start_time = None
        self.fall_duration_threshold = 5.0  # 5 segundos
        self.notification_sent = False
        
        # SISTEMA DE MEMORIA DE MUEBLES (solución a oclusión)
        self.furniture_memory = []  # Memoria persistente de muebles
        self.furniture_memory_timeout = 300  # 5 minutos sin detectar para olvidar mueble
        self.furniture_detection_interval = 60  # Buscar muebles cada 60 frames
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
        
        # Captura de video
        self.cap = cv2.VideoCapture(0)
        
        print("\n🏠 DETECTOR DE CAÍDAS CON ANTI-OCLUSIÓN")
        print("• Sistema de memoria de muebles (persisten aunque se oculten)")
        print("• Análisis de movimiento súbito para detectar caídas reales")
        print("• Análisis de altura relativa del suelo")
        print("• Presiona 'F' para forzar escaneo de muebles")
        print("• Presiona 'T' para alternar visualización de zonas")
        print("• Presiona 'D' para alternar modo debug")
        print("• Presiona 'R' para resetear memoria de muebles")
        print("• Presiona ESC para salir\n")
    
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
            age_indicator = "🟢" if time_since_seen < 5 else "🟡" if time_since_seen < 30 else "🔴"
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
                    label = f"🚨 CAÍDA REAL ({conf:.2f})"
                else:
                    # Podría ser falso positivo, pero mantener vigilancia
                    color = (0, 165, 255)  # Naranja - sospechoso
                    label = f"⚠️ Posible caída ({conf:.2f})"
                    
            elif is_horizontal and in_furniture_zone and zone_confidence > 0.5:
                # Persona en mueble con alta confianza
                color = (0, 255, 255)  # Cian - descansando
                label = f"🛏️ En {furniture_type} ({conf:.2f})"
                
            elif is_horizontal and in_furniture_zone and zone_confidence <= 0.5:
                # Zona de mueble con baja confianza (podría estar oculto)
                if sudden_movement:
                    current_fall_detected = True
                    color = (128, 0, 255)  # Morado - caída cerca de mueble
                    label = f"🚨 Caída cerca de {furniture_type} ({conf:.2f})"
                else:
                    color = (255, 165, 0)  # Naranja - incierto
                    label = f"❓ Incierto cerca de {furniture_type} ({conf:.2f})"
            else:
                # Persona de pie
                color = (0, 255, 0)
                label = f"🚶 De pie ({conf:.2f})"
            
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
            filename, filepath = self.save_incident_image(frame)
            now = datetime.now()
            
            print(f"🚨 CAÍDA CONFIRMADA - Enviando notificación...")
            print(f"Archivo: {filepath}")
            
            form_data = {
                'echa': now.strftime("%d/%m/%Y"),
                'hora': now.strftime("%H:%M:%S"),
                'direccion': self.direccion,
                'idCamara': self.camera_id,
            }
            
            with open(filepath, 'rb') as image_file:
                files = {'imagen': (filename, image_file, 'image/jpeg')}
                response = requests.post(self.api_endpoint, data=form_data, files=files, timeout=30)
            
            if response.status_code == 200:
                print("✅ Notificación enviada exitosamente")
                return True
            else:
                print(f"❌ Error al enviar notificación: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error al enviar notificación: {e}")
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
    
    def run(self):
        """Ejecuta el detector principal"""
        print("🔍 Iniciando detector de caídas avanzado...")
        
        while True:
            ret, frame = self.cap.read()
            if not ret:
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
            status_text = "🟢 SISTEMA ACTIVO"
            status_color = (0, 255, 0)
            
            if self.fall_detected:
                if self.fall_start_time:
                    elapsed = time.time() - self.fall_start_time
                    status_text = f"🔴 VERIFICANDO CAÍDA - {elapsed:.1f}s"
                    status_color = (0, 165, 255) if elapsed < self.fall_duration_threshold else (0, 0, 255)
            
            # Mostrar estado
            status_size = cv2.getTextSize(status_text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)[0]
            cv2.rectangle(frame, (5, 5), (status_size[0] + 15, status_size[1] + 15), (0, 0, 0), -1)
            cv2.putText(frame, status_text, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, status_color, 2)
            
            # Info de memoria
            memory_info = f"🏠 Muebles en memoria: {len(self.furniture_memory)}"
            cv2.putText(frame, memory_info, (10, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            cv2.imshow("Detector de Caídas - YOLOv8", frame)
            
            # Manejar teclas
            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC
                break
            elif key == ord('f') or key == ord('F'):
                print("🔄 Escaneando muebles...")
                self.update_furniture_memory(frame)
            elif key == ord('t') or key == ord('T'):
                self.show_zones = not self.show_zones
                print(f"👁️  Zonas: {'Visible' if self.show_zones else 'Oculto'}")
            elif key == ord('d') or key == ord('D'):
                self.show_debug = not self.show_debug
                print(f"🐛 Debug: {'Activado' if self.show_debug else 'Desactivado'}")
            elif key == ord('r') or key == ord('R'):
                self.furniture_memory = []
                print("🗑️  Memoria de muebles reseteada")
        
        self.cleanup()
    
    def cleanup(self):
        """Limpia recursos"""
        self.cap.release()
        cv2.destroyAllWindows()
        print("🔚 Detector detenido")

# Uso del detector
if __name__ == "__main__":
    detector = FallDetector(
        camera_id="CAM-007",
        direccion="Av. Siempre Viva 742",
        api_endpoint="http://192.168.43.11:8000/webhook"
    )
    
    try:
        detector.run()
    except KeyboardInterrupt:
        print("\n🛑 Detenido por el usuario")
        detector.cleanup()