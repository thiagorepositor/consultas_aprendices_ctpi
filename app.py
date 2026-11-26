from flask import Flask, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Cargar el archivo .env
load_dotenv()

app = Flask(__name__)
# Para que se vean bien las tildes en el navegador
app.json.ensure_ascii = False

# Conectarse a MongoDB Atlas
cliente = MongoClient(os.getenv("MONGO_URI"))
db = cliente["CURSOS_CTPI_2026-SAMUEL"]
aprendices = db["APRENDICES_LOPEZ"]


# AQUÍ VAN LAS RUTAS
@app.route("/api/cantidadAprendices")
def cantidadAprendices():
    cantidad = aprendices.count_documents({})
    return jsonify({"CantidadAprendices": cantidad})

@app.route("/api/cantidadAprendices/<nivel>")
def cantidadPorNivel(nivel):
    cantidad = aprendices.count_documents({"NIVEL_DE_FORMACION": nivel})
    return jsonify({"CantidadAprendices": cantidad, "Nivel de formación": nivel})

@app.route("/api/programas/<nivel>")
def programasPorNivel(nivel):
    # distinct trae los nombres sin repetir
    programas = aprendices.distinct("PROGRAMA", {"NIVEL_DE_FORMACION": nivel})
    return jsonify({"nivel de formación": nivel, "programas": programas})

if __name__ == "__main__":
    app.run(debug=True, port=8000)