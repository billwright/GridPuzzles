def cross(cols, rows):
    # We want the addresses ordered by rows, meaning all the addresses in the first row
    # before going on to the second row. But, we use the column header first in the address.
    # This addressing mimics spreadsheets
    return [c + r for r in rows for c in cols]


def super_cross(list_of_lists):
    if len(list_of_lists) == 1:
        return list_of_lists[0]
    else:
        crossed_tail_of_list = cross(list_of_lists[-2], list_of_lists[-1])
        reduced_list_of_lists = list_of_lists[0:-2]
        reduced_list_of_lists.append(crossed_tail_of_list)
        return super_cross(reduced_list_of_lists)