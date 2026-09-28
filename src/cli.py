import argparse, os
from src.search_engine import search_matches

GREEN = "\033[0;32m"
BLUE = "\033[0;34m"
END = "\033[0m"


def run_cli():
    parser = create_parser()
    args = parser.parse_args()

    print(f"{BLUE}[*] Analizando: {args.project}{END}")

    if args.target:
        print(f"{BLUE}[*] Funcion: {args.target.split(":")[1]}{END}")

    matches = search_matches(args.project, args.target, args.number)

    if len(matches) == 0:
        print(f"{GREEN}No se encontró código repetitivo.{END}")
        return


    print(f"{GREEN}Top {len(matches)} similitudes:{END}")

    for function in matches:
        print(function)

        if args.verbose:
            print("Info extra...")

    


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
    parser = argparse.ArgumentParser(prog="drypy", description="Motor de busqueda de código repetitivo.")
    parser.add_argument("project", type=dir_path, help="Directorio del proyecto")
    parser.add_argument("-t", "--target", type=func_ref, help="Referencia a la función a analizar")
    parser.add_argument("-n", "--number", help="Número de resultados", default=5)
    parser.add_argument("-v", "--verbose", action="store_true", help="Aumenta la cantidad de información de la respuesta")

    return parser