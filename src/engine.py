from src.structures import LinkedList
from src.tree_logic import GeneralTree, Node, encontrar_nodos
import json

class DocumentCollection:
    def __init__(self):
        self.documents = LinkedList() # Aquí guardas objetos GeneralTree

    def load(self, data: list):
        """Recibe una lista de dicts y los convierte en árboles."""
        for item in data:
            # 1. Crear raíz artificial para el documento
            raiz = Node(("Documento", ""))
            # 2. Llenar con la lógica recursiva
            for k, v in item.items():
                raiz.children.append(encontrar_nodos(k, v))
            # 3. Guardar el árbol en la lista enlazada
            nuevo_arbol = GeneralTree(raiz)
            self.documents.append(nuevo_arbol)

    def find(self, criteria: dict):
        # Aquí irá tu lógica de búsqueda (la haremos después)
        pass