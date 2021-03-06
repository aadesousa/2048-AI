import time
import random
from tkinter import Frame, Label, CENTER
import logic
import constants as c
from threading import Thread
class GameGrid(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.grid()
        self.master.title('2048')
        self.commands = {c.KEY_UP: logic.up, c.KEY_DOWN: logic.down,
                         c.KEY_LEFT: logic.left, c.KEY_RIGHT: logic.right,
                         c.KEY_UP_ALT: logic.up, c.KEY_DOWN_ALT: logic.down,
                         c.KEY_LEFT_ALT: logic.left,
                         c.KEY_RIGHT_ALT: logic.right}
        
        

        # self.gamelogic = gamelogic
        self.grid_cells = []
        self.init_grid()
        self.init_matrix()
        self.update_grid_cells()
        self.after(0, self.d)
        self.mainloop()
    
    def sx(self, m):
        return (sorted([item for sublist in m for item in sublist], reverse = True))[0]


    def d(self):
        while logic.game_state(self.matrix) != 'lose':
        #for x in range(100000):
            mlist = ["w", "s", "a", "d"]
            dic= {0 : logic.up(self.matrix)[0],
                  1 : logic.down(self.matrix)[0],
                  2 : logic.left(self.matrix)[0],
                  3 : logic.right(self.matrix)[0]}
            up = logic.up(self.matrix)[0]
            down = logic.down(self.matrix)[0]
            left = logic.left(self.matrix)[0]
            right = logic.right(self.matrix)[0]
            actt=[self.sx(up), self.sx(down), self.sx(left), self.sx(right)]
            max_val = max(actt)
            maxact=[i for i, x in enumerate(actt) if x == max_val]
            acttt= []
            #time.sleep(1)
            for maxx in maxact:
                if logic.game_state(dic[maxx]) != 'lose':
                    acttt.append(maxact.index(maxx))
                
            #max_val = max(act)
            #actt = [i for i, x in enumerate(act) if x == max_val]
            
            if len(acttt) > 0:
                self.key_down(mlist[random.choice(acttt)])
            elif len(actt) == 0:
                self.key_down(random.choice(mlist))
            #time.sleep(.5)
        if logic.game_state(dic[0]) == 'lose' and logic.game_state(dic[1]) == 'lose' and logic.game_state(dic[2]) == 'lose' and logic.game_state(dic[3]) == 'lose':
            logic.new_game(4)
    
        
    def init_grid(self):
        background = Frame(self, bg=c.BACKGROUND_COLOR_GAME,
                           width=c.SIZE, height=c.SIZE)
        background.grid()

        for i in range(c.GRID_LEN):
            grid_row = []
            for j in range(c.GRID_LEN):
                cell = Frame(background, bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                             width=c.SIZE / c.GRID_LEN,
                             height=c.SIZE / c.GRID_LEN)
                cell.grid(row=i, column=j, padx=c.GRID_PADDING,
                          pady=c.GRID_PADDING)
                t = Label(master=cell, text="",
                          bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                          justify=CENTER, font=c.FONT, width=5, height=2)
                t.grid()
                grid_row.append(t)

            self.grid_cells.append(grid_row)

    def gen(self):
        return random.randint(0, c.GRID_LEN - 1)

    def init_matrix(self):
        self.matrix = logic.new_game(4)
        self.history_matrixs = list()
        self.matrix = logic.add_two(self.matrix)
        self.matrix = logic.add_two(self.matrix)

    def update_grid_cells(self):
        for i in range(c.GRID_LEN):
            for j in range(c.GRID_LEN):
                new_number = self.matrix[i][j]
                if new_number == 0:
                    self.grid_cells[i][j].configure(
                        text="", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                else:
                    self.grid_cells[i][j].configure(text=str(
                        new_number), bg=c.BACKGROUND_COLOR_DICT[new_number],
                        fg=c.CELL_COLOR_DICT[new_number])
        self.update_idletasks()

    def key_down(self, event):
        key = repr(event)
        if key == c.KEY_BACK and len(self.history_matrixs) > 1:
            self.matrix = self.history_matrixs.pop()
            self.update_grid_cells()
            print('back on step total step:', len(self.history_matrixs))
        elif key in self.commands:
            self.matrix, done = self.commands[repr(event)](self.matrix)
            if done:
                self.matrix = logic.add_two(self.matrix)
                # record last move
                self.history_matrixs.append(self.matrix)
                self.update_grid_cells()
                return self.matrix
                done = False
                if logic.game_state(self.matrix) == 'win':
                    self.grid_cells[1][1].configure(
                        text="You", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[1][2].configure(
                        text="Win!", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                if logic.game_state(self.matrix) == 'lose':
                    self.grid_cells[1][1].configure(
                        text="You", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[1][2].configure(
                        text="Lose!", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
    def generate_next(self):
        index = (self.gen(), self.gen())
        while self.matrix[index[0]][index[1]] != 0:
            index = (self.gen(), self.gen())
        self.matrix[index[0]][index[1]] = 2
    
    
gamegrid = GameGrid()
#mlist= ["w", "a", "s", "d"]
#key_down(mlist[random.randint(0, 3)])