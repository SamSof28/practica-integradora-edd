from src.structures import LinkedList
from typing import Any, List

class GeneralTree:
  def __init__(self, root: Node = None):
    self.root: Node = root

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

def encontrar_nodos(tupla: tuple[Any, Any]) -> Node:
  new_node: Node = Node(tupla)
  if isinstance(new_node.value[1], dict):
    for dato in new_node.value[1].items():

      new_node.children.append(encontrar_nodos(dato))

  return new_node