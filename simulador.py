# simulador.py
import sys, os
from descuentos import GREMIOS  # % por gremio
from bonos import (
    unidades_bono, foid, conectividad,
    FOID_POR_19HS as DEFAULT_FOID_19,
    CONECTIVIDAD_TOTAL as DEFAULT_CONECT
)

# Import robusto (funciona local y en Streamlit Cloud)
try:
    from salario import calcular_componentes
except ModuleNotFoundError:
    sys.path.append(os.path.dirname(__file__))
    from salario import calcular_componentes

SEGURO_FIJO = 3000.0  # 773 Seguro vida obligatorio

def _descuentos_legales(remunerativo: float) -> dict:
    jubilacion = remunerativo * 0.16
    obra_social = remunerativo * 0.03
    seguro = SEGURO_FIJO
    return {
        "jubilacion": jubilacion,
        "obra_social": obra_social,
        "seguro": seguro,
        "total": jubilacion + obra_social + seguro,
    }

def _descuento_gremial(remunerativo: float, monto_foid: float, gremios: list) -> dict:
    vistos, unicos = set(), []
    for g in (gremios or []):
        if g and g not in vistos:
            unicos.append(g); vistos.add(g)

    tasa_total = sum(GREMIOS.get(g, 0.0) for g in unicos)

    sobre_remun = remunerativo * tasa_total
    sobre_foid  = (monto_foid or 0.0) * tasa_total
    total = sobre_remun + sobre_foid
    return {
        "gremios": unicos,
        "tasa_total": tasa_total,
        "sobre_remunerativo": sobre_remun,
        "sobre_foid": sobre_foid,
        "total": total,
    }

def calcular_simulacion(
    cargos,
    cantidades,
    puntajes_dict,
    vi,
    antiguedad,
    gremios,
    foid_19: float = DEFAULT_FOID_19,
    conect_total: float = DEFAULT_CONECT
):
    comp = calcular_componentes(cargos, cantidades, puntajes_dict, vi, antiguedad)

    uds = unidades_bono(comp["simples"], comp["completo"], comp["total_horas"])
    monto_foid   = foid(comp["simples"], comp["completo"], comp["total_horas"], foid_por_19hs=foid_19)
    monto_conect = conectividad(uds, conect_total)
    bonos_total  = monto_foid + monto_conect

    remunerativo = comp["remunerativo"]

    legales = _descuentos_legales(remunerativo)
    grem    = _descuento_gremial(remunerativo, monto_foid, gremios)
    total_desc = legales["total"] + grem["total"]

    neto = remunerativo - total_desc + bonos_total

    return {
        "Básico": comp["basico"],
        "Función Docente": comp["funcion"],
        "Antigüedad": comp["antiguedad"],
        "Transformación": comp["transformacion"],
        "Bonificación Docente": comp["bonif_docente"],
        "Adicional Jerárquico": comp["adic_jerarquico"],
        "Subtotal": comp["subtotal"],
        "Zona": comp["zona"],
        "Remunerativo": remunerativo,
        "FOID": monto_foid,
        "Conectividad": monto_conect,
        "Bonos (Total)": bonos_total,
        "Descuento Jubilación (16%)": legales["jubilacion"],
        "Descuento Obra Social (3%)": legales["obra_social"],
        "Seguro de Vida": legales["seguro"],
        "Descuentos Legales": legales["total"],
        "Gremios Seleccionados": grem["gremios"],
        "Alicuota Gremial Total": grem["tasa_total"],
        "Descuento Gremial % Remunerativo": grem["sobre_remunerativo"],
        "Descuento Gremial % sobre FOID": grem["sobre_foid"],
        "Descuento Gremial": grem["total"],
        "Total Descuentos": total_desc,
        "NETO": neto,
        "Horas Totales": comp["total_horas"],
        "Unidades Bono": uds,
        "Simples": comp["simples"],
        "Completo": comp["completo"],
    }