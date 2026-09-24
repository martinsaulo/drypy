from usuarios import *
from productos import *
from pedidos import *
from utilidades import *
from reportes import *


def ejecutar_demo():
    usuario = {
        "nombre": "Juan",
        "apellido": "Pérez",
        "id": 10
    }

    productos = [
        {"precio": 100, "cantidad": 2},
        {"precio": 50, "cantidad": 3},
    ]

    print(obtener_nombre_completo(usuario))
    print(calcular_precio_con_iva(100, 0.21))
    print(calcular_total(productos))
    print(es_par(10))
    print(calcular_promedio([10, 20, 30]))


if __name__ == "__main__":
    ejecutar_demo()