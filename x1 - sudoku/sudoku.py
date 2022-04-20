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
    size = len(node['array'])
    loop2 = True
    while loop2:
        loop2 = False
        for i in range(size):  # rows
            for j in range(size):  # columns
                if isinstance(node['array'][i][j], int):
                    # ROW
                    for k in range(size):  # columns
                        if isinstance(node['array'][i][k], set):
                            node['array'][i][k].remove(node['array'][i][j])
                    # COLUMN
                    for k in range(size): # rows
                        if isinstance(node['array'][k][j], set):
                            node['array'][k][j].remove(node['array'][i][j])
                    # BOX
                    for k in range(size): # box cell indices
                        




                # if isinstance(node['rows'][i]['cells'][j], int):
                #     for k in range(size):  # cell
                #         if isinstance(node['rows'][i]['cells'][k], set):
                #             node['rows'][i]['cells'][k].remove(node['rows'][i]['cells'][j])
                # if isinstance(node['rows'][i]['values'][j], int):
                #     for k in range(size):  # cell
                #         if isinstance(node['rows'][i]['values'][k], set):
                #             node['rows'][i]['values'][k].remove(node['rows'][i]['values'][j])

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

    sdk = {"puzzle": puzzle,
           "solution": "",
           "array": []}

    # initiate dict as if puzzle was empty
    for i in range(size):  # iterate over rows
        row = []
        # row = {'cells': [],
        #        'values': []}
        for j in range(size):  # iterate over cells
            row.append(set(range(1, size + 1)))
            # row['cells'].append(set(range(1, size + 1)))
            # row['values'].append(set(range(0, size)))
        sdk["array"].append(row)

    # fill inn given values from puzzle
    for i in range(size ** 2):
        value = int(sdk["puzzle"][i])
        row_idx = int(i / size)
        row_cell_idx = i % size
        if value != 0:
            sdk["array"][row_idx][row_cell_idx] = value
            # sdk["rows"][row_idx]['cells'][row_cell_idx] = value
            # sdk["rows"][row_idx]['values'][value - 1] = row_cell_idx

    return sdk


if __name__ == '__main__':
    f, node = main(puzzle)
    print(node["solution"])
