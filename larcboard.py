

#this is assume 4 x 4

def get_square(click_x, click_y)->(int,int):

    if click_y in range(0,25):
        row = 0

    elif click_y in range(25,50):
        row = 1

    elif click_y in range(50,75):
        row = 2

    elif click_y in range(75,100):
        row = 3


    if click_x in range(0,25):
        col = 0

    elif click_x in range(25,50):
        col = 2

    elif click_x in range(50, 75):
        col = 3

    elif click_x in range(75,100):
        col = 4

    return row, col

# new get_square

def new_get_square(click_x,click_y)->(int,int):

    row_space = 1/ROWS*(heightinfo)# need windowheightinfo

    for row_num in range(ROW):
        if click_y in range(row_space*row_num, row_space*(row_num+1):
                            row= row_num

    for col_num in range(COLS):
        if clicke_x in range(col_space*col_num,col_space*(col_num+1):
                             col = col_num

#make windowheightinfo a attribute in class.

#__drawline and draworal oral 

                             
