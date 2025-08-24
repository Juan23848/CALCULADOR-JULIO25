from salario import calcular_componentes
from bonos import calcular_bonos
from descuentos import descuentos_legales, descuento_gremial

def calcular_simulacion(cargos, cantidades, puntajes_dict, vi, antiguedad, gremios,
                        foid_unit=45000.0, conectividad_total=142600.0):
    comp = calcular_componentes(cargos, cantidades, puntajes_dict, vi, antiguedad)

    bonos = calcular_bonos(comp["simples"], comp["completo"], comp["total_horas"],
                           foid_unit=foid_unit, total_conectividad=conectividad_total)

    legal = descuentos_legales(comp["remunerativo"])
    grem = descuento_gremial(comp["remunerativo"], bonos["TotalBonos"], gremios)
    total_desc = legal["total"] + grem

    neto = comp["remunerativo"] - total_desc + bonos["TotalBonos"]

    return {
        "Básico": comp["basico"],
        "Función Docente": comp["funcion"],
        "Antigüedad": comp["antiguedad"],
        "Transformación": comp["transformacion"],
        "Bonificación Docente": comp["bonif_docente"],
        "Adicional Jerárquico": comp["adic_jerarquico"],
        "Subtotal": comp["subtotal"],
        "Zona": comp["zona"],
        "Remunerativo": comp["remunerativo"],
        "FOID": bonos["FOID"],
        "Conectividad": bonos["Conectividad"],
        "Bonos (Total)": bonos["TotalBonos"],
        "Descuentos Legales": legal["total"],
        "Descuento Gremial": grem,
        "Total Descuentos": total_desc,
        "NETO": neto,
        "Horas Totales": comp["total_horas"],
        "Unidades Conectividad": bonos["Unidades Conectividad"],
        "Simples": comp["simples"],
        "Completo": comp["completo"]
    }
