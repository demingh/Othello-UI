import tkinter
import math
import othello
DEFAULT_FONT = ('Helvetica', 14)

class othelloview:
    def __init__(self, rows, cols,turn,win):
        '''initialized a othelloview GUI object'''
        
        self._root_window = tkinter.Tk()
        self._root_window.title('FULL')
        self._game= othello.status(int(setting.column_number), int(setting.row_number))
        self._rows = rows
        self._cols = cols
        self._board = self._game.position_on_board(int(setting.row_number), int(setting.column_number),setting.top)
        self._turn = turn        
        self._win = win
        
        
        self._root_canvas = tkinter.Canvas(
            master = self._root_window, width = 300, height = 350,
            background = '#008000')

        self.canvas_width = self._root_canvas.winfo_width()
        self.canvas_height = self._root_canvas.winfo_height()
        
        self.score = tkinter.StringVar()
    
        self._score_label = tkinter.Label(
            master = self._root_window, textvariable = self.score,
            font = ('Helvetica',24))
        self.score.set("BLACK: 2 WHITE: 2")

        self._score_label.grid(
        row = 0, column = 0, padx = 5, pady = 5,
        sticky = tkinter.W)

        self.show_turn = tkinter.StringVar()

        self._show_turn = tkinter.Label(
            master = self._root_window, textvariable =self.show_turn,
            font =DEFAULT_FONT)

        if self._turn =='B':
                 self.show_turn.set('TURN: Black')
        elif self._turn =='W':
                 self.show_turn.set('TURN: White')
   

        self._show_turn.grid(
            row = 3, column = 0, padx =5, pady =5,
            sticky = tkinter.E)

        self._valid_move = tkinter.StringVar()
        
        self._valid_move.set('Please make a move')
        self._show_valid = tkinter.Label(
            master = self._root_window, textvariable = self._valid_move,
            font= DEFAULT_FONT)
        self._show_valid.grid(
            row =1, column = 0, padx =5, pady = 5,
            sticky = tkinter.N)
        

        self._root_canvas.grid(
            row = 2 , column = 0, padx = 5, pady =5,
            sticky = tkinter.N +tkinter.S + tkinter.W + tkinter.E)  
        
        self._root_canvas.bind('<Button-1>',self._on_canvas_clicked)
        self._root_canvas.bind('<Configure>',self._on_canvas_resized)

        self._root_window.rowconfigure(0,weight = 0)
        self._root_window.rowconfigure(1,weight = 0)         
        self._root_window.rowconfigure(2, weight = 1)
        self._root_window.rowconfigure(3, weight = 0)
        self._root_window.columnconfigure(0, weight = 1)
        
    def _on_canvas_clicked(self,event: tkinter.Event) -> None:
        '''make a move when click if there is any valid move'''

        try:
            row,col = self._get_square(event.x,event.y)
            if self._game.make_a_move(self._board,row-1,col-1,self._turn):
                self._draw_circle(row,col,self._turn)
                self._valid_move.set("valid move")
                
                
        except(othello.InvalidMoveError,othello.GameOverError):
            self._valid_move.set("Invalid move, try again!")
            return
        
        self._turn = self._game.change_turns(self._turn,self._board,self._win)
        
        if self._game.is_gameover == True:
            if self._game.winner =='B':
                self.show_turn.set('WINNER: Black')
            elif self._game.winner =='W':
                self.show_turn.set('WINNER: White')
            elif self._game.winner =='NONE':
                self.show_turn.set('WINNER: NONE')
            
        if self._turn =='B':
                 self.show_turn.set('TURN: Black')
        elif self._turn =='W':
                 self.show_turn.set('TURN: White')
        
        self._re_draw_board()
               
    
    def _on_canvas_resized(self,event:tkinter.Event) -> None:
        '''call get board and re_draw_board funcation when resized the window'''
        self._get_board()
        self._re_draw_board()
        

    def _get_board(self):
        '''print board with grid'''
        
        self._root_canvas.delete(tkinter.ALL)        
        row_space = 1/self._rows*(self._root_canvas.winfo_height())        
        col_space = 1/self._cols*(self._root_canvas.winfo_width())
       
        for row_num in range(self._rows):
            for col_num in range(self._cols):
                self._root_canvas.create_line(
                    col_space*col_num, row_space*(row_num),
                    col_space*col_num,row_space*(self._rows-row_num) ,fill ='black')

        for col_num in range(self._cols):
            for row_num in range(self._rows):
                self._root_canvas.create_line(
                    col_space*(col_num),row_space*row_num,
                    col_space*(self._cols-col_num),row_space*row_num,fill ='black')
                       

    def _get_square(self,click_x,click_y)-> ( int,int):
        '''get column and row infomation when click happened'''
        
        row_space = 1/self._rows*(self._root_canvas.winfo_height())
        col_space = 1/self._cols*(self._root_canvas.winfo_width())

        for row_num in range(self._rows):
            if click_y in range(int(row_space*row_num),int(row_space*(row_num+1))):
                                row= row_num+1
    
        for col_num in range(self._cols):
            if click_x in range(int(col_space*col_num),int(col_space*(col_num+1))):
                                col = col_num+1

        return(row, col)
    

    def _draw_circle(self,row,col,turn):
        '''draw a disc as a circle'''
        
        if turn =='B':
            color = 'black'
            color_outline ='white'
        elif turn =='W':
            color ='white'
            color_outline ='black'
       
        self._root_canvas.create_oval(
            (col-1)*1/self._cols*(self._root_canvas.winfo_width()),
            (row-1)*1/self._rows*(self._root_canvas.winfo_height()),
            (col)*1/self._cols*(self._root_canvas.winfo_width()),
            (row)*1/self._rows*(self._root_canvas.winfo_height())
            ,outline=color_outline, fill=color)

        
    def _re_draw_board(self):
        '''draw the board again after move'''

        for row in range(self._rows):
            for col in range(self._cols):
                if self._board[row][col] == 1:
                    self._root_canvas.create_oval(
                    (col)*1/self._cols*(self._root_canvas.winfo_width()),
                    (row)*1/self._rows*(self._root_canvas.winfo_height()),
                    (col+1)*1/self._cols*(self._root_canvas.winfo_width()),
                    (row+1)*1/self._rows*(self._root_canvas.winfo_height())
                    ,outline='white',fill='black')
                elif self._board[row][col] == 2:
                    self._root_canvas.create_oval(
                    (col)*1/self._cols*(self._root_canvas.winfo_width()),
                    (row)*1/self._rows*(self._root_canvas.winfo_height()),
                    (col+1)*1/self._cols*(self._root_canvas.winfo_width()),
                    (row+1)*1/self._rows*(self._root_canvas.winfo_height())
                    ,outline='black',fill='white')

        self._game.update_score(self._board,self._win)
        black_score = self._game.black
        white_score = self._game.white

        self.score.set('BLACK: '+str(black_score)+' WHITE: '+str(white_score))        
        
    def run(self) -> None:
        self._root_window.mainloop()
        
 
