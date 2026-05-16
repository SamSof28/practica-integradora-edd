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
    """Representa una colección de documentos cargados como árboles.

    La colección mantiene cada documento como un `GeneralTree` dentro de una
    lista enlazada para poder recorrerlos y administrarlos de forma ordenada.
    """

    def __init__(self):
        """Inicializa una colección vacía de documentos."""
        self.documents = LinkedList() # Aquí guardas objetos GeneralTree

    def __repr__(self) -> str:
        """Devuelve una representación legible de la colección.

        Returns:
            str: Texto con la representación de la lista enlazada interna.
        """
        return f"{self.documents}"

    def load(self, data: list):
        """Carga una lista de diccionarios y los convierte en árboles.

        Args:
            data (list): Lista de documentos estructurados en forma de diccionario.
        """
        for indice, document in enumerate(data):
            raiz = Node(("Documento", f"{indice}"))
            for dato in document.items():
                raiz.children.append(encontrar_nodos(dato))

            nuevo_arbol = GeneralTree(raiz)
            self.documents.append(nuevo_arbol)

    def find(self, criteria: dict):
        """Busca documentos que coincidan con los criterios recibidos.

        Args:
            criteria (dict): Criterios de búsqueda a aplicar sobre los documentos.

        Returns:
            Any: Resultado de la búsqueda. Actualmente no está implementado.
        """
        pass