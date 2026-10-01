import os
from itertools import combinations
from src.extractor import extract_functions, extract_target, FunctionDefinition
from src.comparator import compare_ast


def search_matches(root_path: str, target: str, top: int, threshold: float, method: str) -> list[FunctionDefinition]:

    top_matches = []

    def append_in_order(func1: FunctionDefinition, func2: FunctionDefinition):
        similarity_level = compare_functions(func1, func2, method)
        if similarity_level < threshold:
            return
        
        top_matches.append(func1)
        top_matches.sort(
            key=lambda function: compare_functions(function, func2, method),
            reverse=True,
        )
        del top_matches[top:]


    def brute_force_search(files: list[str], dir_path: str):
        functions = []

        for file in files:
            for function in extract_functions(file, dir_path):
                functions.append(function)


        for func1, func2 in combinations(functions, 2):
            append_in_order(func2, func1)


    def target_search(files: list[str], target: FunctionDefinition, dir_path: str):
        for file in files:
            for function in extract_functions(file, dir_path):
                append_in_order(function, target)



    for root, dirs, files in os.walk(root_path):
        # Filter cache folders
        dirs[:] = [d for d in dirs if d != "__pycache__"]

        if target:
            target_function = extract_target(target)
            target_search(files, target_function, root)
        else:
            brute_force_search(files, root)


    return top_matches



def compare_functions(func1: FunctionDefinition, func2: FunctionDefinition, method: str) -> float:
    if func1 == func2: # Avoid compare the target to itself
        return -1

    return compare_ast(func1.sub_tree, func2.sub_tree, method)