### Sistemas Operativos Taller FastAPI
## Integrantes: Simón Parisca, Juan Esteban Castaño y Nicolás Echeverri
### Descripción:
Este proyecto permite realizar algunos métodos HTTP por medio de endpoints utilizando FastAPI y Swagger.
Dichos métodos se realizan en una base de datos (previamente creada) con datos de usuarios que se encuentran en el siguiente link en formato JSON: https://www.datos.gov.co/resource/jtnk-dmga.json
La aplicación se levanta utilizando la herramienta de uvicorn.
### Requisitos:
- WSL 2 Ubuntu
- Crear un ambiente con miniconda:
  Ejecutar:
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
    bash Miniconda3-latest-Linux-x86_64.sh
    conda create --name myenv python=3.12
- Dentro del proyecto ejecuta:
    bash install_requirements.sh
- Para levantar el proyecto ejecuta:
    python -m uvicorn main:app --reload
- Si prefieres que el proyecto se levante siempre al iniciar la máquina (WSL) debes crear el archivo .service de la siguiente forma:
  Ejecutar:
    sudo nano /etc/systemd/system/fastapi_prueba.service
  El archivo debe verse así:
    [Unit]
    Description=FastAPI service
    After=network.target
    
    [Service]
    User=tu_usuario
    Group=tu_grupo
    WorkingDirectory=/ruta/a/tu/proyecto
    ExecStart=/ruta/a/uvicorn main:app --host 0.0.0.0 --port 8000
    Restart=always
    RestartSec=3
    
    [Install]
    WantedBy=multi-user.target
  
  Para habilitar systemd en WSL:
  
  1. Se debe contar con wsl 2, se puede validar en powershell con: wsl -l -v
  2. Correr en WSL: sudo nano /etc/wsl.conf
  3. Copiar lo siguiente:
    [boot]
    systemd=true
  
  4. Correr en powershell: wsl --shutdown
  5. Si todo fue correcto, en Linux al correr lo siguiente debería aparecer systemd: systemctl list-units --type=service

  Para activar el servicio cada que se inicie la máquina:
  1. Recargar los servicios de systemd: sudo systemctl daemon-reload
  2. Iniciar el servicio: sudo systemctl start fastapi_prueba
  3. Habilitar el servicio para que se inicie al arrancar el sistema: sudo systemctl enable fastapi_prueba
  4. Verificar el estado del servicio: sudo systemctl status fastapi_prueba
  5. Parar el servicio: sudo systemctl stop fastapi_prueba

- crear un archivo .env dentro del proyecto
  Debe verse así:
    # Ambiente
    CONDA_ENV=myenv
    
    # Base de datos
    DB_HOST='localhost'
    DB_NAME='base_de_datos'
    DB_USER='tu_usuario'
    DB_PASSWORD='tu_contraseña'
