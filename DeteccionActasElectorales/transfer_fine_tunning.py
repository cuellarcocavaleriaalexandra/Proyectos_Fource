import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.transforms as transforms
from torch.utils.data import DataLoader, Dataset
from PIL import Image, ImageOps
import os
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
import shutil
from sklearn.model_selection import train_test_split

# Definir la arquitectura DenseNet
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

# Función para organizar automáticamente el dataset en train/val
def organize_dataset(source_dir, target_dir, test_size=0.2):
    """
    Organiza el dataset en carpetas train y val automáticamente
    """
    print("Organizando dataset en train/val...")
    
    for digit in range(10):
        digit_dir = os.path.join(source_dir, str(digit))
        train_dir = os.path.join(target_dir, 'train', str(digit))
        val_dir = os.path.join(target_dir, 'val', str(digit))
        
        # Crear directorios si no existen
        os.makedirs(train_dir, exist_ok=True)
        os.makedirs(val_dir, exist_ok=True)
        
        # Obtener todas las imágenes del dígito
        images = [f for f in os.listdir(digit_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff'))]
        
        if not images:
            print(f"Advertencia: No se encontraron imágenes para el dígito {digit}")
            continue
        
        # Dividir en train y val
        train_images, val_images = train_test_split(images, test_size=test_size, random_state=42)
        
        # Copiar imágenes a train
        for img in train_images:
            src = os.path.join(digit_dir, img)
            dst = os.path.join(train_dir, img)
            shutil.copy2(src, dst)
        
        # Copiar imágenes a val
        for img in val_images:
            src = os.path.join(digit_dir, img)
            dst = os.path.join(val_dir, img)
            shutil.copy2(src, dst)
        
        print(f"Dígito {digit}: {len(train_images)} train, {len(val_images)} val")

# Dataset personalizado
class CustomDigitDataset(Dataset):
    def __init__(self, root_dir, transform=None, split='train'):
        self.root_dir = root_dir
        self.transform = transform
        self.split = split
        self.images = []
        self.labels = []
        
        split_dir = os.path.join(root_dir, split)
        
        for label in range(10):
            label_dir = os.path.join(split_dir, str(label))
            if os.path.exists(label_dir):
                for img_name in os.listdir(label_dir):
                    if img_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
                        self.images.append(os.path.join(label_dir, img_name))
                        self.labels.append(label)
        
        print(f"{split.capitalize()} dataset: {len(self.images)} imágenes")
        
        # Mostrar distribución de clases
        unique, counts = np.unique(self.labels, return_counts=True)
        print(f"Distribución de clases: {dict(zip(unique, counts))}")
    
    def __len__(self):
        return len(self.images)
    
    def __getitem__(self, idx):
        image_path = self.images[idx]
        label = self.labels[idx]
        
        image = Image.open(image_path).convert('L')
        
        if self.transform:
            image = self.transform(image)
        
        return image, label

# Función para invertir colores
def invert_colors(image):
    return ImageOps.invert(image)

# Transformaciones de datos
def get_transforms():
    train_transform = transforms.Compose([
        transforms.Lambda(invert_colors),
        transforms.Resize((28, 28)),
        transforms.RandomRotation(5),
        transforms.RandomAffine(degrees=0, translate=(0.1, 0.1)),
        transforms.RandomHorizontalFlip(p=0.1),
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
    ])
    
    val_transform = transforms.Compose([
        transforms.Lambda(invert_colors),
        transforms.Resize((28, 28)),
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
    ])
    
    return train_transform, val_transform

# Cargar modelo preentrenado
def load_pretrained_model(model_path, device, freeze_features=True):
    model = DenseNet(num_classes=10)
    checkpoint = torch.load(model_path, map_location=device)
    model.load_state_dict(checkpoint['model_state_dict'])
    
    # Congelar capas características
    if freeze_features:
        for param in model.features.parameters():
            param.requires_grad = False
        for param in model.dense_block1.parameters():
            param.requires_grad = False
        for param in model.transition1.parameters():
            param.requires_grad = False
        for param in model.dense_block2.parameters():
            param.requires_grad = False
        for param in model.transition2.parameters():
            param.requires_grad = False
        for param in model.dense_block3.parameters():
            param.requires_grad = False
    
    model.to(device)
    return model

# Entrenamiento con fine-tuning
def train_model(model, train_loader, val_loader, device, num_epochs=10, learning_rate=0.0001):
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(filter(lambda p: p.requires_grad, model.parameters()), 
                          lr=learning_rate, weight_decay=1e-5)
    scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=5, gamma=0.1)
    
    train_losses = []
    val_losses = []
    train_accuracies = []
    val_accuracies = []
    
    best_val_acc = 0.0
    best_model_path = 'densenet_emnist.pth'
    
    print("Iniciando transfer learning...")
    
    for epoch in range(num_epochs):
        # Entrenamiento
        model.train()
        epoch_train_loss = 0
        epoch_train_acc = 0
        
        train_pbar = tqdm(train_loader, desc=f'Epoch {epoch+1}/{num_epochs} [Train]')
        
        for images, labels in train_pbar:
            images = images.to(device)
            labels = labels.to(device)
            
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            _, preds = torch.max(outputs, 1)
            acc = (preds == labels).float().mean()
            
            epoch_train_loss += loss.item()
            epoch_train_acc += acc.item()
            
            train_pbar.set_postfix({
                'Loss': f'{loss.item():.4f}',
                'Acc': f'{acc.item():.4f}'
            })
        
        avg_train_loss = epoch_train_loss / len(train_loader)
        avg_train_acc = epoch_train_acc / len(train_loader)
        
        # Validación
        model.eval()
        epoch_val_loss = 0
        epoch_val_acc = 0
        
        with torch.no_grad():
            val_pbar = tqdm(val_loader, desc=f'Epoch {epoch+1}/{num_epochs} [Val]')
            
            for images, labels in val_pbar:
                images = images.to(device)
                labels = labels.to(device)
                
                outputs = model(images)
                loss = criterion(outputs, labels)
                
                _, preds = torch.max(outputs, 1)
                acc = (preds == labels).float().mean()
                
                epoch_val_loss += loss.item()
                epoch_val_acc += acc.item()
                
                val_pbar.set_postfix({
                    'Loss': f'{loss.item():.4f}',
                    'Acc': f'{acc.item():.4f}'
                })
        
        avg_val_loss = epoch_val_loss / len(val_loader)
        avg_val_acc = epoch_val_acc / len(val_loader)
        
        # Guardar métricas
        train_losses.append(avg_train_loss)
        train_accuracies.append(avg_train_acc)
        val_losses.append(avg_val_loss)
        val_accuracies.append(avg_val_acc)
        
        # Guardar mejor modelo
        if avg_val_acc > best_val_acc:
            best_val_acc = avg_val_acc
            torch.save({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'val_accuracy': avg_val_acc,
                'train_accuracy': avg_train_acc
            }, best_model_path)
            print(f'✓ Mejor modelo guardado (Val Acc: {avg_val_acc:.4f})')
        
        scheduler.step()
        
        print(f'Epoch [{epoch+1}/{num_epochs}]')
        print(f'  Train - Loss: {avg_train_loss:.4f}, Acc: {avg_train_acc:.4f}')
        print(f'  Val   - Loss: {avg_val_loss:.4f}, Acc: {avg_val_acc:.4f}')
        print('-' * 50)
    
    # Graficar resultados
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    plt.plot(train_losses, label='Train Loss', marker='o')
    plt.plot(val_losses, label='Val Loss', marker='o')
    plt.title('Pérdida durante el entrenamiento')
    plt.xlabel('Época')
    plt.ylabel('Pérdida')
    plt.legend()
    plt.grid(True)
    
    plt.subplot(1, 2, 2)
    plt.plot(train_accuracies, label='Train Accuracy', marker='o')
    plt.plot(val_accuracies, label='Val Accuracy', marker='o')
    plt.title('Precisión durante el entrenamiento')
    plt.xlabel('Época')
    plt.ylabel('Precisión')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig('transfer_learning_results.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return best_model_path

# Función principal
def main():
    # Configuración
    pretrained_model_path = "densenet_emnist.pth"
    source_dataset_path = "DatasetNumeros"  # Tu dataset original
    organized_dataset_path = "DatasetOrganizado"  # Dataset organizado automáticamente
    
    # Verificar modelo preentrenado
    if not os.path.exists(pretrained_model_path):
        print(f"Error: No se encontró el modelo preentrenado en {pretrained_model_path}")
        return
    
    # Verificar dataset fuente
    if not os.path.exists(source_dataset_path):
        print(f"Error: No se encontró el dataset en {source_dataset_path}")
        return
    
    # Organizar dataset automáticamente
    if not os.path.exists(organized_dataset_path):
        organize_dataset(source_dataset_path, organized_dataset_path, test_size=0.2)
    else:
        print("Dataset ya organizado, saltando división...")
    
    # Dispositivo
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Usando dispositivo: {device}")
    
    # Transformaciones
    train_transform, val_transform = get_transforms()
    
    # Cargar datasets organizados
    try:
        train_dataset = CustomDigitDataset(organized_dataset_path, train_transform, 'train')
        val_dataset = CustomDigitDataset(organized_dataset_path, val_transform, 'val')
        
        if len(train_dataset) == 0:
            print("Error: No se encontraron imágenes de entrenamiento")
            return
        if len(val_dataset) == 0:
            print("Error: No se encontraron imágenes de validación")
            return
            
    except Exception as e:
        print(f"Error cargando datasets: {e}")
        return
    
    # DataLoaders
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True, num_workers=2)
    val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False, num_workers=2)
    
    # Cargar modelo preentrenado
    print("Cargando modelo preentrenado...")
    model = load_pretrained_model(pretrained_model_path, device, freeze_features=True)
    
    # Mostrar parámetros entrenables
    total_params = sum(p.numel() for p in model.parameters())
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"Parámetros totales: {total_params:,}")
    print(f"Parámetros entrenables: {trainable_params:,}")
    print(f"Porcentaje de parámetros congelados: {(total_params - trainable_params) / total_params * 100:.2f}%")
    
    # Entrenar con fine-tuning
    best_model_path = train_model(
        model, train_loader, val_loader, device,
        num_epochs=35,
        learning_rate=0.0001
    )
    
    print(f"✅ Entrenamiento completado!")
    print(f"✅ Mejor modelo guardado en: {best_model_path}")
    print(f"✅ Dataset organizado en: {organized_dataset_path}")

if __name__ == "__main__":
    main()