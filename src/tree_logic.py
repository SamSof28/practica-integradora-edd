from __future__ import annotations
from src.structures import LinkedList
from typing import Any, Optional

class GeneralTree:
  """Representa un árbol general con un nodo raíz y múltiples hijos."""

  def __init__(self, root: Optional[Node] = None):
    """Inicializa el árbol con una raíz opcional.

    Args:
      root (Node, optional): Nodo raíz inicial del árbol. Por defecto es None.
    """
    self.root: Optional[Node] = root

  def __repr__(self) -> str:
    """Devuelve una representación en texto del árbol.

    Returns:
      str: Cadena con la estructura jerárquica del árbol.
    """
    if not self.root:
      return "GeneralTree(empty)"
    return f"\n{self._repr_tree(self.root)}\n"

  def _repr_tree(self, node, prefix="", is_last=True):
    """Construye recursivamente la representación textual de un subárbol.

    Args:
      node (Node): Nodo actual a representar.
      prefix (str): Prefijo visual acumulado para dibujar la jerarquía.
      is_last (bool): Indica si el nodo es
 el último hijo del nivel.

    Returns:
      str: Texto con el subárbol representado.
    """
    connector = "" if not prefix else ("`-- " if is_last else "|-- ")
    result = f"{prefix}{connector}{node}"

    child_prefix = prefix + ("    " if is_last else "|   ")
    for index, child in enumerate(node.children):
      last_child = index == len(node.children) - 1
      result += "\n" + self._repr_tree(child, child_prefix, last_child)

    return result

  def insert(self, parent_value: dict[Any, Any], child_value: dict[Any, Any], current: Optional[Node] = None) -> None:
    """Inserta un nodo hijo debajo del primer padre que coincida.

    Args:
      parent_value (tuple[Any, Any]): Valor del nodo padre a localizar.
      child_value (tuple[Any, Any]): Valor del nodo hijo a insertar.
      current (Node, optional): Nodo actual usado en la búsqueda recursiva.

    Returns:
      bool: True si la inserción se realizó correctamente, False en caso contrario.
    """
    if(current is None):
      current = self.root

    if(self.root is None):
      self.root = Node(parent_value)
      self.root.children.append(Node(child_value))
      return True

    if(current.value == parent_value):
      current.children.append(Node(child_value))
      return True

    for child in current.children:
      if(self.insert(parent_value, child_value, child)):
        return True

    return False
  
  def obtener_valor_por_ruta(self, ruta: str) -> Any:
    """Busca en el árbol siguiendo una ruta separada por puntos (ej: 'direccion.barrio').

    Args:
        ruta (str): La ruta del atributo a consultar.

    Returns:
        Any: El valor del atributo si existe, o None si la ruta no es válida.
    """
    partes = ruta.split('.')
    return self._buscar_por_ruta_recursivo(self.root, partes)

  def _buscar_por_ruta_recursivo(self, nodo_actual: Optional[Node], partes: list[str]) -> Any:
    if not nodo_actual or not partes:
      return None

    clave_objetivo = partes[0]

    # Recorremos la lista enlazada de hijos del nodo actual
    for hijo in nodo_actual.children:
      # Validamos si la clave objetivo existe dentro del diccionario del nodo
      if isinstance(hijo.value, dict) and clave_objetivo in hijo.value:
        # CASO BASE: Si es la última parte de la ruta, devolvemos su valor real
        if len(partes) == 1:
          return hijo.value[clave_objetivo]
        
        # CASO RECURSIVO: Si faltan más niveles, seguimos bajando por sus hijos
        return self._buscar_por_ruta_recursivo(hijo, partes[1:])

    return None # Caso borde: la ruta consultada no existe en este documento

  def a_dict(self) -> dict[Any, Any]:
    """Convierte el árbol de vuelta a un diccionario Python (árbol → JSON).

    Recorre recursivamente los hijos del nodo raíz y reconstruye el
    diccionario original. El nodo raíz sintético "Documento" se omite.

    Returns:
      dict[Any, Any]: Diccionario que representa el documento original.
    """
    if not self.root:
      return {}
    return self._nodo_a_dict(self.root)

  def _nodo_a_dict(self, nodo: Optional[Node]) -> dict[Any, Any]:
    """Reconstruye recursivamente un diccionario a partir de un nodo.

    Args:
      nodo (Node): Nodo actual a convertir.

    Returns:
      dict[Any, Any]: Diccionario reconstruido desde ese nodo hacia abajo.
    """
    resultado: dict[Any, Any] = {}

    for hijo in nodo.children:
      if not isinstance(hijo.value, dict):
        continue

      clave, valor = next(iter(hijo.value.items()))

      # Si el nodo tiene hijos propios, el valor era un dict: reconstruimos
      if len(hijo.children) > 0:
        resultado[clave] = self._nodo_a_dict(hijo)
      else:
        resultado[clave] = valor

    return resultado
  
  def mayusculas_nivel_k(self, k: int, current: Optional[Node] = None, indice: int = 0) -> None:
    if self.root is None:
      return
    
    if current is None:
      current = self.root
      
    niveles: dict[int, list] = {}
        
    if k == indice:
      for elementos in current.value:
        if isinstance(current.value[elementos], str):
          current.value[elementos] = current.value[elementos].upper()
          return
    
    
    if indice in niveles:
      niveles[indice].append(current)
    else:
      niveles[indice] = [current]
      
    
    for child in current.children:
      self.mayusculas_nivel_k(k, child, indice + 1)
      
      
      
class Node:
  """Representa un nodo del árbol general con un valor y una lista de hijos."""

  def __init__(self, value: dict[Any, Any]) -> None:
    """Inicializa el nodo con un valor y una colección vacía de hijos.

    Args:
      value (dict[Any, Any]): Par clave-valor que almacena el nodo.
    """
    self.value: dict[Any, Any] = value
    self.children = LinkedList()

  def __repr__(self) -> str:
    """Devuelve una representación textual compacta del nodo.

    Returns:
      str: Texto que muestra la clave y, si aplica, el valor del nodo.
    """
    if isinstance(self.value, dict):
      key, value = next(iter(self.value.items()))
      if isinstance(value, dict):
        return f"{key}:"
      return f"{key}: {value}"
    return f"{self.value}"

def encontrar_nodos(tupla: tuple[Any, Any] | dict[Any, Any]) -> Node:
  """Convierte un par clave-valor en un nodo y sus descendientes.

  Args:
    tupla (tuple[Any, Any] | dict[Any, Any]): Par clave-valor a convertir en nodo.

  Returns:
    Node: Nodo construido, con hijos recursivos si el valor es un diccionario.
  """
  if isinstance(tupla, tuple):
    key, value = tupla
    node_value = {key: value}
  else:
    node_value = tupla

  new_node: Node = Node(node_value)

  key, value = next(iter(new_node.value.items()))
  if isinstance(value, dict):
    for dato in value.items():

      new_node.children.append(encontrar_nodos(dato))

  return new_node