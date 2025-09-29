import os
import shutil

# Definir la ruta relativa de la carpeta de origen y destino
source_dir = "ACTAS_PROCESADAS/Chuquisaca/Oropeza/Sucre/Sucre"
destination_dir = "ActasSucreProcesadas"

# Extensiones de archivos de imagen permitidas
image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')

# Crear la carpeta de destino si no existe
if not os.path.exists(destination_dir):
    os.makedirs(destination_dir)

# Recorrer todas las subcarpetas y archivos en la carpeta Sucre
for root, dirs, files in os.walk(source_dir):
    for file in files:
        # Verificar si el archivo tiene una extensión de imagen
        if file.lower().endswith(image_extensions):
            # Ruta completa del archivo de origen
            source_file = os.path.join(root, file)
            # Ruta completa del archivo de destino
            destination_file = os.path.join(destination_dir, file)
            
            # Si ya existe un archivo con el mismo nombre, agregar un sufijo
            base, extension = os.path.splitext(file)
            counter = 1
            while os.path.exists(destination_file):
                destination_file = os.path.join(destination_dir, f"{base}_{counter}{extension}")
                counter += 1
            
            # Copiar la imagen a la carpeta de destino
            shutil.copy2(source_file, destination_file)
            print(f"Copiado: {source_file} -> {destination_file}")

print("Proceso completado. Todas las imágenes han sido copiadas a", destination_dir)