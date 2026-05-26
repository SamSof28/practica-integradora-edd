from __future__ import annotations
from src.structures import LinkedList
from typing import Any, Optional

class KeyValuePair:
  """Representa un par clave-valor que almacena un nodo del árbol.
  
  Esta clase reemplaza el uso de diccionarios de Python como estructura
  interna del árbol, permitiendo su uso solo temporalmente para lectura
  inicial, consultas y reconstrucción JSON.
  """
  
  def __init__(self, key: Any, value: Any) -> None:
    """Inicializa un par clave-valor.
    
    Args:
      key (Any): La clave del par.
      value (Any): El valor del par.
    """
    self.key: Any = key
    self.value: Any = value
  
  def __repr__(self) -> str:
    """Devuelve una representación textual del par clave-valor.
    
    Returns:
      str: Texto con formato 'clave: valor'.
    """
    if isinstance(self.value, dict):
      return f"{self.key}:"
    return f"{self.key}: {self.value}"
  
  def __eq__(self, other: Any) -> bool:
    """Compara dos pares clave-valor.
    
    Args:
      other (Any): Otro objeto para comparar.
    
    Returns:
      bool: True si ambos tienen la misma clave y valor.
    """
    if isinstance(other, KeyValuePair):
      return self.key == other.key and self.value == other.value
    return False

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

  def insert(self, parent_value: KeyValuePair, child_value: KeyValuePair, current: Optional[Node] = None) -> None:
    """Inserta un nodo hijo debajo del primer padre que coincida.

    Args:
      parent_value (KeyValuePair): Valor del nodo padre a localizar.
      child_value (KeyValuePair): Valor del nodo hijo a insertar.
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
      # Validamos si la clave objetivo coincide con la del nodo
      if isinstance(hijo.value, KeyValuePair) and hijo.value.key == clave_objetivo:
        # CASO BASE: Si es la última parte de la ruta, devolvemos su valor real
        if len(partes) == 1:
          return hijo.value.value
        
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
      if not isinstance(hijo.value, KeyValuePair):
        continue

      clave = hijo.value.key
      valor = hijo.value.value

      # Si el nodo tiene hijos propios, el valor era un dict: reconstruimos
      if len(hijo.children) > 0:
        resultado[clave] = self._nodo_a_dict(hijo)
      else:
        resultado[clave] = valor

    return resultado

class Node:
  """Representa un nodo del árbol general con un valor y una lista de hijos."""

  def __init__(self, value: KeyValuePair) -> None:
    """Inicializa el nodo con un valor y una colección vacía de hijos.

    Args:
      value (KeyValuePair): Par clave-valor que almacena el nodo.
    """
    self.value: KeyValuePair = value
    self.children: LinkedList = LinkedList()

  def __repr__(self) -> str:
    """Devuelve una representación textual compacta del nodo.

    Returns:
      str: Texto que muestra la clave y, si aplica, el valor del nodo.
    """
    return str(self.value)

def encontrar_nodos(tupla: tuple[Any, Any]) -> Node:
  """Convierte un par clave-valor en un nodo y sus descendientes.

  Args:
    tupla (tuple[Any, Any]): Par clave-valor a convertir en nodo.

  Returns:
    Node: Nodo construido, con hijos recursivos si el valor es un diccionario.
  """
  key, value = tupla
  node_value: KeyValuePair = KeyValuePair(key, value)
  new_node: Node = Node(node_value)

  # Si el valor es un diccionario (estructura temporal permitida),
  # creamos nodos hijos recursivamente
  if isinstance(value, dict):
    for dato in value.items():
      new_node.children.append(encontrar_nodos(dato))

  return new_node