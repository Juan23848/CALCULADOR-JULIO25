import streamlit as st
import pandas as pd
from simulador import calcular_simulacion

st.set_page_config(page_title="Simulador – Junio 2025", page_icon="📊", layout="centered")

DEFAULT_VI = 87.608881     # Mayo–Junio–Julio 2025
DEFAULT_FOID = 45000.0     # FOID por 19 hs
DEFAULT_CONECT = 142600.0  # Conectividad/Materiales total (prorrateable)

@st.cache_data
def cargar_puntajes(origen):
    df = pd.read_excel(origen, sheet_name=None)
    # Elegimos hoja con 'Simulador' si existe; sino la primera
    hoja = None
    for n in df.keys():
        if "simulador" in str(n).lower():
            hoja = n
            break
    if hoja is None:
        hoja = list(df.keys())[0]
    data = df[hoja].copy()
    data.columns = [str(c).strip() for c in data.columns]

    # Columnas flexibles
    def col_like(opciones):
        for c in data.columns:
            up = c.upper().replace(".", "").replace("Ó", "O")
            for o in opciones:
                if o in up:
                    return c
        return None

    col_cod = col_like(["COD", "CÓD"])
    col_cargo = col_like(["CARGO"])
    if not col_cod or not col_cargo:
        raise KeyError("No se encontraron columnas de código y/o cargo.")

    cols_puntaje = [c for c in data.columns if "PUNTAJE" in c.upper()]
    if not cols_puntaje:
        raise KeyError("No se encontró ninguna columna con 'PUNTAJE'.")
    col_puntaje = cols_puntaje[-1]  # la última

    data["IDENTIFICADOR"] = data[col_cod].astype(str).str.strip() + " - " + data[col_cargo].astype(str).str.strip()
    puntajes = dict(zip(data["IDENTIFICADOR"], data[col_puntaje]))
    lista_cargos = sorted([x for x in data["IDENTIFICADOR"].dropna().tolist()])
    meta = {"hoja": hoja, "col_puntaje": col_puntaje, "col_cod": col_cod, "col_cargo": col_cargo}
    return puntajes, lista_cargos, meta

st.markdown("<h1 style='text-align:center'>📊 Simulador Salarial – Junio 2025</h1>", unsafe_allow_html=True)
archivo = st.file_uploader("📄 Subir Excel de puntajes", type=["xlsx"])
ruta_def = "Cargos_Abril2025.xlsx"

try:
    if archivo is not None:
        puntajes, lista_cargos, meta = cargar_puntajes(archivo)
    else:
        puntajes, lista_cargos, meta = cargar_puntajes(ruta_def)
except Exception as e:
    st.error(f"Error al leer el Excel: {e}")
    st.stop()

with st.expander("ℹ️ Fuente detectada"):
    st.write(f"Hoja: **{meta['hoja']}**")
    st.write(f"Puntaje: **{meta['col_puntaje']}**")
    st.write(f"Código/Cargo: **{meta['col_cod']} / {meta['col_cargo']}**")

# Parámetros
vi = st.number_input("Valor Índice (VI):", value=float(DEFAULT_VI), step=0.000001, format="%.6f")
foid_unit = st.number_input("FOID por 19 hs ($):", value=float(DEFAULT_FOID), step=100.0)
conect_total = st.number_input("Conectividad/Materiales total ($):", value=float(DEFAULT_CONECT), step=100.0)

antiguedad = st.number_input("Antigüedad (años):", min_value=0, max_value=40, value=0)

st.subheader("Selección de cargos/horas")
cargos, cantidades = [], []
for i in range(3):
    c1, c2 = st.columns([3,1])
    cargo = c1.selectbox(f"Cargo #{i+1}", options=[""] + lista_cargos, key=f"c_{i}")
    cant  = c2.number_input("Cantidad", min_value=0, value=0, key=f"q_{i}")
    cargos.append(cargo); cantidades.append(cant)

g_opc = ["Ninguno","AMET","SUTEF","SUETRA","ATE","UDAF","UDA","UPCN"]
g1 = st.selectbox("Gremio 1", g_opc, index=0)
g2 = st.selectbox("Gremio 2", g_opc, index=0)
gremios = []
if g1 != "Ninguno": gremios.append(g1)
if g2 != "Ninguno" and g2 != g1: gremios.append(g2)

if st.button("Calcular Junio 2025"):
    res = calcular_simulacion(cargos, cantidades, puntajes, vi, antiguedad, gremios,
                              foid_unit=foid_unit, conectividad_total=conect_total)

    df = pd.DataFrame({
        "Concepto": list(res.keys()),
        "Monto ($)": list(res.values())
    })

    def estilo(row):
        return ['background-color:#1f77b4;color:white;font-weight:bold' if row["Concepto"]=="NETO" else '' for _ in row]

    st.dataframe(df.style.apply(estilo, axis=1).format({"Monto ($)":"{:,.2f}"}))

    st.markdown(f"### 💰 NETO Junio 2025: **${res['NETO']:,.2f}**")

    if st.checkbox("🔍 Modo debug"):
        st.write("Horas Totales:", res["Horas Totales"])
        st.write("Simples / Completo:", res["Simples"], "/", res["Completo"])
        st.write("Unidades Conectividad:", res["Unidades Conectividad"])
        st.write("FOID calculado:", res["FOID"])
        st.write("Conectividad calculada:", res["Conectividad"])
        st.write("Gremios:", gremios)
        st.write("VI usado:", vi)
