import numpy as np
from itertools import combinations

import PossValsBox

def singles(poss_vals, sudoku_board):
    '''
    Checks all squares to see if there is only one canditate value. If there is only
    one, sets the board value to the candidate value.
    '''

    for i in range(9):
        for j in range(9):

            if len(poss_vals[i][j]) == 1:
                [sudoku_board[i,j]] = poss_vals[i][j]

    return poss_vals

def box(box_i, box_j, poss_vals, sudoku_board): 
    '''
    If a pair of values have to go in a pair of squares, then these values can't go into
    other squares in the same box. Thus these values are removed from the poss_vals of
    the other squares.
    '''

    # Run on {2/2},{3/3/3},{4/4/4/4} naked groups
    
    val_loc_box = np.argwhere(sudoku_board[3*box_i:3*box_i+3, 3*box_j:3*box_j+3] == 0)
    if len(val_loc_box) != 0:

        # Storing location sets for each possible value in a box
    
        locs_storage = [] 
        for val in range(1,10):
    
            poss_val_locs, poss_vals_box = PossValsBox.func(box_i, box_j, val, poss_vals) 
            locs_storage.append(poss_val_locs) 

        # Generate every length (length) combination of location sets in box and store location sets that are the same
    
            # Running pairs, triples, quads
        for length in range(2,5): 

            worthy_groups = [(val+1, loc_set) 
                             for val, loc_set in enumerate(locs_storage)
                             if len(loc_set) == length # <- Problematic for triples (doesn't allow for triples of {3/2/2})
                            ]
            if len(worthy_groups) >= length: # Combinations requires at least (length) location sets 
            
                for combo in combinations(worthy_groups, length): 
                    loc_sets = [loc_set for _, loc_set in combo] # <- Problematic for triples
                    vals = {val for val, _ in combo}
    
                    if all(set(loc_set) == set(loc_set[0]) # <- Problematic for triples
                           for loc_set in loc_sets
                          ):
        
                        naked_group_coords = set(tuple(loc) for loc in loc_sets[0]) # All locs same, so only need first location set
        
            # Removing vals from other locations in box if val exists in a naked group
    
                # Finding empty locations in box
                        empty_locs = np.argwhere(sudoku_board[3*box_i:3*box_i+3,3*box_j:3*box_j+3] == 0)
    
                        for val in vals:
                            for loc in empty_locs:

                                # loc in empty locs are 2D coords
                                global_i = 3*box_i+loc[0]
                                global_j = 3*box_j+loc[1]
                                
                                if (loc[0], loc[1]) in naked_group_coords : # If local empty location is equal to local naked group location
                                    continue # Skips locations of naked group
                                    
                                elif len(poss_vals[global_i][global_j]) != 0 and val in poss_vals[global_i][global_j]:
                                    poss_vals[global_i][global_j].remove(val)
    
                                    # Error Check
    
                                    if len(poss_vals[global_i][global_j]) == 0:
                                        print(f'Error: No possible values at global {global_i,global_j} due to Naked.box()')
    
                                if len(poss_vals[global_i][global_j]) == 1:
                                    [sudoku_board[global_i][global_j]] = poss_vals[global_i][global_j]


        # Run on {3/2/2}, {3/3/2}, {2/2/2} naked triples and quads

        for length in range(3,5):
                    # Storing all local location of cells which have between 2 and 3 possible values (no singles)
            worthy_groups = [(local_i, local_j, vals) 
                             for local_i, row in enumerate(poss_vals_box)
                             for local_j, vals in enumerate(row)
                             if 2 <= len(vals) <= length
                            ]
    
            if len(worthy_groups) >= length: # Combinations requires at least 3 locations
                
                for combo in combinations(worthy_groups, length): 
                    poss_vals_set = set().union(*[set(vals) for _, __, vals in combo]) 
                    if len(poss_vals_set) == length: # If combo includes 3 possible values across all locations
                        
                        naked_triple_ij_indices = set((local_i, local_j) for local_i, local_j, __ in combo)
                        
                        for val in poss_vals_set: 
                            for local_i in range(3):
                                for local_j in range(3):
    
                                    global_i = 3*box_i + local_i
                                    global_j = 3*box_j + local_j
                
                                    if (local_i, local_j) in naked_triple_ij_indices:
                                        continue
        
                                    elif val in set(poss_vals[global_i][global_j]):
                                        poss_vals[global_i][global_j].remove(val)
        
                                    # Error Check
            
                                    if len(poss_vals[global_i][global_j]) == 0:
                                        print(f'Error: No possible values at global {global_i,global_j} due to Naked.box()')
        
                                    if len(poss_vals[global_i][global_j]) == 1:
                                            [sudoku_board[global_i][global_j]] = poss_vals[global_i][global_j]
            
    return poss_vals
                            
                            
