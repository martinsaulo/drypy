def registrar_usuario(usuarios, nombre, documento):
    usuarios[documento] = {
        "nombre": nombre,
        "documento": documento,
        "activo": True
    }


def desactivar_usuario(usuarios, documento):
    if documento in usuarios:
        usuarios[documento]["activo"] = False
        return True

    return False


def obtener_usuario(usuarios, documento):
    return usuarios.get(documento)


def listar_usuarios_activos(usuarios):
    return [
        usuario
        for usuario in usuarios.values()
        if usuario["activo"]
    ]


def cambiar_nombre(usuarios, documento, nuevo_nombre):
    if documento not in usuarios:
        return False

    usuarios[documento]["nombre"] = nuevo_nombre
    return True


def cantidad_usuarios(usuarios):
    return len(usuarios)