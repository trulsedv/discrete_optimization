import numpy as np
from pprint import pprint
from copy import deepcopy
import time
from collections import deque
import cProfile
import pstats


def dynamic_programing(items, item_count, capacity):
    # CREATE TABLE
    # 0 items
    dp_table = np.zeros((capacity + 1, item_count + 1), dtype=int)
    # 1 to N items
    for item in range(item_count):
        weight = items[item].weight
        value = items[item].value
        # 0 to K capacity
        for cap in range(capacity + 1):
            # if capacity cap is smaller than weight of item
            # then choose the solution where items was one less
            # else choose the max of that solution, and
            # the solution where items was one less and
            # capacity was cap minus weight pluss value
            if cap < weight:
                dp_table[cap][item + 1] = dp_table[cap, item]
            else:
                dp_table[cap][item + 1] = max(dp_table[cap][item],
                                              dp_table[cap - weight][item]
                                              + value)

    # TRACE BACK
    value = 0
    taken = np.zeros((item_count,), dtype=int)
    cap = capacity
    for item in range(item_count):
        # check lower right corner and the value to the left
        # if different this item in in the optimal solution
        value_0 = dp_table[cap][item_count - item]
        value_1 = dp_table[cap][item_count - item - 1]
        if value_0 > value_1:
            value += items[item_count - item - 1].value
            taken[item_count - item - 1] = 1
            # remove weight of the item for next test
            cap -= items[item_count - item - 1].weight

    # OUTPUT
    # prepare the solution in the specified output format
    # NOTE str(1) for opimal solution
    output_data = str(value) + ' ' + str(1) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data


def linear_relaxation(items, indices, value, room):
    estimate = value
    density = 0
    for i in range(len(indices), len(items)):
        item = items[i]
    # for item in items:
        # if item.index not in indices:
        if item.weight <= room:
            estimate += item.value
            room -= item.weight
            density = item.density
        else:
            estimate += room / item.weight * item.value
            room = 0  # -= room / item.weight * item.weight
            density = item.density
            break
    return estimate, density


def DFS_iterative(items, item_count, capacity):
    # print(f'\nNEW INPUT\nitem count: {item_count}, capacity: {capacity}',
    #       flush=True)
    # print('Depth First Search, Branch and Bound', flush=True)

    debug = False
    start = time.time()
    start_timer = start

    # profile = cProfile.Profile()
    # profile.enable()

    # SORT ITEMS
    items = sorted(items, key=lambda x: x.weight)
    items = sorted(items, key=lambda x: x.density, reverse=True)
    # print('Items sorted by density', flush=True)
    if debug:
        pprint(items)

    # LINEAR RELAXATION
    estimate, c_density = linear_relaxation(items, [], 0,
                                            capacity)
    # print('Linear Relaxation', flush=True)
    # print(f'estimate: {estimate}, critical density: {c_density}', flush=True)

    # PREPARATION
    stack = deque()
    stack = []
    best_solution = 0
    best_taken = []
    node = {'value': 0, 'room': capacity, 'estimate': estimate,
            'taken': [], 'indices': []}
    stack.append(node)
    nodes_visited = 0

    # ITERATION
    while stack:
        nodes_visited += 1
        node = stack.pop()
        tree_depth = len(node['taken'])
        result = bounding(node, tree_depth, item_count, best_solution)

        if result == 'branch':
            X = [0, 1]
            # if items[tree_depth].density <= c_density:
            #     X = [1, 0]
            for x in X:
                child_node = {'value': node['value'],
                              'room': node['room'],
                              'estimate': node['estimate'],
                              'taken': node['taken'] + [x],
                              'indices': node['indices']
                              + [items[tree_depth].index]}
                child_node = calculate_node(items,
                                            child_node,
                                            tree_depth)
                stack.append(child_node)
        elif result == 'solution':
            if node['value'] > best_solution:
                best_solution = node['value']
                best_taken = node['taken']

        if debug:
            debug_print(node, result, best_solution)

        end_timer = time.time()
        if end_timer - start_timer > 10:
            print(f'still running, elapsed time: {end_timer - start:.2f}'
                  f', nodes visited: {nodes_visited}', flush=True)
            # input('press any button to continue...')
            start_timer = time.time()
        if end_timer - start > 5 * 60:
            print(f'stopped after 5 min')
            break

    # SORT TAKEN AND OUTPUT
    taken = np.zeros((item_count,), dtype=int)
    for idx, item in enumerate(items):
        taken[item.index] = best_taken[idx]
    output_data = str(best_solution) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, taken))

    # profile.disable()
    # ps = pstats.Stats(profile)
    # ps.print_stats()

    end = time.time()
    print(f'value: {best_solution:10d}, '
          f'elapsed time: {end - start:10.4f} s, '
          f'nodes visited: {nodes_visited:10d}\n', flush=True)
    return output_data


