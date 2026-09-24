from datetime import datetime, timedelta


def crear_prestamo(usuario, libro):
    if not libro["disponible"]:
        return None

    libro["disponible"] = False

    return {
        "usuario": usuario["documento"],
        "isbn": libro["isbn"],
        "fecha": datetime.now(),
        "vencimiento": datetime.now() + timedelta(days=15)
    }


def devolver_libro(prestamo, libro):
    libro["disponible"] = True
    prestamo["devolucion"] = datetime.now()


def esta_atrasado(prestamo):
    if "devolucion" in prestamo:
        return False

    return datetime.now() > prestamo["vencimiento"]


def dias_de_retraso(prestamo):
    if not esta_atrasado(prestamo):
        return 0

    diferencia = datetime.now() - prestamo["vencimiento"]
    return diferencia.days


def obtener_prestamos_usuario(prestamos, documento):
    return [
        prestamo
        for prestamo in prestamos
        if prestamo["usuario"] == documento
    ]