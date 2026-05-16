from src.structures import LinkedList
from src.tree_logic import GeneralTree, Node, encontrar_nodos
import json

"""def leer_archivo(ruta):
    with open(ruta, 'r', encoding='utf-8') as archivo:
        # .load (sin la 's') lee un objeto de archivo
        datos = json.load(archivo) 
    return datos # Esto devuelve una lista o dict de Python

print("----"*5)
"""

class DocumentCollection:
    def __init__(self):
        self.documents = LinkedList() # Aquí guardas objetos GeneralTree

    def __repr__(self) -> str:
        return f"{self.documents}"

    def load(self, data: list):
        """Recibe una lista de dicts y los convierte en árboles."""
        for indice, document in enumerate(data):
            raiz = Node(("Documento", f"{indice}"))
            for dato in document.items():
                raiz.children.append(encontrar_nodos(dato))

            nuevo_arbol = GeneralTree(raiz)
            self.documents.append(nuevo_arbol)

    def find(self, criteria: dict):
        # Aquí irá tu lógica de búsqueda (la haremos después)
        pass