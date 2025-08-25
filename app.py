
import streamlit as st
import pandas as pd
import numpy as np
import os

from descuentos import get_descuentos
from bonos import get_bonos
from salario import calcular_salario
from antiguedad import calcular_antiguedad
from simulator import calcular_simulacion
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

# Crear diccionario de puntajes para búsqueda rápida
puntajes = {}
for _, row in puntajes_df.iterrows():
    codigo = str(row["CODIGO"]).strip()
    nombre = row["CARGO"].strip()
    puntaje = row["PUNTAJE"]
    puntajes[f"{codigo} - {nombre}"] = puntaje

st.image("Python-logo-notext.svg", width=80)
st.title("🧮 Simulador Salarial – Junio 2025")
st.write("Carga tu recibo o elegí cargos desde el listado actualizado.")

# Mostrar valor índice y conectividad actual
valor_indice = st.number_input("Valor Índice VI:", value=87.608881, step=0.000001)
foid_19 = st.number_input("FOID por 19 hs:", value=DEFAULT_FOID_19, step=1000)
conect_total = st.number_input("💻 *Conectividad total*", value=DEFAULT_CONECT_TOTAL, step=1000)
vi = valor_indice

# Antigüedad
antiguedad = st.number_input("Antigüedad (años):", min_value=0, max_value=50, value=13)

# Selección de cargos
cargos = []
cantidades = []

for i in range(3):
    col1, col2 = st.columns([3, 1])
    with col1:
        cargo = st.selectbox(f"Cargo #{i+1}", [""] + list(puntajes.keys()), index=0, key=f"cargo_{i}")
    with col2:
        cantidad = st.number_input("Cantidad", min_value=0, value=0, key=f"cantidad_{i}")
    if cargo and cantidad > 0:
        cargos.append(cargo)
        cantidades.append(cantidad)

# Selección de gremios
def pick_gremios():
    opc = ["NINGUNO", "AMET", "SUTEF", "SUETRA", "ATE", "UDAF", "UDA", "UPCN"]
    g1 = st.selectbox("Gremio 1", opc, index=0)
    g2 = st.selectbox("Gremio 2", opc, index=0)
    gremios = []
    if g1 != "NINGUNO": gremios.append(g1)
    if g2 != "NINGUNO" and g2 != g1: gremios.append(g2)
    return gremios

gremios = pick_gremios()

if st.button("Calcular Junio 2025"):
    res = calcular_simulacion(
        cargos, cantidades, puntajes, vi, antiguedad, gremios,
        foid_19=DEFAULT_FOID_19, conect_total=DEFAULT_CONECT_TOTAL
    )

    df = pd.DataFrame({
        "Concepto": list(res.keys()),
        "Monto ($)": list(res.values())
    })

    try:
        df["Monto ($)"] = df["Monto ($)"].apply(lambda x: float(x) if isinstance(x, (int, float)) else x)
        st.dataframe(df.style.format({"Monto ($)": "{:,.2f}"}))
    except Exception as e:
        st.error(f"Error al mostrar resultados: {e}")
        st.dataframe(df)

    try:
        st.markdown(f"### 🏅 NETO Junio 2025: **${float(res['NETO']):,.2f}**")
    except Exception as e:
        st.error(f"Error mostrando NETO: {e}")
        st.write("Valor NETO bruto:", res["NETO"])
