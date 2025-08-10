def unidades_bono(simples, completo, horas):
    if completo:
        return 38
    if simples >= 2:
        return 38
    if simples == 1 and horas >= 22:
        return 38
    base = 19 * min(simples, 2) + horas
    return min(base, 38)

def monto_bonos(unidades):
    bono1 = unidades * (90000 / 38)
    bono2 = unidades * (142600 / 38)
    return bono1 + bono2
