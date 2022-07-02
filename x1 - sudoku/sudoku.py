def main(puzzle):
    node = create_dict(puzzle)
    print_puzzle(node['puzzle'])
    stack = [node]
    nodes_visited = 0
    while stack:
        node = stack.pop()
        nodes_visited += 1
        if node['guess']:
            print('\n__________________________________________________')
            print('Guessing row ', node['guess'][0] + 1, ' column ', node['guess'][1] + 1, ' is ', node['guess'][2])
            # pretty(node)
            string = compile_string(node['cells'])
            print_puzzle(string)
        valid, node = pruning(node)
        if valid:
            child_nodes = choose_children(node)
            # child_nodes = []
            if child_nodes:
                print('\n==================================================')
                print('The following guesses are added to the stack:')
                # child_nodes.reverse()
                for child in child_nodes:
                    print(child['guess'])
                    stack.append(child)
            else:
                valid = check_solution(node)
                if valid:
                    string = compile_string(node['cells'])
                    node['solution'] = string
                    print('THE SOLUTION!')
                    print('Nodes visited: ', nodes_visited)
                    print_puzzle(node['solution'])
                    return valid, node
        else:
            print('Not valid!')
            print('¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤')
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

        new = input('Search for new?')
        if new == 'q':
            return False, node

        found, node = hidden_singles(node)  # n as input
        if found is True:
            continue

        found, node = naked_singles(node)
        if found is True:
            continue

        found, node = pointing_tuple(node)
        if found is True:
            continue

        found, node = locked_candidate(node)
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
                            print('Row ', i + 1, ' column ', k + 1, ' has no possible values!')
                            return False, node
                # COLUMN
                for k in range(size):  # rows
                    if isinstance(node['cells'][k][j], set):
                        node['cells'][k][j].discard(node['cells'][i][j])
                        if len(node['cells'][k][j]) == 0:
                            print('Row ', k + 1, ' column ', j + 1, ' has no possible values!')
                            return False, node
                # BOX
                r0 = int(size ** 0.5 * int(i / (size ** 0.5)))
                c0 = int(size ** 0.5 * int(j / (size ** 0.5)))
                for r in range(r0, r0 + int(size ** 0.5)):
                    for c in range(c0, c0 + int(size ** 0.5)):
                        if isinstance(node['cells'][r][c], set):
                            node['cells'][r][c].discard(node['cells'][i][j])
                            if len(node['cells'][r][c]) == 0:
                                print('Row ', r + 1, ' column ', c + 1, ' has no possible values!')
                                return False, node
    return True, node


def naked_singles(node):
    size = len(node['cells'])
    for i in range(size):  # rows
        for j in range(size):  # columns
            if isinstance(node['cells'][i][j], set) and len(node['cells'][i][j]) == 1:
                node['cells'][i][j] = node['cells'][i][j].pop()
                print('\nNAKED SINGLE!')
                print('Row ', i + 1, ' column ', j + 1, ' is ', node['cells'][i][j])
                string = compile_string(node['cells'])
                print_puzzle(string)
                return True, node
    return False, node


def hidden_singles(node):  # n as input
    size = len(node['cells'])
    for n in range(1, size + 1):  # values
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
                print('\nHIDDEN SINGLE IN A BOX!')
                print('In box ', i + 1, ', ', n, 'can only be in row ', ids[0][0] + 1, ' column ', ids[0][1] + 1)
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
                print('\nHIDDEN SINGLE IN A ROW!')
                print('In row ', i + 1, ', ', n, ' can only be in column ', ids[0] + 1)
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
                print('\nHIDDEN SINGLE IN A COLUMN!')
                print('In column ', i + 1, ', ', n, ' can only be in row ', ids[0] + 1)
                string = compile_string(node['cells'])
                print_puzzle(string)
                return True, node
    return False, node


def locked_candidate(node):
    size = len(node['cells'])
    for n in range(1, size + 1):  # values
        # ROWS
        for i in range(size):
            check = set()
            for j in range(size):  # cells
                if isinstance(node['cells'][i][j], set):
                    if n in node['cells'][i][j]:
                        box = int(size ** 0.5 * int(i / size ** 0.5) + int(j / size ** 0.5))
                        check.add(box)
            if len(check) == 1:
                box = check.pop()
                r0 = int(size ** 0.5 * int(box / size ** 0.5))
                c0 = int(size ** 0.5 * (box % size ** 0.5))
                removed = False
                for row in range(r0, r0 + int(size ** 0.5)):
                    if row == i:
                        continue
                    for col in range(c0, c0 + int(size ** 0.5)):
                        if isinstance(node['cells'][row][col], set):
                            if n in node['cells'][row][col]:
                                if removed is False:
                                    removed = True
                                    print('\nLOCKED CANDIDATE IN A ROW!')
                                    print('Row ', i + 1, ' can only have ', n, ' in box ', box + 1)
                                    print(n, ' is removed as a possibility from:')
                                node['cells'][row][col].discard(n)
                                print('Row ', row + 1, 'column ', col + 1)
                if removed is True:
                    return True, node
        # COLUMNS
        for i in range(size):
            check = set()
            for j in range(size):  # cells
                if isinstance(node['cells'][j][i], set):
                    if n in node['cells'][j][i]:
                        box = int(size ** 0.5 * int(j / size ** 0.5) + int(i / size ** 0.5))
                        check.add(box)
            if len(check) == 1:
                box = check.pop()
                r0 = int(size ** 0.5 * int(box / size ** 0.5))
                c0 = int(size ** 0.5 * (box % size ** 0.5))
                removed = False
                for col in range(c0, c0 + int(size ** 0.5)):
                    if col == i:
                        continue
                    for row in range(r0, r0 + int(size ** 0.5)):
                        if isinstance(node['cells'][row][col], set):
                            if n in node['cells'][row][col]:
                                if removed is False:
                                    removed = True
                                    print('\nLOCKED CANDIDATE IN A COLUMN!')
                                    print('Column ', i + 1, ' can only have ', n, ' in box ', box + 1)
                                    print(n, ' is removed as a possibility from:')
                                node['cells'][row][col].discard(n)
                                print('Row ', row + 1, 'column ', col + 1)
                if removed is True:
                    return True, node
    return False, node


