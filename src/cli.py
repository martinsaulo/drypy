import argparse, os
from src.search_engine import search_matches
from src.extractor import extract_source, extract_target
from src.colors import GREEN, BLUE, RED, END
from src.util import SEPARATOR
from src.search_engine import compare_functions


def run_cli():
    parser = create_parser()
    args = parser.parse_args()

    print(f"{BLUE}[*] Analizando: {args.project}{END}")

    if args.target:
        print(f"{BLUE}[*] Funcion: {args.target.split(":")[1]}{END}")

    try:
        matches = search_matches(args.project, args.target, args.number, args.threshold, args.method)
    except StopIteration:
        path, target = args.target.split(":")
        print(f"{RED}No existe ninguna función {target} en el archivo {path}{END}")
        return

    if len(matches) == 0:
        print(f"{GREEN}No se encontró código repetitivo.{END}")
        return

    if has_verbose_level(args) and args.target:
        target_function = extract_target(args.target)
        print(SEPARATOR)
        print(extract_source(target_function, get_verbose_level(args)))
        print(SEPARATOR + "\n")

    # Target search
    if args.target:
        print(f"{GREEN}Top {len(matches)} similitudes:{END}")
        for function in matches:
            print(function)
            target_function = extract_target(args.target)
            diff = compare_functions(function, target_function, args.method)
            print(f"{BLUE}Nivel de similitud:{END} {round(diff, 2)}")

            if has_verbose_level(args):
                print(SEPARATOR)
                print(extract_source(function, get_verbose_level(args)))
                print(SEPARATOR)
        return

    # Pairs search
    print(f"{GREEN}Top {len(matches)} pares de similitudes:{END}")
    for first, second, similarity in matches:
        print(first)
        print(second)
        print(f"{BLUE}Nivel de similitud:{END} {round(similarity, 2)}")

        if has_verbose_level(args):
            print(SEPARATOR)
            print(extract_source(first, get_verbose_level(args)))
            print(SEPARATOR)
            print(extract_source(second, get_verbose_level(args)))
            print(SEPARATOR)

    

def has_verbose_level(args: argparse.Namespace):
    return args.target and args.verbose or args.vv or args.vvv


def get_verbose_level(args: argparse.Namespace):
    if args.verbose:
        return 15
    if args.vv:
        return  50
    
    return None


def dir_path(string: str) -> str:
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)


def func_ref(string: str) -> str:
    parts = string.split(":")


    if len(parts) != 2:
        raise ValueError(string)

    if os.path.isfile(parts[0]):
        return string
    else:
        raise FileNotFoundError(parts[0])


def method_ref(string: str) -> str:
    if string in ["SQ", "LD", "TED"]:
        return string
    else:
        raise ValueError(string)


def create_parser() -> argparse.ArgumentParser: 
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
        type=int,
        default=5,
        help=(
            "Cantidad máxima de resultados a mostrar. En búsquedas sin objetivo "
            "representa la cantidad máxima de pares (por defecto: 5)."
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
    parser.add_argument(
        "-m", "--method",
        type=method_ref,
        default="SQ",
        help=(
            "Método de comparación. "
            "Opciones: [SQ = Sequence Matcher, LD = Levenshtein Distance, TED = Tree Edit Distance] (por defecto: SQ)"
        )
    )
    parser.add_argument("-vv", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("-vvv", action="store_true", help=argparse.SUPPRESS)    

    return parser