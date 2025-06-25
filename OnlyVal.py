import numpy as np
import PossValsBox

'''
Runs functions associated with Hidden Singles. Principle is if a row/column/box only
has one instance of a single value in it's possible values, since all values need
to be used up, this value must go in that location.
'''

def col(j, val, poss_vals, sudoku_board): 
    '''
    Assigns value to a blank square if it's the only square that contains a 
    given value in the column (even if it has more possible values).
    '''

    poss_vals_col = [poss_vals[i][j] for i in range(9)]
        
    val_loc = [i for i, cell in enumerate(poss_vals_col) if val in cell] # i for i, cell in enumerate means takes the first value of the enumerate() function, which outputs (index, cell). Thus val_loc takes the index value of the element if val is in poss_vals[y][x].

    if len(val_loc) == 1:
        sudoku_board[val_loc[0],j] = val
        poss_vals[val_loc[0]][j] = [val] # Upating poss_vals

    
    # Error Check

    val_loc_col = np.argwhere(sudoku_board[:,j] == val)

    if len(val_loc_col) > 1:
        print(f'Code Error: Same value occured twice in column {j}')

    return poss_vals

def row(i, val, poss_vals, sudoku_board):
    '''
    Assigns value to a blank square if it's the only square that contains a 
    given value in the row (even if it has more possible values)
    '''

    poss_vals_row = [poss_vals[i][j] for j in range(9)]
        
    val_loc = [j
               for j, cell in enumerate(poss_vals_row)
               if val in cell
              ] # i for i, cell in enumerate means takes the first value of the enumerate() function, which outputs (index, cell). Thus val_loc takes the index value of the element if val is in poss_vals[y][x].

    if len(val_loc) == 1:
        sudoku_board[i,val_loc[0]] = val
        poss_vals[i][val_loc[0]] = [val]
    
    # Error Check

    val_loc_row = np.argwhere(sudoku_board[i] == val)

    if len(val_loc_row) > 1:
        print(f'Code Error: Same value occured twice in row {i}')

    return poss_vals

def box(box_i, box_j, val, poss_vals, sudoku_board):
    '''
    Assigns value to a blank square if it's the only square that contains a 
    given value in the box (even if it has more possible values)
    '''
    
    val_loc, poss_vals_box = PossValsBox.func(box_i, box_j, val, poss_vals)

    global_i = val_loc[0][0]+3*box_i
    global_j = val_loc[0][1]+3*box_j

    if len(val_loc) == 1:
        sudoku_board[global_i, global_j] = val
        poss_vals[global_i][global_j] = [val]

    
    # Error Check
    
    val_loc_box = np.argwhere(sudoku_board[3*box_j:3*box_j+3,3*box_i:3*box_i+3] == val)

    if len(val_loc_box) > 1: 
        print(f'Code Error: Same value occured twice in box {box_i, box_j}')

    return poss_vals

        