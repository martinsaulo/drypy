def calcular_precio_con_iva(precio, iva):
    return precio * (1 + iva)


def agregar_impuesto(valor, porcentaje):
    impuesto = valor * porcentaje
    return valor + impuesto


def precio_final(precio_base, tasa):
    return precio_base + precio_base * tasa


def calcular_descuento(precio, porcentaje):
    descuento = precio * porcentaje
    return precio - descuento


def aplicar_rebaja(valor, porcentaje):
    return valor * (1 - porcentaje)


def precio_con_descuento(precio_original, descuento):
    return precio_original - (precio_original * descuento)


def producto_disponible(stock):
    return stock > 0


def hay_existencias(cantidad):
    return cantidad >= 1