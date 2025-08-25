
import streamlit as st
import pandas as pd
import numpy as np
import os
import sys

# Asegura que el directorio actual esté en el path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import descuentos
import bonos
import salario
import antiguedad
import simulador
from pathlib import Path

DEFAULT_FOID_19 = 45000
DEFAULT_CONECT = 142600
DEFAULT_FOID = {19: DEFAULT_FOID_19}
DEFAULT_CONECT_TOTAL = DEFAULT_CONECT

@st.cache_data
def cargar_puntajes():
    file_path = Path("cargos_mayo_2025.xlsx")
    if not file_path.exists():
        st.error("No se encontró el archivo 'cargos_mayo_2025.xlsx'.")
        return None
    return pd.read_excel(file_path)

puntajes_df = cargar_puntajes()

if puntajes_df is not None:
    st.title("Simulador Salarial – Junio 2025")
    st.write("Archivo de puntajes cargado con éxito.")

    valor_indice = st.number_input("Valor índice (VI):", value=87.608881)
    foid_19 = st.number_input("FOID por 19 hs:", value=DEFAULT_FOID_19)
    conectividad = st.number_input("**Conectividad total**:", value=DEFAULT_CONECT)

    antiguedad_input = st.number_input("Antigüedad (años):", min_value=0, value=13)

    st.subheader("Selección de cargos/horas")
    cargos_seleccionados = []
    for i in range(3):
        col1, col2 = st.columns([3, 1])
        with col1:
            cargo_codigo = st.selectbox(f"Cargo #{i+1}", puntajes_df["codigo"], key=f"cargo_{i}")
        with col2:
            cantidad = st.number_input(f"Cantidad", min_value=0, step=1, key=f"cantidad_{i}")

        cargos_seleccionados.append((cargo_codigo, cantidad))

    gremio1 = st.selectbox("Gremio 1", options=["AMET", "SUTEF", "ATE", "UDAF", "UDA", "UPCN", "SUETRA"])
    gremio2 = st.selectbox("Gremio 2", options=["Ninguno", "AMET", "SUTEF", "ATE", "UDAF", "UDA", "UPCN", "SUETRA"])

    if st.button("Calcular Junio 2025"):
        resultado = simulador.calcular_simulacion(
            cargos_seleccionados,
            antiguedad_input,
            puntajes_df,
            valor_indice,
            foid_19,
            conectividad,
            [gremio for gremio in [gremio1, gremio2] if gremio != "Ninguno"]
        )

        st.subheader("Resultado")
        st.json(resultado)

else:
    st.error("No se pudo cargar el archivo de puntajes.")
