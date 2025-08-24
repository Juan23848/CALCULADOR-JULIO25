# Cálculo de FOID/FONID y Conectividad
# Reglas provistas por el usuario (Junio/Julio 2025):
# - FOID base: 45.000 por cada 19 hs cátedra (proporcional por hora).
# - Tope horas: 38 hs -> máximo 2 unidades de FOID (90.000).
# - Acumulación:
#     * 2 cargos simples -> 90.000
#     * 1 simple + 19 hs -> 90.000
#     * 1 cargo completo -> 45.000 (puede tener hasta 16 hs, pero el FOID queda en 45.000)
# - Conectividad/Materiales: se mantiene como monto total que se prorratea por unidades (hasta 38),
#   a menos que se desee fijarlo a valor plano. Dejamos parametrizado.

def foid_monto(simples:int, completo:bool, horas:int, foid_unit:float=45000.0) -> float:
    """Calcula el monto FOID con las reglas nuevas.
    - Cada cargo simple cuenta como 1 unidad FOID (45k).
    - Las horas aportan horas/19 unidades FOID (proporcional), con tope 38 hs.
    - Cap de 2 unidades (90k).
    - 'Completo' fuerza a 1 unidad (45k), ignorando horas para FOID.
    """
    if completo:
        return foid_unit  # 45k fijo para cargo completo

    horas_consideradas = min(max(horas, 0), 38)
    unidades_por_horas = horas_consideradas / 19.0

    unidades = simples + unidades_por_horas

    # Caps por reglas explícitas
    if simples >= 2:
        unidades = 2.0
    elif simples == 1 and horas_consideradas >= 19:
        unidades = 2.0

    unidades = min(unidades, 2.0)
    return unidades * foid_unit

def unidades_conectividad(simples:int, completo:bool, horas:int) -> int:
    """Unidades para prorratear Conectividad/Materiales (0..38).
    Tomamos un criterio operativo:
    - Completo o 2 simples -> 38
    - 1 simple + >=19 horas -> 38
    - Si no, 19 por cada simple (máx 2) + horas, tope 38
    """
    if completo:
        return 38
    if simples >= 2:
        return 38
    if simples == 1 and horas >= 19:
        return 38
    base = 19 * min(simples, 2) + max(horas, 0)
    return min(base, 38)

def conectividad_monto(simples:int, completo:bool, horas:int, total_conectividad:float=142600.0) -> float:
    """Prorratea el monto de Conectividad/Materiales por unidades (0..38)."""
    uds = unidades_conectividad(simples, completo, horas)
    return total_conectividad * (uds / 38.0)

def calcular_bonos(simples:int, completo:bool, horas:int, foid_unit:float=45000.0, total_conectividad:float=142600.0) -> dict:
    foid = foid_monto(simples, completo, horas, foid_unit=foid_unit)
    con  = conectividad_monto(simples, completo, horas, total_conectividad=total_conectividad)
    return {
        "FOID": foid,
        "Conectividad": con,
        "TotalBonos": foid + con,
        "Unidades Conectividad": unidades_conectividad(simples, completo, horas)
    }
