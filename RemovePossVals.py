import numpy as np
from itertools import combinations

import OnlyVal 
import PossValsBox

'''
Runs functions which clear rows/columns/boxes based on known values on the 
sudoku board.
'''

def square_filled(poss_vals, sudoku_board):
        '''
        Removing all other possible values from completed tiles
        '''
        
        filled_locs = np.argwhere(sudoku_board != 0)
        
        for n in range(len(filled_locs)):
            i, j = filled_locs[n]
            poss_vals[i][j] = [sudoku_board[i,j]]

        return poss_vals, filled_locs


def col(j, val, poss_vals, sudoku_board):
    '''
    Removing value from possible values if value already exists in column
    '''

    val_loc_col = np.argwhere(sudoku_board[:,j] == val)
    
    if len(val_loc_col) == 1:
        for i in range(len(sudoku_board[0])):
            if i != val_loc_col[0][0] and val in poss_vals[i][j]:
                poss_vals[i][j].remove(val) # Deletes value from list

                # Error Check: No possible values remain
                if len(poss_vals[i][j]) == 0:
                    print(f'Error: No possible values at global {i,j} due to RemovePossVals.col()')

            if len(poss_vals[i][j]) == 1:
                [sudoku_board[i,j]] = poss_vals[i][j]

    # Error Check: Value placed incorrectly

    elif len(val_loc_col) > 1: 
        print(f'Error: Same value occured twice in column {j}')

    return poss_vals


def row(i, val, poss_vals, sudoku_board): 
    '''
    Removing value from possible values if value already exists in row
    '''
    
    val_loc_row = np.argwhere(sudoku_board[i] == val)
    
    if len(val_loc_row) == 1:
        for j in range(len(sudoku_board[0])):
            if j != val_loc_row[0] and val in poss_vals[i][j]:
                poss_vals[i][j].remove(val)

                # Error Check: No possible values remain 
                if len(poss_vals[i][j]) == 0:
                    print(f'Error: No possible values at global {i,j} due to RemovePossVals.row()')

            if len(poss_vals[i][j]) == 1:
                [sudoku_board[i,j]] = poss_vals[i][j]

    # Error Check: Value placed incorrectly

    elif len(val_loc_row) > 1: 
        print(f'Error: Same value occured twice in row {i}')

    return poss_vals
    

def box(box_i, box_j, val, poss_vals, sudoku_board):
    '''
    Removing value from possible values if value already exists in box
    '''

    # Runs only if box isn't solved

    val_loc_box = np.argwhere(sudoku_board[3*box_i:3*box_i+3, 3*box_j:3*box_j+3] == 0)
    
    if len(val_loc_box) != 0:

        # Local to global indices from boxes to board
        val_cells = [] # Stores location of single poss_val in a box
        for i_box in range(3):
            for j_box in range(3):
                global_i = 3*box_i+i_box # Row index
                global_j = 3*box_j+j_box # Column index 
    
                if poss_vals[global_i][global_j] == [val]:
                    val_cells.append((global_i,global_j))
        
        
        if len(val_cells) == 1:
            i_val, j_val = val_cells[0]
            for i_box in range(3): # Iterating over every threes grid
                for j_box in range(3):
                    global_i = 3*box_i+i_box
                    global_j = 3*box_j+j_box
    
                    if (global_i, global_j) != (i_val, j_val): 
                        if val in poss_vals[global_i][global_j]: 
                            poss_vals[global_i][global_j].remove(val)

                            #Error Check
                            if len(poss_vals[global_i][global_j]) == 0:
                                print(f"Error: No possible values at {global_i,global_j} due to RemovePossVals.box()")
    
                        if len(poss_vals[global_i][global_j]) == 1:
                            [sudoku_board[global_i,global_j]] = poss_vals[global_i][global_j]

        elif len(val_cells) > 1: 
            print(f'Error: More than one of the same value in box {box_i, box_j}')
                            

    return poss_vals

