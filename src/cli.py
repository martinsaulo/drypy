import argparse, os
from src.search_engine import search_matches
from src.extractor import extract_source
from src.colors import GREEN, BLUE, RED, END


def run_cli():
    parser = create_parser()
    args = parser.parse_args()

    print(f"{BLUE}[*] Analizando: {args.project}{END}")

    if args.target:
        print(f"{BLUE}[*] Funcion: {args.target.split(":")[1]}{END}")

    try:
        matches = search_matches(args.project, args.target, args.number)
    except StopIteration:
        path, target = args.target.split(":")
        print(f"{RED}No existe ninguna función {target} en el archivo {path}{END}")
        return

    if len(matches) == 0:
        print(f"{GREEN}No se encontró código repetitivo.{END}")
        return


    print(f"{GREEN}Top {len(matches)} similitudes:{END}")

    for function in matches:
        print(function)

        if args.verbose:
            max_lines = 15
        if args.vv:
            max_lines = 50
        if args.vvv:
            max_lines = None

        if args.verbose or args.vv or args.vvv:
            print(extract_source(function, max_lines))
            print("------------------------------------------")

    


def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)


def func_ref(string):
    parts = string.split(":")


    if len(parts) != 2:
        raise ValueError(string)

    if os.path.isfile(parts[0]):
        return string
    else:
        raise FileNotFoundError(parts[0])


def create_parser():
    parser = argparse.ArgumentParser(
        prog="drypy", 
        description="Motor de busqueda de código Python repetitivo."
    )
    parser.add_argument(
        "project", 
        type=dir_path, 
        help="Directorio raíz del proyecto a analizar."
    )
    parser.add_argument(
        "-t", "--target"
        , type=func_ref, 
        help=(
            "Función objetivo que se utilizará para la comparación. "
            "Si no se especifica, se compararán todas las funciones entre sí."
        )
    )
    parser.add_argument(
        "-n", 
        "--number", 
        default=5,
        help=(
            "Cantidad de resultados a mostrar. "
            "Se devolverán las N funciones más similares (por defecto: 5)."
        )
    )
    parser.add_argument(
        "-v", "--verbose", 
        action="store_true", 
        help=(
            "Muestra las primeras 15 líneas del código fuente. "
            "Usar -vv para mostrar las primeras 50 líneas y -vvv para mostrar la función completa."
        )
    )
    parser.add_argument(
        "-th", "--threshold",
        type=float,
        default=50.0,
        help=(
            "Umbral de tolerancia [0, 100]. "
            "Únicamente se mostrarán las funciones que superen el umbral (por defecto: 50)"
        )

    )
    parser.add_argument("-vv", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("-vvv", action="store_true", help=argparse.SUPPRESS)    

    return parser