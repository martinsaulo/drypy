def calcular_multa(dias_retraso, tarifa_diaria=100):
    if dias_retraso <= 0:
        return 0

    return dias_retraso * tarifa_diaria


def registrar_pago(multa, monto):
    if monto <= 0:
        raise ValueError("El monto debe ser positivo")

    multa["pagado"] += monto

    if multa["pagado"] >= multa["total"]:
        multa["estado"] = "pagada"


def saldo_pendiente(multa):
    return max(0, multa["total"] - multa["pagado"])


def generar_multa(prestamo):
    dias = prestamo.get("dias_retraso", 0)

    return {
        "usuario": prestamo["usuario"],
        "total": calcular_multa(dias),
        "pagado": 0,
        "estado": "pendiente"
    }


def cancelar_multa(multa):
    multa["estado"] = "cancelada"