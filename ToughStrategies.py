import numpy as np
from itertools import combinations

def x_wing(poss_vals, sudoku_board):
    '''
    Runs if a rectangle of locations occurs where each pair of rows or columns
    makes up a locked set (naked pair). So this means that either the top
    left and bottom right squares need to be filed, or the top right and
    bottom left. This means that any other squares along these columns
    containing the filled value in their possible values needs to be 
    removed. 
    '''

    for val in range(1,10): # Runs x-wing on each value
    
    # Locked pair in rows (one value only exists in two locations in two different rows, and column indices match)

        # Initialising list for each value so that x-wing only runs when
        # there are two rows with two locations where val can be
        valid_rows = []
        for i in range(9): 
            val_loc_row = [(i,j)
                           for j in range(9)
                           if val in poss_vals[i][j]
                          ] # Stores set of j indices for each value 
            if len(val_loc_row) == 2:
                valid_rows.append(val_loc_row)  
        
        if len(valid_rows) in {2,4,6,8}: # If number of valid rows is even, accounts for non-interacting x-wings 
            for combo in combinations(valid_rows, 2): 

                valid_rows_i = {loc[0] # Extracts i index
                                for row in combo
                                for loc in row
                               }
                # print(valid_rows_i)
                valid_rows_j = {loc[1] # Extracts j index
                                for row in combo
                                for loc in row
                               }
                # print(valid_rows_j)

                if len(valid_rows_j) == 2: # If total of 2 column indices between both rows

                    # Removing val from all cells in columns contained in x-wing
                    for j in valid_rows_j:
                        for i in range(9):
                            
                            if i in valid_rows_i: # Don't remove val from cells in x-wing
                                continue 
    
                            elif val in poss_vals[i][j]:
                                poss_vals[i][j].remove(val)

                                # Error Check

                                if len(poss_vals[i][j]) == 0:
                                    print(f'Error: No possible values at global {i,j} due to ToughStrategies.x_wing()')
    
                                if len(poss_vals[i][j]) == 1:
                                        [sudoku_board[i][j]] = poss_vals[i][j]
                                
                            
    # Locked pair in columns (one value only exists in two locations in two different columns, and row indices match)

        # Initialising list for each value so that x-wing only runs when
        # there are two columns with two locations where val can be
        valid_cols = []
        for j in range(9): 
            val_loc_col = [(i,j)
                           for i in range(9)
                           if val in poss_vals[i][j]
                          ] # Stores set of j indices for each value 
            if len(val_loc_col) == 2:
                valid_cols.append(val_loc_col)  
        
        if len(valid_cols) in {2,4,6,8}: # If number of valid rows is even, accounts for non-interacting x-wings 
            for combo in combinations(valid_cols, 2): 
                
                valid_cols_i = {loc[0] # Extracts i index
                                for col in combo
                                for loc in col
                               }
                valid_cols_j = {loc[1] # Extracts j index
                                for col in combo
                                for loc in col
                               }

                if len(valid_cols_i) == 2: # If total of 2 row indices between both columns

                    # Removing val from all cells in columns contained in x-wing
                    
                    for i in valid_cols_i:
                        for j in range(9):
                            
                            if j in valid_cols_j: # Don't remove val from cells in x-wing
                                continue 
    
                            elif val in poss_vals[i][j]:
                                poss_vals[i][j].remove(val)
                                
                                # Error Check

                                if len(poss_vals[i][j]) == 0:
                                    print(f'Error: No possible values at global {i,j} due to ToughStrategies.x_wing()')
    
                                if len(poss_vals[i][j]) == 1:
                                        [sudoku_board[i][j]] = poss_vals[i][j]



    return poss_vals