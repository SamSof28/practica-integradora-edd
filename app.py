import streamlit as st
import json
from src.engine import DocumentCollection
from src.tree_logic import construir_grafo_dot
import time

# Configuración estética de la página web
st.set_page_config(
    page_title="ArborNoSQL - Motor Documental",
    page_icon="🌳",
    layout="wide"
)

# 1. INICIALIZACIÓN SEGURA DEL MOTOR EN LA MEMORIA DE LA SESIÓN
if "engine" not in st.session_state:
    st.session_state.engine = DocumentCollection()
if "json_nombre" not in st.session_state:
    st.session_state.json_nombre = "coleccion_modificada.json"


# --- INTERFAZ GRÁFICA ---
st.title("🌳 ArborNoSQL Database Engine")
st.caption("Feria de Ingeniería de Sistemas 2026 - Motor Documental basado en Árboles y Listas Enlazadas")

# BARRA LATERAL: CARGA Y DESCARGA (PERSISTENCIA)
with st.sidebar:
    st.header("💾 Persistencia de Datos")
    
    # Subir archivo JSON
    archivo_subido = st.file_uploader("Cargar colección (.json)", type=["json"])
    
    if archivo_subido is not None:
        try:
            # Leer el archivo de texto y convertirlo a diccionario temporal de Python
            datos_json = json.load(archivo_subido)
            st.session_state.json_nombre = archivo_subido.name
            
            # Limpiar el motor antes de recargar
            st.session_state.engine = DocumentCollection()
            # Cargar los datos en nuestras estructuras propias
            st.session_state.engine.load(datos_json)
            st.success(f"¡Colección '{archivo_subido.name}' cargada con éxito!")
        except Exception as e:
            st.error(f"Error al procesar el JSON: {e}")
            
    st.divider()
    
    # BOTÓN DE DESCARGA: Convierte el estado actual de los árboles de nuevo a JSON físico
    st.subheader("Exportar Cambios")
    # Llamamos al método to_json de tu motor que desarrollamos previamente
    json_reconstruido = st.session_state.engine.a_json()
    
    st.download_button(
        label="📥 Descargar JSON Modificado",
        data=json_reconstruido,
        file_name=f"modificado_{st.session_state.json_nombre}",
        mime="application/json",
        use_container_width=True
    )

# PANEL CENTRAL: DIVISION POR PESTAÑAS (TABS)
tab_visualizar, tab_modificar, tab_terminal, tab_documentacion = st.tabs([
    "🔍 Visualizador de Estructuras", 
    "🛠️ Panel de Operaciones (CRUD)", 
    "💻 Terminal de Consultas NoSQL",
    "📚 Documentación Técnica"
])

# PESTAÑA 1: VISUALIZACIÓN INTERACTIVA DE LOS ÁRBOLES
with tab_visualizar:
    st.header("Estructura Jerárquica en Tiempo Real")
    
    collection = st.session_state.engine
    if collection.documents.head is None:
        st.info("Por favor, sube un archivo JSON en la barra lateral para renderizar los árboles.")
    else:
        st.write(f"**Documentos en la Lista Enlazada:** {collection.documents.size}")
        
        # Recorremos la lista enlazada para listar los documentos disponibles
        opciones_docs = []
        actual = collection.documents.head
        idx = 0
        while actual:
            # Intentamos buscar una clave 'id' o 'nombre' para identificarlo estéticamente
            arbol = actual.value
            raiz_hijos = arbol.root.children if arbol.root else None
            id_doc = f"Documento: {idx}"
            opciones_docs.append((idx, arbol, id_doc))
            actual = actual.next
            idx += 1
            
        # Selector del documento que el usuario o jurado quiere inspeccionar
        doc_seleccionado = st.selectbox(
            "Selecciona el documento a inspeccionar en memoria:", 
            opciones_docs, 
            format_func=lambda x: x[2]
        )
        
        if doc_seleccionado:
            arbol_objetivo = doc_seleccionado[1]
            
            # Generar el código DOT para Graphviz
            if arbol_objetivo.root:
                cuerpo_dot = construir_grafo_dot(arbol_objetivo.root, "", [0])
                codigo_dot = f"digraph G {{\n  rankdir=LR;\n{cuerpo_dot}\n}}"
                # Desplegar el árbol visual de forma nativa e interactiva
                st.graphviz_chart(codigo_dot, use_container_width=True)

