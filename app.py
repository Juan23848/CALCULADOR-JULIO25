import streamlit as st
import pandas as pd
import numpy as np
import os

try:
    from descuentos import get_descuentos
except ImportError:
    st.error("Error: No se pudo importar 'get_descuentos' desde descuentos.py")

try:
    from bonos import get_bonos
except ImportError:
    st.error("Error: No se pudo importar 'get_bonos' desde bonos.py")

try:
    from salario import calcular_salario
except ImportError:
    st.error("Error: No se pudo importar 'calcular_salario' desde salario.py")

try:
    from antiguedad import calcular_antiguedad
except ImportError:
    st.error("Error: No se pudo importar 'calcular_antiguedad' desde antiguedad.py")

try:
    from simulador import calcular_simulacion
except ImportError:
    st.error("Error: No se pudo importar 'calcular_simulacion' desde simulador.py")

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

# Cargar los puntajes automáticamente
puntajes_df = cargar_puntajes()

if puntajes_df is None:
    st.stop()

# Mostrar interfaz básica para verificar funcionamiento
st.title("Simulador Salarial – Junio 2025")
st.write("Archivo de puntajes cargado con éxito.")
