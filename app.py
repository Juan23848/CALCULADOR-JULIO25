
import streamlit as st
from simulador import calcular_simulacion

st.title("Simulador Salarial Docente")
st.caption("Versión Julio - Corregida")

# Valores por defecto
vi = st.number_input("Valor Índice (VI)", value=86.76, step=0.01)
antiguedad = st.slider("Años de antigüedad", min_value=0, max_value=40, value=5)
gremios = st.multiselect("Gremios", ["AMET", "SUTEF", "SUETRA", "ATE", "UDAF", "UDA", "UPCN"])

# Demo cargos
cargos = ["101 - Cargo simple", "102 - Cargo completo", "201 - Hora cátedra"]
puntajes = {
    "101 - Cargo simple": 65.1306574,
    "102 - Cargo completo": 130.2613148,
    "201 - Hora cátedra": 1.0,
}

cantidades = []
st.subheader("Cargos y cantidades")
for cargo in cargos:
    cantidad = st.number_input(f"{cargo}", min_value=0, value=0, step=1)
    cantidades.append(cantidad)

if st.button("Calcular"):
    resultado = calcular_simulacion(
        cargos=cargos,
        cantidades=cantidades,
        puntajes_dict=puntajes,
        vi=vi,
        antiguedad=antiguedad,
        gremios=gremios,
    )

    st.success(f"💰 Neto a cobrar: ${resultado['neto']:,.2f}")

    with st.expander("📋 Ver detalle del cálculo"):
        st.write("**Componentes remunerativos:**")
        st.json(resultado["componentes"])
        st.write("**Bonos no remunerativos:**")
        st.write(f"FOID: ${resultado['foid']:,.2f}")
        st.write(f"Conectividad: ${resultado['conectividad']:,.2f}")
        st.write("**Descuentos:**")
        st.json({
            "Descuentos legales": resultado["descuentos_legales"],
            "Descuento gremial": resultado["descuento_gremial"],
            "Total descuentos": resultado["descuentos_totales"],
        })
