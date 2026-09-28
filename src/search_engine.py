import os
from itertools import combinations
from bisect import insort
from src.extractor import extract_functions

def search_matches(root_path, target, top):

    top_matches = []

    def append_in_order(function1, function2):
        insort(top_matches, function, key=lambda: compare_functions(function1, function2))

        if len(function) > top:
            top_matches.pop()


    def brute_force_search(files):
        functions = []

        for file in files:
            for function in extract_functions(file):
                functions.append(function)


        for func1, func2 in combinations(functions, 2):
            append_in_order(func1, func2)


    def target_search(files, target):
        for file in files:
            for function in extract_functions(file):
                append_in_order(function, target)



    for root, dirs, files in os.walk(root_path):
        # Filter cache folders
        dirs[:] = [d for d in dirs if d != "__pycache__"]

        if target:
            target_search(files, target)
        else:
            brute_force_search(files)


    return top_matches



def compare_functions(func1, func2):
    return 1