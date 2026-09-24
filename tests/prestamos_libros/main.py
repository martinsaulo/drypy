from libros import (
    registrar_libro,
    buscar_por_autor,
    ordenar_por_titulo
)

from usuarios import (
    registrar_usuario,
    obtener_usuario
)

from prestamos import crear_prestamo
from multas import calcular_multa
from estadisticas import generar_reporte


def ejecutar():
    libros = []
    usuarios = {}
    prestamos = []

    registrar_libro(
        libros,
        "El principito",
        "Antoine de Saint-Exupéry",
        "978-0156012195"
    )

    registrar_libro(
        libros,
        "1984",
        "George Orwell",
        "978-0451524935"
    )

    registrar_usuario(
        usuarios,
        "Juan Pérez",
        "12345678"
    )

    usuario = obtener_usuario(
        usuarios,
        "12345678"
    )

    libro = libros[0]

    prestamo = crear_prestamo(
        usuario,
        libro
    )

    if prestamo:
        prestamos.append(prestamo)

    print(
        "Libros:",
        ordenar_por_titulo(libros)
    )

    print(
        "Multa de 5 días:",
        calcular_multa(5)
    )

    print(
        "Reporte:",
        generar_reporte(prestamos, libros)
    )


if __name__ == "__main__":
    ejecutar()