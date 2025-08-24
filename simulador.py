
def calcular_descuentos(res, gremios):
    # Calcular monto total remunerativo (excluyendo FOID y Conectividad)
    remunerativos = (
        res.get("Básico", 0) +
        res.get("Función Docente", 0) +
        res.get("Antigüedad", 0) +
        res.get("Transformación", 0) +
        res.get("Bonificación Docente", 0) +
        res.get("Zona", 0)
    )

    # Descuento legal: 17%
    descuento_legal = remunerativos * 0.17

    # Descuento gremial (2% por gremio, sin repetir si mismo gremio)
    descuento_gremial = 0
    if gremios:
        descuento_gremial = remunerativos * 0.02 * len(set(gremios))

    # Calcular totales
    total_descuentos = descuento_legal + descuento_gremial
    neto = (
        res.get("Remunerativo", 0) +
        res.get("FOID", 0) +
        res.get("Conectividad", 0) -
        total_descuentos
    )

    # Guardar resultados en el diccionario
    res["Descuentos Legales"] = round(descuento_legal, 2)
    res["Descuento Gremial"] = round(descuento_gremial, 2)
    res["Total Descuentos"] = round(total_descuentos, 2)
    res["NETO"] = round(neto, 2)
    return res
