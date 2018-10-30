import re
import sys

import numpy as np


constants = []
coefficients = []
variables = {}
equations = []
variable_index = 0
file_name = sys.argv[1]#'input.txt'

def build_coefficient_matrix():
    A_list = []
    for equation in equations:
        row = np.zeros(len(variables))
        literals = re.findall(r"(?:\-|\+)?\s?\d?[a-z]", equation)
        for literal in literals:
            if literal.startswith('+') or literal.startswith('-'):
                if len(literal) == 3:
                    value = 1
                else:
                    value = int(literal[2:-1])
                if literal.startswith('-'):
                    value = -value
            else:
                if len(literal) == 1:
                    value = 1
                else:
                    value = int(literal[:-1])
            variable = literal[-1]
            row[variables[variable]] = value
        A_list.append(row)
    return A_list


for line in open(file_name, 'r', encoding="utf8"):
    equation = line.split('=')
    left_side = equation[0].strip()
    equations.append(left_side)
    right_side = int(equation[1].strip())
    constants.append([right_side])

    variables_list = re.findall(r"[a-z]", left_side)
    for v in variables_list:
        if v not in variables:
            variables[v] = variable_index
            variable_index += 1

A = np.array(build_coefficient_matrix())
B = np.array(constants)

rank = np.linalg.matrix_rank(A)
matrix_augmented = np.append(A, B, axis=1)
rank_augmented = np.linalg.matrix_rank(matrix_augmented)

if rank != rank_augmented:
    print('no solution')
elif len(variables) > rank:
    print("solution space dimension: " + str(len(variables) - rank))
else:
    X = np.linalg.solve(A, B)
    result = 'solution: '
    values = []
    for i, solution in enumerate(X):
        for variable_name, variable_index in variables.items():
            if i == variable_index:
                values.append(variable_name + ' = ' + str(solution[0]))
    values.sort()
    result += ', '.join(values)
    print(result)
