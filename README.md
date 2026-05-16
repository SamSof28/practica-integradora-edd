# **Practica Integradora - Estructuras de Datos Dinamicos**

![Python](https://img.shields.io/badge/python-3.14+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![JSON](https://img.shields.io/badge/data-JSON-000000?style=for-the-badge&logo=json&logoColor=white)

---

# ArborNexus Engine 🌳🔗
> **Mini motor documental NoSQL basado en estructuras jerárquicas y lineales propias.**

Proyecto integrador para la materia **Estructuras de Datos (2026-1)**. El sistema está diseñado para emular el comportamiento de una colección documental NoSQL (como MongoDB) utilizando árboles generales y listas enlazadas construidas desde cero.

---

## 🚀 Objetivo del Proyecto
Diseñar e implementar un sistema autónomo de almacenamiento y consulta de documentos JSON, transformando cada registro en un árbol general propio y organizando la colección completa dentro de una lista enlazada de documentos.

## 🏗️ Arquitectura del Sistema
Para cumplir con las restricciones estrictas del proyecto, la arquitectura se divide en clases nativas interconectadas, eliminando por completo el uso de listas (`[]`) o diccionarios (`{}`) nativos de Python para la persistencia estructural interna:

1. **Estructura Lineal (`src/structures.py`)**
   * `NodeDocument`: Nodo de control que encapsula el contenido de la lista enlazada.
   * `LinkedList`: Lista enlazada propia utilizada tanto para almacenar los documentos de la colección como para la lista de hijos de cada nodo del árbol.

2. **Estructura Jerárquica (`src/tree_logic.py`)**
   * `Node`: Representa un par clave-valor (atributo de un documento JSON). Maneja de forma recursiva los tipos primitivos y objetos anidados.
   * `GeneralTree`: Encapsula la raíz del documento y gestiona la visualización jerárquica estética.

3. **Motor de Datos (`src/engine.py`)**
   * `DocumentCollection`: Interfaz de cara al usuario que expone los métodos de carga de archivos, conversión bidireccional y motor de búsqueda con operadores avanzados.

---

## ✨ Características y Requisitos Soportados

* **Conversión Bidireccional:** Serialización completa de JSON a Árbol y deserialización inversa desde el Árbol a formato estructurado JSON.
* **Tipos de Datos Autónomos:** Soporte nativo para cadenas de texto, valores numéricos, booleanos, identificadores nulos (`null`) y objetos anidados complejos.
* **Motor de Consultas Avanzado:**
  * Consultas simples y por rutas anidadas mediante notación de puntos (ej: `direccion.barrio`).
  * Soporte de operadores lógicos de comparación: `$eq`, `$ne`, `$gt`, `$gte`, `$lt`, `$lte`.
  * Filtros multi-condicionales combinados (operación lógica AND implícita).

---

## 🛠️ Ejemplos de Uso

```python
from src.engine import DocumentCollection

# 1. Instanciar la colección
collection = DocumentCollection()

# 2. Cargar datos estructurados
data = [
    {
        "id": 1,
        "nombre": "Ana",
        "edad": 25,
        "ciudad": "Medellín",
        "direccion": { "barrio": "Laureles" }
    }
]
collection.load(data)

# 3. Consultas avanzadas por rutas y operadores
resultados = collection.find({"direccion.barrio": "Laureles", "edad": {"$gte": 18}})
print(resultados)

```

---

## 📊 Análisis de Complejidad Algorítmica

* **Carga de Documentos:** **O(N * M)** donde *N* es la cantidad de documentos JSON y *M* el número de atributos/campos internos procesados recursivamente.
* **Búsqueda por Ruta:** **O(D * C)** donde *D* representa la profundidad máxima de la ruta provista (splits) y *C* es el número de hijos en la lista enlazada local por nivel.
* **Consulta sobre la Colección:** **O(N * P)** siendo *N* el tamaño de la lista enlazada de documentos y *P* el costo de evaluar cada predicado sobre los árboles.
* **Conversión de Árbol a JSON:** **O(V)** donde *V* es la cantidad total de nodos que componen el árbol del documento, visitando cada elemento una única vez de manera recursiva.

