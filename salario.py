from antiguedad import calcular_antiguedad_factor

# Códigos jerárquicos (30% sobre el básico de esos cargos)
JERARQUICOS = {
    "954","814","800","302","820","806","809","804","210","501","202","200","826","208","803",
    "400","402","502","837","204","827","206","107","811","700","901","828","407","301","201",
    "300","821","862","905","500","817","207","813","203","401","601","511","822","818","105",
    "906","408","805","864","812","952","949","303","406","825","211","953","103","403","405",
    "819","513","205","838","512","824","815","807","802","902","808","816","823","900","951",
    "602","106","101","104","404","600","810","801","209","102","950"
}

# Códigos excluidos de bonificación docente
EXCLUIDOS_BONIF = {"404", "405", "411", "420", "422", "423"}

def calcular_componentes(cargos, cantidades, puntajes, vi, antiguedad):
    total_puntaje = 0.0
    basico_jera = 0.0
    bonif_doc = 0.0
    total_horas = 0
    simples = 0
    completo = False

    for i, cargo in enumerate(cargos):
        if not cargo or cantidades[i] <= 0:
            continue
        codigo = cargo.split(" - ")[0].strip()
        desc = cargo.lower()
        puntaje = float(puntajes.get(cargo, 0.0))
        cant = int(cantidades[i])

        total_puntaje += puntaje * cant

        # Jerárquico
        if codigo in JERARQUICOS:
            basico_jera += puntaje * cant * vi

        # Conteo de horas/cargos para bonos
        if "hora" in desc:
            total_horas += cant
        elif "completo" in desc:
            completo = True
        elif "simple" in desc:
            simples += cant  # sumar cantidad

        # Bonificación docente sobre horas (códigos que inician con 3 o 4, no excluidos)
        if "hora" in desc and (codigo.startswith("3") or codigo.startswith("4")) and codigo not in EXCLUIDOS_BONIF:
            bonif_doc += (puntaje * cant * vi) * 0.2775

    basico = total_puntaje * vi
    funcion = basico * 2.30
    antig = basico * calcular_antiguedad_factor(antiguedad)
    transf = basico * 1.23
    adic_jera = basico_jera * 0.30

    subtotal = basico + funcion + antig + transf + bonif_doc + adic_jera
    zona = subtotal                   # Zona = Subtotal
    remunerativo = subtotal + zona    # Remun = Subtotal + Zona

    return {
        "basico": basico,
        "funcion": funcion,
        "antiguedad": antig,
        "transformacion": transf,
        "bonif_docente": bonif_doc,
        "adic_jerarquico": adic_jera,
        "subtotal": subtotal,
        "zona": zona,
        "remunerativo": remunerativo,
        "total_horas": total_horas,
        "simples": simples,
        "completo": completo
    }
