import streamlit as st
import pandas as pd
from simulador import calcular_simulacion

VALOR_INDICE_ABRIL = 85.056195
VALOR_INDICE_MAYO  = 87.608881

@st.cache_data
def cargar_datos():
    df = pd.read_excel("Cargos_Abril2025.xlsx", sheet_name="Simulador Abril 2025")
    df["IDENTIFICADOR"] = df["COD."].astype(str).str.strip() + " - " + df["CARGO"].astype(str).str.strip()
    punt_abr = dict(zip(df["IDENTIFICADOR"], df["PUNTAJE 04/2025"]))
    punt_may = dict(zip(df["IDENTIFICADOR"], df["PUNTAJE 05/2025"]))
    return punt_abr, punt_may, sorted(df["IDENTIFICADOR"].dropna().tolist())

st.markdown("<h1 style='text-align:center'>📊 Simulador Salarial Docente – AMET TDF</h1>", unsafe_allow_html=True)

puntajes_abril, puntajes_mayo, lista_cargos = cargar_datos()

antiguedad = st.number_input("Antigüedad (años):", min_value=0, max_value=40, value=0)

st.subheader("Selección de cargos/horas")
cargos, cantidades = [], []
for i in range(3):
    c1, c2 = st.columns([3,1])
    cargo = c1.selectbox(f"Cargo #{i+1}", options=[""] + lista_cargos, key=f"c_{i}")
    cant  = c2.number_input("Cantidad", min_value=0, value=0, key=f"q_{i}")
    cargos.append(cargo); cantidades.append(cant)

gremios = []
g_opc = ["Ninguno","AMET","SUTEF","SUETRA","ATE","UDAF","UDA","UPCN"]
g1 = st.selectbox("Gremio 1", g_opc, index=0)
g2 = st.selectbox("Gremio 2", g_opc, index=0)
if g1 != "Ninguno": gremios.append(g1)
if g2 != "Ninguno" and g2 != g1: gremios.append(g2)

if st.button("Calcular Comparación Abril vs Mayo"):
    abr = calcular_simulacion(cargos, cantidades, puntajes_abril, VALOR_INDICE_ABRIL, antiguedad, gremios)
    may = calcular_simulacion(cargos, cantidades, puntajes_mayo,  VALOR_INDICE_MAYO,  antiguedad, gremios)

    df = pd.DataFrame({
        "Concepto": list(abr.keys()),
        "Abril ($)": list(abr.values()),
        "Mayo ($)":  [may[k] for k in abr],
        "Diferencia ($)": [may[k]-abr[k] if isinstance(abr[k], (int,float)) else 0 for k in abr],
        "Variación (%)": [((may[k]-abr[k])/abr[k]*100) if isinstance(abr[k], (int,float)) and abr[k] else 0 for k in abr]
    })

    def estilo(row):
        return ['background-color:#1f77b4;color:white;font-weight:bold' if row["Concepto"]=="NETO" else '' for _ in row]

    st.dataframe(
        df.style.apply(estilo, axis=1)
              .format({"Abril ($)":"{:,.2f}","Mayo ($)":"{:,.2f}","Diferencia ($)":"{:,.2f}","Variación (%)":"{:+.2f}%"})
    )

    st.subheader("Resultado final")
    st.markdown(f"**Diferencia real (NETO Mayo - NETO Abril):** ${may['NETO']-abr['NETO']:,.2f}")

    if st.checkbox("🔍 Modo debug"):
        st.write("Horas Totales Abril/Mayo:", abr["Horas Totales"], may["Horas Totales"])
        st.write("Unidades Bono:", abr["Unidades Bono"], may["Unidades Bono"])
        st.write("Gremios:", gremios)
