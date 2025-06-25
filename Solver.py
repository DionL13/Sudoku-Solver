import numpy as np
import time

# Importing Solving Techniques
import RemovePossVals  
import OnlyVal
import Naked
import Hidden
import ToughStrategies

'Techniques from https://www.sudokuwiki.org/sudoku.htm'

# Initializing 9x9 sudoku board, index array with (i,j) as (row,column)

sudoku_board = np.array([[5,0,0,  0,3,0,  0,1,4]
                        ,[7,0,0,  9,4,0,  0,0,0],
                         [0,0,4,  0,0,0,  6,0,0],
                         
                         [0,0,0,  0,0,0,  0,7,0],
                         [9,1,0,  0,2,0,  0,5,0],
                         [0,7,0,  0,0,0,  0,0,3],
                         
                         [0,0,9,  0,0,0,  3,0,0],
                         [0,0,0,  0,9,5,  0,0,6],
                         [3,4,0,  0,7,0,  0,0,1]]) 

# Defining possible values for each element of 9x9 sudoku board

poss_vals = [[list(range(1,10)) for i in range(9)] for j in range(9)] # For each (i,j) creates a list of possible values between 1 and 9, each row corresponds to a row of the sudoku board

def solve_puzzle(sudoku_board, poss_vals):
    '''
    Funcion runs the solver on the intial sudoku board, and takes the
    threes_grids as an argumentsince it needs to be updated with
    each iteration and taken as an input.
    '''

    # Starting Stopwatch

    start_time = time.time()

    # Checking conditions iteratively for possible values

         # Initially filled tiles
        
    poss_vals, filled_locs = RemovePossVals.square_filled(poss_vals, sudoku_board)

        # While Loop variables

    num_blank_squares = len(filled_locs)
    num_squares_store = [0,0] # To make sure while condition works properly
    num_iterations = 0

    
    while num_blank_squares != num_squares_store[-2] and num_blank_squares != 81: # While the number of blank tiles is decreasing, stops at 3 in a row since poss_vals may change in last iteration but can't trigger next remove_vals condition because of ordering
    
            # Rows, Columns, Boxes
    
        for val in range(1,10):

            # Updating all filled squares 
            poss_vals, filled_locs = RemovePossVals.square_filled(poss_vals, sudoku_board) 
    
            # Make placements for rows and columns simultaneously, each function returns updated poss_vals
            
            for i in range(9):
                poss_vals = OnlyVal.col(i, val, poss_vals, sudoku_board) # Updates poss_vals after running onlyval.col
                poss_vals = OnlyVal.row(i, val, poss_vals, sudoku_board)
                    
            for box_j in range(3):
                for box_i in range(3):
                    poss_vals = OnlyVal.box(box_i, box_j, val,poss_vals, sudoku_board)

            # Checking for singletons in poss_vals
            poss_vals = Naked.singles(poss_vals,sudoku_board)

            # Re-updating filled squares after OnlyVal updates the sudoku board
            poss_vals, filled_locs = RemovePossVals.square_filled(poss_vals, sudoku_board)
            
            # Removing vals from updated poss_vals for rows and columns simultaneously 
            
            for i in range(9):
                poss_vals = RemovePossVals.col(i, val, poss_vals, sudoku_board)
                poss_vals = RemovePossVals.row(i, val, poss_vals, sudoku_board)

            # Box clearances separated due to interactions between poss_vals boxes, so needs to be fully updated first.
            
            for box_j in range(3):
                for box_i in range(3):
                    poss_vals = RemovePossVals.box(box_i, box_j, val, poss_vals, sudoku_board)

            # Checking for singletons in poss_vals
            poss_vals = Naked.singles(poss_vals,sudoku_board)
            
            for box_j in range(3): 
                for box_i in range(3):
                    poss_vals = RemovePossVals.pointing(box_i, box_j, val, poss_vals, sudoku_board)

            # Checking for singletons in poss_vals
            poss_vals = Naked.singles(poss_vals,sudoku_board)
            
            # Running Hidden pairs, triples and quads on rows, columns and boxes

            for i in range(9):
                poss_vals = Hidden.row(i,poss_vals,sudoku_board)
            for j in range(9):
                poss_vals = Hidden.col(j,poss_vals,sudoku_board)

            for box_j in range(3):
                for box_i in range(3):       
                    poss_vals = Hidden.box(box_i, box_j, poss_vals, sudoku_board)

            # Running Naked pairs/triples/quads on rows/columns/boxes

            for box_j in range(3):
                for box_i in range(3):
                    poss_vals = Naked.box(box_i, box_j, poss_vals, sudoku_board)

            for i in range(9):
                poss_vals = Naked.row(i, poss_vals, sudoku_board)

            for j in range(9):
                poss_vals = Naked.col(j, poss_vals, sudoku_board)

            # Running box_line_reduction
            poss_vals = RemovePossVals.box_line_reduction(poss_vals, sudoku_board)

            # Checking for singletons in poss_vals
            poss_vals = Naked.singles(poss_vals,sudoku_board)

            # Running x-wing
            poss_vals = ToughStrategies.x_wing(poss_vals,sudoku_board)
            
            # Updating number of blank squares
            
        filled_locs = np.argwhere(sudoku_board != 0)
        num_blank_squares = len(filled_locs)
        num_iterations += 1
            
            # Conditions for rinting 
        
        if num_blank_squares != num_squares_store[-1]: # If sudoku board isn't the same as previous iteration, reprint
            if num_blank_squares != 81:
                print(f'Iteration {num_iterations}:') 
                print("\n", sudoku_board, "\n")

        if num_blank_squares == 81:

            # Final Error Check
            for val in range(1,10):
                    # Column Check
                for j in range(9):
                    val_loc_col = np.argwhere(sudoku_board[:,j] == val)
        
                    if len(val_loc_col) > 1:
                        print(f'Code Error: Same value occured twice in column {j}')
    
                    # Row Check
    
                for i in range(9):
                    val_loc_row = np.argwhere(sudoku_board[i] == val)
    
                    if len(val_loc_row) > 1:
                        print(f'Code Error: Same value occured twice in row {i}')
    
                    # Box Check
    
                for box_j in range(3):
                    for box_i in range(3):
                        val_loc_box = np.argwhere(sudoku_board[3*box_j:3*box_j+3,3*box_i:3*box_i+3] == val)

                        if len(val_loc_box) > 1: 
                            print(f'Code Error: Same value occured twice in box {box_i, box_j}')

            print("Completed Sudoku Board")
            print("\n", sudoku_board, "\n")

        num_squares_store.append(num_blank_squares)

    # Stopping stopwatch

    end_time = time.time()

    time_elapsed = end_time - start_time # Since time.time() takes time from a specfic point (Jan 1 1970)
    if num_blank_squares != 81:
        print(f'Number of iterations = {num_iterations-1}') # Accounting for rerun condition
    elif num_blank_squares == 81: 
        print(f'Number of iterations = {num_iterations}')
    print(f'Time elapsed = {time_elapsed} \n')
    

print("\n Initial Sudoku Board \n\n", sudoku_board, "\n")

solve_puzzle(sudoku_board, poss_vals) 