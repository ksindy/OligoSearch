import numpy as np
from matplotlib import animation, rc
import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)


# import xlrd
# import re
# #file = open('/Users/ksindy/PycharmProjects/oligo_search_website/KH Oligos (1) .xlsx')
# book = xlrd.open_workbook('/Users/ksindy/PycharmProjects/oligo_search_website/KH Oligos (1) .xlsx')
# sheet = book.sheet_by_index(0)
# oligo_list = []
#
# for i in range(sheet.nrows):
#     oligo = (sheet.cell_value(
#         rowx=i,
#         colx= 2)).upper().replace(" ", "")
#     regex = re.compile('[^agctuAGCTU]')
#     oligo = regex.sub('', oligo)
#     if oligo:
#         oligo_list.append(oligo)
# print (oligo_list)




    # if i < sheet.nrows and oligo != "" and mismatches_choice != 0:
    #     name = sheet.cell_value(rowx=i, colx=int(name_column_input))
    #     name_match = str(name)


# def find_in(reference, pattern):
#     if pattern in reference:
#         return 'yes'
#
#
# list = ['GTACACCGTGGG']
# final_list = []
# working_list = []
#
# def neighbors(list, mismatch_num):
#     nucleotides = 'ACGT'
#     current_list = []
#
#     for pattern in list:
#         pattern_whole = ''
#         for index, nucleotide in enumerate(pattern):
#             rest = pattern[(index+1)::]
#
#             for i, nuc in enumerate(nucleotides):
#                 working_pattern = ''
#                 working_pattern += pattern_whole
#                 working_pattern += nuc
#                 working_pattern += rest
#
#                 if working_pattern not in final_list:
#                     final_list.append(working_pattern)
#                     current_list.append(working_pattern)
#                     print(final_list)
#             pattern_whole += nucleotide
#
#     if mismatch_num > 1:
#         for item in current_list:
#             working_list.append(item)
#         return neighbors(working_list, mismatch_num-1)
#     else:
#         return 'this is result{}'.format("\n".join(final_list))
#
#
#
# print(neighbors(list, 2))

# def neighbours (pattern, d):
#     if d == 0:
#         return pattern
#     if len(pattern) == 1:
#         return ['A','C','G','T']
#     neighbourhood = set()
#     suffix_neighbours = neighbours(pattern[1:], d)
#     for suffix_neighbour in suffix_neighbours:
#         if hamm(pattern[1:], suffix_neighbour) < d:
#             for base in 'ACGT':
#                 neighbourhood.add(base + suffix_neighbour)
#         else:
#             neighbourhood.add(pattern[0] + suffix_neighbour)
#     return neighbourhood
#
# print(neighbours('GTACACCGTGGG',2))