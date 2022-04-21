puzzle = """070 000 043
            040 009 610
            800 634 900

            094 052 000
            358 460 020
            000 800 530

            080 070 091
            902 100 005
            007 040 802"""


def main(puzzle):
    node = create_dict(puzzle)
    print_puzzle(node['puzzle'])
    stack = [node]
    nodes_visited = 0
    while stack:
        node = stack.pop()
        nodes_visited += 1
        valid, node = pruning(node)
        if valid:
            child_nodes = []
            if child_nodes:
                stack.append(child_nodes)
            else:
                valid = check_solution(node)
                if valid:
                    string = compile_string(node['cells'])
                    node['solution'] = string
                    print('THE SOLUTION!')
                    print('Nodes visited: ', nodes_visited)
                    print_puzzle(node['solution'])
                    return valid, node
    print('No solution found! :(')
    print('More advanced techniques needed.')
    return False, node


def pruning(node):
    found = True
    while found:
        found = False

        valid, node = apply_rules(node)
        if valid is False:
            return False, node

        found, node = naked_singles(node)
        if found is True:
            continue

        found, node = hidden_singles(node)
        if found is True:
            continue
    return True, node


def apply_rules(node):
    size = len(node['cells'])
    for i in range(size):  # rows
        for j in range(size):  # columns
            if isinstance(node['cells'][i][j], int):
                # ROW
                for k in range(size):  # columns
                    if isinstance(node['cells'][i][k], set):
                        node['cells'][i][k].discard(node['cells'][i][j])
                        if len(node['cells'][i][k]) == 0:
                            return False, node
                # COLUMN
                for k in range(size):  # rows
                    if isinstance(node['cells'][k][j], set):
                        node['cells'][k][j].discard(node['cells'][i][j])
                        if len(node['cells'][k][j]) == 0:
                            return False, node
                # BOX
                r0 = int(size ** 0.5 * int(i / (size ** 0.5)))
                c0 = int(size ** 0.5 * int(j / (size ** 0.5)))
                for r in range(r0, r0 + int(size ** 0.5)):
                    for c in range(c0, c0 + int(size ** 0.5)):
                        if isinstance(node['cells'][r][c], set):
                            node['cells'][r][c].discard(node['cells'][i][j])
                            if len(node['cells'][r][c]) == 0:
                                return False, node
    return True, node


def naked_singles(node):
    size = len(node['cells'])
    for i in range(size):  # rows
        for j in range(size):  # columns
            if isinstance(node['cells'][i][j], set) and len(node['cells'][i][j]) == 1:
                node['cells'][i][j] = node['cells'][i][j].pop()
                print('NAKED SINGLE!')
                print('Row ', i, ' column ', j, ' is ', node['cells'][i][j])
                string = compile_string(node['cells'])
                print_puzzle(string)
                return True, node
    return False, node


def hidden_singles(node):
    size = len(node['cells'])
    for n in range(1, size + 1):  # numbers
        # BOXES
        for i in range(size):
            ids = []
            r0 = int(size ** 0.5 * int(i / (size ** 0.5)))
            c0 = int(size ** 0.5 * int(i % (size ** 0.5)))
            for r in range(r0, r0 + int(size ** 0.5)):
                for c in range(c0, c0 + int(size ** 0.5)):
                    if isinstance(node['cells'][r][c], set):
                        if n in node['cells'][r][c]:
                            ids.append((r, c))
            if len(ids) == 1:
                node['cells'][ids[0][0]][ids[0][1]] = n
                print('HIDDEN SINGLE IN A BOX!')
                print('Row ', ids[0][0], ' column ', ids[0][1], ' is ', n)
                string = compile_string(node['cells'])
                print_puzzle(string)
                return True, node

        # ROWS
        for i in range(size):  # rows
            ids = []
            for j in range(size):  # columns
                if isinstance(node['cells'][i][j], set):
                    if n in node['cells'][i][j]:
                        ids.append(j)
            if len(ids) == 1:
                node['cells'][i][ids[0]] = n
                print('HIDDEN SINGLE IN A ROW!')
                print('Row ', i, ' column ', ids[0], ' is ', n)
                string = compile_string(node['cells'])
                print_puzzle(string)
                return True, node

        # COLUMNS
        for i in range(size):  # columns
            ids = []
            for j in range(size):  # rows
                if isinstance(node['cells'][j][i], set):
                    if n in node['cells'][j][i]:
                        ids.append(j)
            if len(ids) == 1:
                node['cells'][ids[0]][i] = n
                print('HIDDEN SINGLE IN A COLUMN!')
                print('Row ', ids[0], ' column ', i, ' is ', n)
                string = compile_string(node['cells'])
                print_puzzle(string)
                return True, node
    return False, node


def compile_string(cells):
    string = ''
    for i, row in enumerate(cells):
        for j, cell_value in enumerate(row):
            if isinstance(cell_value, set):
                string += str(0)
            else:
                string += str(cell_value)
    return string


def print_puzzle(puzzle):
    size = len(puzzle) ** 0.5
    puzzle = puzzle.replace('0', ' ')
    string = ''
    for i, ch in enumerate(puzzle):
        if i % size == 0 and i != 0:
            string += '\n'
            if i % size ** 1.5 == 0:
                string += '---+---+---\n'
        elif i % size ** 0.5 == 0 and i != 0:
            string += '|'
        string += str(ch)
    string += '\n\n'
    print(string, flush=True)


def check_solution(node):
    size = len(node['cells'])
    for i in range(size):
        row_ids = set()
        col_ids = set()
        box_ids = set()
        for j in range(size):
            # ROWS
            if not isinstance(node['cells'][i][j], int):
                return False
            row_ids.add(node['cells'][i][j])

            # COLUMNS
            if not isinstance(node['cells'][j][i], int):
                return False
            col_ids.add(node['cells'][j][i])

            # BOXES
            r = int(j / (size ** 0.5)) + int(size ** 0.5 * int(i / (size ** 0.5)))
            c = int(j % (size ** 0.5)) + int(size ** 0.5 * int(i % (size ** 0.5)))
            if not isinstance(node['cells'][r][c], int):
                return False
            box_ids.add(node['cells'][r][c])

        if len(row_ids) != 9 or len(col_ids) != 9 or len(box_ids) != 9:
            return False
    return True


def create_dict(puzzle):
    for ch in ["\n", " "]:
        puzzle = puzzle.replace(ch, "")

    size = int(len(puzzle) ** 0.5)

    node = {"puzzle": puzzle,
            "solution": "",
            "cells": []}

    # initiate dict as if puzzle was empty
    for i in range(size):  # iterate over rows
        row = []
        for j in range(size):  # iterate over cells
            row.append(set(range(1, size + 1)))
        node["cells"].append(row)

    # fill inn given values from puzzle
    for i in range(size ** 2):
        value = int(node["puzzle"][i])
        row_idx = int(i / size)
        row_cell_idx = i % size
        if value != 0:
            node["cells"][row_idx][row_cell_idx] = value

    return node


if __name__ == '__main__':
    valid, node = main(puzzle)
