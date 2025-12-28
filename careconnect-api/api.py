from flask import Flask, jsonify
from flask_cors import CORS
import pymysql

app = Flask(__name__)
CORS(app)

def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="careconnect_app",
        password="careconnect123",
        database="careconnect",
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route("/appointments/upcoming")
def upcoming_appointments():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT
                  a.start_datetime,
                  a.status,
                  p.first_name AS patient,
                  mp.last_name AS provider,
                  c.clinic_name
                FROM appointment a
                JOIN patient p ON p.patient_id = a.patient_id
                JOIN medical_provider mp ON mp.provider_id = a.provider_id
                JOIN clinic c ON c.clinic_id = a.clinic_id
                WHERE a.start_datetime >= NOW()
                ORDER BY a.start_datetime
                LIMIT 10
            """)
            rows = cursor.fetchall()
        return jsonify(rows)
    finally:
        conn.close()

@app.route("/reports/no_show_rate")
def no_show_rate():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT
                  mp.last_name AS provider,
                  ROUND(100 * SUM(a.status='no_show') / COUNT(*), 2) AS no_show_rate
                FROM appointment a
                JOIN medical_provider mp ON mp.provider_id = a.provider_id
                GROUP BY mp.provider_id
                HAVING COUNT(*) > 10
                ORDER BY no_show_rate DESC
                LIMIT 5
            """)
            rows = cursor.fetchall()
        return jsonify(rows)
    finally:
        conn.close()
        
@app.route("/reports/appointments_by_clinic")
def appointments_by_clinic():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT
                  c.clinic_name,
                  COUNT(a.appointment_id) AS total_appointments,
                  SUM(a.status = 'no_show') AS no_shows
                FROM clinic c
                LEFT JOIN appointment a ON a.clinic_id = c.clinic_id
                GROUP BY c.clinic_id
                ORDER BY total_appointments DESC
            """)
            rows = cursor.fetchall()
        return jsonify(rows)
    finally:
        conn.close()


if __name__ == "__main__":
    app.run(debug=True)
