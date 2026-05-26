from src.structures import LinkedList
from src.tree_logic import GeneralTree, Node, encontrar_nodos, KeyValuePair
from typing import Any

import operator
import json

"""def leer_archivo(ruta):
    with open(ruta, 'r', encoding='utf-8') as archivo:
        # .load (sin la 's') lee un objeto de archivo
        datos = json.load(archivo) 
    return datos # Esto devuelve una lista o dict de Python

print("----"*5)
"""

DICCIONARIO_OPERADORES: dict[str, Any] = {
    "$eq": operator.eq,   # (==)
    "$ne": operator.ne,   # (!=)
    "$gt": operator.gt,   # (>)
    "$gte": operator.ge,  # (>=)
    "$lt": operator.lt,   # (<)
    "$lte": operator.le   # (<=)
}

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

    def load(self, data: list) -> None:
        """Carga una lista de diccionarios y los convierte en árboles.

        Args:
            data (list): Lista de documentos estructurados en forma de diccionario.
        """
        for indice, document in enumerate(data):
            raiz = Node(KeyValuePair("Documento", f"{indice}"))
            for dato in document.items():
                raiz.children.append(encontrar_nodos(dato))

            nuevo_arbol = GeneralTree(raiz)
            self.documents.append(nuevo_arbol)

    def a_json(self) -> str:
        """Convierte todos los documentos de la colección a una cadena JSON.

        Recorre cada árbol de la colección, llama a su método `a_dict` para
        reconstruir el diccionario original (uso temporal permitido) y lo
        serializa usando json.dumps. Los documentos se recopilan en una
        lista de Python temporalmente solo para serialización JSON.

        Returns:
            str: Representación JSON de todos los documentos de la colección.
        """
        # Usamos una lista de Python temporalmente solo para serializar a JSON
        # (uso temporal permitido por restricciones)
        lista_documentos: list[dict[Any, Any]] = []
        for documento in self.documents:
            lista_documentos.append(documento.a_dict())
        return json.dumps(lista_documentos, ensure_ascii=False, indent=2)

    def find(self, criterio: dict) -> LinkedList:
        """Busca y filtra los documentos que cumplan con todos los criterios.

        Args:
            criterio (dict): Diccionario con las rutas y condiciones de búsqueda.

        Returns:
            LinkedList: Una nueva lista enlazada con los árboles que coincidieron.
        """
        resultados: LinkedList = LinkedList()

        # Caso borde exigido: la colección está vacía
        if self.documents is None:
            return resultados

        # Recorremos cada árbol (documento) de la colección linealmente
        for documento in self.documents:
            cumple_con_todo = True

            # Evaluamos cada una de las condiciones del criterio de búsqueda
            for ruta, condicion in criterio.items():
                valor_real = documento.obtener_valor_por_ruta(ruta)

                # Si una sola condición falla, descartamos el documento inmediatamente
                if not evaluar_condicion(valor_real, condicion):
                    cumple_con_todo = False
                    break

            # Si pasó todos los filtros exitosamente, lo añadimos a los resultados
            if cumple_con_todo:
                resultados.append(documento)

        return resultados

def evaluar_condicion(valor_documento: Any, condicion: Any) -> bool:
    """Compara el valor del documento contra la condición usando métodos especiales."""
    
    # Si la condición es un diccionario (ej: {"$gt": 25})
    if isinstance(condicion, dict):
        for op_texto, valor_esperado in condicion.items():
            # Verificamos si el operador existe en nuestro mapeo de métodos especiales
            if op_texto not in DICCIONARIO_OPERADORES:
                raise ValueError(f"Operador desconocido: {op_texto}")
            
            operacion = DICCIONARIO_OPERADORES[op_texto]
            try:
                # Aquí se ejecuta el método especial (ej: valor_documento.__gt__(valor_esperado))
                if not operacion(valor_documento, valor_esperado):
                    return False
            except TypeError:
                # Caso borde: Intentar comparar un string con un entero ("Ana" > 25)
                return False
        return True
    
    # Si es una consulta simple (ej: {"ciudad": "Medellín"}), usamos la igualdad común
    return valor_documento == condicion


