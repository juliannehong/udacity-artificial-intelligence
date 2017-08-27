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

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a+b for a in A for b in B]
    #pass


""" Global Variables """
rows = 'ABCDEFGHI'
cols = '123456789'

boxes = cross(rows,cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diag_units = [[rows[i]+cols[i] for i in range(9)],[rows[i]+cols[8-i] for i in range(9)]] # add diagonal units
unitlist = row_units + column_units + square_units + diag_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


def naked_twins(values):
    # Find all instances of naked twins
    no_more_twin = False
    while not no_more_twin:
        value_before = values
        for unit in unitlist:
            possible_twin_dict = {}
            for key, val in values.items():
                if key in unit and len(values[key]) == 2:
                    possible_twin_dict[key] = val

            # get twin value lists in a single unit
            for v in possible_twin_dict.values():
                if list(possible_twin_dict.values()).count(v) == 2:
                    for box in unit:
                        if values[box] != v:
                            values = assign_value(values, box, values[box].replace(v[0],"")) 
                            values = assign_value(values, box, values[box].replace(v[1],""))
        value_after = values
        if value_before == value_after:
            no_more_twin = True
    return values


def grid_values(grid):

    s_dict = {}
    for x in range(81):
        if grid[x] == '.':
            s_dict[boxes[x]] = '123456789'
        else:
            s_dict[boxes[x]] = grid[x]

    return s_dict

def display(values):

    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    for b in boxes:
        if (len(values[b]) == 1):
            v = values[b] # stores the dup. digit
            for p in peers[b]:
                values = assign_value(values, p, values[p].replace(v,"")) # replace the dup. digit to empty str
    return values

def only_choice(values):
    for each_unit in unitlist:
        for d in '123456789':
        # get list of box in a single unit that contains d
            d_list = [box for box in each_unit if d in values[box]]
            if len(d_list) == 1:
                solved_box = d_list[0] # now this box is solved
                values = assign_value(values, solved_box, d)
    return values

def reduce_puzzle(values):
    stalled = False # not doing the same thing yet.
    while not stalled:
        solved_before_count = len([box for box in values.keys() if len(values[box]) == 1])

        eliminate(values)
        only_choice(values)

        solved_after_count = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = (solved_before_count == solved_after_count) # did this loop do something useful?

        # Sanity Check (this shouldn't happen unless dfs search is performed and tried wrong solution)
        if (len([box for box in values.keys() if len(values[box]) == 0]) > 0):
            return False
    return values

def search(values):

    values = reduce_puzzle(values)
   # small_box = min(len(values[small_box]) for small_box in values.keys() if len(values[small_box]) > 1)

    # return cases
    if (values == False):
        return False

    if all(len(values[box]) == 1 for box in boxes):
        return values
    n,small_box = min((len(values[small_box]),small_box) for small_box in values.keys() if len(values[small_box])>1)
    for maybe_answer in values[small_box]:
        temp_values = values.copy()
        temp_values[small_box] = maybe_answer
        ret = search(temp_values)
        """
        ret can be:
        1. False if the 'maybe_answer' is not an answer
        2. None if the 'maybe_answer' is an answer but the reduce_puzzle method is still not enough
        3. values if 'maybe_answer' is actually answer
        """
        if ret:
            return ret

def solve(grid):
    
    values = grid_values(grid)
    ret_values = search(values)
    if ret_values:
        return ret_values
    else:
        return False


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))
    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')



