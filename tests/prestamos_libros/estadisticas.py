def promedio_dias_prestamo(prestamos):
    if not prestamos:
        return 0

    total = 0

    for prestamo in prestamos:
        if "devolucion" not in prestamo:
            continue

        dias = (
            prestamo["devolucion"] - prestamo["fecha"]
        ).days

        total += dias

    return total / len(prestamos)


def autor_mas_prestado(prestamos, libros):
    contador = {}

    for prestamo in prestamos:
        isbn = prestamo["isbn"]

        for libro in libros:
            if libro["isbn"] == isbn:
                autor = libro["autor"]
                contador[autor] = contador.get(autor, 0) + 1

    if not contador:
        return None

    return max(contador, key=contador.get)


def porcentaje_devoluciones_atrasadas(prestamos):
    if not prestamos:
        return 0

    atrasadas = sum(
        1 for prestamo in prestamos
        if prestamo.get("dias_retraso", 0) > 0
    )

    return (atrasadas / len(prestamos)) * 100


def generar_reporte(prestamos, libros):
    return {
        "prestamos": len(prestamos),
        "libros": len(libros),
        "autor_mas_prestado": autor_mas_prestado(
            prestamos,
            libros
        ),
        "promedio_dias": promedio_dias_prestamo(prestamos)
    }