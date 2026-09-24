def es_par(numero):
    return numero % 2 == 0


def comprobar_par(valor):
    if valor % 2 == 0:
        return True
    return False


def numero_par(n):
    return not n % 2


def es_mayor_de_edad(edad):
    return edad >= 18


def puede_votar(edad):
    return edad >= 18


def tiene_edad_legal(anios):
    if anios < 18:
        return False

    return True


def buscar_usuario_por_id(usuarios, identificador):
    for usuario in usuarios:
        if usuario["id"] == identificador:
            return usuario

    return None


def encontrar_usuario(usuarios, user_id):
    return next(
        (usuario for usuario in usuarios if usuario["id"] == user_id),
        None
    )