import streamlit as st
from simulador import calcular_simulacion
from descuentos import get_descuentos

st.set_page_config(page_title="Simulador Salarial", layout="wide")

st.title("Simulador Salarial - Versión Ajustada")

# Selector de cargos (demo simplificada)
cargos = {
    "001": "Gerente de Finanzas",
    "002": "Analista de Datos",
    "003": "Desarrollador Web"
}

nombre_cargo = st.selectbox("Cargo", list(cargos.values()))
codigo_cargo = [k for k, v in cargos.items() if v == nombre_cargo][0]

remunerativo = st.number_input("Remunerativo base", min_value=0.0, step=100.0)
bonos = st.number_input("Bonos adicionales", min_value=0.0, step=50.0)
vi = st.number_input("Valor índice (VI)", value=1000.0, step=50.0)
antiguedad = st.slider("Años de antigüedad", min_value=0, max_value=40, value=10)
gremios = st.multiselect("Gremios", ["AMET", "SUTEF", "SUETRA", "ATE", "UDAF", "UDA", "UPCN"])

# Mostrar logo si existe
import os
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

    total_descuentos = resultado["descuentos_legales"]["total"] + resultado["descuento_gremial"]["total"]
    salario_final = resultado["remunerativo_total"] - total_descuentos

    st.write("### Resultado:")
    st.write(f"Salario final: ${salario_final:,.2f}")
    st.write("Detalle de descuentos:")
    st.json(resultado["descuentos_legales"])
    st.json(resultado["descuento_gremial"])