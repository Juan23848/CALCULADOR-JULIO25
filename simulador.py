
# simulador.py
from salario import calcular_componentes
from bonos import (
    unidades_bono, foid, conectividad,
    FOID_POR_19HS as DEFAULT_FOID_19,
    CONECTIVIDAD_TOTAL as DEFAULT_CONECT
)

# === Parámetros / constantes ===
SEGURO_FIJO = 3000.0  # 773 Seguro Vida

# % por gremio (aplican SOLO sobre remunerativos; además se aplican sobre FOID)
GREMIO_PORC = {
    "AMET": 0.015,
    "SUTEF": 0.02,
    "SUETRA": 0.02,
    "ATE": 0.022,
    "UDAF": 0.013,
    "UDA": 0.015,
    "UPCN": 0.022,
}

def _descuentos_legales(remunerativo: float) -> dict:
    """Devuelve desglose legal: jubilación (16%), obra social (3%), seguro fijo y total."""
    jubilacion = remunerativo * 0.16  # 701
    obra_social = remunerativo * 0.03  # 719
    seguro = SEGURO_FIJO               # 773
    return {
        "jubilacion": jubilacion,
        "obra_social": obra_social,
        "seguro": seguro,
        "total": jubilacion + obra_social + seguro
    }

def _descuento_gremial(remunerativo: float, monto_foid: float, gremios: list) -> dict:
    """
    Descuento gremial generalizado:
    - Suma los % de los gremios elegidos (sin duplicados) y los aplica sobre:
      a) Remunerativo
      b) FOID (mismo %)
    - Conectividad no integra la base gremial adicional.
    """
    # quitar duplicados preservando orden
    vistos = set()
    gremios_unicos = []
    for g in (gremios or []):
        if g not in vistos:
            gremios_unicos.append(g)
            vistos.add(g)

    # % total resultante de los gremios seleccionados
    total_rate = sum(GREMIO_PORC.get(g, 0.0) for g in gremios_unicos)

    porcentual_sobre_remun = remunerativo * total_rate
    porcentual_sobre_foid = (monto_foid or 0.0) * total_rate

    total = porcentual_sobre_remun + porcentual_sobre_foid
    return {
        "gremios": gremios_unicos,
        "rate_total": total_rate,
        "sobre_remunerativo": porcentual_sobre_remun,
        "sobre_foid": porcentual_sobre_foid,
        "total": total
    }

def calcular_simulacion(
    cargos,
    cantidades,
    puntajes_dict,
    vi,
    antiguedad,
    gremios,
    foid_19: float = DEFAULT_FOID_19,       # $45.000 por 19 hs (tope 2×)
    conect_total: float = DEFAULT_CONECT    # $142.600 (2×71.300) prorrateo por 38 uds
):
    """
    JUNIO 2025:
    - Remunerativos (básico, función, antig., transf., bonif. docente, adic. jerárquico, zona)
    - NO remunerativos: FOID + Conectividad
    - Descuentos legales SOLO sobre remunerativos
    - Descuento gremial: % sobre remunerativos + MISMO % sobre FOID (para todos los gremios)
    - NETO = Remun - (Legales + Gremial) + (FOID + Conectividad)
    """
    # 1) Componentes remunerativos por cargos
    comp = calcular_componentes(cargos, cantidades, puntajes_dict, vi, antiguedad)

    # 2) Bonos NO remunerativos (FOID + Conectividad)
    uds = unidades_bono(comp["simples"], comp["completo"], comp["total_horas"])
    monto_foid = foid(comp["simples"], comp["completo"], comp["total_horas"], foid_por_19hs=foid_19)
    monto_conect = conectividad(uds, conect_total)
    bonos_total = monto_foid + monto_conect  # informativo

    # 3) Base remunerativa para descuentos (SIN FOID ni Conectividad)
    remunerativo = comp["remunerativo"]

    # 4) Descuentos legales (701, 719, 773)
    legales = _descuentos_legales(remunerativo)

    # 5) Descuento gremial generalizado
    grem = _descuento_gremial(remunerativo, monto_foid, gremios)

    total_desc = legales["total"] + grem["total"]

    # 6) NETO final
    neto = remunerativo - total_desc + bonos_total

    # 7) Resultado detallado
    return {
        # Remunerativos (desglose)
        "Básico": comp["basico"],
        "Función Docente": comp["funcion"],
        "Antigüedad": comp["antiguedad"],
        "Transformación": comp["transformacion"],
        "Bonificación Docente": comp["bonif_docente"],
        "Adicional Jerárquico": comp["adic_jerarquico"],
        "Subtotal": comp["subtotal"],
        "Zona": comp["zona"],
        "Remunerativo": remunerativo,

        # NO remunerativos (fuera de base de descuentos)
        "FOID": monto_foid,
        "Conectividad": monto_conect,
        "Bonos (Total)": bonos_total,  # informativo

        # Descuentos legales (separados)
        "Descuento Jubilación (16%)": legales["jubilacion"],
        "Descuento Obra Social (3%)": legales["obra_social"],
        "Seguro de Vida": legales["seguro"],
        "Descuentos Legales": legales["total"],

        # Descuento gremial (separado)
        "Gremios Seleccionados": grem["gremios"],
        "Alicuota Gremial Total": grem["rate_total"],
        "Descuento Gremial % Remunerativo": grem["sobre_remunerativo"],
        "Descuento Gremial % sobre FOID": grem["sobre_foid"],
        "Descuento Gremial": grem["total"],

        # Totales
        "Total Descuentos": total_desc,
        "NETO": neto,

        # Debug / control
        "Horas Totales": comp["total_horas"],
        "Unidades Bono": uds,
        "Simples": comp["simples"],
        "Completo": comp["completo"]
    }
