from src.structures import LinkedList
from typing import Any, List

class GeneralTree:
  """Representa un árbol general con un nodo raíz y múltiples hijos."""

  def __init__(self, root: Node = None):
    """Inicializa el árbol con una raíz opcional.

    Args:
      root (Node, optional): Nodo raíz inicial del árbol. Por defecto es None.
    """
    self.root: Node = root

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
      is_last (bool): Indica si el nodo es el último hijo del nivel.

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

  def insert(self, parent_value: tuple[Any, Any], child_value: tuple[Any, Any], current: Node = None) -> None:
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

class Node:
  """Representa un nodo del árbol general con un valor y una lista de hijos."""

  def __init__(self, value: tuple[Any, Any]) -> None:
    """Inicializa el nodo con un valor y una colección vacía de hijos.

    Args:
      value (tuple[Any, Any]): Par clave-valor que almacena el nodo.
    """
    self.value: tuple[Any, Any] = value
    self.children = LinkedList()

  def __repr__(self) -> str:
    """Devuelve una representación textual compacta del nodo.

    Returns:
      str: Texto que muestra la clave y, si aplica, el valor del nodo.
    """
    if isinstance(self.value, tuple):
      if isinstance(self.value[1], dict):
        return f"{self.value[0]}:"
      return f"{self.value[0]}: {self.value[1]}"
    return f"{self.value}"

def encontrar_nodos(tupla: tuple[Any, Any]) -> Node:
  """Convierte un par clave-valor en un nodo y sus descendientes.

  Args:
    tupla (tuple[Any, Any]): Par clave-valor a convertir en nodo.

  Returns:
    Node: Nodo construido, con hijos recursivos si el valor es un diccionario.
  """
  new_node: Node = Node(tupla)
  if isinstance(new_node.value[1], dict):
    for dato in new_node.value[1].items():

      new_node.children.append(encontrar_nodos(dato))

  return new_node