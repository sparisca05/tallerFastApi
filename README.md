# Sistemas Operativos Taller FastAPI
## Integrantes: Simón Parisca, Juan Esteban Castaño y Nicolás Echeverri
### Descripción:
Este proyecto permite realizar algunos métodos HTTP por medio de endpoints utilizando FastAPI y Swagger.
Dichos métodos se realizan en una base de datos (previamente creada) con datos de usuarios que se encuentran en el siguiente link en formato JSON: https://www.datos.gov.co/resource/jtnk-dmga.json
La aplicación se levanta utilizando la herramienta de uvicorn.
### Requisitos:
- WSL 2 Ubuntu
- Crear un ambiente con miniconda:

  Ejecutar:
  ```bash
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
  ```
  ```bash
    bash Miniconda3-latest-Linux-x86_64.sh
  ```
  ```bash
    conda create --name myenv python=3.12
  ```
- Dentro del proyecto ejecuta:
    ```bash
    bash install_requirements.sh
    ```
    
- Para levantar el proyecto ejecuta:
    ```bash
    python -m uvicorn main:app --reload
    ```
  
- Si prefieres que el proyecto se levante siempre al iniciar la máquina (WSL) debes crear el archivo .service de la siguiente forma:

  Ejecutar:
  ```bash
    sudo nano /etc/systemd/system/fastapi_prueba.service
  ```
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
  
  1. Se debe contar con wsl 2, se puede validar en powershell con:
    ```bash
     wsl -l -v
    ```
  3. Correr en WSL:
    ```bash
     sudo nano /etc/wsl.conf
    ```
  4. Copiar lo siguiente:

    [boot]
    systemd=true
  
  5. Correr en powershell:
    ```bash
     wsl --shutdown
    ```
  7. Si todo fue correcto, en Linux al correr lo siguiente debería aparecer systemd: systemctl list-units --type=service

  Para activar el servicio cada que se inicie la máquina:
  1. Recargar los servicios de systemd: sudo systemctl daemon-reload
  2. Iniciar el servicio: sudo systemctl start fastapi_prueba
  3. Habilitar el servicio para que se inicie al arrancar el sistema: sudo systemctl enable fastapi_prueba
  4. Verificar el estado del servicio: sudo systemctl status fastapi_prueba
  5. Parar el servicio: sudo systemctl stop fastapi_prueba

- crear un archivo .env dentro del proyecto

  Debe verse así:
  
    CONDA_ENV=myenv

    DB_HOST='localhost'
    DB_NAME='base_de_datos'
    DB_USER='tu_usuario'
    DB_PASSWORD='tu_contraseña'

- comando para entrar a psql
  ```bash
  sudo -u postgres psql
  ```
  Dentro de psql:
  ```bash
    CREATE DATABASE base_de_datos;
    \c base_de_datos
    CREATE TABLE tabla (
      uid VARCHAR(255) PARIMARY KEY,
      display_name VARCHAR(255) NOT NULL,
      email_address VARCHAR(255) NOT NULL,
      status VARCHAR(50),
      role VARCHAR(50),
      last_active VARCHAR(50)
    );
    CREATE USER tu_usuario WITH PASSWORD 'tu_contraseña';
    GRANT ALL PRIVILEGES ON DATABASE base_de_datos TO tu_usuario;
    GRANT ALL PRIVILEGES ON TABLE tabla TO tu_usuario;
  ```
