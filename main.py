from src.engine import DocumentCollection

# 1. Instanciar la colección
collection = DocumentCollection()

# 2. Cargar datos estructurados
data = [
    {
        "id": 1,
        "nombre": "Ana",
        "edad": 25,
        "ciudad": "Medellín",
        "direccion": { "barrio": "Laureles" }
    },
    {
        "id": 1,
        "nombre": "Ana",
        "edad": 25,
        "ciudad": "Medellín",
        "direccion": { "barrio": "Laureles" }
    }
]
collection.load(data)

print(collection)