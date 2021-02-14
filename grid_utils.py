def cross(cols, rows):
    # We want the addresses ordered by rows, meaning all the addresses in the first row
    # before going on to the second row. But, we use the column header first in the address.
    # This addressing mimics spreadsheets
    return [c + r for r in rows for c in cols]


def tuple_cross(list1, list2):
    return [(item1, item2) for item2 in list2 for item1 in list1]


def super_cross(list_of_lists):
    if len(list_of_lists) == 1:
        return list_of_lists[0]
    else:
        crossed_tail_of_list = cross(list_of_lists[-2], list_of_lists[-1])
        reduced_list_of_lists = list_of_lists[0:-2]
        reduced_list_of_lists.append(crossed_tail_of_list)
        return super_cross(reduced_list_of_lists)


def flatten(list_of_lists):
    return [item for sublist in list_of_lists for item in sublist]


def de_dup(list_with_duplicates):
    return list(set(list_with_duplicates))


def flatten_and_de_dup(list_of_lists):
    return de_dup(flatten(list_of_lists))
