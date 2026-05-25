import unittest
import json
from src.engine import DocumentCollection, evaluar_condicion

# Dataset de prueba reutilizable en todos los tests
DATOS = [
  {
    "id": 1,
    "nombre": "Ana",
    "edad": 25,
    "ciudad": "Medellín",
    "direccion": {"barrio": "Laureles"}
  },
  {
    "id": 2,
    "nombre": "Samuel",
    "edad": 18,
    "ciudad": "Medellín",
    "direccion": {"barrio": "Alfonso Lopez"}
  },
  {
    "id": 3,
    "nombre": "Carlos",
    "edad": 55,
    "ciudad": "Bogotá",
    "direccion": {"barrio": "Chapinero"}
  }
]


class TestEvaluarCondicion(unittest.TestCase):

  # ──────────────── igualdad simple ────────────────

  def test_igualdad_string_verdadero(self):
    self.assertTrue(evaluar_condicion("Medellín", "Medellín"))

  def test_igualdad_string_falso(self):
    self.assertFalse(evaluar_condicion("Bogotá", "Medellín"))

  def test_igualdad_entero_verdadero(self):
    self.assertTrue(evaluar_condicion(25, 25))

  def test_igualdad_entero_falso(self):
    self.assertFalse(evaluar_condicion(25, 30))

  # ──────────────── operadores de comparación ────────────────

  def test_gt_verdadero(self):
    self.assertTrue(evaluar_condicion(30, {"$gt": 20}))

  def test_gt_falso(self):
    self.assertFalse(evaluar_condicion(10, {"$gt": 20}))

  def test_gte_igual(self):
    self.assertTrue(evaluar_condicion(20, {"$gte": 20}))

  def test_gte_mayor(self):
    self.assertTrue(evaluar_condicion(21, {"$gte": 20}))

  def test_gte_menor(self):
    self.assertFalse(evaluar_condicion(19, {"$gte": 20}))

  def test_lt_verdadero(self):
    self.assertTrue(evaluar_condicion(5, {"$lt": 10}))

  def test_lt_falso(self):
    self.assertFalse(evaluar_condicion(15, {"$lt": 10}))

  def test_lte_igual(self):
    self.assertTrue(evaluar_condicion(10, {"$lte": 10}))

  def test_ne_distinto(self):
    self.assertTrue(evaluar_condicion("Bogotá", {"$ne": "Medellín"}))

  def test_ne_igual(self):
    self.assertFalse(evaluar_condicion("Medellín", {"$ne": "Medellín"}))

  def test_eq_operador_explicito(self):
    self.assertTrue(evaluar_condicion(42, {"$eq": 42}))

  # ──────────────── casos borde ────────────────

  def test_tipo_incompatible_no_lanza_excepcion(self):
    """Comparar string con entero retorna False sin lanzar TypeError."""
    self.assertFalse(evaluar_condicion("texto", {"$gt": 10}))

  def test_condicion_none_contra_none(self):
    self.assertTrue(evaluar_condicion(None, None))


