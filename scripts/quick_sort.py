# algorithm for quicksort
def quick_sort(list, low, high):
    if (low < high):
        pivot = partition(list, low, high)
        quick_sort(list, low, pivot - 1)
        quick_sort(list, pivot + 1, high)


def partition(list, low, high):
    pivot = list[low][1]
    up = low
    down = high

    while up < down:
        while up < high:
            if list[up][1] > pivot:
                break
            up += 1
        while down > low:
            if list[down][1] < pivot:
                break
            down -= 1
        if up < down:
            list[up], list[down] = list[down], list[up]
    list[low], list[down] = list[down], list[low]
    return down