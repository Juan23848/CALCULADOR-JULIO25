import streamlit as st
from descuentos import get_descuentos
from simulador import calcular_salario  # Asumo que esta es tu lógica principal

st.set_page_config(page_title="Simulador Salarial", layout="wide")

st.title("Simulador Salarial - Versión Ajustada")

# Simulación de selector de cargos con nombres
cargos = {
    "001": "Gerente de Finanzas",
    "002": "Analista de Datos",
    "003": "Desarrollador Web"
}

# Mostrar solo nombres
nombre_cargo = st.selectbox("Cargo", list(cargos.values()))
codigo_cargo = [k for k, v in cargos.items() if v == nombre_cargo][0]

# Evitar errores si cargo está vacío
if not codigo_cargo:
    st.warning("Por favor, seleccioná un cargo válido.")
    st.stop()

# Inputs restantes
remunerativo = st.number_input("Remunerativo", min_value=0.0, step=100.0)
bonos = st.number_input("Bonos", min_value=0.0, step=50.0)
gremios = st.multiselect("Gremios", ["AMET", "SUTEF", "SUETRA", "ATE", "UDAF", "UDA", "UPCN"])

# Mostrar logo correspondiente
import os
from PIL import Image

logo_path = f"{codigo_cargo}.png"
if os.path.exists(logo_path):
    st.image(logo_path, width=100)

# Calcular
if st.button("Calcular"):
    descuentos = get_descuentos(remunerativo, bonos, gremios)
    salario_final = calcular_salario(remunerativo, bonos, descuentos)
    st.success(f"Salario final: ${salario_final:,.2f}")