def calcular_promedio(numeros):
    if not numeros:
        return 0

    return sum(numeros) / len(numeros)


def obtener_media(valores):
    cantidad = len(valores)

    if cantidad == 0:
        return 0

    total = sum(valores)
    return total / cantidad


def promedio_lista(datos):
    return sum(datos) / len(datos) if datos else 0


def encontrar_maximo(numeros):
    if not numeros:
        return None

    mayor = numeros[0]

    for numero in numeros[1:]:
        if numero > mayor:
            mayor = numero

    return mayor


def obtener_valor_mas_alto(valores):
    return max(valores) if valores else None


def buscar_mayor(datos):
    resultado = None

    for valor in datos:
        if resultado is None or valor > resultado:
            resultado = valor

    return resultado