import time

# assuming a list of tuples is being passed through
def mergeSort(list):
    # If the passed list has more than one element divide and conquer
    if len(list) > 1:
        left = list[0: len(list) // 2]
        right = list[len(list) // 2: len(list) + 1]
        # Merge sort the respective halves recursively
        mergeSort(left)
        mergeSort(right)

        merge(list, left, right)


def merge(list, left, right):
    leftCounter = 0
    rightCounter = 0
    listIndex = 0

    # Sort the two separate arrays into one
    while leftCounter < len(left) and rightCounter < len(right):
        if left[leftCounter][1] < right[rightCounter][1]:
            list[listIndex] = left[leftCounter]
            leftCounter += 1
        else:
            list[listIndex] = right[rightCounter]
            rightCounter += 1
        listIndex += 1

    # Collect any remaining elements in the two array structures
    while leftCounter < len(left):
        list[listIndex] = left[leftCounter]
        leftCounter += 1
        listIndex += 1

    while rightCounter < len(right):
        list[listIndex] = right[rightCounter]
        rightCounter += 1
        listIndex += 1


x = [("me", 500), ("matthew", 20), ("andres", 1)]

startTime = time.time()
mergeSort(x)
endTime = time.time()

print("Quicksort took " + str(endTime - startTime) + " seconds to run.")

print(x)