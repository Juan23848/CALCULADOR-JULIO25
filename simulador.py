# simulador.py (fixed)
import sys, os
from typing import List, Dict

# Tasas por gremio (aplican sobre FOID solamente)
from descuentos import GREMIOS  # porcentajes por gremio

from bonos import (
    unidades_bono, foid, conectividad,
    FOID_POR_19HS as DEFAULT_FOID_19,
    CONECTIVIDAD_TOTAL as DEFAULT_CONECT
)

# Import robusto para salario.calcular_componentes
try:
    from salario import calcular_componentes
except ModuleNotFoundError:
    sys.path.append(os.path.dirname(__file__))
    from salario import calcular_componentes

SEGURO_FIJO = 3000.0  # Seguro de vida obligatorio

def _descuentos_legales(remunerativo_solo: float) -> Dict[str, float]:
    """
    Descuentos legales SOLO sobre lo remunerativo (no incluye FOID ni conectividad).
    """
    jubilacion = remunerativo_solo * 0.16
    obra_social = remunerativo_solo * 0.03
    seguro = SEGURO_FIJO
    total = jubilacion + obra_social + seguro
    return {
        "jubilacion": jubilacion,
        "obra_social": obra_social,
        "seguro": seguro,
        "total": total,
    }

def _descuento_gremial(monto_foid: float, gremios: List[str]) -> Dict[str, float]:
    """
    Descuento gremial: aplica sobre FOID (no sobre remunerativo).
    Suma las tasas únicas de los gremios seleccionados.
    """
    vistos, unicos = set(), []
    for g in (gremios or []):
        if g and g not in vistos:
            unicos.append(g); vistos.add(g)

    tasa_total = sum(GREMIOS.get(g, 0.0) for g in unicos)
    total = (monto_foid or 0.0) * tasa_total
    return {
        "gremios": unicos,
        "tasa_total": tasa_total,
        "sobre_foid": monto_foid or 0.0,
        "total": total,
    }

def calcular_simulacion(
    cargos: List[str],
    cantidades: List[int],
    puntajes_dict: Dict[str, float],
    vi: float,
    antiguedad: int,
    gremios: List[str],
    foid_monto: float = None,
    conect_monto: float = None,
) -> Dict[str, float]:
    """
    Calcula todos los componentes del salario, bonos no remunerativos y descuentos.
    """
    # Filtrar entradas vacías
    cargos_limpios, cantidades_limpias = [], []
    for cargo, cantidad in zip(cargos, cantidades):
        if cargo and (cantidad or 0) > 0:
            cargos_limpios.append(cargo)
            cantidades_limpias.append(int(cantidad))

    # Componentes remunerativos
    comp = calcular_componentes(cargos_limpios, cantidades_limpias, puntajes_dict, vi, antiguedad)

    # Unidades para bonos (derivadas del cálculo de componentes)
    simples = int(comp.get("simples", 0))
    completos_flag = 1 if comp.get("completo", False) else 0
    total_horas = int(comp.get("total_horas", 0))

    # FOID y conectividad (no remunerativos)
    monto_foid = foid(simples, completos_flag, total_horas, foid_monto or DEFAULT_FOID_19)
    unidades = unidades_bono(simples, completos_flag, total_horas)
    monto_conect = conectividad(unidades, conect_monto or DEFAULT_CONECT)

    # Totales
    remunerativo_solo = float(comp["remunerativo"])
    total_bonos = (monto_foid or 0.0) + (monto_conect or 0.0)
    bruto_total = remunerativo_solo + total_bonos

    # Descuentos
    desc_legales = _descuentos_legales(remunerativo_solo)
    desc_gremial = _descuento_gremial(monto_foid, gremios)

    descuentos_totales = desc_legales["total"] + desc_gremial["total"]
    neto = bruto_total - descuentos_totales

    return {
        "componentes": comp,
        "foid": monto_foid,
        "conectividad": monto_conect,
        "bruto_remunerativo": remunerativo_solo,
        "bonos_no_remunerativos": total_bonos,
        "bruto_total": bruto_total,
        "descuentos_legales": desc_legales,
        "descuento_gremial": desc_gremial,
        "descuentos_totales": descuentos_totales,
        "neto": neto,
    }
