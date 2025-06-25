import numpy as np
from itertools import combinations

import PossValsBox

'''
Note: Hidden Triples requires same fix as naked triples
'''

def box(box_i, box_j, poss_vals, sudoku_board):
    '''
    Runs Hidden pairs, triples, quads on a box.
    
    If two values can only go in two locations in a box, removes all other
    possible values from these squares since these values can't go elsewhere.
    '''

    # Runs if box isn't complete 

    val_loc_box = np.argwhere(sudoku_board[3*box_i:3*box_i+3, 3*box_j:3*box_j+3] == 0)
    if len(val_loc_box) != 0:
    
        locs_storage = [] 
        for val in range(1,10):
            poss_val_locs, poss_vals_box = PossValsBox.func(box_i, box_j, val, poss_vals) 
            locs_storage.append(poss_val_locs) 
        
        # If locations for any two values are the same, remove all other possible values from these locations
    
            # Runs on Hidden groups of size {2/2}, {3/3/3}, {4/4/4/4}
        for length in range(2,5): 
            
            # Comparing all possible combinations of locs_storage for the same locations of same length
            worthy_groups = [(val+1, loc_set)
                             for val, loc_set in enumerate(locs_storage)
                             if len(loc_set) == length
                            ]
            
            for combo in combinations(worthy_groups, length):
                loc_sets = [loc_set for _, loc_set in combo]
                vals = {val for val, _ in combo}
        
                if all(set(loc_set) == set(loc_sets[0]) for loc_set in loc_sets): # If all loc_sets are identical
    
                    for loc_idx in range(length):
                        i, j = loc_sets[0][loc_idx] # All locs same, so only need first location set
                        
                        global_i = 3*box_i+i
                        global_j = 3*box_j+j
    
                        for val in range(1,10):
                            if val not in vals:  
                                if len(poss_vals[global_i][global_j]) == 1: # Fills the box if length is 1
                                        [sudoku_board[global_i,global_j]] = poss_vals[global_i][global_j]
                                elif val in poss_vals[global_i][global_j]: # Ensuring val exists in list
                                    poss_vals[global_i][global_j].remove(val) # Removes val from poss vals
    
                                    # Error Check 
                                    
                                    if len(poss_vals[global_i][global_j]) == 0:
                                        print(f"Error: No possible values at global {[global_i,global_j]} due to Hidden.box() for val = {val}")



        # Run on {3/2/2}, {3/3/2}, {2/2/2} naked triples, and quads of same sort

        for length in range(3,5):
            
            worthy_groups = [(val+1, loc_set) 
                             for val, loc_set in enumerate(locs_storage)
                             if 2 <= len(loc_set) <= length
                            ] # Stores sets of local (i,j) indices in loc_set
    
            if len(worthy_groups) >= length: # Combinations requires at least 3 locations 
                
                for combo in combinations(worthy_groups, length):
                    vals = {val for val, _ in combo}
                    hidden_triple_ij_indices = {(local_i, local_j)
                                                for _, loc_set  in combo
                                                for local_i, local_j in loc_set
                                               } 
                    
                    if len(hidden_triple_ij_indices) == length: 
                       
                        for val in range(1,10):
                            for local_i in range(3):
                                for local_j in range(3):

                                    global_i = 3*box_i + local_i
                                    global_j = 3*box_j + local_j

                                    if (local_i,local_j) in hidden_triple_ij_indices:
                                        if val not in vals and val in poss_vals[global_i][global_j]:
                                            poss_vals[global_i][global_j].remove(val)

                                        elif val in vals or val not in poss_vals[global_i][global_j]:
                                            continue
        
                                    # Error Check
            
                                    if len(poss_vals[global_i][global_j]) == 0:
                                        print(f'Error: No possible values at global {global_i,global_j} due to Hidden.box()')
        
                                    if len(poss_vals[global_i][global_j]) == 1:
                                            [sudoku_board[global_i][global_j]] = poss_vals[global_i][global_j]

        

    return poss_vals