def pointing(box_i, box_j, val, poss_vals, sudoku_board): # NEEDS TO FIX ERRORS
    '''
    Removes value from poss_vals for all elements in a row/column if value occurs along 
    same line in box (i.e. two possible 1s in the same vertical line mean no other ones
    can be in that column across all boxes)

    Note: uses box_coord_i, box_coord_j to denote box y,x coords (Cartesian)
    '''

    # Runs only if box isn't solved

    val_loc_box = np.argwhere(sudoku_board[3*box_i:3*box_i+3, 3*box_j:3*box_j+3] == 0)
    
    if len(val_loc_box) != 0:


        poss_val_locs, poss_vals_box = PossValsBox.func(box_i, box_j, val, poss_vals)
    
        num_locs = len(poss_val_locs)
        if 2 <= num_locs <= 3: # Only runs if poss_vals value occurs in single row/column (when val_locs length is 2 or 3)
    
            col_idxs = [point[1] for point in poss_val_locs] # Pulls out column index from val_locs
            row_idxs = [point[0] for point in poss_val_locs]  # " " row " "
    
            # Rows check 
            
            if len(set(row_idxs)) == 1: # If only one row index across all locations 
    
                # Defining coords over entire board in terms of box local coords
                global_i = 3*box_i + row_idxs[0]
            
                for j in range(9): # For a single row, iterates over columns of poss_vals
                    if (j // 3) != box_j: # Runs box_line() only on boxes other than checked box
                        if val in poss_vals[global_i][j]:
                            poss_vals[global_i][j].remove(val) # Removes val from other cells in line\

                            # Error Check
                            if len(poss_vals[global_i][j]) == 0:
                                print(f"Error: No possible values at {global_i,j} due to box_line()")
    
                            # Updating sudoku board if only one poss_val remains
                            if len(poss_vals[global_i][j]) == 1:
                                [sudoku_board[global_i,j]] = poss_vals[global_i][j]

    
    
            # Column check 
         
            if len(set(col_idxs)) == 1: 
                
                # Defining coords over entire board in terms of box local coords
                global_j = 3*box_j + col_idxs[0]
                
                for i in range(9): # Iterates over row of poss_vals
                    if (i // 3) != box_i: 
                        if val in poss_vals[i][global_j]:
                            poss_vals[i][global_j].remove(val)
    
                            if len(poss_vals[i][global_j]) == 1:
                                [sudoku_board[i,global_j]] = poss_vals[i][global_j]
    
                            # Error Check
                            
                            if len(poss_vals[i][global_j]) == 0:
                                print(f"Error: No possible values at {i,global_j} due to box_line()")

    return poss_vals



def box_line_reduction(poss_vals, sudoku_board):
    '''
    Removes value from a box if in a given row or column a value
    can only exist in restricted locations (i.e. a 7 hasn't been placed
    in row 2 but can only go in squares 0 and 2 of box (0,0), so all 
    other 7's get removed from this box), and so all other possible 
    values are removed from this box.
    '''
        
    # box_line_reduction on rows

        # Defining possible values for each value in row

    for i in range(9):

        # Runs if row isn't full
        val_loc_row = np.argwhere(sudoku_board[i] == 0)

        if len(val_loc_row) != 0:
            
            locs_storage = [] # Stores a set of j-locations for each values within the row
            for val in range(1,10):
                poss_vals_row = [j
                                 for j, cell in enumerate(poss_vals[i])
                                 if val in cell
                                ]
                locs_storage.append(poss_vals_row)

            # Checking to see whether all possible values lie in a single box

            worthy_groups = [# loc_set is set of j for each val if has length 2 or 3 and all occur in same box
                (val+1, j_set) 
                for val, j_set in enumerate(locs_storage) 
                if 2<=len(j_set)<=3 and len(set(j//3 for j in j_set)) == 1
            ] 
            
            if len(worthy_groups) != 0:
                vals = [pt[0] for pt in worthy_groups] 
                j_locs = [pt[1] for pt in worthy_groups] # list of j_set lists
                
        # Removing all other instances of value in box except for on restricted locations
                
                for val, j_set in zip(vals, j_locs): # Zip iterator object that pairs (val1,j1),(val2,j2), etc.
                    box_i = i // 3
                    box_j = j_set[0] // 3 
                    
                    for i_box in range(3): # Defining local coords within box
                        for j_box in range(3): 
                            global_i = 3*box_i + i_box
                            global_j = 3*box_j + j_box

                            # Skipping iterations where global_j is in j_sets, global_i = i
                            if global_i == i and global_j in j_set:
                                continue 
                            
                            if val in poss_vals[global_i][global_j]: 
                                poss_vals[global_i][global_j].remove(val)

                                if len(poss_vals[global_i][global_j]) == 0:
                                    print(f'Error: No possible values at global {global_i,global_j} due to claiming')
                            if len(poss_vals[global_i][global_j]) == 1:
                                [sudoku_board[global_i][global_j]] = poss_vals[global_i][global_j]
                                        

                            
                        
            

    # box_line_reduction on columns
        for j in range(9):

            # Runs if col isn't full
            val_loc_col = np.argwhere(sudoku_board[:,j] == 0)
    
            if len(val_loc_col) != 0:
                
                locs_storage = [] # Stores a set of i-locations for each values within the column
                for val in range(1,10):
                    poss_vals_col = [i for i in range(9) if val in poss_vals[i][j]] # Only includes val if is in poss_vals
                    locs_storage.append(poss_vals_col)
    
                # Checking to see whether all possible values lie in a single box
    
                worthy_groups = [# loc_set is set of i for each val if has length 2 and all occur in same box
                    (val+1, i_set) 
                    for val, i_set in enumerate(locs_storage) 
                    if 2<=len(i_set)<=3 and len(set(i//3 for i in i_set)) == 1
                ] 
                
                if len(worthy_groups) != 0:
                    vals = [pt[0] for pt in worthy_groups] 
                    i_locs = [pt[1] for pt in worthy_groups] # list of j_set lists
                    
            # Removing all other instances of value in box except for on restricted locations
                    
                    for val, i_set in zip(vals, i_locs): # Zip iterator object that pairs (val1,j1),(val2,j2), etc.
                        box_i = i_set[0] // 3
                        box_j = j // 3 
                        
                        for i_box in range(3): # Defining local coords within box
                            for j_box in range(3): 
                                global_i = 3*box_i + i_box
                                global_j = 3*box_j + j_box
    
                                # Skipping iterations where global_j is in j_sets, global_i = i
                                if global_j == j and global_i in i_set:
                                    continue 
                                
                                if val in poss_vals[global_i][global_j]: 
                                    poss_vals[global_i][global_j].remove(val)
    
                                    if len(poss_vals[global_i][global_j]) == 0:
                                        print(f'Error: No possible values at global {global_i,global_j} due to box_line_reduction')
                                if len(poss_vals[global_i][global_j]) == 1:
                                    [sudoku_board[global_i][global_j]] = poss_vals[global_i][global_j]


            

    return poss_vals


    