import streamlit as st
import json
import os

from simulador import calcular_simulacion

# Cargar diccionario de cargos desde archivo JSON
with open("diccionario_cargos_completo.json", "r", encoding="utf-8") as f:
    cargos_dict = json.load(f)

# Página
st.set_page_config(page_title="Simulador Salarial Docente", layout="wide")
st.title("Simulador Salarial Docente")
st.caption("Actualizado a Agosto 2025")

# Mostrar los logos si existen
if os.path.exists("ametdf.jpeg") and os.path.exists("ametnac.jpeg"):
    col1, col2 = st.columns([1, 6])
    with col1:
        st.image("ametdf.jpeg", width=100)
        st.image("ametnac.jpeg", width=100)
    with col2:
        st.title("Simulador Salarial Docente")
        st.caption("Actualizado a Agosto 2025")

# Selección de cargos
st.subheader("Cargos")
cargo_seleccionado = st.selectbox(
    "Elegí un cargo", options=list(cargos_dict.keys()),
    help="Escribí el código o el nombre del cargo para filtrar"
)
cantidad = st.number_input("Cantidad", min_value=1, step=1, value=1)

# Parámetros
st.subheader("Parámetros")
vi = st.number_input("Valor Índice (VI)", min_value=0.0, value=86.76, step=0.01)
antiguedad = st.slider("Años de antigüedad", 0, 40, 5)
gremios = st.selectbox("Gremios", options=["AMET", "SUTEF", "SUTEIRA", "ATE", "UDAF", "UDA", "UPCN"])

# Simulación (aquí solo como demostración de conexión)
if st.button("Calcular"):
    st.success(f"Cargo: {cargo_seleccionado} x {cantidad}")
    st.write(f"VI: {vi} | Antigüedad: {antiguedad} años | Gremio: {gremios}")
    # Aquí se llamaría a calcular_simulacion(...) con los datos correctos
