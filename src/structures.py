from typing import Any, List, Optional
from tree_logic import GeneralTree

class NodeDocument:
  """
  Nodos que van a contener cada documento de los archivos .json.
  
  Args:
    document: Documentos de los archivos json.
    next: Puntero que le apunta a su documento siguiente en la linkedlist.
  """
  def __init__(self, document: GeneralTree, next = None) -> None:
    self.value: GeneralTree = document
    self.next: NodeDocument | None = next

  def __repr__(self) -> str:
    return f"{self.value}"

class LinkedList:
  """
  La clase LinkedList es la encargada de organizar correctamente los documentos completos

  Args:
    head: Es el primer elemento de nuestra lista enlazada (Nos permite recorrer de manera correcta la lista enlazada)
    tail: Es el ultimo elemento de nuestra lista enlazada
    size: Nos dira el tamaño de nuestra lista enlazada o cuantos documentos hay

  """
  def __init__(self) -> None:
    self.head: Optional[NodeDocument] = None
    self.tail: Optional[NodeDocument] = None
    self.size: int = 0

  def __iter__(self):
    """Permite usar la LinkedList en ciclos 'for'."""
    current = self.head
    while current:
        # Devolvemos el valor (que será un Nodo del árbol)
        yield current.value 
        current = current.next

  def append(self, value: Any) -> None:
    """Permite agregar al final de la LinkedList un Objeto

    Args:
        value: Elemento u Objeto agregar
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
    """Permite eliminar y retornar el ultimo elemento de la LinkedList
    """
    #llegando al penúltimo
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
    """Permite eliminar y retornar el primer elemento de la LinkedList
    """
    if(self.head is None):
      return None

    old_head = self.head
    self.head = self.head.next
    old_head.next = None
    self.size -= 1
    return old_head.value

  def __repr__(self) -> str:
    values = []
    current = self.head
    while current:
      values.append(str(current.value))
      current = current.next
    return " → ".join(values) if values else "[]"

  def __len__(self) -> int:
    """Nos permite obtener el tamaño de linkedlist"""
    return self.size