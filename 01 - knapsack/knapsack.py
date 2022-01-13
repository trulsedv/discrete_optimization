import numpy as np
from pprint import pprint
from copy import deepcopy
import time


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


def linear_relaxation(items_sorted, indices, value, room):
    estimate = value
    for item in items_sorted:
        if item.index not in indices:
            if item.weight <= room:
                estimate += item.value
                room -= item.weight
            else:
                estimate += room / item.weight * item.value
                room = 0  # -= room / item.weight * item.weight
                break
    return estimate


def DFS_iterative(items, item_count, capacity):
    debug = False

    print('depth_first_branch_and_bound', flush=True)
    start = time.time()
    start_timer = start

    items_sorted = sorted(items, key=lambda x: x.weight)
    items_sorted = sorted(items_sorted, key=lambda x: x.density, reverse=True)
    estimate = linear_relaxation(items_sorted, [], 0, capacity)
    print('linear_relaxation', flush=True)

    items = items_sorted
    print('items_sorted_by_density', flush=True)

    best_solution = 0
    best_taken = []

    vertex = {'value': 0, 'room': capacity, 'estimate': estimate,
              'taken': [], 'indices': []}
    if debug:
        pprint(items)

    stack = []
    stack.append(vertex)
    while stack:
        vertex = stack.pop()

        item_index = len(vertex['taken']) - 1
        end_timer = time.time()

        if end_timer - start > 36000:
            break
        elif end_timer - start_timer > 10:
            print('still running, elapsed time: '
                  + str(end_timer - start), flush=True)
            start_timer = time.time()

        if debug:
            print(vertex['taken'])

        if item_index >= 0:
            vertex['room'] -= (vertex['taken'][item_index]
                               * items[item_index].weight)

        if vertex['room'] >= 0:
            if item_index >= 0:
                vertex['value'] += (vertex['taken'][item_index]
                                    * items[item_index].value)
            if item_index >= 0:
                vertex['estimate'] = linear_relaxation(items_sorted,
                                                       vertex['indices'],
                                                       vertex['value'],
                                                       vertex['room'])

            if item_index + 1 < item_count:
                if vertex['estimate'] > (1 + 1e-3) * best_solution:
                    if debug:
                        print('value = ' + str(vertex['value'])
                              + ' | room = ' + str(vertex['room'])
                              + ' | estimate = ' + str(vertex['estimate'])
                              + ' | best_solution = '
                              + str(best_solution)
                              + ' ---> BRANCH')
                    for x in range(2):
                        w = deepcopy(vertex)
                        w['taken'].append(x)
                        w['indices'].append(items[item_index + 1].index)
                        stack.append(w)
                else:
                    if debug:
                        print('value = ' + str(vertex['value'])
                              + ' | room = ' + str(vertex['room'])
                              + ' | estimate = ' + str(vertex['estimate'])
                              + ' | best_solution = '
                              + str(best_solution)
                              + ' ---> BOUND')
            else:
                if vertex['value'] > best_solution:
                    best_solution = vertex['value']
                    best_taken = vertex['taken']
                if debug:
                    print('value = ' + str(vertex['value'])
                          + ' | room = ' + str(vertex['room'])
                          + ' | estimate = ' + str(vertex['estimate'])
                          + ' | best_solution = ' + str(best_solution)
                          + ' ---> SOLUTION = '
                          + str(vertex['value']))
        else:
            if debug:
                print('value = ' + '---'
                      + ' | room = ' + str(vertex['room'])
                      + ' | estimate = ' + '---'
                      + ' | best_solution = ' + str(best_solution)
                      + ' ---> INFEASIBLE')

    end = time.time()
    print('elapsed time: ' + str(end - start))

    output_data = str(best_solution) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, best_taken))
    return output_data

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
