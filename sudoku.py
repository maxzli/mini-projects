#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 00:14:37 2020

@author: maxzli
"""
from IPython import get_ipython
get_ipython().magic('reset -sf')

import time

# # have some way to get a sudoku grid
# def read_file(file):
#     with open(file) as f:
#         for line in f:
            
def manual_input_sudoku():
    grid = [" "]*81
    # for i in grid:
    #     i = input("number? ")
        
    grid[27] = 3; grid[28] = 8; grid[29] = 4; grid[80] = 2
    return grid

def read_sudoku_string(s, n):
    grid = [" "]*n**2
    index = 0
    for char in s:
        if char == '.':
            grid[index] = " "
        elif char in "123456789":
            grid[index] = int(char)
        else:
            raise Exception("Check inputted string!")
        index += 1
    return grid

def is_sudoku_valid(grid):
    n = int(len(grid)**(1/2))
    for i in range(0, n):
        l = []
        for j in range(n*i, n*i+n):
            if grid[j] in l and grid[j] != " ":
                return False
            l.append(grid[j])
    for i in range(0, n):
        l = []
        for j in range(0, n):
            if grid[i+n*j] in l and grid[i+n*j] != " ":
                return False
            l.append(grid[i+n*j])
    for i in range(0, n):
        l = []
        for j in range(0, n):
            cell = int(i/3)*27+3*(i%3)+int(j/3)*9+j%3
            if grid[cell] in l and grid[cell] != " ":
                return False
            l.append(grid[cell])
    return True

def solve(grid, memo = {}):
    grid2 = grid.copy()
    if " " not in grid:
        return (True, grid)
    if tuple(grid) in memo:
        return (memo[tuple(grid)], grid)
    for i in range(0, len(grid2)):
        if grid2[i] == " ":
            for j in range(1, int(len(grid2)**0.5)+1):
                grid2[i] = j
                if is_sudoku_valid(grid2):
                    x = solve(grid2)
                    if x[0] == True:
                        return x
    memo[tuple(grid)] = False
    return (False, grid)

def even_smarter_solve(grid, first, p, memo = {}):
    grid2 = grid.copy()
    if " " not in grid:
        return (True, grid)
    if tuple(grid) in memo:
        return (memo[tuple(grid)], grid)
    for i in generate_priority(grid, first, p):
        if grid2[i] == " ":
            for j in range(1, int(len(grid2)**0.5)+1):
                grid2[i] = j
                if is_sudoku_valid(grid2):
                    x = even_smarter_solve(grid2, i, p)
                    if x[0] == True:
                        return x
    memo[tuple(grid)] = False
    return (False, grid)

def generate_priority(grid, first, x):
    priority = []
    # x = [[0, 1, 2, 9, 10, 11, 18, 19, 20], \
    #       [3, 4, 5, 12, 13, 14, 21, 22, 23], \
    #           [6, 7, 8, 15, 16, 17, 24, 25, 26], \
    #               [27, 28, 29, 36, 37, 38, 45, 46, 47], \
    #                   [30, 31, 32, 39, 40, 41, 48, 49, 50], \
    #                       [33, 34, 35, 42, 43, 44, 51, 52, 53], \
    #                               [54, 55, 56, 63, 64, 65, 72, 73, 74], \
    #                                   [57, 58, 59, 66, 67, 68, 75, 76, 77], \
    #                                       [60, 61, 62, 69, 70, 71, 78, 79, 80]]
    for y in x:
        if first in y:
            for z in y:
                if grid[z] == " ":
                    priority.append(z)
            break
    
    first2 = first
    for j in range(1, 9):
        if (first2+j)%9 == 0:
            first2 = first2-9
        if grid[first2+j] == " " and first2+j not in priority:
            priority.append(first2+j)
        
    for j in range(1,9):
        if grid[(first+9*j)%81] == " " and (first+9*j)%81 not in priority:
            priority.append((first+9*j)%81)
    
    for y in x:
        for z in y:
            if z not in priority and grid[z] == " ":
                priority.append(z)
    return priority
            
# def smarter_solve(grid, gaps, memo = {}): # gaps dictionary
#     grid2 = grid.copy()
#     gaps2 = gaps.copy()
#     if " " not in grid:
#         return (True, grid)
#     if tuple(grid) in memo:
#         return (memo[tuple(grid)], grid)
#     for i in sorted(gaps, key = gaps.get): # control order of selecting gaps
#         if grid2[i] == " ":
#             for j in range(1, int(len(grid2)**0.5)+1):
#                 grid2[i] = j
#                 gaps2 = decrease_gaps(gaps2, i)
#                 if is_sudoku_valid(grid2):
#                     x = smarter_solve(grid2, gaps2)
#                     if x[0] == True:
#                         return x
#     memo[tuple(grid)] = False
#     return (False, grid)

# def count_gaps(grid):
#     gaps = {}
#     n = int(len(grid)**(1/2))
#     for i in range (0, n**2):
#         gaps[i] = 0
#     for i in range(0, n):
#         count = 0
#         for j in range(n*i, n*i+n):
#             if grid[j] == " ":
#                 count += 1
#         for k in range(n*i, n*i+n):
#             gaps[k] += count

#     for i in range(0, n):
#         count = 0
#         for j in range(0, n):
#             if grid[i+n*j] == " ":
#                 count += 1
#         for k in range(0, n):
#             gaps[i+n*k] += count
    
#     for i in range(0, n):
#         count = 0
#         for j in range(0, n):
#             cell = int(i/3)*27+3*(i%3)+int(j/3)*9+j%3
#             if grid[cell] == " ":
#                 count += 1
#         for j in range (0, n):
#             cell = int(i/3)*27+3*(i%3)+int(j/3)*9+j%3
#             gaps[cell] += count

#     return gaps
        
# def decrease_gaps(gaps, i):
#     i2 = i
#     gaps2 = gaps.copy()
#     gaps2[i] -= 1
#     for j in range(1, 9):
#         if (i+j)%9 == 0:
#             i = i-9
#         gaps2[i+j] -= 1
        
#     gaps2[i2] -= 1
#     for j in range(1,9):
#         gaps2[(i2+9*j)%81] -= 1
    
#     x = [[0, 1, 2, 9, 10, 11, 18, 19, 20], \
#           [3, 4, 5, 12, 13, 14, 21, 22, 23], \
#               [6, 7, 8, 15, 16, 17, 24, 25, 26], \
#                   [27, 28, 29, 36, 37, 38, 45, 46, 47], \
#                       [30, 31, 32, 39, 40, 41, 48, 49, 50], \
#                           [33, 34, 35, 42, 43, 44, 51, 52, 53], \
#                                   [54, 55, 56, 63, 64, 65, 72, 73, 74], \
#                                       [57, 58, 59, 66, 67, 68, 75, 76, 77], \
#                                           [60, 61, 62, 69, 70, 71, 78, 79, 80]]
         
#     for index in range(0, 9):
#         if i2 in x[index]:
#             for j in x[index]:
#                 gaps2[j] -= 1
#             break
    
#     return gaps2
    
x = [[0, 1, 2, 9, 10, 11, 18, 19, 20], \
          [3, 4, 5, 12, 13, 14, 21, 22, 23], \
              [6, 7, 8, 15, 16, 17, 24, 25, 26], \
                  [27, 28, 29, 36, 37, 38, 45, 46, 47], \
                      [30, 31, 32, 39, 40, 41, 48, 49, 50], \
                          [33, 34, 35, 42, 43, 44, 51, 52, 53], \
                                  [54, 55, 56, 63, 64, 65, 72, 73, 74], \
                                      [57, 58, 59, 66, 67, 68, 75, 76, 77], \
                                          [60, 61, 62, 69, 70, 71, 78, 79, 80]]

                
grid = manual_input_sudoku()
# grid = read_sudoku_string(".....8.....53..68.6..1....425....8.1....5....8..92.3...9..3...21..6..4..76.......", 9)
st = time.time()
# gaps = count_gaps(grid)

y1 = solve(grid)
t1 = time.time() - st
print("Time:", t1, "seconds for normal solve")
print(y1)

# st = time.time()
# gaps = count_gaps(grid)
# y2 = smarter_solve(grid, gaps)
# t2 = time.time()-st
# print("Time:", t2, "seconds for smarter solve")
# print(y2)

st = time.time()
y3 = even_smarter_solve(grid, 0, x)
t3 = time.time()-st
print("Time:", t3, "seconds for even smarter solve")
print(y3)