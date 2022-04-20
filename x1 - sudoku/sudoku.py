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
    stack = [node]

    nodes_visited = 0
    while stack:
        node = stack.pop()
        nodes_visited += 1
    #   f, node = pruning(node)
    #   if f
    #       child_nodes = choose(node)
    #       if child_nodes
    #           stack.append(child_nodes)
    #       else
    #           node = compile_solution(node)
    #           return True, node

    return False, node


def pruning(node):
    size = len(node['rows'])
    loop2 = True
    while loop2:
        loop2 = False
        for i in range(size):  # row / column / box
            for j in range(size):  # cell
                # ROWS
                if isinstance(node['rows'][i]['values'][j], int):
                    for k in range(size):  # cell
                        if isinstance(node['rows'][i]['values'][k], set):
                            node['rows'][i]['values'][k].remove(node['rows'][i]['values'][j])
                if isinstance(node['rows'][i]['cells'][j], int):
                    for k in range(size):  # cell
                        if isinstance(node['rows'][i]['cells'][k], set):
                            node['rows'][i]['cells'][k].remove(node['rows'][i]['cells'][j])
                # COLUMNS
                if isinstance(node['columns'][i]['values'][j], int):
                    for k in range(size):  # cell
                        if isinstance(node['columns'][i]['values'][k], set):
                            node['columns'][i]['values'][k].remove(node['columns'][i]['values'][j])
                if isinstance(node['columns'][i]['cells'][j], int):
                    for k in range(size):  # cell
                        if isinstance(node['columns'][i]['cells'][k], set):
                            node['columns'][i]['cells'][k].remove(node['columns'][i]['cells'][j])
                # BOXES
                if isinstance(node['boxes'][i]['values'][j], int):
                    for k in range(size):  # cell
                        if isinstance(node['boxes'][i]['values'][k], set):
                            node['boxes'][i]['values'][k].remove(node['boxes'][i]['values'][j])
                if isinstance(node['boxes'][i]['cells'][j], int):
                    for k in range(size):  # cell
                        if isinstance(node['boxes'][i]['cells'][k], set):
                            node['boxes'][i]['cells'][k].remove(node['boxes'][i]['cells'][j])

        # remove values from cells ("values") if value already in row, column or box
        # remove cells from values ("cells") if cell is filled
        # if any len(list) == 1:
        #   change to int (filling in hidden or naked single)
        #   loop2 = True
        #   continue
        # elif any len(list) == 0:
        #   return -1, node

        # check locked candidate
        # if pruned
        #   loop2 = True
        #   continue

        # check
    return 0, node


def create_dict(puzzle):
    for ch in ["\n", " "]:
        puzzle = puzzle.replace(ch, "")

    size = int(len(puzzle) ** 0.5)

    sdk = {"puzzle": puzzle.replace("\n", ""),
           "solution": "",
           "rows": [],
           "columns": [],
           "boxes": []}

    # initiate dict as if puzzle was empty
    for i in range(size):  # iterate over rows, columns, and boxes
        row = {"values": [],  # values that a cell can be
               "cells": []}  # cells that a value can be in
        column = {"values": [],
                  "cells": []}
        box = {"values": [],
               "cells": []}
        for j in range(size):  # iterate over cells, and values
            row["values"].append(set(range(1, size + 1)))
            row["cells"].append(set(range(0, size)))
            column["values"].append(set(range(1, size + 1)))
            column["cells"].append(set(range(0, size)))
            box["values"].append(set(range(1, size + 1)))
            box["cells"].append(set(range(0, size)))
        sdk["rows"].append(row)
        sdk["columns"].append(column)
        sdk["boxes"].append(box)

    # fill inn given values from puzzle
    for i in range(size ** 2):
        value = int(sdk["puzzle"][i])
        row_idx = int(i / size)
        row_cell_idx = i % size
        column_idx = i % size
        column_cell_idx = int(i / size)
        box_idx = (int(i / (size ** 0.5)) % int(size ** 0.5)
                   + int(size ** 0.5) * int(i / (size ** 1.5)))
        box_cell_idx = (i - int(size ** 0.5) * box_idx
                        - (int(size ** 0.5) * (int(size ** 0.5) - 1))
                        * row_idx)
        if value != 0:
            sdk["rows"][row_idx]["values"][row_cell_idx] = value
            sdk["rows"][row_idx]["cells"][value - 1] = row_cell_idx
            sdk["columns"][column_idx]["values"][column_cell_idx] = value
            sdk["columns"][column_idx]["cells"][value - 1] = column_cell_idx
            sdk["boxes"][box_idx]["values"][box_cell_idx] = value
            sdk["boxes"][box_idx]["cells"][value - 1] = box_cell_idx

    return sdk


if __name__ == '__main__':
    f, node = main(puzzle)
    print(node["solution"])
