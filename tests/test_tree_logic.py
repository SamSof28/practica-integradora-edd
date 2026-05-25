import unittest
from src.tree_logic import Node, GeneralTree, encontrar_nodos

class TestNode(unittest.TestCase):

  def test_crea_nodo_con_valor_primitivo(self):
    """El nodo guarda el diccionario recibido como valor."""
    nodo = Node({"nombre": "Ana"})
    self.assertEqual(nodo.value, {"nombre": "Ana"})

  def test_children_es_lista_enlazada_vacia(self):
    """Al crear un nodo sus hijos son una lista enlazada vacía."""
    nodo = Node({"edad": 25})
    self.assertEqual(len(nodo.children), 0)

  def test_repr_valor_primitivo(self):
    """__repr__ muestra 'clave: valor' para valores primitivos."""
    nodo = Node({"ciudad": "Medellín"})
    self.assertEqual(repr(nodo), "ciudad: Medellín")

  def test_repr_valor_dict(self):
    """__repr__ muestra solo 'clave:' cuando el valor es un dict."""
    nodo = Node({"direccion": {"barrio": "Laureles"}})
    self.assertEqual(repr(nodo), "direccion:")


class TestEncontrarNodos(unittest.TestCase):

  def test_tupla_con_valor_primitivo(self):
    """Una tupla con valor primitivo produce un nodo hoja sin hijos."""
    nodo = encontrar_nodos(("nombre", "Samuel"))
    self.assertEqual(nodo.value, {"nombre": "Samuel"})
    self.assertEqual(len(nodo.children), 0)

  def test_tupla_con_valor_dict_crea_hijos(self):
    """Una tupla con valor dict produce un nodo con hijos recursivos."""
    nodo = encontrar_nodos(("direccion", {"barrio": "Laureles"}))
    self.assertEqual(len(nodo.children), 1)
    hijo = list(nodo.children)[0]
    self.assertEqual(hijo.value, {"barrio": "Laureles"})

  def test_anidamiento_profundo(self):
    """Dicts anidados generan la jerarquía de nodos correctamente."""
    nodo = encontrar_nodos(("a", {"b": {"c": 99}}))
    # a -> b -> c
    hijo_b = list(nodo.children)[0]
    self.assertIn("b", hijo_b.value)
    hijo_c = list(hijo_b.children)[0]
    self.assertEqual(hijo_c.value, {"c": 99})

  def test_valor_entero(self):
    """Valores enteros se preservan sin conversión."""
    nodo = encontrar_nodos(("edad", 30))
    self.assertEqual(nodo.value["edad"], 30)


class TestGeneralTree(unittest.TestCase):

  def _arbol_simple(self):
    """Construye un árbol con dos campos planos: nombre y edad."""
    raiz = Node({"Documento": "0"})
    raiz.children.append(encontrar_nodos(("nombre", "Ana")))
    raiz.children.append(encontrar_nodos(("edad", 25)))
    return GeneralTree(raiz)

  def _arbol_anidado(self):
    """Construye un árbol con un campo nested: direccion.barrio."""
    raiz = Node({"Documento": "0"})
    raiz.children.append(encontrar_nodos(("nombre", "Luis")))
    raiz.children.append(encontrar_nodos(("direccion", {"barrio": "Robledo"})))
    return GeneralTree(raiz)

  # ──────────────── obtener_valor_por_ruta ────────────────

  def test_ruta_simple_existente(self):
    """Una ruta de un nivel retorna el valor correcto."""
    arbol = self._arbol_simple()
    self.assertEqual(arbol.obtener_valor_por_ruta("nombre"), "Ana")

  def test_ruta_simple_entero(self):
    """Retorna correctamente un entero por ruta simple."""
    arbol = self._arbol_simple()
    self.assertEqual(arbol.obtener_valor_por_ruta("edad"), 25)

  def test_ruta_anidada_existente(self):
    """Una ruta compuesta por puntos recorre el subárbol correctamente."""
    arbol = self._arbol_anidado()
    self.assertEqual(arbol.obtener_valor_por_ruta("direccion.barrio"), "Robledo")

  def test_ruta_inexistente_retorna_none(self):
    """Una ruta que no existe retorna None (caso borde)."""
    arbol = self._arbol_simple()
    self.assertIsNone(arbol.obtener_valor_por_ruta("telefono"))

  def test_ruta_parcialmente_incorrecta(self):
    """Una ruta con segundo segmento inexistente retorna None."""
    arbol = self._arbol_anidado()
    self.assertIsNone(arbol.obtener_valor_por_ruta("direccion.ciudad"))

  # ──────────────── a_dict ────────────────

  def test_a_dict_campos_planos(self):
    """a_dict reconstruye el diccionario con campos primitivos."""
    arbol = self._arbol_simple()
    resultado = arbol.a_dict()
    self.assertEqual(resultado["nombre"], "Ana")
    self.assertEqual(resultado["edad"], 25)

  def test_a_dict_campo_anidado(self):
    """a_dict reconstruye correctamente un campo nested."""
    arbol = self._arbol_anidado()
    resultado = arbol.a_dict()
    self.assertIn("direccion", resultado)
    self.assertEqual(resultado["direccion"]["barrio"], "Robledo")

  def test_a_dict_arbol_vacio(self):
    """a_dict sobre árbol vacío retorna diccionario vacío."""
    arbol = GeneralTree()
    self.assertEqual(arbol.a_dict(), {})

  # ──────────────── repr ────────────────

  def test_repr_arbol_vacio(self):
    """__repr__ indica que el árbol está vacío."""
    arbol = GeneralTree()
    self.assertEqual(repr(arbol), "GeneralTree(empty)")

  def test_repr_arbol_con_nodos_contiene_clave(self):
    """__repr__ del árbol no vacío contiene la clave raíz."""
    arbol = self._arbol_simple()
    self.assertIn("Documento", repr(arbol))


if __name__ == "__main__":
  unittest.main()
