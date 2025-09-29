import cv2
import time
import requests
import json
import os
from datetime import datetime
from ultralytics import YOLO

class FallDetector:
    def __init__(self, camera_id="CAM-007", direccion="Av. Siempre Viva 742", api_endpoint="http://your-api-endpoint.com/api/incidents", video_path=None, use_camera=False, fps_multiplier=1.0):
        # Configuración
        self.camera_id = camera_id
        self.direccion = direccion
        self.api_endpoint = api_endpoint
        self.video_path = video_path
        self.use_camera = use_camera
        self.fps_multiplier = fps_multiplier  # Multiplicador de velocidad
        
        # Cargar modelo YOLOv8
        self.model = YOLO("yolov8n.pt")
        
        # Variables para seguimiento de caídas
        self.fall_detected = False
        self.fall_start_time = None
        self.fall_duration_threshold = 5.0  # 5 segundos
        self.notification_sent = False
        
        # Crear directorio para imágenes si no existe
        self.image_dir = "fall_incidents"
        os.makedirs(self.image_dir, exist_ok=True)
        
        # Configurar captura de video
        if self.use_camera:
            print("📷 Usando cámara...")
            self.cap = cv2.VideoCapture(0)
            self.target_fps = 30  # FPS deseado para cámara
        elif self.video_path and os.path.exists(self.video_path):
            print(f"🎬 Usando video: {self.video_path}")
            self.cap = cv2.VideoCapture(self.video_path)
            # Obtener información del video
            self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
            self.original_fps = self.cap.get(cv2.CAP_PROP_FPS)
            self.target_fps = self.original_fps * self.fps_multiplier
            print(f"📊 Video info: {self.total_frames} frames, {self.original_fps:.2f} FPS original")
            print(f"🚀 Velocidad configurada: {self.fps_multiplier}x ({self.target_fps:.2f} FPS target)")
        else:
            raise ValueError("Debe especificar un video válido o usar la cámara")
        
        # Control de timing para FPS
        self.frame_delay = 1.0 / self.target_fps if self.target_fps > 0 else 0
        self.last_frame_time = 0
        
        # Variables para control de bucle de video
        self.current_frame = 0
        self.loop_count = 0
    
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
    
    def detect_fall(self, frame):
        """Detecta caídas en el frame actual"""
        results = self.model(frame)[0]
        
        current_fall_detected = False
        
        for r in results.boxes:
            cls_id = int(r.cls[0])
            conf = float(r.conf[0])
            
            # Solo procesar detecciones de personas (clase 0)
            if cls_id != 0:
                continue
            
            x1, y1, x2, y2 = map(int, r.xyxy[0])
            w = x2 - x1
            h = y2 - y1
            
            # Calcular si la persona está caída (más ancho que alto)
            fallen = w > h * 1.2  # Factor de 1.2 para más precisión
            
            if fallen:
                current_fall_detected = True
                color = (0, 0, 255)  # Rojo para caída
                label = f"CAÍDA DETECTADA ({conf:.2f})"
                
                # Mostrar tiempo transcurrido si hay caída activa
                if self.fall_detected and self.fall_start_time:
                    elapsed_time = time.time() - self.fall_start_time
                    label += f" - {elapsed_time:.1f}s"
            else:
                color = (0, 255, 0)  # Verde para persona de pie
                label = f"De pie ({conf:.2f})"
            
            # Dibujar bounding box y etiqueta
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, label, (x1, y1 - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        
        return current_fall_detected
    
    def update_fall_status(self, current_fall_detected, frame):
        """Actualiza el estado de la caída y maneja las notificaciones"""
        current_time = time.time()
        
        if current_fall_detected:
            if not self.fall_detected:
                # Nueva caída detectada
                self.fall_detected = True
                self.fall_start_time = current_time
                self.notification_sent = False
                print("⚠️  Caída detectada - Iniciando conteo...")
            
            elif self.fall_start_time:
                # Caída en progreso
                elapsed_time = current_time - self.fall_start_time
                
                if elapsed_time >= self.fall_duration_threshold and not self.notification_sent:
                    # Caída sostenida por más de 5 segundos
                    print(f"🚨 Caída sostenida por {elapsed_time:.1f} segundos!")
                    self.send_notification(frame)
                    self.notification_sent = True
        else:
            if self.fall_detected:
                # La persona se levantó
                elapsed_time = current_time - self.fall_start_time if self.fall_start_time else 0
                print(f"✅ Persona recuperada después de {elapsed_time:.1f} segundos")
                
                # Reset del estado
                self.fall_detected = False
                self.fall_start_time = None
                self.notification_sent = False
    
    def reset_video_loop(self):
        """Reinicia el video para reproducción en bucle"""
        if not self.use_camera:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            self.current_frame = 0
            self.loop_count += 1
            print(f"🔄 Reiniciando video - Bucle #{self.loop_count}")
    
    def run(self):
        """Ejecuta el detector principal"""
        print("🔍 Iniciando detector de caídas...")
        print(f"📷 Cámara ID: {self.camera_id}")
        print(f"📍 Ubicación: {self.direccion}")
        print(f"⏱️  Umbral de notificación: {self.fall_duration_threshold} segundos")
        
        if not self.use_camera:
            print(f"🎬 Modo video en bucle: {self.video_path}")
            print("Presiona 'R' para reiniciar video manualmente")
            print("Presiona '+' para acelerar, '-' para desacelerar")
        
        print("Presiona ESC para salir\n")
        
        while True:
            # Control de timing para mantener FPS objetivo
            current_time = time.time()
            if not self.use_camera and self.frame_delay > 0:
                time_since_last_frame = current_time - self.last_frame_time
                if time_since_last_frame < self.frame_delay:
                    time.sleep(self.frame_delay - time_since_last_frame)
            
            ret, frame = self.cap.read()
            
            # Si no se puede leer el frame y estamos usando video, reiniciar
            if not ret:
                if not self.use_camera:
                    print("🔄 Fin del video alcanzado, reiniciando...")
                    self.reset_video_loop()
                    continue
                else:
                    print("❌ Error al leer frame de la cámara")
                    break
            
            # Actualizar tiempo del último frame
            self.last_frame_time = time.time()
            
            # Incrementar contador de frame para videos
            if not self.use_camera:
                self.current_frame += 1
            
            # Detectar caídas en el frame actual
            current_fall_detected = self.detect_fall(frame)
            
            # Actualizar estado y manejar notificaciones
            self.update_fall_status(current_fall_detected, frame)
            
            # Mostrar información de estado en pantalla
            status_text = "SISTEMA ACTIVO"
            status_color = (0, 255, 0)
            
            if self.fall_detected:
                if self.fall_start_time:
                    elapsed = time.time() - self.fall_start_time
                    status_text = f"CAÍDA DETECTADA - {elapsed:.1f}s"
                    status_color = (0, 0, 255) if elapsed < self.fall_duration_threshold else (0, 165, 255)
            
            cv2.putText(frame, status_text, (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, status_color, 2)
            
            # Mostrar información del video si no es cámara
            if not self.use_camera:
                video_info = f"Frame: {self.current_frame}/{self.total_frames} | Bucle: {self.loop_count}"
                speed_info = f"Velocidad: {self.fps_multiplier:.1f}x ({self.target_fps:.1f} FPS)"
                cv2.putText(frame, video_info, (10, 60), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                cv2.putText(frame, speed_info, (10, 80), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
            
            # Mostrar frame
            window_title = "Detector de Caídas - YOLOv8 (Video)" if not self.use_camera else "Detector de Caídas - YOLOv8 (Cámara)"
            cv2.imshow(window_title, frame)
            
            # Manejar teclas
            key = cv2.waitKey(1) & 0xFF
            
            # Salir con ESC
            if key == 27:
                break
            
            # Reiniciar video manualmente con 'R'
            elif key == ord('r') or key == ord('R'):
                if not self.use_camera:
                    print("🔄 Reinicio manual del video")
                    self.reset_video_loop()
            
            # Acelerar con '+' o '='
            elif key == ord('+') or key == ord('='):
                if not self.use_camera:
                    self.fps_multiplier = min(self.fps_multiplier + 0.5, 5.0)
                    self.target_fps = self.original_fps * self.fps_multiplier
                    self.frame_delay = 1.0 / self.target_fps if self.target_fps > 0 else 0
                    print(f"🚀 Velocidad aumentada a {self.fps_multiplier:.1f}x")
            
            # Desacelerar con '-'
            elif key == ord('-'):
                if not self.use_camera:
                    self.fps_multiplier = max(self.fps_multiplier - 0.5, 0.1)
                    self.target_fps = self.original_fps * self.fps_multiplier
                    self.frame_delay = 1.0 / self.target_fps if self.target_fps > 0 else 0
                    print(f"🐌 Velocidad reducida a {self.fps_multiplier:.1f}x")
            
            # Pausar/reanudar con ESPACIO
            elif key == ord(' '):
                print("⏸️ Pausado - Presiona cualquier tecla para continuar...")
                cv2.waitKey(0)
        
        self.cleanup()
    
    def cleanup(self):
        """Limpia recursos"""
        self.cap.release()
        cv2.destroyAllWindows()
        print("🔚 Detector detenido")

# Funciones de conveniencia para diferentes modos
def create_camera_detector(camera_id="CAM-007", direccion="Av. Siempre Viva 742", api_endpoint="http://192.168.43.11:8000/webhook"):
    """Crea un detector usando la cámara"""
    return FallDetector(
        camera_id=camera_id,
        direccion=direccion,
        api_endpoint=api_endpoint,
        use_camera=True
    )

def create_video_detector(video_path, camera_id="CAM-007", direccion="Av. Siempre Viva 742", api_endpoint="http://192.168.43.11:8000/webhook"):
    """Crea un detector usando un video en bucle"""
    return FallDetector(
        camera_id=camera_id,
        direccion=direccion,
        api_endpoint=api_endpoint,
        video_path=video_path,
        use_camera=False
    )

# Uso del detector
if __name__ == "__main__":
    # OPCIÓN 1: Usar video en bucle (recomendado para pruebas)
    # Cambia "tu_video_de_prueba.mp4" por la ruta de tu video
    video_path = "C:/Users/Cuboz/Desktop/video.mp4"  # Pon aquí la ruta de tu video
    
    # Verificar si el archivo de video existe
    if os.path.exists(video_path):
        detector = create_video_detector(
            video_path=video_path,
            camera_id="CAM-007",
            direccion="Av. Siempre Viva 742",
            api_endpoint="http://192.168.43.11:8000/webhook"
        )
        print(f"🎬 Usando video: {video_path}")
    else:
        print(f"❌ Video no encontrado: {video_path}")
        print("🔄 Cambiando a modo cámara...")
        detector = create_camera_detector(
            camera_id="CAM-007",
            direccion="Av. Siempre Viva 742",
            api_endpoint="http://192.168.43.11:8000/webhook"
        )
    
    # OPCIÓN 2: Usar cámara (descomenta estas líneas si prefieres usar la cámara)
    # detector = create_camera_detector(
    #     camera_id="CAM-007",
    #     direccion="Av. Siempre Viva 742",
    #     api_endpoint="http://192.168.43.11:8000/webhook"
    # )
    
    try:
        detector.run()
    except KeyboardInterrupt:
        print("\n🛑 Detenido por el usuario")
        detector.cleanup()
    except Exception as e:
        print(f"❌ Error: {e}")
        detector.cleanup()