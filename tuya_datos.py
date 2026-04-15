import time
import json
from datetime import datetime
from tuya_connector import TuyaOpenAPI

ACCESS_ID = "g944ut3cseynwr5vhyxg"
ACCESS_SECRET = "5245ef053af94c0faa631085053522f1"
ENDPOINT = "https://openapi.tuyaeu.com"

USER_ID = "eu1687040115730CEb1M" 

TIEMPO_ESPERA = 3600

openapi = TuyaOpenAPI(ENDPOINT, ACCESS_ID, ACCESS_SECRET)
openapi.connect()

def obtener_ids_dispositivos():
    respuesta = openapi.get(f"/v1.0/users/{USER_ID}/devices")
    
    if respuesta.get('success'):
        dispositivos = respuesta.get('result', [])
        lista_de_ids = []             
        for disp in dispositivos:
            lista_de_ids.append(disp['id'])
        return lista_de_ids
    else:
        print(f"Error al obtener dispositivos: {respuesta.get('msg')}")
        return []

def guardar_datos_en_fichero(datos):
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    registro = {
        "fecha": ahora,
        "dispositivos": datos
    }
    
    with open("historial_tuya.jsonl", "a", encoding="utf-8") as archivo:
        archivo.write(json.dumps(registro, ensure_ascii=False) + "\n")


device_ids = obtener_ids_dispositivos()

if not device_ids:
    print("No se han encontrado IDs.")
else:
    print(f"Se han encontrado {len(device_ids)} dispositivos: {device_ids}")
    
    while True:
        
        datos_iteracion = {}
        
        for device_id in device_ids:
            status = openapi.get(f"/v1.0/iot-03/devices/{device_id}/status")
            datos_iteracion[device_id] = status.get('result', status)
            
        guardar_datos_en_fichero(datos_iteracion)
        print("Datos guardados en 'historial_tuya.jsonl'")
        
        time.sleep(TIEMPO_ESPERA)