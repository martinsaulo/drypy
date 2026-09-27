import argparse, os

def run_cli():
    parser = create_parser()
    args = parser.parse_args()

    print(f"Analizando: {args.project}")
    print(f"Funcion: {args.target}")
    print(f"Top {args.number} similares")

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
    parser.add_argument("-t", "--target", type=func_ref, help="Referencia a la función a analizar", required=True)
    parser.add_argument("-n", "--number", help="Número de ocurrencias", default=5)
    parser.add_argument("-v", "--verbose", action="store_true", help="Aumenta la cantidad de información de la respuesta")

    return parser