def row(i, poss_vals, sudoku_board): 
    '''
    Runs Naked pairs/triples/quads on a row
    '''

    # Run on {2/2},{3/3/3},{4/4/4/4} naked groups
    
    val_loc_row = np.argwhere(sudoku_board[i] == 0)
    if len(val_loc_row) != 0:

        # Storing sets of locations for each possible value in a row
    
        locs_storage = [] 
        for val in range(1,10):

            poss_vals_row = [j
                             for j, cell in enumerate(poss_vals[i])
                             if val in cell
                            ]
            locs_storage.append(poss_vals_row) 

        # Generate every length (length) combination of location sets in a row and store location sets that are the same
    
            # Running pairs, triples, quads of from {2/2}, {3/3/3}, {4/4/4/4}
        for length in range(2,5): 
    
            worthy_groups = [(val+1, loc_set) 
                             for val, loc_set in enumerate(locs_storage)
                             if len(loc_set) == length
                            ]
            if len(worthy_groups) >= length: # Combinations requires at least (length) location sets 
            
                for combo in combinations(worthy_groups, length): 
                    loc_sets = [loc_set for _, loc_set in combo]
                    vals = {val for val, _ in combo}
    
                    if all(set(loc_set) == set(loc_sets[0]) for loc_set in loc_sets):
        
                        naked_group_indices = set(loc_sets[0]) # All locs same, so only need first location set
    
            # Removing vals from other locations in a row if val exists in a naked group

                # Finding empty locations in row
                        empty_locs = [j 
                                      for j in range(9)
                                      if sudoku_board[i][j] == 0
                                     ]

                        for val in vals:
                            for j in empty_locs:
                                if j in naked_group_indices: # if global row empty locations are equal to global naked groups
                                    continue # Skips locations of naked group
                                elif len(poss_vals[i][j]) > 1 and val in poss_vals[i][j]:
                                    poss_vals[i][j].remove(val)   

                                    # Error Check
    
                                    if len(poss_vals[i][j]) == 0:
                                        print(f'Error: No possible values at global {i,j} due to Naked.row()')
    
                                if len(poss_vals[i][j]) == 1:
                                    [sudoku_board[i][j]] = poss_vals[i][j]

        # Run on {3/2/2}, {3/3/2}, {2/2/2} naked triples and quads of same sort

        for length in range(3,5):
        
            # Storing all location of cells which have between 2 and 3 possible values (no singles)
            worthy_groups = [(loc, vals) 
                                 for loc, vals in enumerate(poss_vals[i])
                                 if 2 <= len(vals) <= length
                                ]
            if len(worthy_groups) >= length: # Combinations requires at least 3 locations
                
                for combo in combinations(worthy_groups, length): 
                    poss_vals_set = set().union(*[set(vals) for _, vals in combo]) # Defines a set of vals for each combo, no duplicates, takes the union of an empty set with each set of values. * unpacks list into each element to take the union with.
                    if len(poss_vals_set) == length: # If combo includes 3 possible values across all locations
                        naked_triple_indices = [loc for loc, vals in combo] 
        
                        for val in poss_vals_set: 
                            for j in range(9):
            
                                if j in naked_triple_indices:
                                    continue
    
                                elif val in set(poss_vals[i][j]):
                                    poss_vals[i][j].remove(val)
    
                                # Error Check
        
                                if len(poss_vals[i][j]) == 0:
                                    print(f'Error: No possible values at global {i,j} due to Naked.row()')
    
                                if len(poss_vals[i][j]) == 1:
                                        [sudoku_board[i][j]] = poss_vals[i][j]

    return poss_vals


