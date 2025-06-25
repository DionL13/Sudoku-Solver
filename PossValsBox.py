def func(box_i, box_j, val, poss_vals):
    '''
    Initialises all locations of a possible value in a single box for poss_vals
    '''
    
    top_row, middle_row, bottom_row = [],[],[]
    poss_vals_box = [top_row, middle_row, bottom_row]

    for i_box in range(3):
        for j_box in range(3):
                global_j = 3*box_j+j_box
                global_i = 3*box_i+i_box

                poss_vals_box[i_box].append(poss_vals[global_i][global_j])

    val_loc = [(i,j) 
               for i, row in enumerate(poss_vals_box)
               for j, cell in enumerate(row)
               if val in cell
              ] # i,row enumerate gives (index, row of poss_vals_box), then for each index j of the row, each element is a cell. 

    return val_loc, poss_vals_box