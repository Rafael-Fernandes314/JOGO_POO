artefatos_coletados = {
    "chave": False,
    "orbe": False,
    "espada": False,
    "escudo": False,
    "anel": False,
    "emblema": False,
    "sangue": False
}

def resetar_artefatos():
    for key in artefatos_coletados:
        artefatos_coletados[key] = False