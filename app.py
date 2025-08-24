
import streamlit as st
import pandas as pd
from simulador import calcular_simulacion
from PIL import Image
import os

st.set_page_config(page_title="Simulador Salarial – AMET TDF (Junio 2025)", page_icon="📊", layout="centered")

# Encabezado con logos y título
col1, col2, col3 = st.columns([1, 4, 1])

with col1:
    if os.path.exists("ametnac.jpeg"):
        st.image("ametnac.jpeg", width=110)
with col2:
    st.markdown("<h1 style='text-align:center;'>📊 Simulador Salarial Docente – AMET TDF (Junio 2025)</h1>", unsafe_allow_html=True)
with col3:
    if os.path.exists("ametdf.jpeg"):
        st.image("ametdf.jpeg", width=110)

DEFAULT_VI = 87.608881
DEFAULT_FOID_19 = 45000.0
DEFAULT_CONECT = 142600.0

@st.cache_data
def cargar_puntajes(origen):
    df_all = pd.read_excel(origen, sheet_name=None)
    sheet = next((n for n in df_all.keys() if "simulador" in str(n).lower()), list(df_all.keys())[0])
    df = df_all[sheet].copy()
    df.columns = [str(c).strip() for c in df.columns]

    def pick(colnames, needles):
        for c in colnames:
            up = c.upper().replace(".", "").replace("Ó", "O")
            for n in needles:
                if n in up:
                    return c
        return None

    col_cod = pick(df.columns, ["COD", "CÓD"])
    col_cargo = pick(df.columns, ["CARGO"])
    if not col_cod or not col_cargo:
        raise KeyError("No se encontraron columnas de código y/o cargo en el Excel.")

    cols_punt = [c for c in df.columns if "PUNTAJE" in c.upper()]
    if not cols_punt:
        raise KeyError("No se encontró ninguna columna que contenga 'PUNTAJE' en el Excel.")
    col_punt = cols_punt[-1]

    df["IDENTIFICADOR"] = df[col_cod].astype(str).str.strip() + " - " + df[col_cargo].astype(str).str.strip()
    puntajes = dict(zip(df["IDENTIFICADOR"], df[col_punt]))
    lista = sorted([x for x in df["IDENTIFICADOR"].dropna().tolist()])
    meta = {"hoja": sheet, "col_puntaje": col_punt, "col_cod": col_cod, "col_cargo": col_cargo}
    return puntajes, lista, meta

st.caption("Cargá tu Excel o dejá 'Cargos_Abril2025.xlsx' en el repo. Este simulador usa VI=87.608881 por defecto y FOID=45.000 cada 19 hs (tope 38 hs).")

archivo = st.file_uploader("📄 Subir Excel de puntajes", type=["xlsx"])
ruta_defecto = "Cargos_Abril2025.xlsx"

try:
    if archivo is not None:
        puntajes, lista_cargos, meta = cargar_puntajes(archivo)
    else:
        puntajes, lista_cargos, meta = cargar_puntajes(ruta_defecto)
except Exception as e:
    st.error(f"Error al leer el Excel: {e}")
    st.stop()

with st.expander("ℹ️ Fuente detectada"):
    st.write(f"📄 Hoja: **{meta['hoja']}**")
    st.write(f"Puntaje: **{meta['col_puntaje']}**")
    st.write(f"Código/Cargo: **{meta['col_cod']} / {meta['col_cargo']}**")

# Parámetros
vi = st.number_input("Valor Índice (VI):", value=float(DEFAULT_VI), step=0.000001, format="%.6f")
st.markdown(f"**FOID por 19 hs:** ${DEFAULT_FOID_19:,.2f} &nbsp;&nbsp;|&nbsp;&nbsp; **Conectividad total:** ${DEFAULT_CONECT:,.2f}")
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
    res = calcular_simulacion(cargos, cantidades, puntajes, vi, antiguedad, gremios)

    df = pd.DataFrame({"Concepto": list(res.keys()), "Monto ($)": list(res.values())})

    def estilo(row):
        return ['background-color:#1f77b4;color:white;font-weight:bold' if row["Concepto"]=="NETO" else '' for _ in row]

    st.dataframe(df.style.apply(estilo, axis=1).format({"Monto ($)":"{:,.2f}"}))
    st.markdown(f"### 💰 NETO Junio 2025: **${res['NETO']:,.2f}**")

    st.markdown("---")
    st.markdown("<h4 style='text-align:center; color:gray;'>Simulador elaborado por AMET Tierra del Fuego – Junio 2025</h4>", unsafe_allow_html=True)

    if os.path.exists("amet nuevo.JPG"):
        st.image("amet nuevo.JPG", use_column_width=True)

    if st.checkbox("🔍 Modo debug"):
        st.write({k: res[k] for k in ["Horas Totales", "Unidades Bono", "Simples", "Completo"]})
        st.write("Gremios:", gremios)
        st.write("VI usado:", vi)
        st.subheader("🧩 Detalle por cargo (bonificación docente)")
        st.write(pd.DataFrame(res["detalle"]["items"]))
