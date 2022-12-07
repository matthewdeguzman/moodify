import timeit

def quickSort(list, low, high):
    if (low < high):
        pivot = partition(list, low, high)
        quickSort(list, low, pivot - 1)
        quickSort(list, pivot + 1, high)


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


x = [("me", 500), ("matthew", 20), ("andres", 1), ("john", 325), ("hannahmontana", 3284)]

start = timeit.default_timer()
quickSort(x, 0, len(x) - 1)
end = timeit.default_timer()

print("Quicksort took " + str((end - start) * 1000) + " milliseconds to run.")

print(x)