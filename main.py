import pygame
import random
import colors

# define width/height of window
# extra 25 pixels of height for text
WIDTH, HEIGHT = 800, 600 + 25
# width of each col
COL_WIDTH = 4
# the height of a col is determined by its value * MULT
MULT = 3.75
# delay
SLP = 4
# which sort is running
SORT = ''
# comparisons
COMPS = 0
# array accesses
ARRACC = 0
# swaps
SWAPS = 0
# elements to sort
ELEMENTS = 160
# determine wether the algorithm is paused
PAUSED = False

# create and randomize a list of numbers 1 - ELEMENTS
arr = list(range(1, ELEMENTS + 1))
random.shuffle(arr)

# set up the window
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption('Sorting viz')
screen.fill(colors.WHITE)

# define the text ot display before formatting
text = '{} Sort - {} comparisons, {} array accesses, {} swaps, {} ms delay, {} elements'
# get the font
font = pygame.font.SysFont('consolas', 15)

# function to draw a col
def draw_col(height, width, col, color):
    pygame.draw.rect(screen, color, (col * (width + 1), HEIGHT - int(height), width, HEIGHT - 1))

# main draw function
# spec(ial)s are different colored cols
def draw(*specs):
    # empty screen
    screen.fill(colors.BLACK)
    # display text
    screen.blit(font.render(text.format(SORT, COMPS, ARRACC, SWAPS, SLP, ELEMENTS), True, colors.WHITE), (5, 5))
    # iterate over each col
    for i in range(len(arr)):
        # if the column is given as an arg it is drawn in its color
        for j in specs:
            if j[0] == i:
                draw_col(arr[i] * MULT, COL_WIDTH, i, j[1])
                break
        # if the col is not special then draw it white
        else:
            draw_col(arr[i] * MULT, COL_WIDTH, i, colors.WHITE)
    # update the display
    pygame.display.update()

# function to handle input and pausing/resuming
def inp():
    # get the global PAUSED var
    global PAUSED
    # check every input
    for event in pygame.event.get():
        # quit if window is closed
        if event.type == pygame.QUIT:
            quit()
        # if a key is pressed
        elif event.type == pygame.KEYDOWN:
            # quit if 'q' is pressed
            if chr(event.key) == 'q':
                quit()
            # pause the algorithm if space is pressed
            elif chr(event.key) == ' ':
                # pause if running / resume if paused
                PAUSED = not PAUSED
                while PAUSED: inp()

#############################################
#####           Bubble Sort             #####
#############################################

# bubble sort algorithm
def bubbleSort():
    # get global vars
    global SORT, SWAPS, COMPS, ARRACC
    # set the sort algorithm name
    SORT = 'Bubble'
    # actual algorithm https://en.wikipedia.org/wiki/Bubble_sort
    n = len(arr)
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                SWAPS += 1
                ARRACC += 4
            ARRACC += 2
            COMPS += 1
            # handle input
            inp()
            # wait a delay
            pygame.time.wait(SLP)
            # draw the array with the col getting sorted in red
            draw([j + 1, colors.RED])


#############################################
#####           Selection Sort          #####
#############################################

# selection sort algorithm
def selectSort():
    # get global vars
    global SORT, SWAPS, COMPS, ARRACC
    # set sort name
    SORT = 'Selection'
    # actual algorithm https://en.wikipedia.org/wiki/Selection_sort
    for i in range(len(arr)):
        min_idx = i
        for j in range(i + 1, len(arr)):
            if arr[min_idx] > arr[j]:
                min_idx = j
            COMPS += 1; ARRACC += 2
            # handle input
            inp()
            # wait delay
            pygame.time.wait(SLP)
            # draw array with the current col in red and smallest col as green
            draw([j, colors.RED], [min_idx, colors.GREEN])
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        ARRACC += 4; SWAPS += 1


#############################################
#####           Insertion Sort          #####
#############################################

