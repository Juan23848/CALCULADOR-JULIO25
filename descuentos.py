GREMIOS = {
    "AMET": 0.015, "SUTEF": 0.02, "SUETRA": 0.02,
    "ATE": 0.022, "UDAF": 0.013, "UDA": 0.015, "UPCN": 0.022
}

def descuentos_legales(remunerativo: float) -> dict:
    jubilacion = remunerativo * 0.16
    obra_social = remunerativo * 0.03
    seguro = 3000.0
    return {
        "jubilacion": jubilacion,
        "obra_social": obra_social,
        "seguro": seguro,
        "total": jubilacion + obra_social + seguro
    }

def descuento_gremial(remunerativo: float, bonos: float, gremios: list) -> float:
    total = 0.0
    for g in gremios:
        total += GREMIOS.get(g, 0.0) * (remunerativo + bonos)
    return total
