assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    naked_twins = []
    for unit in unit_list:
        i = 0
        while i < len(unit) :
            v = values[unit[i]]
            if len(v) == 2:
                for box in unit:
                    if values[box] == v and box != unit[i] and v not in naked_twins:
                        print (unit[i] + " is : " + v)
                        naked_twins.append(v)
            i += 1
    print (naked_twins)
    # Eliminate the naked twins as possibilities for their peers
    if naked_twins:
        for unit in unit_list:
            for digit in naked_twins:
                for d in digit:
                    for box in unit :
                        if d in values[box] and values[box] not in naked_twins and len(values[box]) > 1:
                            assign_value(values, box, values[box].replace(d,''))
    return values

def cross(a, b):
    "Cross product of elements in A and elements in B."
    return [s+t for s in a for t in b]


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    assert len(grid) == 81, "Input grid must be of 81 character"
    sudoku = dict(zip(boxes, grid))
    for box in sudoku :
        if sudoku[box] == '.':
            sudoku[box] = '123456789'
    return sudoku

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    for box in values:
        if len(values[box]) == 1 :
            c = values[box]
            for s in peers[box]:
                assign_value(values, s, values[s].replace(c, '')) 
    
    return values

def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    for unit in unit_list:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                assign_value(values, dplaces[0], digit)
    return values

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # display(values)
        # Use the Eliminate Strategy
        values = eliminate(values)
        # print("After eliminating")
        # display(values)
        # Use the Naked Twins Strategy
        # values = naked_twins(values)
        # print("After Naked Twins")
        # display(values) 
        # Use the Only Choice Strategy
        values = only_choice(values)
        # print("After Only Choice")
        # display(values)
        # print("\n\n")
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    "Using depth-first search and propagation, try all possible values."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and 
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        # global char
        # if not char:
        #     # print("Sudoko : ")
        #     # display(values)
        #     # print( " New with one value : ")
        #     # display(new_sudoku)
        #     char = input()
        attempt = search(new_sudoku)
        if attempt:
            return attempt
        else :
            print ("Can't solve")


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)

    values = search(values)

    if values:
        return values
    print ("No solution")
    return False

# String for representing column and rows name of sudoku board
cols = "123456789"
rows = "ABCDEFGHI"

# Creating labels for boxes
boxes = cross(rows, cols)

# Creating row units label
row_units = [cross(r, cols) for r in rows]

# Creating col units label
col_units = [cross(rows, c) for c in cols]

# Creating square units label
square_units =[cross(r, c) for r in ("ABC","DEF","GHI") for c in ("123", "456", "789")]

diagonal_units = [['A1','B2','C3','D4','E5','F6','G7','H8','I9'],['A9','B8','C7','D6','E5','F4','G3','H2','I1']]
char = ''
unit_list = row_units + col_units + square_units + diagonal_units

units = dict((s, [u for u in unit_list if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except Exception as e:
        print (e.args)
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
