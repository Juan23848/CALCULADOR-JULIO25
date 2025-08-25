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
    foid_monto = None,
    conect_monto = None,
) -> dict:
    cargos_limpios, cantidades_limpias = [], []
    for cargo, cantidad in zip(cargos, cantidades):
        if cargo and cantidad > 0:
            cargos_limpios.append(cargo)
            cantidades_limpias.append(cantidad)

    comp = calcular_componentes(cargos_limpios, cantidades_limpias, puntajes_dict, vi, antiguedad)
    monto_foid = foid(cargos_limpios, cantidades_limpias, foid_monto or DEFAULT_FOID_19)
    monto_conect = conectividad(cargos_limpios, cantidades_limpias, conect_monto or DEFAULT_CONECT)
    total_remunerativo = comp["total"] + monto_foid + monto_conect

    return {
        "componentes": comp,
        "foid": monto_foid,
        "conectividad": monto_conect,
        "remunerativo_total": total_remunerativo,
        "descuentos_legales": _descuentos_legales(total_remunerativo),
        "descuento_gremial": _descuento_gremial(total_remunerativo, monto_foid, gremios),
    }
