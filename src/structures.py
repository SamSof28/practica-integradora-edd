from typing import Any, Optional, TYPE_CHECKING

if TYPE_CHECKING:
  from src.tree_logic import GeneralTree, Node

class NodeDocument:
  """Nodo de la lista enlazada que almacena un documento o árbol.

  Args:
    document (GeneralTree | Node): Valor que se guarda en el nodo.
    next (NodeDocument | None): Referencia al siguiente nodo de la lista.
  """
  def __init__(self, document: GeneralTree, next = None) -> None:
    self.value: GeneralTree | Node = document
    self.next: NodeDocument | None = next

  def __repr__(self) -> str:
    """Devuelve una representación textual del valor almacenado.

    Returns:
      str: Texto legible del contenido del nodo.
    """
    return f"{self.value}"

class LinkedList:
  """Implementa una lista enlazada simple para guardar documentos.

  La estructura permite agregar, recorrer y eliminar documentos manteniendo
  referencias al primer y al último nodo.
  """
  def __init__(self) -> None:
    """Inicializa una lista enlazada vacía."""
    self.head: Optional[NodeDocument] = None
    self.tail: Optional[NodeDocument] = None
    self.size: int = 0

  def __iter__(self):
    """Permite iterar sobre los valores almacenados en la lista.

    Yields:
      Any: Cada elemento guardado en la lista enlazada.
    """
    current = self.head
    while current:
        yield current.value 
        current = current.next

  def append(self, value: Any) -> None:
    """Agrega un valor al final de la lista enlazada.

    Args:
        value (Any): Elemento u objeto que se almacenará en un nuevo nodo.
    """
    new_node = NodeDocument(value)
    if not self.head:
      self.head = self.tail = new_node
    else:
      assert self.tail is not None
      self.tail.next = new_node
      self.tail = new_node

    self.size += 1

  def delete_and_return_last(self) -> Any:
    """Elimina y retorna el último elemento de la lista enlazada.

    Returns:
      Any: Valor almacenado en el último nodo eliminado.
    """
    if(self.size == 1):
      old_tail = self.head
      self.head = None
      self.tail = None
      self.size -= 1
      return old_tail.value

    current = self.head
    while(current.next != self.tail):
      current = current.next

    old_tail = self.tail
    self.tail = current
    self.tail.next = None

    self.size -= 1
    return old_tail.value

  def delete_and_return_first(self) -> Any:
    """Elimina y retorna el primer elemento de la lista enlazada.

    Returns:
      Any: Valor almacenado en el primer nodo eliminado, o None si está vacía.
    """
    if(self.head is None):
      return None

    old_head = self.head
    self.head = self.head.next
    old_head.next = None
    self.size -= 1
    return old_head.value

  def __repr__(self) -> str:
    """Devuelve una representación legible de la lista enlazada.

    Returns:
      str: Cadena con todos los elementos separados por flechas.
    """
    values = []
    current = self.head
    while current:
      values.append(str(current.value.root))
      current = current.next
    return " → ".join(values) if values else "[]"

  def __len__(self) -> int:
    """Devuelve la cantidad de nodos almacenados en la lista.

    Returns:
      int: Tamaño actual de la lista enlazada.
    """
    return self.size