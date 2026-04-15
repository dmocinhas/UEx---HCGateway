import time
import json
import requests
from datetime import datetime

URL_BASE = "http://localhost:6644"

USUARIO = "Spilab"
CONTRASENA = "Spilab"

TIPOS_DE_DATOS = ["steps", "heartRate", "sleepSession", "weight"]

TIEMPO_ESPERA = 3600


url_login = f"{URL_BASE}/api/v2/login"
datos_login = {
    "username": USUARIO,
    "password": CONTRASENA
}

respuesta_login = requests.post(url_login, json=datos_login)

if respuesta_login.status_code == 200 or respuesta_login.status_code == 201:
    token = respuesta_login.json().get("token")
else:
    print(f"Error en el login: {respuesta_login.text}")
    exit()

cabeceras = {
    "Authorization": f"Bearer {token}"
}



while True:
    hora_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    for tipo in TIPOS_DE_DATOS:
        
        url_datos = f"{URL_BASE}/api/v2/fetch/{tipo}"
        
        respuesta_datos = requests.post(url_datos, headers=cabeceras, json={})
        
        if respuesta_datos.status_code == 200:
            info_salud = respuesta_datos.json()
            
            registro = {
                "fecha": hora_actual,
                "datos": info_salud
            }
            
            nombre_archivo = f"historial_{tipo}.jsonl"
            
            with open(nombre_archivo, "a", encoding="utf-8") as archivo:
                archivo.write(json.dumps(registro, ensure_ascii=False) + "\n")
                
            print(f"{len(info_salud)} registros de '{tipo}' guardados en '{nombre_archivo}'")
            
        else:
            print(f"Error al obtener {tipo}: {respuesta_datos.text}")

    time.sleep(TIEMPO_ESPERA)