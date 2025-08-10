from salario import calcular_componentes
from bonos import unidades_bono, monto_bonos
from descuentos import descuentos_legales, descuento_gremial

def calcular_simulacion(cargos, cantidades, puntajes_dict, vi, antiguedad, gremios):
    comp = calcular_componentes(cargos, cantidades, puntajes_dict, vi, antiguedad)

    uds = unidades_bono(comp["simples"], comp["completo"], comp["total_horas"])
    bonos = monto_bonos(uds)

    legal = descuentos_legales(comp["remunerativo"])
    grem = descuento_gremial(comp["remunerativo"], bonos, gremios)
    total_desc = legal["total"] + grem

    neto = comp["remunerativo"] - total_desc + bonos

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
        "Bonos": bonos,
        "Descuentos Legales": legal["total"],
        "Descuento Gremial": grem,
        "Total Descuentos": total_desc,
        "NETO": neto,
        "Horas Totales": comp["total_horas"],
        "Unidades Bono": uds
    }
