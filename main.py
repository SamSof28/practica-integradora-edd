from src.engine import DocumentCollection
import json
import os

os.system("cls")

# 1. Instanciar la colección
collection = DocumentCollection()

def leer_archivo(ruta):
    with open(ruta, 'r', encoding='utf-8') as archivo:
        # .load (sin la 's') lee un objeto de archivo
        datos = json.load(archivo) 
    return datos # Esto devuelve una lista o dict de Python


data = leer_archivo("data/deep_dataset.json")
collection.load(data)

print(collection.find({
    "usuario.perfil.personal.contacto.direccion.ubicacion.coordenadas.metadata.zona.clasificacion.detalles.transporte.informacion.rutas": {
        "$gte": 5,
        "$lte": 15
    },
    "usuario.perfil.personal.contacto.direccion.ubicacion.coordenadas.metadata.zona.clasificacion.detalles.transporte.informacion.estado": {
        "$ne": "suspendido"
    }
})
)
print("----"*5)

print(collection)

print(collection.documents.head)

print(collection.documents.head.value.mayusculas_nivel_k(4))

print(collection.documents.head.value)