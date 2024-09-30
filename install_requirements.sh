#!/bin/bash

# Cargar el archivo .env
export $(grep -v '^#' .env | xargs)

# Activar conda y entorno
source ~/miniconda3/etc/profile.d/conda.sh
conda activate $CONDA_ENV

# Instalar las dependencias del archivo requirements.txt
echo "Instalando las bibliotecas necesarias..."
pip install -r requirements.txt

echo "El entorno virtual ha sido activado y las bibliotecas se han instalado."
