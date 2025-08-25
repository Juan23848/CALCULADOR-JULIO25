
import streamlit as st
import pandas as pd
import numpy as np
import os

from descuentos import descuentos_legales
from bonos import get_bonos
from salario import calcular_salario
from antiguedad import calcular_antiguedad
from simulador import calcular_simulacion
from pathlib import Path

DEFAULT_FOID_19 = 45000
DEFAULT_CONECT = 142600
DEFAULT_FOID = {19: DEFAULT_FOID_19}
DEFAULT_CONECT_TOTAL = DEFAULT_CONECT

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

if puntajes_df is None:
    st.stop()

# Acá debería ir el resto del código de la app como ya lo tenías