def row(i, poss_vals, sudoku_board):
    '''
     Runs Hidden pairs, triples, quads on a row
    '''

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

            # Runs on Hidden groups of size {2/2}, {3/3/3}, {4/4/4/4}
        for length in range(2,5):
            worthy_groups = [(val+1, loc_set)
                             for val, loc_set in enumerate(locs_storage)
                             if len(loc_set) == length
                            ] # loc_set is set of j for each val, stores only if there are (length) locations
            
            for combo in combinations(worthy_groups, length):
                loc_sets = [loc_set for _, loc_set in combo]
                vals = {val for val, _ in combo}
                
                if all(set(loc_set) == set(loc_sets[0]) for loc_set in loc_sets):
    
                    for loc_idx in range(length):
                        j = loc_sets[0][loc_idx] # Each loc_set has set of j's, so take first set, each j index
    
                        for val in range(1,10):
                            if val not in vals:  
                                if len(poss_vals[i][j]) == 1: # Fills the box if length is 1
                                    [sudoku_board[i,j]] = poss_vals[i][j]
                                elif val in poss_vals[i][j]: # Ensuring val exists in list
                                    poss_vals[i][j].remove(val) # Removes val from poss vals
    
                                    # Error Check 
                                    
                                    if len(poss_vals[i][j]) == 0:
                                        print(f"Error: No possible values at global {i,j} due to Hidden.row() for val = {val}")

        # Run on {3/2/2}, {3/3/2}, {2/2/2} hidden triples, and quads of same sort 

        for length in range(3,5):
            
            worthy_groups = [(val+1, loc_set)
                             for val, loc_set in enumerate(locs_storage)
                             if 2 <= len(loc_set) <= length
                            ] # loc_set is set of j for each val, stores only if exists in between 2 and (length) squares

            if len(worthy_groups) >= length:
                
                for combo in combinations(worthy_groups, length):
                    vals = {val for val, _ in combo}
                    hidden_triple_indices = {j
                                            for _, loc_set in combo
                                            for j in loc_set
                                            } # Stores j index from each location set in combo 
                    
                    if len(hidden_triple_indices) == length: 
                        for val in range(1,10):
                            
                            for j in hidden_triple_indices:
                                if val not in vals and val in poss_vals[i][j]:
                                    poss_vals[i][j].remove(val)

                                elif val in vals or val not in poss_vals[i][j]:
                                    continue

                                # Error Check
        
                                if len(poss_vals[i][j]) == 0:
                                    print(f'Error: No possible values at global {i,j} due to Hidden.row()')
    
                                if len(poss_vals[i][j]) == 1:
                                        [sudoku_board[i][j]] = poss_vals[i][j]
                    

                
    return poss_vals

def col(j, poss_vals, sudoku_board):
    '''
     Runs Hidden pairs, triples, quads on a row
    '''

    # Runs if columns isn't full
    val_loc_col = np.argwhere(sudoku_board[:,j] == 0)
    
    if len(val_loc_col) != 0:
        locs_storage = [] # Stores a set of i-locations for each values within the column
        for val in range(1,10):
            poss_vals_col = [i for i in range(9) if val in poss_vals[i][j]] 
            locs_storage.append(poss_vals_col)
            
            # Runs on Hidden groups of size {2/2}, {3/3/3}, {4/4/4/4}
        for length in range(2,5):
            worthy_groups = [(val+1, loc_set)
                             for val, loc_set in enumerate(locs_storage)
                             if len(loc_set) == length
                            ] # loc_set is set of j for each val
            
            for combo in combinations(worthy_groups, length):
                loc_sets = [loc_set for _, loc_set in combo]
                vals = {val for val, _ in combo}
                
                if all(set(loc_set) == set(loc_sets[0]) for loc_set in loc_sets):
    
                    for loc_idx in range(length):
                        i = loc_sets[0][loc_idx] # Each loc_set has set of j's, so take first set, each j index
    
                        for val in range(1,10):
                            if val not in vals:  
                                if len(poss_vals[i][j]) == 1: # Fills the box if length is 1
                                    [sudoku_board[i,j]] = poss_vals[i][j]
                                elif val in poss_vals[i][j]: # Ensuring val exists in list
                                    poss_vals[i][j].remove(val) # Removes val from poss vals
    
                                    # Error Check 
                                    
                                    if len(poss_vals[i][j]) == 0:
                                        print(f"Error: No possible values at global {i,j} due to Hidden.col() for val = {val}")


        # Run on {3/2/2}, {3/3/2}, {2/2/2} naked triples, and quads of same sort
        
        for length in range(3,5):
            
            worthy_groups = [(val+1, loc_set)
                             for val, loc_set in enumerate(locs_storage)
                             if 2 <= len(loc_set) <= length
                            ] # loc_set is set of j for each val, stores only if exists in between 2 and (length) squares
            if len(worthy_groups) >= length:
                
                for combo in combinations(worthy_groups, length):
                    vals = {val for val, _ in combo}
                    hidden_triple_indices = {i
                                            for _, loc_set in combo
                                            for i in loc_set
                                            } # Stores i index from each location set in combo 
                    
                    if len(hidden_triple_indices) == length: 
                        for val in range(1,10):
                            
                            for i in hidden_triple_indices:
                                if val not in vals and val in poss_vals[i][j]:
                                    poss_vals[i][j].remove(val)

                                elif val in vals or val not in poss_vals[i][j]:
                                    continue

                                # Error Check
        
                                if len(poss_vals[i][j]) == 0:
                                    print(f'Error: No possible values at global {i,j} due to Hidden.row()')
    
                                if len(poss_vals[i][j]) == 1:
                                        [sudoku_board[i][j]] = poss_vals[i][j]
                    

        
    return poss_vals

    