def calculate_node(items, node, tree_depth):
    node['room'] -= (node['taken'][tree_depth] * items[tree_depth].weight)
    node['value'] += (node['taken'][tree_depth] * items[tree_depth].value)
    node['estimate'] = linear_relaxation(items,
                                         node['indices'],
                                         node['value'],
                                         node['room'])[0]
    return node


def bounding(node, tree_depth, item_count, best_solution):
    if node['room'] >= 0:
        if tree_depth < item_count:
            if node['estimate'] > best_solution:
                result = 'branch'
            else:
                result = 'bound'
        else:
            result = 'solution'
    else:
        result = 'infeasible'
    return result


def debug_print(node, result, best_solution):
    print(node['taken'])
    if result == 'branch':
        print('value = ' + str(node['value'])
              + ' | room = ' + str(node['room'])
              + ' | estimate = ' + str(node['estimate'])
              + ' | best_solution = '
              + str(best_solution)
              + ' ---> BRANCH\n')
    elif result == 'bound':
        print('value = ' + str(node['value'])
              + ' | room = ' + str(node['room'])
              + ' | estimate = ' + str(node['estimate'])
              + ' | best_solution = '
              + str(best_solution)
              + ' ---> BOUND\n')
    elif result == 'solution':
        print('value = ' + str(node['value'])
              + ' | room = ' + str(node['room'])
              + ' | estimate = ' + str(node['estimate'])
              + ' | best_solution = ' + str(best_solution)
              + ' ---> SOLUTION = '
              + str(node['value'])
              + '\n')
    elif result == 'infeasible':
        print('value = ' + '---'
              + ' | room = ' + str(node['room'])
              + ' | estimate = ' + '---'
              + ' | best_solution = ' + str(best_solution)
              + ' ---> INFEASIBLE\n')


# def density_sort(items, item_count, capacity):
#     taken = np.zeros((item_count,), dtype=int)
#     items_sorted = sorted(items, key=lambda x: x.weight)
#     items_sorted = sorted(items, key=lambda x: x.density, reverse=True)
#     value = 0
#     weight = 0
#     for item in items_sorted:
#         if weight + item.weight <= capacity:
#             value += item.value
#             weight += item.weight
#             taken[item.index] = 1

#     output_data = str(value) + ' ' + str(0) + '\n'
#     output_data += ' '.join(map(str, taken))
#     return output_data

# def depth_first_branch_and_bound(items, item_count, capacity):
#     # estimate = 0
#     # for item in items:
#     #     estimate += item.value
#     items_sorted = sorted(items, key=lambda x: x.weight)
#     items_sorted = sorted(items_sorted, key=lambda x: x.density,
#                           reverse=True)
#     estimate = linear_relaxation(items, 0, 0, capacity)
#     branch_0 = {'taken': [], 'value': 0, 'room': capacity,
#                 'estimate': estimate, 'best_solution': 0}

#     debug = False
#     if debug:
#         pprint(items_sorted)
#         print('value = ' + str(branch_0['value'])
#               + ' | room = ' + str(branch_0['room'])
#               + ' | estimate = ' + str(branch_0['estimate'])
#               + ' | best_solution = ' + str(branch_0['best_solution'])
#               + ' ---> BRANCH')
#     branch = branching(items_sorted, branch_0, debug)

#     value = branch['value']
#     taken = np.zeros((item_count,), dtype=int)
#     for idx, item in enumerate(items_sorted):
#         taken[item.index] = branch['taken'][idx]

#     output_data = str(value) + ' ' + str(0) + '\n'
#     output_data += ' '.join(map(str, taken))
#     return output_data


# def branching(items, branch_0, debug):
#     branches = []
#     branches.append(deepcopy(branch_0))
#     branches.append(deepcopy(branch_0))
#     item_index = len(branch_0['taken'])
#     best_solution = branch_0['best_solution']

#     # iterate over the two branches (choose or not choose next item)
#     for x in [1, 0]:
#         branches[x]['best_solution'] = best_solution
#         branches[x]['taken'].append(x)
#         if debug:
#             print("taken: " + str(branches[x]['taken']))

#         # check if contraint is upheld, if not the branch is infeasible
#         branches[x]['room'] -= x * items[item_index].weight
#         if branches[x]['room'] >= 0:
#             branches[x]['value'] += x * items[item_index].value

#             # branches[x]['estimate'] -= (1 - x) * items[item_index].value
#             branches[x]['estimate'] = linear_relaxation(items,
#                                                         item_index + 1,
#                                                         branches[x]['value'],
#                                                         branches[x]['room'])

#             # check if further branching is possible,
#             # if not this is a solution
#             if item_index + 1 < len(items):