class TestDocumentCollection(unittest.TestCase):

  def setUp(self):
    """Crea y carga una colección fresca antes de cada test."""
    self.coleccion = DocumentCollection()
    self.coleccion.load(DATOS)

  # ──────────────── load ────────────────

  def test_load_crea_cantidad_correcta_de_documentos(self):
    """load debe crear un árbol por cada documento del JSON."""
    self.assertEqual(len(self.coleccion.documents), 3)

  def test_load_en_coleccion_vacia(self):
    """load sobre colección vacía (lista []) deja la colección sin documentos."""
    col = DocumentCollection()
    col.load([])
    self.assertEqual(len(col.documents), 0)

  # ──────────────── find — consultas simples ────────────────

  def test_find_por_ciudad(self):
    """find filtra correctamente por campo de texto."""
    resultados = self.coleccion.find({"ciudad": "Medellín"})
    self.assertEqual(len(resultados), 2)

  def test_find_sin_resultados(self):
    """find retorna lista vacía cuando ningún documento cumple el criterio."""
    resultados = self.coleccion.find({"ciudad": "Cali"})
    self.assertEqual(len(resultados), 0)

  def test_find_por_entero_exacto(self):
    """find por igualdad de entero retorna el documento correcto."""
    resultados = self.coleccion.find({"edad": 18})
    self.assertEqual(len(resultados), 1)
    doc = list(resultados)[0]
    self.assertEqual(doc.obtener_valor_por_ruta("nombre"), "Samuel")

  # ──────────────── find — operadores de comparación ────────────────

  def test_find_con_gte(self):
    """$gte filtra documentos cuyo campo sea mayor o igual al valor."""
    resultados = self.coleccion.find({"edad": {"$gte": 25}})
    self.assertEqual(len(resultados), 2)  # Ana (25) y Carlos (55)

  def test_find_con_gt(self):
    """$gt filtra documentos cuyo campo sea estrictamente mayor."""
    resultados = self.coleccion.find({"edad": {"$gt": 25}})
    self.assertEqual(len(resultados), 1)  # solo Carlos (55)

  def test_find_con_lt(self):
    """$lt filtra documentos cuyo campo sea estrictamente menor."""
    resultados = self.coleccion.find({"edad": {"$lt": 25}})
    self.assertEqual(len(resultados), 1)  # solo Samuel (18)

  def test_find_con_lte(self):
    """$lte filtra documentos cuyo campo sea menor o igual."""
    resultados = self.coleccion.find({"edad": {"$lte": 25}})
    self.assertEqual(len(resultados), 2)  # Ana (25) y Samuel (18)

  def test_find_con_ne(self):
    """$ne excluye documentos cuyo campo sea igual al valor."""
    resultados = self.coleccion.find({"ciudad": {"$ne": "Medellín"}})
    self.assertEqual(len(resultados), 1)  # solo Carlos

  # ──────────────── find — AND lógico (múltiples criterios) ────────────────

  def test_find_multiples_criterios_and(self):
    """Múltiples criterios se combinan con lógica AND."""
    resultados = self.coleccion.find({"ciudad": "Medellín", "edad": {"$gte": 25}})
    self.assertEqual(len(resultados), 1)  # solo Ana

  def test_find_and_sin_coincidencia(self):
    """AND entre dos criterios incompatibles retorna lista vacía."""
    resultados = self.coleccion.find({"ciudad": "Bogotá", "edad": {"$lt": 18}})
    self.assertEqual(len(resultados), 0)

  # ──────────────── find — rutas anidadas ────────────────

  def test_find_por_ruta_anidada(self):
    """find con dot-path navega correctamente el subárbol."""
    resultados = self.coleccion.find({"direccion.barrio": "Laureles"})
    self.assertEqual(len(resultados), 1)
    doc = list(resultados)[0]
    self.assertEqual(doc.obtener_valor_por_ruta("nombre"), "Ana")

  def test_find_ruta_anidada_inexistente(self):
    """Una ruta anidada que no existe no lanza excepción, retorna vacío."""
    resultados = self.coleccion.find({"direccion.pais": "Colombia"})
    self.assertEqual(len(resultados), 0)

  # ──────────────── a_json ────────────────

  def test_a_json_retorna_string(self):
    """a_json retorna una cadena de texto."""
    resultado = self.coleccion.a_json()
    self.assertIsInstance(resultado, str)

  def test_a_json_es_json_valido(self):
    """a_json retorna JSON que puede parsearse de vuelta."""
    resultado = self.coleccion.a_json()
    lista = json.loads(resultado)
    self.assertIsInstance(lista, list)

  def test_a_json_cantidad_documentos(self):
    """a_json contiene tantos elementos como documentos cargados."""
    lista = json.loads(self.coleccion.a_json())
    self.assertEqual(len(lista), 3)

  def test_a_json_round_trip_campo_plano(self):
    """Los campos planos se reconstruyen con el valor original."""
    lista = json.loads(self.coleccion.a_json())
    nombres = [doc["nombre"] for doc in lista]
    self.assertIn("Ana", nombres)
    self.assertIn("Samuel", nombres)
    self.assertIn("Carlos", nombres)

  def test_a_json_round_trip_campo_anidado(self):
    """Los campos anidados se reconstruyen correctamente."""
    lista = json.loads(self.coleccion.a_json())
    barrios = [doc["direccion"]["barrio"] for doc in lista]
    self.assertIn("Laureles", barrios)
    self.assertIn("Chapinero", barrios)

  def test_a_json_coleccion_vacia(self):
    """a_json sobre colección vacía retorna lista JSON vacía."""
    col = DocumentCollection()
    self.assertEqual(json.loads(col.a_json()), [])


if __name__ == "__main__":
  unittest.main()