def pointing_tuple(node):
    size = len(node['cells'])
    for n in range(1, size + 1):  # values
        for box in range(size):
            r0 = int(size ** 0.5 * int(box / size ** 0.5))
            c0 = int(size ** 0.5 * (box % size ** 0.5))
            check_row = set()
            check_col = set()
            for row in range(r0, r0 + int(size ** 0.5)):
                for col in range(c0, c0 + int(size ** 0.5)):
                    if isinstance(node['cells'][row][col], set):
                        if n in node['cells'][row][col]:
                            check_row.add(row)
                            check_col.add(col)
            # ROWS
            if len(check_row) == 1:
                row = check_row.pop()
                removed = False
                for col in range(size):
                    if col >= c0 and col < c0 + size ** 0.5:
                        continue
                    if isinstance(node['cells'][row][col], set):
                        if n in node['cells'][row][col]:
                            if removed is False:
                                removed = True
                                print('\nPOINTING TUPLE IN A ROW!')
                                print('Box ', box + 1, ' can only have ', n, ' in row ', row + 1)
                                print(n, ' is removed as a possibility from:')
                            node['cells'][row][col].discard(n)
                            print('Row ', row + 1, 'column ', col + 1)
                if removed is True:
                    return True, node
            # COLUMNS
            if len(check_col) == 1:
                col = check_col.pop()
                removed = False
                for row in range(size):
                    if row >= r0 and row < r0 + size ** 0.5:
                        continue
                    if isinstance(node['cells'][row][col], set):
                        if n in node['cells'][row][col]:
                            if removed is False:
                                removed = True
                                print('\nPOINTING TUPLE IN A COLUMN!')
                                print('Box ', box + 1, ' can only have ', n, ' in column ', col + 1)
                                print(n, ' is removed as a possibility from:')
                            node['cells'][row][col].discard(n)
                            print('Row ', row + 1, 'column ', col + 1)
                if removed is True:
                    return True, node
    return False, node


def hidden_pairs(node):
    size = len(node['cells'])
    for i in range(size):
        # BOX
        check_box = []
        for n in range(1, size + 1):  # values
            check_box.append(set())
        r0 = int(size ** 0.5 * int(box / size ** 0.5))
        c0 = int(size ** 0.5 * (box % size ** 0.5))
        for row in range(r0, r0 + int(size ** 0.5)):
            for col in range(c0, c0 + int(size ** 0.5)):
                for n in range(1, size + 1):  # values
                    if isinstance(node['cells'][row][col], set):
                        if n in node['cells'][row][col]:
                            check_box[n].add((row, col))
        for n in range(1, size + 1):
            if len(check_box[n]) == 2:
                for m in range(n + 1, size + 1):
                    if check_box[n] == check_box[m]:
                        
                        return True, node



    return False, node


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


def choose_children(node):
    child_nodes = []
    for i, row in enumerate(node['cells']):
        for j, cell in enumerate(row):
            if isinstance(cell, set):
                for value in cell:
                    child = deepcopy_node(node)
                    child['cells'][i][j] = value
                    child['guess'] = (i, j, value)
                    child_nodes.append(child)
                return child_nodes
    return child_nodes


def deepcopy_node(node):
    deepcopy = {'puzzle': node['puzzle'],
                'solution': node['solution'],
                'cells': [],
                'guess': node['guess']}
    for row in node['cells']:
        row_copy = []
        for cell in row:
            if isinstance(cell, set):
                row_copy.append(cell.copy())
            else:
                row_copy.append(cell)
        deepcopy['cells'].append(row_copy)
    return deepcopy


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
    string += '\n'
    print(string, flush=True)


def pretty(node):
    print('puzzle:\t', node['puzzle'])
    print('solution:\t', node['solution'])
    print('guess:\t', node['guess'])
    print('cells:')
    for row in node['cells']:
        print(row)
    print('')


def create_dict(puzzle):
    for ch in ["\n", " "]:
        puzzle = puzzle.replace(ch, "")

    size = int(len(puzzle) ** 0.5)

    node = {"puzzle": puzzle,
            "solution": "",
            'guess': '',
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


puzzle = """070 000 043
            040 009 610
            800 634 900

            094 052 000
            358 460 020
            000 800 530

            080 070 091
            902 100 005
            007 040 802"""

if __name__ == '__main__':
    valid, node = main(puzzle)