#                 # check if estimate of this branch is better than the best
#                 # solution found, if not bound
#                 if branches[x]['estimate'] > 1.1 * best_solution:
#                     if debug:
#                         print('value = ' + str(branches[x]['value'])
#                               + ' | room = ' + str(branches[x]['room'])
#                               + ' | estimate = '
#                               + str(branches[x]['estimate'])
#                               + ' | best_solution = '
#                               + str(best_solution)
#                               + ' ---> BRANCH')
#                     branches[x] = branching(items, branches[x], debug)
#                 else:
#                     branches[x]['best_solution'] = -1
#                     if debug:
#                         print('value = ' + str(branches[x]['value'])
#                               + ' | room = ' + str(branches[x]['room'])
#                               + ' | estimate = '
#                               + str(branches[x]['estimate'])
#                               + ' | best_solution = '
#                               + str(best_solution)
#                               + ' ---> BOUND')
#             else:
#                 branches[x]['best_solution'] = branches[x]['value']
#                 if debug:
#                     print('value = ' + str(branches[x]['value'])
#                           + ' | room = ' + str(branches[x]['room'])
#                           + ' | estimate = ' + str(branches[x]['estimate'])
#                           + ' | best_solution = ' + str(best_solution)
#                           + ' ---> SOLUTION = '
#                           + str(branches[x]['best_solution']))
#         else:
#             branches[x]['value'] = -1
#             branches[x]['estimate'] = -1
#             branches[x]['best_solution'] = -1
#             if debug:
#                 print('value = ' + str(branches[x]['value'])
#                       + ' | room = ' + str(branches[x]['room'])
#                       + ' | estimate = ' + str(branches[x]['estimate'])
#                       + ' | best_solution = ' + str(best_solution)
#                       + ' ---> INFEASIBLE')
#         if branches[x]['best_solution'] > best_solution:
#             best_solution = branches[x]['best_solution']

#     branch = max(branches, key=lambda x: x['best_solution'])
#     if debug:
#         print('return to ' + str(branch_0['taken'])
#               + ', best solution = ' + str(best_solution))
#         input('press key to continue...')
#     return branch
# def depth_first_branch_and_bound(items, item_count, capacity):
#     estimate = 0
#     for item in items:
#         estimate += item.value

#     taken = -np.ones((item_count,), dtype=int)
#     print(str(0) + " | " + str(capacity) + " | " + str(estimate))
#     taken = branch(items, taken, 0, 0, capacity,
#                    estimate, 0)
#     value = 0
#     for item in items:
#         if taken[item.index] == 1:
#             value += item.value

#     output_data = str(value) + ' ' + str(0) + '\n'
#     output_data += ' '.join(map(str, taken))

#     return output_data

# def bound(items, taken, item, value, room, estimate, best_solution):
#     if taken[item] == 1:
#         room -= items[item].weight
#         if room >= 0:
#             value += items[item].value
#             if item + 1 < len(items):
#                 print(str(value) + " | " + str(room) + " | " + str(estimate))
#                 taken = branch(items, taken, item + 1, value, room,
#                                estimate, best_solution)
#                 print("return")
#             else:
#                 print("found a solution")
#                 print(str(value) + " | " + str(room) + " | " + str(value))

#         else:
#             print("-" + " | " + str(room) + " | " + "-")
#             print("not enough room")
#             return -1
#     else:
#         if item + 1 < len(items):
#             estimate -= items[item].value
#             if estimate > best_solution:
#                 print(str(value) + " | " + str(room) + " | " + str(estimate))
#                 taken = branch(items, taken, item + 1, value, room,
#                                estimate, best_solution)
#                 print("return")
#             else:
#                 print(best_solution)
#                 print(str(value) + " | " + str(room) + " | " + str(estimate))
#                 print("estimate lower than best solution")
#                 return -1
#         else:
#             print("found a solution")
#             print(str(value) + " | " + str(room) + " | " + str(value))

#     return value

# def branch(items, taken, item, value, room, estimate, best_solution):
#     for choice in [1, 0]:
#         taken[item] = choice
#         print(items[item])
#         print(taken)
#         solution = bound(items, taken, item, value,
#                          room, estimate, best_solution)
#         if solution > best_solution:
#             best_solution = solution
#             best_choice = choice
#             print("new best = " + str(solution) + " (" + str(item) + ")")

#     taken[item] = best_choice
#     return taken

# def calc_value(items, taken):
#     value = 0
#     for item in items:
#         if taken[item.index] == 1:
#             value += item.value

#     return value

# def calc_room(items, taken, capacity):
#     weight = 0
#     for item in items:
#         if taken[item.index] == 1:
#             weight += item.weight
#     room = capacity - weight

#     return room

# def calc_estimate(items, taken):
#     estimate = 0
#     for item in items:
#         if taken[item.index] == 1:
#             estimate += item.value
#         if taken[item.index] == -1:
#             estimate += item.value

#     return estimate
