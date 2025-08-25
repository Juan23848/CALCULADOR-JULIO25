import streamlit as st
st.title("Marca de agua: VERSION v9 🔧")
st.write("Ruta:", __file__)
# app.py (failsafe)

import os
import streamlit as st

# Intentar importar (pero no depender de) get_descuentos
try:
    from descuentos import get_descuentos  # noqa: F401
    IMPORT_ERR = ""
except Exception as e:
    IMPORT_ERR = f"(import falló: {e})"
    get_descuentos = None

from simulador import calcular_simulacion  # usamos solo esto

st.set_page_config(page_title="Simulador Salarial - Failsafe v3", layout="wide")
st.title("Simulador Salarial - Failsafe v3")

if IMPORT_ERR:
    st.warning(f"Aviso: {IMPORT_ERR}")

# Demo inputs
cargos_demo = {
    "001": "Gerente de Finanzas",
    "002": "Analista de Datos",
    "003": "Desarrollador Web"
}

nombre_cargo = st.selectbox("Cargo", list(cargos_demo.values()))
codigo_cargo = [k for k, v in cargos_demo.items() if v == nombre_cargo][0]

vi = st.number_input("Valor índice (VI)", value=1000.0, step=50.0)
antiguedad = st.slider("Años de antigüedad", min_value=0, max_value=40, value=10)
gremios = st.multiselect("Gremios", ["AMET", "SUTEF", "SUETRA", "ATE", "UDAF", "UDA", "UPCN"])

logo_path = f"{codigo_cargo}.png"
if os.path.exists(logo_path):
    st.image(logo_path, width=100)

if st.button("Calcular"):
    resultado = calcular_simulacion(
        cargos=[f"{codigo_cargo} - {nombre_cargo}"],
        cantidades=[1],
        puntajes_dict={f"{codigo_cargo} - {nombre_cargo}": 10.0},
        vi=vi,
        antiguedad=antiguedad,
        gremios=gremios
    )

    st.subheader("Resultado")
    st.metric("Salario Neto", f"${resultado['neto']:,.2f}")
    st.write("**Detalle**")
    st.json({
        "Bruto remunerativo": resultado["bruto_remunerativo"],
        "Bonos no remunerativos (FOID + Conectividad)": resultado["bonos_no_remunerativos"],
        "Bruto total": resultado["bruto_total"],
        "FOID": resultado["foid"],
        "Conectividad": resultado["conectividad"],
        "Descuentos legales": resultado["descuentos_legales"],
        "Descuento gremial": resultado["descuento_gremial"],
        "Descuentos Totales": resultado["descuentos_totales"],
    })
