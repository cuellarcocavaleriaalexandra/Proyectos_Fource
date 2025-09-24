import torch
import torch.nn as nn
import torchvision.transforms as transforms
from PIL import Image, ImageOps
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv

# Definir la misma arquitectura DenseNet
class DenseNet(nn.Module):
    def __init__(self, num_classes=10):
        super(DenseNet, self).__init__()
        
        self.features = nn.Sequential(
            nn.Conv2d(1, 64, kernel_size=3, stride=1, padding=1, bias=False),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2)
        )
        
        self.dense_block1 = self._make_dense_block(64, 128)
        self.transition1 = self._make_transition(128, 64)
        
        self.dense_block2 = self._make_dense_block(64, 256)
        self.transition2 = self._make_transition(256, 128)
        
        self.dense_block3 = self._make_dense_block(128, 512)
        
        self.classifier = nn.Sequential(
            nn.AdaptiveAvgPool2d((1, 1)),
            nn.Flatten(),
            nn.Linear(512, 256),
            nn.ReLU(inplace=True),
            nn.Dropout(0.5),
            nn.Linear(256, num_classes)
        )
    
    def _make_dense_block(self, in_channels, growth_rate):
        return nn.Sequential(
            nn.BatchNorm2d(in_channels),
            nn.ReLU(inplace=True),
            nn.Conv2d(in_channels, growth_rate, kernel_size=3, padding=1, bias=False),
            nn.Dropout2d(0.2)
        )
    
    def _make_transition(self, in_channels, out_channels):
        return nn.Sequential(
            nn.BatchNorm2d(in_channels),
            nn.ReLU(inplace=True),
            nn.Conv2d(in_channels, out_channels, kernel_size=1, bias=False),
            nn.AvgPool2d(kernel_size=2, stride=2)
        )
    
    def forward(self, x):
        x = self.features(x)
        x = self.dense_block1(x)
        x = self.transition1(x)
        x = self.dense_block2(x)
        x = self.transition2(x)
        x = self.dense_block3(x)
        x = self.classifier(x)
        return x

# Cargar el modelo entrenado
def load_model(model_path, device):
    model = DenseNet(num_classes=10)
    checkpoint = torch.load(model_path, map_location=device)
    model.load_state_dict(checkpoint['model_state_dict'])
    model.to(device)
    model.eval()
    return model

# Función para invertir colores (fondo blanco -> negro, dígito negro -> blanco)
def invert_colors(image):
    return ImageOps.invert(image)

# Preprocesamiento de imágenes
def preprocess_image(image_path):
    transform = transforms.Compose([
        transforms.Lambda(lambda img: invert_colors(img)),  # INVERTIR COLORES
        transforms.Grayscale(num_output_channels=1),
        transforms.Resize((28, 28)),
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
    ])
    
    image = Image.open(image_path)
    image = transform(image)
    image = image.unsqueeze(0)  # Añadir dimensión batch
    return image

# Predecir una sola imagen
def predict_single_image(model, image_path, device):
    image = preprocess_image(image_path)
    image = image.to(device)
    
    with torch.no_grad():
        outputs = model(image)
        probabilities = torch.nn.functional.softmax(outputs, dim=1)
        confidence, predicted = torch.max(probabilities, 1)
    
    return predicted.item(), confidence.item()

# Explorar la estructura de carpetas y predecir todas las imágenes
def process_all_images(model, base_folder, device, output_csv='predictions.csv'):
    """
    Itera sobre toda la estructura de carpetas:
    base_folder/
        mesa_XXX/
            partido1/
            partido2/
            ...
    """
    
    results = []
    supported_formats = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff')
    
    print(f"Iniciando procesamiento de: {base_folder}")
    
    # Iterar sobre todas las mesas
    for mesa_folder in os.listdir(base_folder):
        mesa_path = os.path.join(base_folder, mesa_folder)
        
        if not os.path.isdir(mesa_path):
            continue
            
        print(f"\nProcesando mesa: {mesa_folder}")
        
        # Iterar sobre todos los partidos en cada mesa
        for partido_folder in os.listdir(mesa_path):
            partido_path = os.path.join(mesa_path, partido_folder)
            
            if not os.path.isdir(partido_path):
                continue
                
            print(f"  Partido: {partido_folder}")
            
            # Procesar todas las imágenes del partido
            for filename in os.listdir(partido_path):
                if filename.lower().endswith(supported_formats):
                    image_path = os.path.join(partido_path, filename)
                    
                    try:
                        prediction, confidence = predict_single_image(model, image_path, device)
                        
                        result = {
                            'mesa': mesa_folder,
                            'partido': partido_folder,
                            'archivo': filename,
                            'ruta_completa': image_path,
                            'prediccion': prediction,
                            'confianza': confidence,
                            'tipo': determinar_tipo_imagen(filename)
                        }
                        
                        results.append(result)
                        
                        print(f"    {filename} -> Dígito: {prediction}, Confianza: {confidence:.4f}")
                        
                    except Exception as e:
                        print(f"    Error procesando {filename}: {e}")
                        # Agregar resultado con error
                        results.append({
                            'mesa': mesa_folder,
                            'partido': partido_folder,
                            'archivo': filename,
                            'ruta_completa': image_path,
                            'prediccion': -1,
                            'confianza': 0.0,
                            'tipo': determinar_tipo_imagen(filename),
                            'error': str(e)
                        })
    
    # Guardar resultados en CSV
    save_to_csv(results, output_csv)
    
    return results

