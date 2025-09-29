import torch
import torch.nn as nn
import torchvision.transforms as transforms
from PIL import Image, ImageOps
import os
import pandas as pd
import csv

# ---------------------------
# Definición del modelo DenseNet (igual que antes)
# ---------------------------
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

# ---------------------------
# Funciones auxiliares
# ---------------------------
def invert_colors(image):
    return ImageOps.invert(image)

def preprocess_image(image_path):
    transform = transforms.Compose([
        transforms.Lambda(lambda img: invert_colors(img)),
        transforms.Grayscale(num_output_channels=1),
        transforms.Resize((28, 28)),
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
    ])
    image = Image.open(image_path)
    image = transform(image)
    return image.unsqueeze(0)

def predict_single_image(model, image_path, device):
    image = preprocess_image(image_path).to(device)
    with torch.no_grad():
        outputs = model(image)
        predicted = torch.argmax(outputs, 1)
    return predicted.item()

def determinar_tipo_imagen(filename):
    filename_lower = filename.lower()
    if "centena" in filename_lower: return "centena"
    if "decena" in filename_lower: return "decena"
    if "unidad" in filename_lower: return "unidad"
    return "desconocido"

# ---------------------------
# Procesamiento por mesa
# ---------------------------
def process_all_images(model, base_folder, device, output_csv="predicciones_final.csv"):
    results = []
    supported_formats = (".png", ".jpg", ".jpeg", ".bmp", ".tiff")
    id_counter = 1

    for mesa_folder in os.listdir(base_folder):
        mesa_path = os.path.join(base_folder, mesa_folder)
        if not os.path.isdir(mesa_path): 
            continue

        mesa_data = {"id": id_counter, "mesa": mesa_folder}

        # Iterar partidos dentro de la mesa
        for partido_folder in os.listdir(mesa_path):
            partido_path = os.path.join(mesa_path, partido_folder)
            if not os.path.isdir(partido_path): 
                continue

            # Guardar los dígitos de centenas, decenas y unidades
            digits = {"centena": 0, "decena": 0, "unidad": 0}

            for filename in os.listdir(partido_path):
                if filename.lower().endswith(supported_formats):
                    image_path = os.path.join(partido_path, filename)
                    tipo = determinar_tipo_imagen(filename)
                    try:
                        pred = predict_single_image(model, image_path, device)
                        if tipo in digits:
                            digits[tipo] = pred
                    except:
                        continue

            # Reconstruir número completo
            total_votos = digits["centena"]*100 + digits["decena"]*10 + digits["unidad"]
            mesa_data[f"votos_{partido_folder}"] = total_votos

        results.append(mesa_data)
        id_counter += 1

    # Guardar CSV final
    df = pd.DataFrame(results)
    df.to_csv(output_csv, index=False, encoding="utf-8")
    print(f"CSV guardado en {output_csv}")

# ---------------------------
# Main
# ---------------------------
def main():
    model_path = "densenet_emnist_70.pth"
    base_folder = "F:/2-2025/IA2/ProyectoActasElectorales/Recortes_finales_sin_lineas"
    output_csv = "predicciones_final.csv"

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = DenseNet(num_classes=10)
    checkpoint = torch.load(model_path, map_location=device)
    model.load_state_dict(checkpoint["model_state_dict"])
    model.to(device)
    model.eval()

    process_all_images(model, base_folder, device, output_csv)

if __name__ == "__main__":
    main()
