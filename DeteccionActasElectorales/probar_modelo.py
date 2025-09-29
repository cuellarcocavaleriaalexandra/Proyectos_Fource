import torch
import torch.nn as nn
import torchvision.transforms as transforms
from PIL import Image, ImageOps
import os
import matplotlib.pyplot as plt
import numpy as np

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

# Preprocesamiento de imágenes CORREGIDO
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

# Predecir múltiples imágenes desde una carpeta
def predict_images_from_folder(model, folder_path, device):
    results = []
    supported_formats = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff')
    
    print(f"Buscando imágenes en: {folder_path}")
    
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(supported_formats):
            image_path = os.path.join(folder_path, filename)
            try:
                prediction, confidence = predict_single_image(model, image_path, device)
                results.append({
                    'filename': filename,
                    'path': image_path,
                    'prediction': prediction,
                    'confidence': confidence
                })
                print(f"Imagen: {filename} -> Predicción: {prediction}, Confianza: {confidence:.4f}")
            except Exception as e:
                print(f"Error procesando {filename}: {e}")
    
    return results

# Mostrar comparación antes/después del preprocesamiento
def show_preprocessing_comparison(image_path):
    # Imagen original
    original = Image.open(image_path).convert('L')
    
    # Imagen procesada (sin invertir)
    transform_no_invert = transforms.Compose([
        transforms.Grayscale(num_output_channels=1),
        transforms.Resize((28, 28)),
    ])
    no_invert = transform_no_invert(original)
    
    # Imagen procesada (con inversión)
    transform_with_invert = transforms.Compose([
        transforms.Lambda(lambda img: invert_colors(img)),
        transforms.Grayscale(num_output_channels=1),
        transforms.Resize((28, 28)),
    ])
    with_invert = transform_with_invert(original)
    
    # Mostrar comparación
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    axes[0].imshow(original, cmap='gray')
    axes[0].set_title('Imagen Original')
    axes[0].axis('off')
    
    axes[1].imshow(no_invert, cmap='gray')
    axes[1].set_title('Sin inversión (como el modelo veía)')
    axes[1].axis('off')
    
    axes[2].imshow(with_invert, cmap='gray')
    axes[2].set_title('Con inversión (como debe ser)')
    axes[2].axis('off')
    
    plt.tight_layout()
    plt.show()
    
    # Mostrar histogramas
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    
    axes[0].hist(np.array(no_invert).flatten(), bins=50, alpha=0.7, color='red')
    axes[0].set_title('Histograma sin inversión')
    axes[0].set_xlabel('Valor de pixel')
    axes[0].set_ylabel('Frecuencia')
    
    axes[1].hist(np.array(with_invert).flatten(), bins=50, alpha=0.7, color='green')
    axes[1].set_title('Histograma con inversión')
    axes[1].set_xlabel('Valor de pixel')
    axes[1].set_ylabel('Frecuencia')
    
    plt.tight_layout()
    plt.show()

# Mostrar resultados con imágenes
def display_results(results, num_cols=3):
    num_images = len(results)
    if num_images == 0:
        print("No hay imágenes para mostrar")
        return
    
    num_rows = (num_images + num_cols - 1) // num_cols
    
    fig, axes = plt.subplots(num_rows, num_cols, figsize=(15, 5*num_rows))
    
    # Aplanar el array de axes para facilitar el acceso
    if hasattr(axes, 'flat'):
        axes_flat = axes.flat
    else:
        axes_flat = [axes]
    
    for i, result in enumerate(results):
        # Mostrar imagen original y procesada
        original_image = Image.open(result['path']).convert('L')
        
        # Procesar con inversión para mostrar
        transform = transforms.Compose([
            transforms.Lambda(lambda img: invert_colors(img)),
            transforms.Grayscale(num_output_channels=1),
            transforms.Resize((28, 28)),
        ])
        processed_image = transform(original_image)
        
        axes_flat[i].imshow(processed_image, cmap='gray')
        axes_flat[i].set_title(f'{result["filename"]}\nPred: {result["prediction"]} - Conf: {result["confidence"]:.3f}')
        axes_flat[i].axis('off')
    
    # Ocultar ejes vacíos
    for i in range(len(results), len(axes_flat)):
        axes_flat[i].axis('off')
    
    plt.tight_layout()
    plt.show()

# Función principal
def main():
    # Configuración
    model_path = "densenet_emnist_70.pth"
    images_folder = "F:/2-2025/IA2/ProyectoActasElectorales/Recortes_finales_sin_lineas/mesa_24_1006401_recortada/LIBRE"
    
    # Verificar si el modelo existe
    if not os.path.exists(model_path):
        print(f"Error: No se encontró el modelo en {model_path}")
        return
    
    # Verificar si la carpeta de imágenes existe
    if not os.path.exists(images_folder):
        print(f"Error: No se encontró la carpeta {images_folder}")
        return
    
    # Dispositivo
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Usando dispositivo: {device}")
    
    # Cargar modelo
    print("Cargando modelo...")
    model = load_model(model_path, device)
    print("Modelo cargado exitosamente!")
    
    # Mostrar comparación de preprocesamiento para la primera imagen
    print("\nMostrando comparación de preprocesamiento...")
    image_files = [f for f in os.listdir(images_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff'))]
    if image_files:
        first_image_path = os.path.join(images_folder, image_files[0])
        show_preprocessing_comparison(first_image_path)
    
    # Predecir imágenes
    print("\nIniciando predicciones...")
    results = predict_images_from_folder(model, images_folder, device)
    
    # Mostrar resultados
    if results:
        print(f"\nResumen de predicciones:")
        for result in results:
            print(f"{result['filename']}: Dígito {result['prediction']} (Confianza: {result['confidence']:.4f})")
        
        # Mostrar imágenes con predicciones
        display_results(results)
        
    else:
        print("No se encontraron imágenes válidas en la carpeta especificada.")

if __name__ == "__main__":
    main()