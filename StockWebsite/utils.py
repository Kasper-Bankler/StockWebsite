

def partition(array, low, high, sort_by, descending):

    # Choose the rightmost element as pivot
    pivot = array[high][sort_by]
    # Pointer for greater element
    i = low - 1
    # Traverse through all elements
    # compare each element with pivot
    for j in range(low, high):
        if descending:
            if array[j][sort_by] >= pivot:
                # If element greater than pivot is found
                # swap it with the smaller element pointed by i
                i = i + 1
                # Swapping element at i with element at j
                (array[i], array[j]) = (array[j], array[i])
        else:
            if array[j][sort_by] <= pivot:
                # If element smaller than pivot is found
                # swap it with the greater element pointed by i
                i = i + 1
                # Swapping element at i with element at j
                (array[i], array[j]) = (array[j], array[i])
    # Swap the pivot element with
    # the greater element specified by i
    (array[i + 1], array[high]) = (array[high], array[i + 1])
    # Return the position from where partition is done
    return i + 1
 

def quicksort(array, low, high, sort_by, descending=False): #Inspireret af geeksforgeeks https://www.geeksforgeeks.org/quick-sort/
    if low < high:
        # Find pivot element such that
        # element smaller than pivot are on the left
        # element greater than pivot are on the right
        pi = partition(array, low, high, sort_by, descending)
        # Recursive call on the left of pivot
        quicksort(array, low, pi - 1, sort_by, descending)
        # Recursive call on the right of pivot
        quicksort(array, pi + 1, high, sort_by, descending)
        
    return array