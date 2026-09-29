import os
from itertools import combinations
from bisect import insort
from src.extractor import extract_functions, extract_target

def search_matches(root_path, target, top):

    top_matches = []

    def append_in_order(function1, function2):
        insort(top_matches, function1, key=lambda x: compare_functions(function1, function2))

        if len(top_matches) > top:
            top_matches.pop()


    def brute_force_search(files, dir_path):
        functions = []

        for file in files:
            for function in extract_functions(file, dir_path):
                functions.append(function)


        for func1, func2 in combinations(functions, 2):
            append_in_order(func2, func1)


    def target_search(files, target, dir_path):
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



def compare_functions(func1, func2):
    # TODO: check if func1 and func2 are exacly the same function (same file and same signature)
    return 1