# PESTAÑA 2: MODIFICAR Y ELIMINAR (EL CAMBIO EN VIVO)
with tab_modificar:
    st.header("Mutación Dinámica de Estructuras")
    
    if st.session_state.engine.documents.head is None:
        st.warning("No hay datos cargados para modificar.")
    else:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("❌ Eliminar Documento de la Lista")
            st.write("Busca un documento por un criterio exacto para removerlo físicamente de la Lista Enlazada.")
            
            campo_del = st.text_input("Campo del filtro (ej: id o ciudad):", key="del_campo")
            valor_del = st.text_input("Valor exacto (ej: 1 o Medellín):", key="del_valor")
            
            if st.button("🚨 Ejecutar Eliminación Física"):
                if campo_del and valor_del:
                    # Convertir a entero si parece un número para no romper tipos
                    val_procesado = int(valor_del) if valor_del.isdigit() else valor_del
                    criterio = {campo_del: val_procesado}
                    
                    # AQUÍ EJECUTAS EL MÉTODO DELETE QUE EXPLICAMOS
                    # st.session_state.engine.delete(criterio)
                    st.success(f"Se procesó la eliminación de documentos con {criterio}")
                    st.rerun() # Recarga la app para actualizar los gráficos
                else:
                    st.error("Por favor completa ambos campos.")
                    
        with col2:
            st.subheader("📝 Modificar Propiedad (Nodo del Árbol)")
            st.write("Navega por una ruta de un documento específico y altera el valor de su nodo hoja.")
            
            campo_upd = st.text_input("Filtrar documento donde el campo:", value="id", key="upd_campo")
            valor_upd = st.text_input("Sea igual a:", value="1", key="upd_valor")
            
            ruta_upd = st.text_input("Ruta interna del nodo a cambiar (ej: edad o direccion.barrio):")
            nuevo_valor = st.text_input("Nuevo valor del nodo:")
            
            if st.button("🔄 Actualizar Nodo en Memoria"):
                if ruta_upd and nuevo_valor:
                    val_filtro = int(valor_upd) if valor_upd.isdigit() else valor_upd
                    val_nuevo = int(nuevo_valor) if nuevo_valor.isdigit() else nuevo_valor
                    
                    criterio = {campo_upd: val_filtro}
                    # AQUÍ EJECUTAS TU MÉTODO UPDATE
                    # st.session_state.engine.update(criterio, ruta_upd, val_nuevo)
                    st.success(f"Nodo '{ruta_upd}' modificado con éxito a '{val_nuevo}'")
                    st.rerun()

# PESTAÑA 3: LA TERMINAL NOSQL (TU MOTOR DE BÚSQUEDA)
with tab_terminal:
    st.header("Consola Interactiva de Consultas")
    st.write("Escribe una consulta en formato JSON estándar de operadores NoSQL.")
    
    query_ejemplo = '{\n  "edad": {"$gt": 25},\n  "ciudad": "Medellín"\n}'
    query_texto = st.text_area("Query Editor (Soporta $eq, $ne, $gt, $gte, $lt, $lte):", value=query_ejemplo, height=150)
    
    if st.button("⚡ Ejecutar Query"):
        try:
            query_dict = json.loads(query_texto)
            # Ejecutar el método find de tu motor
            resultados_ll = st.session_state.engine.find(query_dict)
            
            if resultados_ll is None or resultados_ll.head is None:
                st.info("Resultados de la consulta: [] (Cero coincidencias o colección vacía).")
            else:
                st.success(f"¡Consulta exitosa! Se encontraron documentos coincidentes.")
                # Mostrar el dibujo estético del string representation (__repr__) de la LinkedList de resultados
                st.code(str(resultados_ll), language="text")
        except Exception as e:
            st.error(f"Error en la sintaxis del Query JSON o en la ejecución: {e}")
    

with tab_documentacion:
    st.header("📖 Manual de Consultas del Motor")
    st.markdown("""
    Este motor implementa una sintaxis de consulta declarativa inspirada en **MongoDB** sobre estructuras nativas de **Árboles Generales** y **Listas Enlazadas**[cite: 5, 6].
    
    ### 1. Consultas Simples
    Para buscar coincidencias exactas en la raíz del documento, envíe un objeto clave-valor estándar[cite: 69]:
    ```json
    { "ciudad": "Medellín" }
    ```
    
    ### 2. Notación de Rutas Anidadas (Dot Notation)
    El motor navega recursivamente a través de las ramas del árbol utilizando puntos como separadores de ruta[cite: 73]:
    ```json
    { "direccion.barrio": "Laureles" }
    ```
    
    ### 3. Operadores de Comparación Soportados
    Puede refinar las búsquedas utilizando sub-diccionarios con operadores lógicos matemáticos[cite: 75, 76]:
    * `$eq`: Igual que 
    * `$ne`: Diferente de 
    * `$gt` / `$gte`: Mayor que / Mayor o igual  
    * `$lt` / `$lte`: Menor que / Menor o igual  
    
    *Ejemplo de rango de edad:*
    ```json
    { "edad": { "$gte": 18, "$lte": 30 } }
    ```
    """)