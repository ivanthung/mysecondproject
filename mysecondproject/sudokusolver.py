import copy
import sys
sys.setrecursionlimit(10**6)

potential_grid = [
    ['x','x','x', 'x','x','x', 'x','x','x'],
    ['x','x','x', 'x','x','x', 'x','x','x'],
    ['x','x','x', 'x','x','x', 'x','x','x'],
    ['x','x','x', 'x','x','x', 'x','x','x'],
    ['x','x','x', 'x','x','x', 'x','x','x'],
    ['x','x','x', 'x','x','x', 'x','x','x'],
    ['x','x','x', 'x','x','x', 'x','x','x'],
    ['x','x','x', 'x','x','x', 'x','x','x'],
    ['x','x','x', 'x','x','x', 'x','x','x']
]

EASY_GRID = [
    [0,7,0,  0,2,0,  0,4,6],
    [0,6,0,  0,0,0,  8,9,0],
    [2,0,0,  8,0,0,  7,1,5],

    [0,8,4,  0,9,7,  0,0,0],
    [7,1,0,  0,0,0,  0,5,9],
    [0,0,0,  1,3,0,  4,8,0],

    [6,9,7,  0,0,2,  0,0,8],
    [0,5,8,  0,0,0,  0,6,0],
    [4,3,0,  0,8,0,  0,7,0]
]


def progress(percent=0, width=40):
    left = width * percent // 100
    right = width - left

    tags = "#" * left
    spaces = " " * right
    percents = f"{percent:.0f}%"

    print("\r[", tags, spaces, "]", percents, sep="", end="")
    print("\n")

def good_shape(grid):
    if len(grid) != 9:
        return False
    if type(grid) is not list:
        return False
    return True

def sudoku_validator(grid):

    # Function that checks if rows are valid.
    def numbercheck(tocheck):
        ''' Checks if all numbers are in the list'''
        test_list = [1,2,3,4,5,6,7,8,9]
        return all(t in rows for rows in tocheck for t in test_list)

    # Swithing columns and rows using zip(*) and map
    columns = list(map( list, zip(*grid)))

    #transforming blocks in quadrants with a double loop
    blocks = []
    slicer = list(range(0,10,3))
    for range1 in range(0,3):
        for range2 in range(0,3):
            block = list(
                g[r3] for r3 in range(slicer[range2], slicer[range2+1])
                for g in grid[slicer[range1] : slicer[range1+1]]
                )
            blocks.append(block)

    return numbercheck(grid) and numbercheck(columns) and numbercheck(blocks)

def get_missing_value(a_list):
    """
    Check missing values in the given row
    """
    test_list = [1,2,3,4,5,6,7,8,9]
    return [t for t in test_list if t not in a_list]

def get_clmn(coord, grid):
    return [grid[i][coord[1]] for i in range(9)]

def get_qdr(coord, grid):
    block = []
    qdr = [int(coord[0]/3), int(coord[1]/3)]
    for j in range(qdr[0]*3,qdr[0]*3+3):
        for k in range(qdr[1]*3,qdr[1]*3+3):
            block.append(grid[j][k])
    return block

def get_row(coord, grid):
    return grid[coord[0]]

def potential_values(coord, grid):
    column = get_clmn(coord, grid)
    quadrant = get_qdr(coord, grid)
    row = get_row(coord, grid)

    column_missing = get_missing_value(column)
    qdr_missing = get_missing_value(quadrant)
    row_missing = get_missing_value(row)

    potential = find_duplicates(column_missing, qdr_missing, row_missing)

    return potential if potential else [0]

def find_duplicates(list1, list2, list3):
    duplicates = []
    for l1 in list1:
        for l2 in list2:
            for l3 in list3:
                if l1 == l2 == l3:
                    duplicates.append(l3)
    return duplicates

def find_all_empty(grid):
    """Returns all empty instances. Might not be necessary"""
    empty_coord = []
    for i in range(0,9):
        for j in range(0,9):
            if not grid[i][j]:
                empty_coord.append([i,j])
    return empty_coord

def reset_cell(coord, grid):
    grid[coord[0]][coord[1]] = 0

def print_grid(grid):
    """
    Print our grid on a new line
    """
    for g in (grid):
         print (g)
    print("......")

def set_item(coord: list, number, grid: list):
    """ Set coord at a value"""
    grid[coord[0]][coord[1]] = number
    return grid

