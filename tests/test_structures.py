import unittest
from src.structures import LinkedList, NodeDocument

class TestNodeDocument(unittest.TestCase):

  def test_crea_nodo_con_valor(self):
    """El nodo almacena correctamente el valor recibido."""
    nodo = NodeDocument("dato")
    self.assertEqual(nodo.value, "dato")

  def test_next_es_none_por_defecto(self):
    """El puntero .next debe ser None si no se especifica."""
    nodo = NodeDocument(42)
    self.assertIsNone(nodo.next)

  def test_next_puede_enlazarse(self):
    """Dos nodos pueden enlazarse manualmente."""
    nodo1 = NodeDocument("a")
    nodo2 = NodeDocument("b")
    nodo1.next = nodo2
    self.assertIs(nodo1.next, nodo2)

  def test_repr_delega_al_valor(self):
    """__repr__ devuelve la representación del valor almacenado."""
    nodo = NodeDocument("hola")
    self.assertEqual(repr(nodo), "hola")


class TestLinkedList(unittest.TestCase):

  # ──────────────── append ────────────────

  def test_append_en_lista_vacia(self):
    """append en lista vacía establece head y tail al mismo nodo."""
    lista = LinkedList()
    lista.append("primero")
    self.assertEqual(lista.size, 1)
    self.assertEqual(lista.head.value, "primero")
    self.assertIs(lista.head, lista.tail)

  def test_append_multiples_elementos(self):
    """Varios append mantienen orden FIFO y actualizan tail."""
    lista = LinkedList()
    lista.append("a")
    lista.append("b")
    lista.append("c")
    self.assertEqual(lista.size, 3)
    self.assertEqual(lista.head.value, "a")
    self.assertEqual(lista.tail.value, "c")

  def test_append_incrementa_size(self):
    """size aumenta con cada append."""
    lista = LinkedList()
    for i in range(5):
      lista.append(i)
    self.assertEqual(lista.size, 5)

  # ──────────────── delete_and_return_first ────────────────

  def test_delete_first_en_lista_vacia(self):
    """delete_and_return_first retorna None si la lista está vacía."""
    lista = LinkedList()
    self.assertIsNone(lista.delete_and_return_first())

  def test_delete_first_con_un_elemento(self):
    """Eliminar el único elemento deja la lista vacía."""
    lista = LinkedList()
    lista.append("único")
    valor = lista.delete_and_return_first()
    self.assertEqual(valor, "único")
    self.assertEqual(lista.size, 0)
    self.assertIsNone(lista.head)

  def test_delete_first_con_varios_elementos(self):
    """delete_and_return_first elimina y retorna el primer elemento."""
    lista = LinkedList()
    lista.append(10)
    lista.append(20)
    lista.append(30)
    valor = lista.delete_and_return_first()
    self.assertEqual(valor, 10)
    self.assertEqual(lista.size, 2)
    self.assertEqual(lista.head.value, 20)

  # ──────────────── delete_and_return_last ────────────────

  def test_delete_last_con_un_elemento(self):
    """Eliminar el único elemento deja la lista vacía."""
    lista = LinkedList()
    lista.append("solo")
    valor = lista.delete_and_return_last()
    self.assertEqual(valor, "solo")
    self.assertEqual(lista.size, 0)
    self.assertIsNone(lista.head)
    self.assertIsNone(lista.tail)

  def test_delete_last_con_varios_elementos(self):
    """delete_and_return_last elimina y retorna el último elemento."""
    lista = LinkedList()
    lista.append("x")
    lista.append("y")
    lista.append("z")
    valor = lista.delete_and_return_last()
    self.assertEqual(valor, "z")
    self.assertEqual(lista.size, 2)
    self.assertEqual(lista.tail.value, "y")

  def test_delete_last_actualiza_tail(self):
    """Tras delete_last, tail apunta al nuevo último nodo."""
    lista = LinkedList()
    lista.append(1)
    lista.append(2)
    lista.delete_and_return_last()
    self.assertEqual(lista.tail.value, 1)
    self.assertIsNone(lista.tail.next)

  # ──────────────── __iter__ ────────────────

  def test_iter_devuelve_valores_en_orden(self):
    """__iter__ recorre los valores en el mismo orden de inserción."""
    lista = LinkedList()
    lista.append("p")
    lista.append("q")
    lista.append("r")
    self.assertEqual(list(lista), ["p", "q", "r"])

  def test_iter_lista_vacia(self):
    """Iterar una lista vacía no produce ningún elemento."""
    lista = LinkedList()
    self.assertEqual(list(lista), [])

  # ──────────────── __len__ ────────────────

  def test_len_lista_vacia(self):
    """len() sobre lista vacía devuelve 0."""
    lista = LinkedList()
    self.assertEqual(len(lista), 0)

  def test_len_tras_operaciones(self):
    """len() refleja el tamaño real después de appends y deletes."""
    lista = LinkedList()
    lista.append(1)
    lista.append(2)
    lista.delete_and_return_first()
    self.assertEqual(len(lista), 1)


if __name__ == "__main__":
  unittest.main()
