
def calcular_simulacion(cargos, cantidades, puntajes, vi, antiguedad, gremios, foid_unit=0, conectividad_total=0):
    resultados = {}
    total_horas = sum(cantidades)
    
    # Remunerativos (simplificado)
    basico = vi * sum(puntajes)
    funcion_docente = basico * 0.26
    antig = basico * (antiguedad * 0.01)
    transf = basico * 1.23
    bonif_docente = 0
    adicional_jerarquico = 0

    for cargo, cant in zip(cargos, cantidades):
        if cargo in ["421", "312"]:  # Códigos que cobran bonificación docente
            bonif_docente += ((vi * puntajes[cargos.index(cargo)]) * 0.2775)
        if cargo in ["600", "601"]:  # Ejemplo: códigos con adicional jerárquico
            adicional_jerarquico += ((vi * puntajes[cargos.index(cargo)]) * 0.15)

    resultados["Básico"] = basico
    resultados["Función Docente"] = funcion_docente
    resultados["Antigüedad"] = antig
    resultados["Transformación"] = transf
    resultados["Bonificación Docente"] = bonif_docente
    resultados["Adicional Jerárquico"] = adicional_jerarquico

    remunerativo_base = basico + funcion_docente + antig + transf + bonif_docente + adicional_jerarquico
    resultados["Zona"] = remunerativo_base

    # FOID y Conectividad (no remunerativos)
    foid_total = (total_horas // 19) * foid_unit
    resultados["FOID"] = foid_total
    resultados["Conectividad"] = conectividad_total

    # Descuentos sobre remunerativos solamente
    desc_legales = remunerativo_base * 0.169  # 16.9%
    desc_gremial = 0
    if "AMET" in gremios:
        desc_gremial = remunerativo_base * 0.015  # 1.5% para AMET

    resultados["Remunerativo"] = remunerativo_base
    resultados["Descuentos Legales"] = desc_legales
    resultados["Descuento Gremial"] = desc_gremial
    resultados["Total Descuentos"] = desc_legales + desc_gremial

    resultados["NETO"] = remunerativo_base + foid_total + conectividad_total - resultados["Total Descuentos"]
    resultados["Horas Totales"] = total_horas
    resultados["Unidades Conectividad"] = total_horas // 19

    return resultados
