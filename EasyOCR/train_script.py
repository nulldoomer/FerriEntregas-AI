import os
import subprocess

# Configura las rutas correctamente
train_data = os.path.abspath("./dataset")
model_storage = os.path.abspath("./trainer/saved_models")
epochs = 50

# Construye el comando
command = [
    "python",
    "trainer/train.py",
    "--train_data",
    train_data,
    "--model_storage_directory",
    model_storage,
    "--epochs",
    str(epochs),
    "--verbose",
]

# Ejecuta el entrenamiento
print(f"Ejecutando: {' '.join(command)}\n")
process = subprocess.run(command, capture_output=True, text=True)

# Muestra la salida
print(process.stdout)
print(process.stderr)