def determinar_tipo_imagen(filename):
    """Determina el tipo de imagen basado en el nombre del archivo"""
    filename_lower = filename.lower()
    
    if 'centena' in filename_lower or 'hundred' in filename_lower:
        return 'centena'
    elif 'decena' in filename_lower or 'ten' in filename_lower:
        return 'decena'
    elif 'unidad' in filename_lower or 'unit' in filename_lower or 'digit' in filename_lower:
        return 'unidad'
    elif 'total' in filename_lower:
        return 'total'
    else:
        # Intentar deducir por el nombre del archivo
        if 'c' in filename_lower and 'd' in filename_lower and 'u' in filename_lower:
            return 'completo'
        elif 'c' in filename_lower:
            return 'centena'
        elif 'd' in filename_lower:
            return 'decena'
        elif 'u' in filename_lower:
            return 'unidad'
        else:
            return 'desconocido'

def save_to_csv(results, output_file):
    """Guardar resultados en archivo CSV"""
    if not results:
        print("No hay resultados para guardar")
        return
    
    # Definir campos del CSV
    fieldnames = ['mesa', 'partido', 'archivo', 'ruta_completa', 'tipo', 'prediccion', 'confianza', 'error']
    
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for result in results:
            # Asegurar que todos los campos existan
            row = {field: result.get(field, '') for field in fieldnames}
            writer.writerow(row)
    
    print(f"\nResultados guardados en: {output_file}")
    
    # También crear un resumen por mesa y partido
    crear_resumen_estadisticas(results, 'resumen_estadisticas.csv')

def crear_resumen_estadisticas(results, output_file):
    """Crear un resumen estadístico de los resultados"""
    if not results:
        return
    
    # Filtrar resultados válidos (sin errores)
    resultados_validos = [r for r in results if r.get('prediccion', -1) >= 0]
    
    if not resultados_validos:
        return
    
    # Crear DataFrame para análisis
    df = pd.DataFrame(resultados_validos)
    
    # Resumen por mesa y partido
    resumen = df.groupby(['mesa', 'partido', 'tipo']).agg({
        'prediccion': 'count',
        'confianza': 'mean'
    }).reset_index()
    
    resumen.rename(columns={
        'prediccion': 'cantidad_imagenes',
        'confianza': 'confianza_promedio'
    }, inplace=True)
    
    # Guardar resumen
    resumen.to_csv(output_file, index=False, encoding='utf-8')
    print(f"Resumen estadístico guardado en: {output_file}")

# Función para mostrar estadísticas rápidas
def mostrar_estadisticas(results):
    """Mostrar estadísticas básicas de los resultados"""
    resultados_validos = [r for r in results if r.get('prediccion', -1) >= 0]
    con_errores = len(results) - len(resultados_validos)
    
    print(f"\n=== ESTADÍSTICAS ===")
    print(f"Total de imágenes procesadas: {len(results)}")
    print(f"Imágenes procesadas correctamente: {len(resultados_validos)}")
    print(f"Imágenes con errores: {con_errores}")
    
    if resultados_validos:
        confianzas = [r['confianza'] for r in resultados_validos]
        print(f"Confianza promedio: {np.mean(confianzas):.4f}")
        print(f"Confianza mínima: {np.min(confianzas):.4f}")
        print(f"Confianza máxima: {np.max(confianzas):.4f}")
        
        # Distribución de predicciones
        predicciones = [r['prediccion'] for r in resultados_validos]
        unique, counts = np.unique(predicciones, return_counts=True)
        print("\nDistribución de dígitos predichos:")
        for digito, count in zip(unique, counts):
            print(f"  Dígito {digito}: {count} imágenes")

# Función principal
def main():
    # Configuración
    model_path = "densenet_emnist_70.pth"
    base_folder = "F:/2-2025/IA2/ProyectoActasElectorales/Recortes_finales_sin_lineas"
    output_csv = "predicciones_completas.csv"
    
    # Verificar si el modelo existe
    if not os.path.exists(model_path):
        print(f"Error: No se encontró el modelo en {model_path}")
        return
    
    # Verificar si la carpeta base existe
    if not os.path.exists(base_folder):
        print(f"Error: No se encontró la carpeta base: {base_folder}")
        return
    
    # Dispositivo
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Usando dispositivo: {device}")
    
    # Cargar modelo
    print("Cargando modelo...")
    model = load_model(model_path, device)
    print("Modelo cargado exitosamente!")
    
    # Procesar todas las imágenes
    print("\nIniciando procesamiento de todas las imágenes...")
    results = process_all_images(model, base_folder, device, output_csv)
    
    # Mostrar estadísticas
    mostrar_estadisticas(results)
    
    print(f"\nProcesamiento completado. Resultados guardados en: {output_csv}")

if __name__ == "__main__":
    main()