def col(j, poss_vals, sudoku_board): 
    '''
    Runs Naked pairs/triples/quads on a column
    '''

    # Run on {2/2},{3/3/3},{4/4/4/4} naked groups
    
    val_loc_col = np.argwhere(sudoku_board[:,j] == 0)
    if len(val_loc_col) != 0:

        # Storing sets locations for each possible value in a column
    
        locs_storage = [] 
        for val in range(1,10):

            poss_val_locs = [i for i in range(9) if val in poss_vals[i][j]]
            locs_storage.append(poss_val_locs) 

        # Generate every length (length) combination of location sets in a column and store location sets that are the same
    
            # Running pairs, triples, quads
        for length in range(2,5): 
    
            worthy_groups = [(val+1, loc_set) 
                             for val, loc_set in enumerate(locs_storage)
                             if len(loc_set) == length
                            ]
            if len(worthy_groups) >= length: # Combinations requires at least (length) location sets 
            
                for combo in combinations(worthy_groups, length): 
                    loc_sets = [loc_set for _, loc_set in combo]
                    vals = {val for val, _ in combo}
    
                    if all(set(loc_set) == set(loc_sets[0]) for loc_set in loc_sets):
        
                        naked_group_indices = set(loc_sets[0]) # All locs same, so only need first location set
    
            # Removing vals from other locations in a row if val exists in a naked group

                # Finding empty locations in row
                        empty_locs = [i
                                      for i in range(9)
                                      if sudoku_board[i][j] == 0
                                     ]

                        for val in vals:
                            for i in empty_locs:
                                if i in naked_group_indices: # if global column empty locations are equal to global naked groups
                                    continue # Skips locations of naked group
                                elif len(poss_vals[i][j]) > 1 and val in poss_vals[i][j]:
                                    poss_vals[i][j].remove(val)   

                                    # Error Check
    
                                    if len(poss_vals[i][j]) == 0:
                                        print(f'Error: No possible values at global {i,j} due to Naked.col() triples')
    
                                if len(poss_vals[i][j]) == 1:
                                    [sudoku_board[i][j]] = poss_vals[i][j]

        # Run on {3/2/2}, {3/3/2}, {2/2/2} naked triples, and quads of same sort

        poss_vals_col = [poss_vals[i][j] for i in range(9)]

        for length in range(3,5):

            # Storing all location of cells which have between 2 and 3 possible values (no singles)
            worthy_groups = [(loc, vals) 
                                 for loc, vals in enumerate(poss_vals_col)
                                 if 2 <= len(vals) <= length
                                ]
            if len(worthy_groups) >= length: # Combinations requires at least 3 locations
                
                for combo in combinations(worthy_groups, length): 
                    poss_vals_set = set().union(*[set(vals) for _, vals in combo])
                    if len(poss_vals_set) == length: 
                        naked_triple_indices = [loc for loc, vals in combo] 

                        for val in poss_vals_set:
                            for i in range(9):
            
                                if i in naked_triple_indices:
                                    continue
    
                                elif val in set(poss_vals[i][j]):
                                    poss_vals[i][j].remove(val)
                                        
                                # Error Check
        
                                if len(poss_vals[i][j]) == 0:
                                    print(f'Error: No possible values at global {i,j} due to Naked.col() triples')
    
                                if len(poss_vals[i][j]) == 1:
                                        [sudoku_board[i][j]] = poss_vals[i][j]
            
    return poss_vals

    




