import json
from flask import Flask, jsonify, request
import psycopg2

app = Flask(__name__)

DB_HOST = "timescaledb"
DB_PORT = "5432"
DB_NAME = "mydb"
DB_USER = "myuser"
DB_PASSWORD = "mypassword"

def get_db_connection():
    """Establece una conexión con la base de datos."""
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

@app.route('/data', methods=['GET'])
def get_data():
    """
    Endpoint para obtener datos de la tabla `consumos`.
    Permite filtrar por rango de fechas usando parámetros `start_date` y `end_date`.
    """
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    query = "SELECT * FROM consumos"
    params = []

    if start_date and end_date:
        query += " WHERE timestamp BETWEEN %s AND %s"
        params.extend([start_date, end_date])

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()

        data = [
            {"id": row[0], "timestamp": row[1], "data": row[2]}
            for row in rows
        ]

        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/data', methods=['POST'])
def insert_data():
    """
    Endpoint para insertar datos en la tabla `kafka_messages`.
    Espera un JSON con la clave `data`.
    """
    content = request.json
    if not content:
        return jsonify({"error": "El cuerpo de la solicitud no ha sido encontrado."}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            #"INSERT INTO consumos (data) VALUES (%s) RETURNING id;",
            #[json.dumps(content['data'])]
            "INSERT INTO consumos (id_casa, consumo_kwh, temperatura, irradiacion_solar, placas, produccion_solar_kwh) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;",
            #(content['ID_CASA'], content['CONSUMO_KWH'], content['TEMPERATURA'], content['IRRADIACION_SOLAR'], content['PLACAS'], content['PRODUCCION_SOLAR_KWH'])
            (content['id_casa'], content['consumo_kwh'], content['temperatura'], content['irradiacion_solar'], content['placas'], content['produccion_solar_kwh'])
        )
        conn.commit()
        new_id = cursor.fetchone()[0]

        return jsonify({"message": "Dato insertado correctamente.", "id": new_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)