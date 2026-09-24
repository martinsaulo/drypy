def registrar_libro(libros, titulo, autor, isbn):
    libro = {
        "titulo": titulo,
        "autor": autor,
        "isbn": isbn,
        "disponible": True
    }

    libros.append(libro)


def eliminar_libro(libros, isbn):
    for libro in libros:
        if libro["isbn"] == isbn:
            libros.remove(libro)
            return True

    return False


def buscar_por_autor(libros, autor):
    resultados = []

    for libro in libros:
        if libro["autor"].lower() == autor.lower():
            resultados.append(libro)

    return resultados


def ordenar_por_titulo(libros):
    return sorted(libros, key=lambda libro: libro["titulo"].lower())


def contar_libros_disponibles(libros):
    return sum(1 for libro in libros if libro["disponible"])


def exportar_catalogo(libros, archivo):
    with open(archivo, "w", encoding="utf-8") as f:
        for libro in libros:
            f.write(
                f"{libro['titulo']} - "
                f"{libro['autor']} - "
                f"{libro['isbn']}\n"
            )