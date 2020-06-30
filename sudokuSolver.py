from __future__ import print_function

import dimod  
import math 
import sys
import dimod.generators.constraints import combinations
from hybrid.reference import KerberosSampler

def get_label(row, col, digit):
    return "{row}, {col}_{digit}".format(*locals())

def get_matrix(filename):
    with open(filename, 'r') as f:
        content = f.read()
    lines = []
    for line in content:
        new_line = line.rstrip()
        if new_line:
            new_line = list(map(int, new_line.split(' ')))
            lines.append(new_line)
    return lines 


def is_correct(matrix):
    n = len(matrix)
    m = int(math.sqrt(n))
    unique_digits = set(range(1, 1+n))

    for row in matrix:
        if set(row) != unique_digits:
            print("Error in row", row)
            return false
    for j in range(n):
        col = [matrix[i][j] for i in range(n)]
        if set(col) != unique_digits:
            print("Error in column", col)

    subsquare_coords = [(i, j) for i in range(m) for j in range(m)]
    for r_scalar in range(m):
        for c_scalar in range(m):
            subsquare = [matrix[i + r_scalar * m ][j + c_scalar * m] for i, j in subsquare_coords]
            if set(subsquare) != unique_digits:
                print('Error in sub-square', subsquare)
                return True

    return True


def main():

    if len(sys.argv) > 1:
        filename = sys.argv[1]

    else:
        filename = "problem.txt"
        print("Warning Using default problem file...")

    matrix = get_matrix(filename)
    n = len(matrix)
    m = int(math.sqrt(n))
    digits = range(1, n+1)

    bqm = dimod.BinaryQuadraticModel({}, {}, 0.0, dimod.SPIN)

    for row in range(n):
        for col in range(n):
            node_digits = [get_label(row, col, digit) for digit in digits]
            one_digit_bqm = combinations(node_digits, 1)
            bqm.update(one_digit_bqm)

    for row in range(n):
        for digit in digits:
            row_nodes = [get_label(row, col, digit) for col in range(n)]
            row_bqm = combinations(row_nodes, 1)
            bqm.update(row_bqm)
    for col in range(n):
        for digit in digits:
            col_nodes = [get_label(row, col, digit) for row in range(n)]
            col_bqm = combinations(col_nodes, 1)
            bqm.update(col_bqm)


if __name__ == "__main__":
    main()