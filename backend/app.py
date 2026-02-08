import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, request, jsonify
from flask_cors import CORS
from algorithm.routing_algorithm import route_vulnerability_case
from data.sample_inputs import ngos
from database import create_tables, connect_db

app = Flask(__name__)
CORS(app)

create_tables()

@app.route("/route", methods=["POST"])
def route_case():
    report = request.json
    result = route_vulnerability_case(report, ngos)

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO reports VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        report["id"],
        report["lat"],
        report["lon"],
        report["condition"],
        result["priority_score"],
        result["assigned_ngo"],
        result["status"]
    ))

    conn.commit()
    conn.close()

    return jsonify(result)

@app.route("/cases", methods=["GET"])
def get_cases():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM reports")
    rows = cursor.fetchall()
    conn.close()

    return jsonify(rows)

@app.route("/")
def home():
    return "CareNet Backend Running"

if __name__ == "__main__":
    app.run(debug=True)

