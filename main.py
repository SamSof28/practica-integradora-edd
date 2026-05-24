from src.engine import DocumentCollection
import json
import os

os.system("clear")

# 1. Instanciar la colección
collection = DocumentCollection()

def leer_archivo(ruta):
    with open(ruta, 'r', encoding='utf-8') as archivo:
        # .load (sin la 's') lee un objeto de archivo
        datos = json.load(archivo) 
    return datos # Esto devuelve una lista o dict de Python


data = leer_archivo("data/ejemplo1.json")
collection.load(data)

print(collection.find({
"ciudad": "Medellín",
"edad": {"$gte": 50}
}))
print("----"*5)

print(collection)
