
import streamlit as st
import pandas as pd
import numpy as np
import os

from descuentos import get_descuentos
from bonos import get_bonos
from salario import calcular_salario
from antiguedad import calcular_antiguedad
from simulador import calcular_simulacion
from pathlib import Path

# Mostrar los logos
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    st.image("ametdf.jpeg", use_column_width=True)
with col3:
    st.image("ametnac.jpeg", use_column_width=True)

st.markdown("## Simulador Salarial – Junio 2025")

# Cargar archivo de puntajes desde el repositorio directamente
@st.cache_data
def cargar_puntajes():
    file_path = Path("cargos_mayo_2025.xlsx")
    if not file_path.exists():
        st.error("No se encontró el archivo 'cargos_mayo_2025.xlsx'.")
        return None
    return pd.read_excel(file_path)

# Cargar los puntajes automáticamente
puntajes_df = cargar_puntajes()

if puntajes_df is None or puntajes_df.empty:
    st.stop()

# Mostrar controles iniciales
valor_indice = st.number_input("Valor índice (VI):", value=87.61)
antiguedad_anios = st.number_input("Antigüedad (años):", min_value=0, value=13)

st.markdown("### Selección de cargos/horas")

# Crear opciones legibles para el selectbox
puntajes_df["display"] = puntajes_df["codigo"].astype(str) + " - " + puntajes_df["nombre"]

cargos_seleccionados = []
cantidades = []

for i in range(3):
    col1, col2 = st.columns(2)
    with col1:
        cargo = st.selectbox(f"Cargo #{i+1}", options=puntajes_df["display"], key=f"cargo_{i}")
    with col2:
        cantidad = st.number_input(f"Cantidad", min_value=0, value=0, key=f"cantidad_{i}")
    cargos_seleccionados.append(cargo)
    cantidades.append(cantidad)

# Gremios
GREMIO_OPCIONES = ["Ninguno", "AMET", "SUETF", "SUETRA", "ATE", "UDAF", "UDA", "UPCN"]
gremio1 = st.selectbox("Gremio 1", GREMIO_OPCIONES, index=1)
gremio2 = st.selectbox("Gremio 2", GREMIO_OPCIONES, index=0)

# Botón de cálculo
if st.button("Calcular Junio 2025"):

    # Armar lista de códigos y extraer puntajes
    codigos = [c.split(" - ")[0] for c in cargos_seleccionados]
    puntajes = []
    for cod in codigos:
        try:
            puntaje = puntajes_df.loc[puntajes_df["codigo"] == int(cod), "puntaje"].values[0]
        except IndexError:
            st.error(f"No se encontró puntaje para el código {cod}")
            st.stop()
        puntajes.append(puntaje)

    # Calcular salario
    resultado = calcular_simulacion(codigos, cantidades, puntajes, valor_indice, antiguedad_anios, [gremio1, gremio2])

    # Mostrar resultado
    st.subheader("Resultado de la Simulación:")
    for key, val in resultado.items():
        st.write(f"**{key}**: ${val:,.2f}")
