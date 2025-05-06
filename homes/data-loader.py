import json
import logging
import time
import threading
import requests
import pandas as pd

API_URL = "http://localhost:30002/ingest"

def send_message(message):
    try:
        response = requests.post(API_URL, json=message)
        if response.status_code == 200:
            print("Mensaje enviado correctamente al ingestor")
        else:
            print("Fallo en el envío. Respuesta:", response.text)
    except Exception as e:
        print("Error al conectar con el ingestor Kafka:", str(e))

def message_loop(thread_id, df):
    logging.info("Thread %d: procesando datos del CSV", thread_id)

    df_filtered = df[df['casa_id'] == thread_id]
    if df_filtered.empty:
        logging.warning("Thread %d: no se encontraron datos para esta casa", thread_id)
        return

    for _, row in df_filtered.iterrows():
        mensaje = {
            "id_casa": row['casa_id'],
            "fecha": row['fecha'],
            "consumo_kwh": row['consumo_kwh'],
            "temperatura": row['temperatura'],
            "irradiacion_solar": row['irradiacion_solar'],
            "placas": bool(row['Tiene_Placas']),
            "produccion_solar_kwh": row['Produccion_Solar_kWh']
        }

        send_message(mensaje)
        time.sleep(1)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(threadName)s] %(levelname)s: %(message)s')

    file_path = "raw-data.csv"

    try:
        df = pd.read_csv(file_path)
        df = df.sort_values(by=['fecha'])

        casa_ids = sorted(df['casa_id'].dropna().unique())
    except Exception as e:
        logging.error("Error leyendo el archivo CSV: %s", str(e))
        exit(1)

    threads = []

    for casa_id in casa_ids:
        thread = threading.Thread(target=message_loop, args=(casa_id, df))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
