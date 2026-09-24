def calcular_total(items):
    total = 0

    for item in items:
        total += item["precio"] * item["cantidad"]

    return total


def obtener_importe_pedido(productos):
    return sum(
        producto["precio"] * producto["cantidad"]
        for producto in productos
    )


def sumar_costos(lineas):
    resultado = 0

    for linea in lineas:
        subtotal = linea["precio"] * linea["cantidad"]
        resultado += subtotal

    return resultado


def contar_productos(items):
    cantidad = 0

    for item in items:
        cantidad += item["cantidad"]

    return cantidad


def cantidad_total(productos):
    return sum(producto["cantidad"] for producto in productos)


def pedido_vacio(pedido):
    return len(pedido) == 0


def no_tiene_productos(productos):
    return not productos