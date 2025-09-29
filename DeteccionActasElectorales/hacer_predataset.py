import os
import shutil

# Definir rutas
source_dir = "Recortes_finales_sin_lineas"
destination_dir = "Pre-dataset"

# Crear la carpeta de destino si no existe
if not os.path.exists(destination_dir):
    os.makedirs(destination_dir)

# Iterar recursivamente sobre la carpeta fuente
for root, dirs, files in os.walk(source_dir):
    for file in files:
        # Verificar si el archivo es una imagen (extensiones comunes)
        if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            # Ruta completa del archivo fuente
            source_file = os.path.join(root, file)
            # Ruta completa del archivo destino
            destination_file = os.path.join(destination_dir, file)
            
            # Manejar nombres de archivo duplicados
            base, ext = os.path.splitext(file)
            counter = 1
            while os.path.exists(destination_file):
                # Agregar un sufijo numérico si el archivo ya existe
                destination_file = os.path.join(destination_dir, f"{base}_{counter}{ext}")
                counter += 1
            
            # Copiar el archivo a la carpeta de destino
            shutil.copy2(source_file, destination_file)
            print(f"Copiado: {source_file} -> {destination_file}")

print("Proceso de copia completado.")