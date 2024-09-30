#!/bin/bash

curl -X GET "http://127.0.0.1:8000/usuarios/jxdi-nmcr"

curl -X POST "http://127.0.0.1:8000/post/" -H "Content-Type: application/json" -d '[
  {
    "uid": "1237",
    "display_name": "Usuario2 Prueba",
    "email_address": "usuario2@prueba.com",
    "status": "enabled",
    "role": "admin",
    "last_active": "2024-09-28"
  }
]'

curl -X GET "http://127.0.0.1:8000/usuarios/1236"

curl -X POST "http://127.0.0.1:8000/post/" -H "Content-Type: application/json" -d '[
  {
    "uid": "1236",
    "display_name": "Usuario Sin Correo",
    "status": "enabled",
    "role": "admin",
    "last_active": "2024-09-28"
  }
]'

curl -X GET "http://127.0.0.1:8000/usuarios/1236"