# app.py (fixed)
import os
import streamlit as st
from simulador import calcular_simulacion

st.set_page_config(page_title="Simulador Salarial", layout="wide")
st.title("Simulador Salarial - Versión Ajustada")

# Selector de cargos (demo simplificada)
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

# Mostrar logo si existe
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