def get_or_set_pv(coord, grid):
    """
    Tests if there are already potential values calculated.
    A. If this is not the case, return the first item, and add the rest to the potential values.
    B. If this is the case, return the first item of that list and remove it from the grid.
    C. If this is the case and there are no values left, return 0.
    """
    x = coord[0]
    y = coord[1]

    if potential_grid[x][y] == 'x':
        newpv = potential_values(coord, grid)
        chosen_value = newpv.pop()
        set_item(coord, newpv, potential_grid)
        return chosen_value

    elif potential_grid[x][y] == [] or potential_grid[x][y] == [0]:
        return [0]

    return potential_grid[x][y].pop()

def reset_pv(coord, grid):
    potential_grid[coord[0]][coord[1]] = 'x'

def forward_search(travel_path, grid, tracker=0, loop_counter=0):
        """
        Recursive function that continues while potential values are still possible
        """
        if tracker > len(travel_path)-1 or loop_counter > 15000:
            return loop_counter

        location = travel_path[tracker]
        pv = get_or_set_pv(location, grid)

        if pv == [0] or pv == 0:
            # print(f"backgtracking... to {location}")
            reset_pv(location, grid)
            reset_cell(location, grid)

            tracker = tracker - 1
            assert tracker >= 0, 'tracker shouldnt be smaller than 1'

            loop_counter +=1
            return forward_search(travel_path, grid, tracker, loop_counter)

        assert pv != [0], 'pv should not be [0] here'
        #print_grid(grid)
        #print_grid(potential_grid)

        set_item(location, pv, grid)
        loop_counter +=1
        tracker += 1
        return forward_search(travel_path, grid, tracker, loop_counter)

def find_optimal_travel_path(travel_path: list, grid: list) -> list:
    """ returns an ordered list of coordinates with the lowest amount of potential values"""
    travel_path_list = []
    for t in travel_path:
        travel_path_list.append([t, len(potential_values(t, grid))])

    travel_path_list.sort(key = lambda x: x[1])
    return [l[0] for l in travel_path_list]

def reverse_travel_path(travel_path):
    reversed_travel_path = []
    for t in travel_path:
        reversed_travel_path.insert(0, t)
    return reversed_travel_path

def percentage_solved(grid, original_grid):
    to_find = len(find_all_empty(original_grid))
    left = len(find_all_empty(grid))
    return int(((to_find-left) / to_find) *100)

def sudoku_solver(original_grid):
    grid = copy.deepcopy(original_grid)

    if not good_shape(grid):
        return "invalid grid"
    # this is the start of the search. May be optimized to start with the coordinate with the lowest amt. of
    # possible values in the future

    travel_path = find_all_empty(grid)

    print(travel_path)
    #trying some optimization options:
    travel_path = find_optimal_travel_path(travel_path, grid)
    #travel_path = reverse_travel_path(travel_path)

    #0. Original (starting with rows) finishes in 500 iterations
    #1. Reversal of path inceases iterations to 5000 (10x)
    #2. Sorting from starting in cells with low possible options increases iterations to 10000 (20x)
    #3. Sorting from starting in cells with high possible options doesn't finish before 15000 iterations.
    #4. A grid with zero's finsihes after 7000 iterations.
    #5. With the easy grid, starting in cells with low options iterations is only 100, but reversed it doesn't evaluate.

    # print("....")
    # print(travel_path)

    loop_counter = forward_search(travel_path, grid)

    print("The original grid is:")
    print_grid(original_grid)
    print(f"Programme has gone through {loop_counter} iterations, and completed {percentage_solved(grid, original_grid)}% ")
    print_grid(grid)
    print(f"According to the validation this is a {sudoku_validator(grid)} solution")

    return grid

# inputgrid = [
#     [7,0,0,  0,0,0,  0,0,6],
#     [0,0,0,  6,0,0,  0,4,0],
#     [0,0,2,  0,0,8,  0,0,0],

#     [0,0,8,  0,0,0,  0,0,0],
#     [0,5,0,  8,0,6,  0,0,0],
#     [0,0,0,  0,2,0,  0,0,0],

#     [0,0,0,  0,0,0,  0,1,0],
#     [0,4,0,  5,0,0,  0,0,0],
#     [0,0,5,  0,0,7,  0,0,4]
# ]
# zerosgrid = [
#     [0,0,0,  0,0,0,  0,0,0],
#     [0,0,0,  0,0,0,  0,0,0],
#     [0,0,0,  0,0,0,  0,0,0],

#     [0,0,0,  0,0,0,  0,0,0],
#     [0,0,0,  0,0,0,  0,0,0],
#     [0,0,0,  0,0,0,  0,0,0],

#     [0,0,0,  0,0,0,  0,0,0],
#     [0,0,0,  0,0,0,  0,0,0],
#     [0,0,0,  0,0,0,  0,0,0]
# ]
