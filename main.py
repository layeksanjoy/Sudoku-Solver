rows = 'ABCDEFGHI'
cols = '123456789'


def cross(a, b):
    return [s + t for s in a for t in b]


boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [
    cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI')
    for cs in ('123', '456', '789')
]
unitlist = row_units + column_units + square_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)

dia_u = ['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8', 'I9']
dia_ut = ['A9', 'B8', 'C7', 'D6', 'E5', 'F4', 'G3', 'H2', 'I1']

for u in units:
    if u in dia_u:
        units[u].append(dia_u)
    if u in dia_ut:
        units[u].append(dia_ut)

peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)


def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return


# grid = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'
# grid = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
grid = '.4.3...8...35.2.4......15.3..24..1..4...2...7..7..38..1.82......7.1.84...2...9.1.'


def grid_values(grid):
    values = []
    all_digits = '123456789'
    for c in grid:
        if c == '.':
            values.append(all_digits)
        elif c in all_digits:
            values.append(c)
    assert len(values) == 81
    return dict(zip(boxes, values))


def elimination(values):
    for box in values.keys():
        if len(values[box]) == 1:
            for peer_box in peers[box]:
                values[peer_box] = values[peer_box].replace(values[box], '')

    return values


def only_choice(value):
    for unit in units:
        u = units[unit][2]
        for i in u:
            if len(value[i]) != 1:
                #check if unique
                unique = 1
                for k in value[i]:
                    for j in u:
                        if (i != j) and k in value[j]:
                            unique = 0
                            break
                    if (unique == 1):
                        value[i] = k
    return value


def naked_twins(values):
    # print(units)
    for unit in units:
        for u in units[unit]:
            # print(u)
            # check for same number
            for i in u:
                for j in u:
                    if (i != j and values[i] == values[j]
                            and len(values[i]) == 2):
                        print(i, j, u)
                        # remove both the elements from their peers
                        for n in values[i]:
                            #checking in peers
                            # print(i,j,peers[i])
                            for pi in u:
                                if n in values[pi] and len(
                                        values[pi]
                                ) >= 2 and pi != j and pi != i:
                                    # print(values[pi])
                                    values[pi] = values[pi].replace(n, '')

    return values


def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len(
            [box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        values = elimination(values)

        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len(
            [box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False  ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values
    # Choose one of the unfilled squares with the fewest possibilities

    node = ''
    min = 10
    for k in values.keys():
        if len(values[k]) < min and len(values[k]) > 1:
            min = len(values[k])
            node = k
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    if (node != ''):
        for i in values[node]:
            new_sodu = values.copy()
            new_sodu[node] = i
            attempt = search(new_sodu)
            if attempt:
                return attempt

    # If you're stuck, see the solution.py tab!


values = grid_values(grid)
t = search(values)
display(t)
