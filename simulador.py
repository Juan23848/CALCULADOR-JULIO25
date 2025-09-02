
from typing import List, Dict
from salario import calcular_componentes
from bonos import unidades_bono, foid, conectividad, FOID_POR_19HS, CONECTIVIDAD_TOTAL
from descuentos import descuentos_legales, descuento_gremial_foid

def calcular_simulacion(
    cargos: List[str],
    cantidades: List[int],
    puntajes_dict: Dict[str, float],
    vi: float,
    antiguedad: int,
    gremios: List[str],
    foid_monto: float | None = None,
    conect_monto: float | None = None,
) -> Dict:
    cargos_limpios, cantidades_limpias = [], []
    for cargo, cantidad in zip(cargos, cantidades):
        if cargo and (cantidad or 0) > 0:
            cargos_limpios.append(cargo)
            cantidades_limpias.append(int(cantidad))

    comp = calcular_componentes(cargos_limpios, cantidades_limpias, puntajes_dict, vi, antiguedad)

    simples = int(comp.get("simples", 0))
    completos = int(comp.get("completos", 0))
    total_horas = int(comp.get("total_horas", 0))

    monto_foid = foid(simples, completos, total_horas)
    unidades = unidades_bono(simples, completos, total_horas)
    monto_conect = conectividad(unidades, conect_monto or CONECTIVIDAD_TOTAL)

    remunerativo_solo = float(comp["remunerativo"])
    bonos_no_rem = (monto_foid or 0.0) + (monto_conect or 0.0)
    bruto_total = remunerativo_solo + bonos_no_rem

    dl = descuentos_legales(remunerativo_solo)
    dg = descuento_gremial_foid(monto_foid, gremios)
    descuentos_totales = dl["total"] + dg["total"]
    neto = bruto_total - descuentos_totales

    return {
        "componentes": comp,
        "foid": monto_foid,
        "conectividad": monto_conect,
        "bruto_remunerativo": remunerativo_solo,
        "bonos_no_remunerativos": bonos_no_rem,
        "bruto_total": bruto_total,
        "descuentos_legales": dl,
        "descuento_gremial": dg,
        "descuentos_totales": descuentos_totales,
        "neto": neto,
    }
        "descuentos_totales": descuentos_totales,
        "neto": neto,
    }
