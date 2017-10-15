#ICS 32 project 4 
#Deming Hao
#60943573

class OutOfBoundError(Exception):
    '''Raise whenever an invalid column and row number made'''
    pass

class InvalidMoveError(Exception):
    '''Raise whenever an invalid move is made'''
    pass

class GameOverError(Exception):
    '''Raise whenever an attempt is made to make a move after the game is already over'''
    pass


class status:
    
    def __init__(self, number_of_column, number_of_row):
        '''initalize board status'''
        self.number_of_column = number_of_column
        self.number_of_row = number_of_row
        self.direction = [[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]]
        self.black = 0
        self.white = 0
        self.blank = 0
        self.winner = ''
        self.is_gameover = False
        self.area = max(number_of_column, number_of_row)


    def position_on_board(self, number_of_row, number_of_column, top):
        '''get the number of rows and columns on the baord'''
        
        board = []
        for row in range(number_of_row):        
            board.append([])
            for column in range(number_of_column):               
                board[-1].append(0)


        if top == 'B':
            board[int(number_of_row/2-1)][int(number_of_column/2-1)] = 1
            board[int(number_of_row/2)][int(number_of_column/2)] = 1
            board[int(number_of_row/2-1)][int(number_of_column/2)] = 2
            board[int(number_of_row/2)][int(number_of_column/2-1)] = 2
        elif top == 'W':
            board[int(number_of_row/2-1)][int(number_of_column/2-1)] = 2
            board[int(number_of_row/2)][int(number_of_column/2)] = 2
            board[int(number_of_row/2-1)][int(number_of_column/2)] = 1
            board[int(number_of_row/2)][int(number_of_column/2-1)] = 1
        self.black = 2
        self.white = 2
        
        return board


    def change_turns(self, turn, board, win):
        '''
        take turns if there is no valid move for one player chagne back
        to the other play, if both has no valid move then, game over. 
        '''
        if turn == 'B':
                turn = 'W'
        elif turn == 'W':
                turn = 'B'
        if self._has_valid_move(board, turn):
            return turn
        else:
            if turn == 'B':
                turn = 'W'
            elif turn == 'W':
                turn = 'B'
                
            if not self._has_valid_move(board, turn):
                self._check_winner(win)
                self.is_gameover = True
           
            else:
                return turn
        

    def make_a_move(self, board, row, column, turn):
        '''
        check if it is a valid move if it is drop the move, else,
        raise Errors
        '''
        if self.is_gameover == True:
            raise GameOverError()
        if not self._require_valid_move(row, column):
            raise OutOfBoundError()
            
        else:
            if self._check_move(board, row, column, turn):
                self._flip(board, row, column, turn)
                if turn == 'B':
                    board[row][column] = 1
                elif turn == 'W':
                    board[row][column] = 2
                return True
                
            else:
                raise InvalidMoveError()

     
    def _require_valid_move(self, row, column):
        '''Raise a ValueError if its parameter is not a valid column and row number'''
        if not self._is_valid_column_number(column, self.number_of_column)\
           or not self._is_valid_row_number(row, self.number_of_row):
        
            return False
        else:
            return True

        
    def _is_valid_column_number(self, column, number_of_column):
        '''return true if the given column is valid'''
        return 0 <= column < number_of_column
  

    def _is_valid_row_number(self, row, number_of_row):
        '''return true if the given row is valid '''
        return 0 <= row < number_of_row


    def _check_move(self, board, row, column, turn):
        '''check all move in every directions'''
        for i in self.direction:
            if self._check_dir(board, turn, row, column, i):
                return True            
        return False

                                              
    def _flip(self, board, row, column, turn):
        '''
        flip all opponent discs between two of yours in any directions
        if it is valid move 
        '''
        for vec in self.direction:
            if self._check_dir(board, turn, row, column, vec):
                if turn == 'B':
                    for n in range(1, self.area):
                        if self._require_valid_move(row+vec[0]*n, column+vec[1]*n):
                            if board[row+vec[0]*n][column+vec[1]*n] == 2:
                                board[row+vec[0]*n][column+vec[1]*n] = 1
                            else:
                                break
                        
                if turn == 'W':
                    for n in range(1, self.area):
                        if self._require_valid_move(row+vec[0]*n, column+vec[1]*n):
                            if board[row+vec[0]*n][column+vec[1]*n] == 1:
                                board[row+vec[0]*n][column+vec[1]*n] = 2
                            else:
                                break
                        
              
    def _check_dir(self, board, turn, row, column, vec):
        """
        check valid move on each direction 
        """
        drop_point = board[row][column]

        if drop_point != 0:          
            return False
      
        if turn == 'B':
            if  self.number_of_row > row+vec[0] >= 0 and self.number_of_column > column+vec[1] >= 0:
                if board[row + vec[0]][column + vec[1]] != 2:
                    return False
                else:
                     for n in range(2, self.area):
                         if self._require_valid_move(row+vec[0]*n, column+vec[1]*n):
                             if board[row+vec[0]*n][column+vec[1]*n] == 1:
                                 return True
                             elif board[row+vec[0]*n][column+vec[1]*n] == 0:
                                 return False
                     return False
                    
        if turn == 'W':
            if self.number_of_row > row+vec[0] >= 0 and self.number_of_column > column+vec[1] >= 0:
                 if board[row+vec[0]][column+vec[1]] != 1: 
                     return False
                 else:
                     for n in range(2, self.area):
                         if self._require_valid_move(row+vec[0]*n, column+vec[1]*n):
                             if board[row+vec[0]*n][column+vec[1]*n] == 2:
                                 return True                            
                             elif board[row+vec[0]*n][column+vec[1]*n] == 0:
                                 return False
                     return False
                         

    def _has_valid_move(self, board, turn):
        '''
        check all space on board if there is any valid move. if not
        return false 
        '''
        for row in range(self.number_of_row):
            for col in range(self.number_of_column):
                if self._check_move(board, row, col, turn):
                    return True
        return False
    

    def update_score(self, board, win):
        '''
        show numbers of black and white after each move
        determine winner if there no valid move
        '''
        self.black = 0
        self.white = 0
        self.blank = 0

                  
        for row in range(self.number_of_row):
            for col in range(self.number_of_column):
     
                if board[row][col] == 1:
                    self.black += 1 
                elif board[row][col] == 2:
                    self.white += 1
                elif board[row][col] == 0:
                    self.blank += 1






    def _check_winner(self, win):
        '''
        neither player will have a valid move on board and there are more empty
        cells in the grid.         
        '''                           
        if win == '>':
            if self.black > self.white:
                self.winner = 'B'
            elif self.white > self.black:
                self.winner = 'W'
            elif self.white == self.black:
                self.winner = 'NONE'                
                
        elif win == '<':
            if self.black < self.white:
                self.winner = 'B'
            elif self.white < self.black:
                self.winner = 'W'
            elif self.white == self.black:
                self.winner = 'NONE'

 



        
                
       

                
            
            

            
  


                
