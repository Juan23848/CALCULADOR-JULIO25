# bonos.py

FOID_POR_19HS = 45000.0  # Monto por cada 19 horas
CONECTIVIDAD_TOTAL = 142600.0  # Total para 38 unidades

def unidades_bono(simples, completos, total_horas):
    """Devuelve cantidad de unidades para prorrateo de conectividad (máx. 38 unidades)."""
    return min(38, simples + 2 * completos)

def foid(simples, completos, total_horas, foid_por_19hs=FOID_POR_19HS):
    """Calcula monto FOID proporcional a las horas (máximo 38)."""
    unidades = simples + 2 * completos
    return foid_por_19hs * unidades / 19 if unidades <= 38 else foid_por_19hs * 2

def conectividad(unidades, conect_total=CONECTIVIDAD_TOTAL):
    """Prorratea conectividad en base a unidades (máximo 38)."""
    return conect_total * min(38, unidades) / 38