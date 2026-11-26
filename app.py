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

if __name__ == "__main__":
    app.run(debug=True, port=8000)