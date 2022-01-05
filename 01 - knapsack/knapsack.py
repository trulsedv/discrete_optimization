import numpy as np


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

# def least_discrepancy_search(items, item_count, capacity):
#     density_vector = np.zeros((item_count, 2))
#     for item in items:
        
