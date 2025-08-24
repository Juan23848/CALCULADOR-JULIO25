
from antiguedad import calcular_antiguedad_factor

JERARQUICOS = {
    "954","814","800","302","820","806","809","804","210","501","202","200","826","208","803",
    "400","402","502","837","204","827","206","107","811","700","901","828","407","301","201",
    "300","821","862","905","500","817","207","813","203","401","601","511","822","818","105",
    "906","408","805","864","812","952","949","303","406","825","211","953","103","403","405",
    "819","513","205","838","512","824","815","807","802","902","808","816","823","900","951",
    "602","106","101","104","404","600","810","801","209","102","950"
}

BONIF_DOCENTE = {
    "312", "421", "301", "302", "303", "304", "305", "306", "307", "308", "309", "310", "311", "313", "314", "315",
    "316", "317", "318", "319", "320", "321", "322", "323", "324", "325", "326", "327", "328", "329", "330", "331",
    "332", "333", "334", "335", "336", "337", "338", "339", "340", "341", "342", "343", "344", "345", "346", "347",
    "348", "349", "350", "351", "352", "353", "354", "355", "356", "357", "358", "359", "360", "361", "362", "363",
    "364", "365", "366", "367", "368", "369", "370", "371", "372", "373", "374", "375", "376", "377", "378", "379",
    "380", "381", "382", "383", "384", "385", "386", "387", "388", "389", "390", "391", "392", "393", "394", "395",
    "396", "397", "398", "399", "401", "402", "403", "406", "407", "408", "409", "410", "412", "413", "414", "415",
    "416", "417", "418", "419", "423", "424", "425", "426", "427", "428", "429", "430", "431", "432", "433", "434",
    "435", "436", "437", "438", "439", "440", "441", "442", "443", "444", "445", "446", "447", "448", "449", "450",
    "451", "452", "453", "454", "455", "456", "457", "458", "459", "460", "461", "462", "463", "464", "465", "466",
    "467", "468", "469", "470", "471", "472", "473", "474", "475", "476", "477", "478", "479", "480", "481", "482",
    "483", "484", "485", "486", "487", "488", "489", "490", "491", "492", "493", "494", "495", "496", "497", "498", "499"
}

def calcular_componentes(cargos, cantidades, puntajes, vi, antiguedad):
    total_puntaje = basico_jera = bonif_doc = 0.0
    total_horas = 0
    simples = 0
    completo = False

    detalle = {
        "items": [],
    }

    for i, cargo in enumerate(cargos):
        if not cargo or cantidades[i] <= 0:
            continue
        codigo = cargo.split(" - ")[0].strip()
        desc = cargo.lower()
        puntaje = float(puntajes.get(cargo, 0.0))
        cant = int(cantidades[i])
        monto = puntaje * cant * vi

        total_puntaje += puntaje * cant

        if codigo in JERARQUICOS:
            basico_jera += monto

        if "hora" in desc:
            total_horas += cant
        elif "completo" in desc:
            completo = True
        elif "simple" in desc:
            simples += cant

        bonif = 0.0
        if codigo in BONIF_DOCENTE:
            bonif = monto * 0.2775
            bonif_doc += bonif

        detalle["items"].append({
            "codigo": codigo,
            "descripcion": cargo,
            "cantidad": cant,
            "puntaje": puntaje,
            "VI": vi,
            "monto_basico": monto,
            "bonificacion_docente": bonif
        })

    basico = total_puntaje * vi
    func = basico * 2.30
    ant = basico * calcular_antiguedad_factor(antiguedad)
    transf = basico * 1.23
    adic_jera = basico_jera * 0.30

    subtotal = basico + func + ant + transf + bonif_doc + adic_jera
    zona = subtotal
    remunerativo = subtotal + zona

    return {
        "basico": basico,
        "funcion": func,
        "antiguedad": ant,
        "transformacion": transf,
        "bonif_docente": bonif_doc,
        "adic_jerarquico": adic_jera,
        "subtotal": subtotal,
        "zona": zona,
        "remunerativo": remunerativo,
        "total_horas": total_horas,
        "simples": simples,
        "completo": completo,
        "detalle": detalle
    }
