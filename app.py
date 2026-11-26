from flask import Flask, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Cargar el archivo .env
load_dotenv()

app = Flask(__name__)
# Para que se vean bien las tildes en el navegador /adorno que observe en una pagina web
app.json.ensure_ascii = False

# Conectarse a  mi MongoDB Atlas
cliente = MongoClient(os.getenv("MONGO_URI"))
db = cliente["CURSOS_CTPI_2026-SAMUEL"]
aprendices = db["APRENDICES_LOPEZ"]


#aqui debo poner todas las rutas para poder consultar 
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

# ruta basada en inteligencia artificial ya que no comprendi el error del porque no ejecutaba ;c
@app.route("/api/certificados/<programa>")
def certificados(programa):
    filtro = {"PROGRAMA": programa, "ESTADO_APRENDIZ": "Certificado"}
    campos = {
        "_id": 0,
        "FICHA": 1,
        "NOMBRE": 1,
        "PRIMER_APELLIDO": 1,
        "SEGUNDO_APELLIDO": 1,
    }
    resultado = list(aprendices.find(filtro, campos))
    return jsonify({"Aprendices_Certificados": resultado, "Programa": programa})

@app.route("/api/porCertificar/<int:ficha>/<int:cantidad>")
def porCertificar(ficha, cantidad):
    filtro = {"FICHA": ficha, "ESTADO_APRENDIZ": "Por certificar"}
    campos = {"_id": 0, "FICHA": 1, "PROGRAMA": 1, "NUMERO_DOCUMENTO": 1,
              "NOMBRE": 1, "PRIMER_APELLIDO": 1, "SEGUNDO_APELLIDO": 1}
    # sort con -1 es descendente, limit es la cantidad que se quiere ver
    resultado = aprendices.find(filtro, campos).sort("PRIMER_APELLIDO", -1).limit(cantidad)

    lista = []
    for aprendiz in resultado:
        lista.append(aprendiz)

    return jsonify({"Cantidad de Aprendices por Certificar": lista})

@app.route("/api/terminadaUnificacion/<programa>")
def terminadaUnificacion(programa):
    filtro = {"PROGRAMA": programa, "ESTADO_FICHA": "Terminada por unificación"}
    campos = {"_id": 0, "FICHA": 1, "NUMERO_DOCUMENTO": 1, "NOMBRE": 1,
              "PRIMER_APELLIDO": 1, "SEGUNDO_APELLIDO": 1}
    resultado = aprendices.find(filtro, campos)

    lista = []
    for aprendiz in resultado:
        lista.append(aprendiz)

    return jsonify({"Programa": programa, "Aprendices": lista})

@app.route("/api/aprendicesPrograma/<programa>")
def aprendicesPrograma(programa):
    filtro = {"PROGRAMA": programa}
    campos = {"_id": 0, "PROGRAMA": 1, "FICHA": 1, "NOMBRE": 1,
              "PRIMER_APELLIDO": 1, "SEGUNDO_APELLIDO": 1}
    resultado = aprendices.find(filtro, campos)

    lista = []
    for aprendiz in resultado:
        lista.append(aprendiz)

    return jsonify({"Aprendices": lista})


if __name__ == "__main__":
    app.run(debug=True, port=8000)