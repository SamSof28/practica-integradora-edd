from typing import Any, List, Optional
import json 

class NodeDocument:
  """
  Nodos que van a contener cada documento de los archivos .json.
  
  Args:
    document: Documentos de los archivos json.
    next: Puntero que le apunta a su documento siguiente en la linkedlist.
  """
  def __init__(self, document: Any, next = None) -> None:
    self.value = document
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
    new_node = NodeDocument(value)
    if not self.head:
      self.head = self.tail = new_node
    else:
      assert self.tail is not None
      self.tail.next = new_node
      self.tail = new_node

    self.size += 1

  def delete_and_return_last(self) -> Any:
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
    return self.size


class Node:
  def __init__(self, value: tuple[Any, Any]) -> None:
    self.value: tuple[Any, Any] = value
    self.children = LinkedList()

  def __repr__(self) -> str:
    if isinstance(self.value, tuple):
      if isinstance(self.value[1], dict):
        return f"{self.value[0]}:"
      return f"{self.value[0]}: {self.value[1]}"
    
    return f"{self.value}"
  

class GeneralTree:
  def __init__(self):
    self.root: Node = None

  def __repr__(self) -> str:
    if not self.root:
      return "GeneralTree(empty)"
    return f"\n{self._repr_tree(self.root)}\n"

  def _repr_tree(self, node, prefix="", is_last=True):
    connector = "" if not prefix else ("`-- " if is_last else "|-- ")
    result = f"{prefix}{connector}{node}"

    child_prefix = prefix + ("    " if is_last else "|   ")
    for index, child in enumerate(node.children):
      last_child = index == len(node.children) - 1
      result += "\n" + self._repr_tree(child, child_prefix, last_child)

    return result

  def insert(self, parent_value: tuple[Any, Any], child_value: tuple[Any, Any], current: Node = None) -> None:
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

gt = GeneralTree()
gt.insert(1,2) #parent, child
gt.insert(1,3)
gt.insert(2,4)
gt.insert(4,1)
gt.insert(4,2)
gt.insert(3,6)
gt.insert(3,7)
gt.insert(3,8)
print(gt)

def json_a_arbol(Json: json) -> GeneralTree:
    for indice, document in enumerate(Json):
      tree: GeneralTree = GeneralTree()
      tree.root = Node(("Documento", f"{indice}"))
      for dato in document.items():
        rama = encontrar_nodos(dato)
        tree.root.children.append(rama)

    return tree

def encontrar_nodos(tupla: tuple[Any, Any]) -> None:
  new_node: Node = Node(tupla)
  if isinstance(new_node.value[1], dict):
    for dato in new_node.value[1].items():

      new_node.children.append(encontrar_nodos(dato))

  return new_node

"""mi_dict: dict = {
        "id": 1,
        "name": "John Doe",
        "email": "john.doe@example.com",
        "Ubicación": {
          "Barrio": "Alfonso Lopez",
          "direccion": "Calle 101 #65-1",
          "Encuentro": {
            "Zona": "A",
            "Roe": "B"
          }
        }
    }

print(json_a_arbol(mi_dict))
"""
def leer_archivo(ruta):
    with open(ruta, 'r', encoding='utf-8') as archivo:
        # .load (sin la 's') lee un objeto de archivo
        datos = json.load(archivo) 
    return datos # Esto devuelve una lista o dict de Python

print("----"*5)

print(json_a_arbol(leer_archivo("data/ejemplo1.json")))