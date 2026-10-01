import os
from itertools import combinations
from src.extractor import extract_functions, extract_target, FunctionDefinition
from src.comparator import compare_ast


def search_matches(
        root_path: str,
        target: str | None,
        top: int,
        threshold: float,
        method: str
    ) -> list[FunctionDefinition] | list[tuple[FunctionDefinition, FunctionDefinition, float]]:
    functions = []

    for root, dirs, files in os.walk(root_path):
        # Filter cache folders
        dirs[:] = [d for d in dirs if d != "__pycache__"]
        for file in files:
            functions.extend(extract_functions(file, root))

    # Target search
    if target:
        target_function = extract_target(target)
        matches = [
            function
            for function in functions
            if compare_functions(function, target_function, method) >= threshold
        ]
        matches.sort(
            key=lambda function: compare_functions(function, target_function, method),
            reverse=True,
        )
        return matches[:top]

    # Pairs search
    pairs = [
        (func1, func2, similarity)
        for func1, func2 in combinations(functions, 2)
        if (similarity := compare_functions(func1, func2, method)) >= threshold
    ]
    pairs.sort(key=lambda pair: pair[2], reverse=True)
    return pairs[:top]



def compare_functions(func1: FunctionDefinition, func2: FunctionDefinition, method: str) -> float:
    if func1 == func2: # Avoid compare the target to itself
        return -1

    return compare_ast(func1.sub_tree, func2.sub_tree, method)