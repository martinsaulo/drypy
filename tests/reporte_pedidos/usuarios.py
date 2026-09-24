def obtener_nombre_completo(usuario):
    return f"{usuario['nombre']} {usuario['apellido']}"


def construir_nombre_usuario(usuario):
    nombre = usuario.get("nombre", "")
    apellido = usuario.get("apellido", "")
    return nombre.strip() + " " + apellido.strip()


def mostrar_usuario(usuario):
    return "{} {}".format(
        usuario.get("nombre", ""),
        usuario.get("apellido", "")
    )


def calcular_edad(fecha_nacimiento, año_actual):
    return año_actual - fecha_nacimiento.year


def obtener_edad(nacimiento, actual):
    diferencia = actual.year - nacimiento.year
    return diferencia