# insertion sort algorithm
def insertionSort():
    # get global vars
    global SORT, SWAPS, COMPS, ARRACC
    # set sort name
    SORT = 'Insertion'
    # actual algorithm https://en.wikipedia.org/wiki/Insertion_sort
    for i in range(1, len(arr)):
        key = arr[i]
        ARRACC += 2; SWAPS += 1
        j = i - 1
        while j >= 0 and key < arr[j]:
            COMPS += 2; ARRACC += 3
            arr[j + 1] = arr[j]
            j -= 1
            # handle input
            inp()
            # wait delay
            pygame.time.wait(SLP)
            # draw array with current col in red if not outside array, col which
            # col which is being checked in green
            draw([j, colors.GREEN], [i + 1, colors.RED] if i < len(arr) else None)
        arr[j + 1] = key


#############################################
#####           Quick Sort              #####
#############################################

# quick sort algorithm
def quickSort(start, end):
    # set sort name
    global SORT
    SORT = 'Quick'
    # check end recursion case
    if start >= end: return
    # get pivot index
    # pivot is always end element
    index = partition(arr, start, end)

    # quicksort first and second part of array
    quickSort(start, index - 1)
    quickSort(index + 1, end)

# helper function for quick sort
def partition(arr, start, end):
    # get global vars
    global SORT, SWAPS, COMPS, ARRACC
    # actual algorithm https://en.wikipedia.org/wiki/Quicksort
    pivotIndex = start
    pivotValue = arr[end]
    for i in range(start, end):
        if arr[i] < pivotValue:
            arr[i], arr[pivotIndex] = arr[pivotIndex], arr[i]
            pivotIndex += 1
            SWAPS += 1; ARRACC += 4; COMPS += 1
        ARRACC += 1
        # handle input
        inp()
        # wait delay
        pygame.time.wait(SLP)
        # draw array with red cols surrounding the sub-array which is
        # being sorted and green pivot index
        draw([start, colors.RED], [end, colors.RED], [pivotIndex, colors.GREEN])
    arr[pivotIndex], arr[end] = arr[end], arr[pivotIndex]
    SWAPS += 1; ARRACC += 5
    return pivotIndex


#############################################
#####           Merge Sort              #####
#############################################

# merge sort algorithm
def mergeSort(start, end):
    # set sort name
    global SORT
    SORT = 'Merge'
    # check recursion end case
    if not start < end: return
    # find middle of current array
    mid = (start + end) // 2
    # sort first half of current array
    mergeSort(start, mid)
    # sort second half of current array
    mergeSort(mid + 1, end)
    # merge the 2 halves
    merge(start, mid, end)

# helper function for merge sort algorithm
def merge(start, mid, end):
    # get global vars
    global SORT, SWAPS, COMPS, ARRACC
    # actual sorting algorithm https://en.wikipedia.org/wiki/Merge_sort
    temp = [0] * (end - start + 1)
    i, j, k = start, mid + 1, 0
    while i <= mid and j <= end:
        COMPS += 3; ARRACC += 1
        if arr[i] <= arr[j]:
            temp[k] = arr[i]
            k += 1; i += 1
            ARRACC += 1
        else:
            temp[k] = arr[j]
            k += 1; j += 1
            ARRACC += 1
    while i <= mid:
        COMPS += 1; ARRACC += 1
        temp[k] = arr[i]
        k += 1; i += 1
    while j <= end:
        COMPS += 1; ARRACC += 1
        temp[k] = arr[j]
        k += 1; j += 1
    for i in range(start, end + 1):
        arr[i] = temp[i - start]
        ARRACC += 1
        # handle input
        inp()
        # wait delay
        pygame.time.wait(SLP)
        # draw array with red cols surrounding the sub-array which is
        # being sorted and green pivot index
        draw([i, colors.GREEN], [start, colors.RED], [end, colors.RED])

# sort array
quickSort(0, ELEMENTS - 1)
# draw finished state of array
draw()
# infinite loop to keep program responsive
while True: inp()