class settingDialog:
    def __init__(self):
        '''create a setting dialog window get infomation from user'''

        self._dialog_window = tkinter.Tk() 
        self._dialog_window.title("Set Your Game")
            
        self.dialog_label = tkinter.Label(
            master = self._dialog_window, text= ' Welcom to Othello FULL verison ',
            font =('Helvetica', 20))

        self.dialog_label.grid(
            row = 0, column = 0, columnspan = 2, padx = 20, pady = 20,
            sticky = tkinter.W+tkinter.E)

        self.row_number_label = tkinter.Label(
            master = self._dialog_window, text ='Row =',
            font = DEFAULT_FONT)

        self.row_number_label.grid(
            row = 1, column = 0, padx = 10, pady = 5,
            sticky = tkinter.W)

        self._row = tkinter.StringVar()
        self._row_number_enter = tkinter.OptionMenu(
            self._dialog_window,self._row,'4','6','8','10','12','14','16')

        self._row_number_enter.grid(
            row = 1, column =1, padx = 10, pady = 10,
            sticky = tkinter.W + tkinter.E)

        self.column_number_label = tkinter.Label(
            master = self._dialog_window, text ='Column =',
            font = DEFAULT_FONT)

        self.column_number_label.grid(
            row =2, column = 0, padx = 10, pady =10,
            sticky = tkinter.W )

        
        self._column = tkinter.StringVar()
        self._column_number_enter = tkinter.OptionMenu(
            self._dialog_window,self._column,'4','6','8','10','12','14','16')


        self._column_number_enter.grid(
            row = 2, column = 1, padx =10, pady = 5,
            sticky = tkinter.W + tkinter.E)         

        self.first_move_label = tkinter.Label(
            master = self._dialog_window, text ="Who's first",
            font = DEFAULT_FONT)

        self.first_move_label.grid(
            row = 3, column = 0, padx = 10, pady =5,
            sticky = tkinter.W)

        self.first_move_button_frame = tkinter.Frame(master = self._dialog_window)

        self.first_move_button_frame.grid(
            row = 3, column =0, columnspan =2, padx = 10, pady =5,
            sticky = tkinter.E)

        self.black_button = tkinter.Button(
            master = self.first_move_button_frame, text ='Black', font = DEFAULT_FONT,
            command = self._on_black_button)

        self.black_button.grid(row = 3, column = 0, padx= 10, pady = 5)

        self.white_button = tkinter.Button(
            master = self.first_move_button_frame, text = 'White', font = DEFAULT_FONT,
            command = self._on_white_button)

        self.white_button.grid(row = 3, column =1, padx = 10, pady = 5)

        self.top_left_pos_label = tkinter.Label(
            master = self._dialog_window, text ="who's on top",
            font = DEFAULT_FONT)

        self.top_left_pos_label.grid(
            row = 4, column = 0, padx = 10, pady = 5,
            sticky = tkinter.W)

        self.top_left_pos_frame = tkinter.Frame(master = self._dialog_window)

        self.top_left_pos_frame.grid(
            row = 4, column = 0 , columnspan =2, padx = 10, pady = 5,
            sticky = tkinter.E)

        self.black_button_1 = tkinter.Button(
            master = self.top_left_pos_frame, text ='Black', font = DEFAULT_FONT,
            command = self._on_black_button_1)

        self.black_button_1.grid(row = 4, column = 0, padx = 10, pady =5)

        self.white_button_1 = tkinter.Button(
            master = self.top_left_pos_frame, text ='White', font = DEFAULT_FONT,
            command = self._on_white_button_1)

        self.white_button_1.grid(row = 4, column = 1, padx = 10, pady = 5)

        self.win_condition_label = tkinter.Label(
            master = self._dialog_window, text = 'Win by: ',
            font = DEFAULT_FONT)

        self.win_condition_label.grid(
            row = 5, column = 0, padx= 10 , pady = 5,
            sticky = tkinter.W)

        self.win_condition_frame = tkinter.Frame(master = self._dialog_window)

        self.win_condition_frame.grid(
            row = 5, column = 0, columnspan = 2, padx = 10, pady = 5,
            sticky = tkinter.E)

        self.win_by_more_button = tkinter.Button(
            master = self.win_condition_frame, text = 'More ', font = DEFAULT_FONT,
            command = self._on_more_button)

        self.win_by_more_button.grid( row = 5, column = 0, padx = 10, pady = 5)

        self.win_by_less_button = tkinter.Button(
            master = self.win_condition_frame, text ='Less ', font = DEFAULT_FONT,
            command = self._on_less_button)

        self.win_by_less_button.grid(
            row =5, column = 1, columnspan =2, padx = 10, pady = 5,
            sticky = tkinter.E)

        self.game_button_frame = tkinter.Frame(master = self._dialog_window)

        self.game_button_frame.grid(
            row = 6, column =0 , columnspan = 2, padx = 10, pady = 5,
            sticky = tkinter.S)

        self.play_button = tkinter.Button(
            master = self.game_button_frame, text ='Play', font = DEFAULT_FONT,
            command = self._on_play_button)

        self.play_button.grid( row = 6, column = 0, padx = 10, pady = 5)

        self._dialog_window.rowconfigure(0, weight =0)
        self._dialog_window.rowconfigure(1, weight =1)
        self._dialog_window.rowconfigure(2, weight =1)
        self._dialog_window.rowconfigure(3, weight =1)
        self._dialog_window.rowconfigure(4, weight =1)
        self._dialog_window.rowconfigure(5, weight =1)
        self._dialog_window.rowconfigure(6, weight =1)
        self._dialog_window.columnconfigure(0, weight =1)
        self._dialog_window.columnconfigure(1, weight =1)
       
        self._ok_clicked = False
        self.row_number = 0
        self.column_number = 0
        self.first_move= ''
        self.top =''
        self.win_by = ''
        self.ready = False
       

    def _on_black_button(self):
        self._ok_clicked = True
        self.first_move ='B'
        self.black_button.configure(text ='selected')
        self.white_button.configure(text ='White')


    def _on_white_button(self):
        self._ok_clicked = True
        self.first_move = 'W'
        self.white_button.configure(text ='selected')
        self.black_button.configure(text ='Black')
        

    def _on_black_button_1(self):
        self._ok_clicked = True
        self.top = 'B'
        self.black_button_1.configure(text='selected')
        self.white_button_1.configure(text ='White')
        

    def _on_white_button_1(self):
        self._ok_clicked = True
        self.top = 'W'
        self.white_button_1.configure(text='selected')
        self.black_button_1.configure(text='Black')
        
        
    def _on_more_button(self):
        self._ok_clicked = True
        self.win_by ='>'
        self.win_by_more_button.configure(text='selected')
        self.win_by_less_button.configure(text='Less ')

        
    def _on_less_button(self):
        self._ok_clicked = True
        self.win_by ='<'
        self.win_by_less_button.configure(text='selected')
        self.win_by_more_button.configure(text='More ')
        

    def _on_play_button(self):
        self._ok_clicked = True
        try:
            self.row_number = int(self._row.get())
            self.column_number = int(self._column.get())
            if self.first_move == '':
                return
            elif self.top =='':
                return
            elif self.win_by =='':
                return
            self.ready=True
            self._dialog_window.destroy()
        except:
            pass
                

    def start(self) -> None:
        self._dialog_window.mainloop()


if __name__ == '__main__':

    setting = settingDialog()
    setting.start()
    if setting.ready == True:
        app = othelloview(int(setting.row_number), int(setting.column_number),setting.first_move,setting.win_by)
        app.run()
    
    
    





  
    
    


 
    
  
