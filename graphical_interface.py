#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Modified from https://github.com/johnafish/othello

# This code was originally created by John Fish

# Now used by Nemo ( BO-YU, Cheng) on 2021/7/21

# This code is based on works licensed under the following terms.
#
#     The MIT License (MIT)
#
#     Copyright (c) 2015 John Fish
#
#     Permission is hereby granted, free of charge, to any person obtaining a copy
#     of this software and associated documentation files (the "Software"), to deal
#     in the Software without restriction, including without limitation the rights
#     to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#     copies of the Software, and to permit persons to whom the Software is
#     furnished to do so, subject to the following conditions:
#
#     The above copyright notice and this permission notice shall be included in all
#     copies or substantial portions of the Software.
#
#     THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#     IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#     FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#     AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#     LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#     OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#     SOFTWARE.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#



from tkinter import *
from math import *
from time import *
import othello
from alpha_beta_agent import AlphaBetaAgent
from mcts_agent import MCTSAgent

class GUI:
    def __init__(self):
        #Tkinter setup
        self.root = Tk()
        self.screen = Canvas(self.root, width=500, height=600, background="#222",highlightthickness=0)
        self.screen.pack()
        #Binding, setting
        self.screen.bind("<Button-1>", self.clickHandle)
        self.screen.bind("<Key>",self.keyHandle)
        self.screen.focus_set()


    def startMenu(self):
        #show menu
        self.showMenu()
        self.isInMenu = True

    def showMenu(self):
        self.screen.delete(ALL)
        #Title and shadow
        self.screen.create_text(250,203,anchor="c",text="Othello",font=("Consolas", 50),fill="#aaa")
        self.screen.create_text(250,200,anchor="c",text="Othello",font=("Consolas", 50),fill="#fff")
        #Creating the difficulty buttons
        for i in range(3):
            #Background
            self.screen.create_rectangle(25+155*i, 310, 155+155*i, 355, fill="#000", outline="#000")
            self.screen.create_rectangle(25+155*i, 300, 155+155*i, 350, fill="#111", outline="#111")
            spacing = 130/(i+2)
            for x in range(i+1):
                #Star with double shadow
                self.screen.create_text(25+(x+1)*spacing+155*i,326,anchor="c",text="\u2605", font=("Consolas", 25),fill="#b29600")
                self.screen.create_text(25+(x+1)*spacing+155*i,327,anchor="c",text="\u2605", font=("Consolas",25),fill="#b29600")
                self.screen.create_text(25+(x+1)*spacing+155*i,325,anchor="c",text="\u2605", font=("Consolas", 25),fill="#ffd700")
        self.screen.update()

    def showButtons(self):
        #Restart button
        #Background/shadow
        self.screen.create_rectangle(0,5,50,55,fill="#000033", outline="#000033")
        self.screen.create_rectangle(0,0,50,50,fill="#000088", outline="#000088")
        #Arrow
        self.screen.create_arc(5,5,45,45,fill="#000088", width="2",style="arc",outline="white",extent=300)
        self.screen.create_polygon(33,38,36,45,40,39,fill="white",outline="white")
        #Quit button
        #Background/shadow
        self.screen.create_rectangle(450,5,500,55,fill="#330000", outline="#330000")
        self.screen.create_rectangle(450,0,500,50,fill="#880000", outline="#880000")
        #"X"
        self.screen.create_line(455,5,495,45,fill="white",width="3")
        self.screen.create_line(495,5,455,45,fill="white",width="3")

    def drawBoardGrid(self, outline=True):
        if outline:
            self.screen.create_rectangle(50,50,450,450,outline="#000")
        #Drawing the intermediate lines
        for i in range(7):
            lineShift = 50+50*(i+1)
            #Horizontal line
            self.screen.create_line(50,lineShift,450,lineShift,fill="#000")
            #Vertical line
            self.screen.create_line(lineShift,50,lineShift,450,fill="#000")

    def clickHandle(self,event):
        xMouse = event.x
        yMouse = event.y
        #  In board game
        if not  self.isInMenu :
            if xMouse>=450 and yMouse<=50:
                self.root.destroy()
            elif xMouse<=50 and yMouse<=50:
                self.startGame()
            else:
                #Is it the player's turn?
                if self.game.next_player==othello.Player.LIGHT:
                    #Delete the highlights
                    x = int((event.x-50)/50)
                    y = int((event.y-50)/50)
                    #Determine the grid index for where the mouse was clicke
                    #If the click is inside the bounds and the move is valid, move to that location
                    if 0<=x<=7 and 0<=y<=7:
                        #print(x,y)
                        moves = self.game.state.get_legal_actions(self.game.next_player)
                        moves = [(m.coords.file, m.coords.rank) for m in moves]
                        if (x,y) in moves:
                            #print('valid move!')
                            self.respond_player((x,y))
        # In menu
        else:
            #Difficulty clicking
            if 300<=yMouse<=350:
                #One star
                if 25<=xMouse<=155:
                    self.AI = AlphaBetaAgent(othello.Player.DARK, search_depth=2)
                #Two star
                elif 180<=xMouse<=310:
                    self.AI = MCTSAgent(othello.Player.DARK, n_iters=100)
                #Three star
                elif 335<=xMouse<=465:
                    self.AI = MCTSAgent(othello.Player.DARK, n_iters=200)
                self.isInMenu = False
                print('game start!')
                self.startGame()


    def keyHandle(self, event):
        symbol = event.keysym
        if symbol.lower()=="r":
            self.startGame()
        elif symbol.lower()=="q":
            self.root.destroy()

    def startGame(self):
        self.screen.delete(ALL)
        self.showButtons()
        self.drawBoardGrid()
        self.game = othello.Game()
        self.game.next_player = othello.Player.LIGHT
        self.showGame()

    def restart(self):
        self.screen.delete(ALL)
        self.isInMenu = True
        self.showMenu()


    def mainloop(self):
        #Run forever
        self.root.wm_title("Othello")
        self.root.mainloop()

    def showGame(self):
        self.screen.delete("highlight")
        self.screen.delete("tile")
        # draw black and white peices
        for x in range(8):
            for y in range(8):
                c = othello.Coords.from_file_rank(x,y)
                if self.game.state.board[c] == othello.Player.LIGHT:
                    self.screen.create_oval(54+50*x,54+50*y,96+50*x,96+50*y,tags="tile {0}-{1}".format(x,y),fill="#aaa",outline="#aaa")
                    self.screen.create_oval(54+50*x,52+50*y,96+50*x,94+50*y,tags="tile {0}-{1}".format(x,y),fill="#fff",outline="#fff")
                elif self.game.state.board[c] == othello.Player.DARK:
                    self.screen.create_oval(54+50*x,52+50*y,96+50*x,94+50*y,tags="tile {0}-{1}".format(x,y),fill="#111",outline="#111")
                    self.screen.create_oval(54+50*x,54+50*y,96+50*x,96+50*y,tags="tile {0}-{1}".format(x,y),fill="#000",outline="#000")
                else:
                    pass
        # highlight possible next moves
        moves = self.game.state.get_legal_actions(self.game.next_player)
        moves = [(m.coords.file, m.coords.rank) for m in moves]
        for x,y in moves:
            self.screen.create_oval(68+50*x,68+50*y,32+50*(x+1),32+50*(y+1),tags="highlight",fill="#008000",outline="#008000")
        self.screen.update()

    def respond_player(self,move):
        self.animate_and_perform_action(move)
        self.highlight_next_moves()
        self.update_score_board()
        self.check_game_end()
        while True :
            act = self.AI.play(self.game.state)
            if act is not None:
                x,y = act.coords.file, act.coords.rank
                self.animate_and_perform_action((x,y))
                self.highlight_next_moves()
                self.update_score_board()
                self.check_game_end()
            else:
                self.game.play(self.game.next_player,None)
                self.highlight_next_moves()
                self.update_score_board()

            if all(False for _ in self.game.state.get_legal_actions(self.game.next_player)):
                self.game.play(self.game.next_player,None)
                self.highlight_next_moves()
                self.update_score_board()
            else:
                break


    def animate_and_perform_action(self,move):
        # clear highlight element
        self.screen.delete("highlight")
        action = othello.Action(othello.Coords.from_file_rank(*move))
        x,y = move
        # first change the peice at action
        if self.game.next_player == othello.Player.LIGHT:
            self.screen.create_oval(54+50*x,54+50*y,96+50*x,96+50*y,tags="tile {0}-{1}".format(x,y),fill="#aaa",outline="#aaa")
            self.screen.create_oval(54+50*x,52+50*y,96+50*x,94+50*y,tags="tile {0}-{1}".format(x,y),fill="#fff",outline="#fff")
        else :
            self.screen.create_oval(54+50*x,54+50*y,96+50*x,96+50*y,tags="tile {0}-{1}".format(x,y),fill="#000",outline="#000")
            self.screen.create_oval(54+50*x,52+50*y,96+50*x,94+50*y,tags="tile {0}-{1}".format(x,y),fill="#111",outline="#111")
        self.screen.update()
        flip_mask = self.game.state.get_flips(self.game.next_player,action)

        for x in range(8):
            for y in range(8):
                if 0x1<<othello.Coords.from_file_rank(x,y).ix & flip_mask != 0:
                    if self.game.next_player == othello.Player.LIGHT:
                        self.screen.delete("{0}-{1}".format(x,y))
                        #42 is width of tile so 21 is half of that
                        #Shrinking
                        for i in range(21):
                            self.screen.create_oval(54+i+50*x,54+i+50*y,96-i+50*x,96-i+50*y,tags="tile animated",fill="#000",outline="#000")
                            self.screen.create_oval(54+i+50*x,52+i+50*y,96-i+50*x,94-i+50*y,tags="tile animated",fill="#111",outline="#111")
                            if i%3==0:
                                sleep(0.01)
                            self.screen.update()
                            self.screen.delete("animated")
                        #Growing
                        for i in reversed(range(21)):
                            self.screen.create_oval(54+i+50*x,54+i+50*y,96-i+50*x,96-i+50*y,tags="tile animated",fill="#aaa",outline="#aaa")
                            self.screen.create_oval(54+i+50*x,52+i+50*y,96-i+50*x,94-i+50*y,tags="tile animated",fill="#fff",outline="#fff")
                            if i%3==0:
                                sleep(0.01)
                            self.screen.update()
                            self.screen.delete("animated")
                        self.screen.create_oval(54+50*x,54+50*y,96+50*x,96+50*y,tags="tile {0}-{1}".format(x,y),fill="#aaa",outline="#aaa")
                        self.screen.create_oval(54+50*x,52+50*y,96+50*x,94+50*y,tags="tile {0}-{1}".format(x,y),fill="#fff",outline="#fff")
                        self.screen.update()
                    # next_player is DARK
                    else:
                        self.screen.delete("{0}-{1}".format(x,y))
                        #42 is width of tile so 21 is half of that
                        #Shrinking
                        for i in range(21):
                            self.screen.create_oval(54+i+50*x,54+i+50*y,96-i+50*x,96-i+50*y,tags="tile animated",fill="#aaa",outline="#aaa")
                            self.screen.create_oval(54+i+50*x,52+i+50*y,96-i+50*x,94-i+50*y,tags="tile animated",fill="#fff",outline="#fff")
                            if i%3==0:
                                sleep(0.01)
                            self.screen.update()
                            self.screen.delete("animated")
                        #Growing
                        for i in reversed(range(21)):
                            self.screen.create_oval(54+i+50*x,54+i+50*y,96-i+50*x,96-i+50*y,tags="tile animated",fill="#000",outline="#000")
                            self.screen.create_oval(54+i+50*x,52+i+50*y,96-i+50*x,94-i+50*y,tags="tile animated",fill="#111",outline="#111")
                            if i%3==0:
                                sleep(0.01)
                            self.screen.update()
                            self.screen.delete("animated")
                        self.screen.create_oval(54+50*x,54+50*y,96+50*x,96+50*y,tags="tile {0}-{1}".format(x,y),fill="#000",outline="#000")
                        self.screen.create_oval(54+50*x,52+50*y,96+50*x,94+50*y,tags="tile {0}-{1}".format(x,y),fill="#111",outline="#111")
                        self.screen.update()
        # update game state after animation
        self.game.play(self.game.next_player,action)

    def highlight_next_moves(self):
        # highlight possible next moves
        moves = self.game.state.get_legal_actions(self.game.next_player)
        moves = [(m.coords.file, m.coords.rank) for m in moves]
        if self.game.next_player == othello.Player.LIGHT:
            highlight_color = '#008000'
        else:
            highlight_color = '#800000'
        for x,y in moves:
            self.screen.create_oval(68+50*x,68+50*y,32+50*(x+1),32+50*(y+1),tags="highlight",fill=highlight_color,outline=highlight_color)
        self.screen.update()

    def check_game_end(self):
        winner = self.game.get_conclusion()
        if winner is None:
            return
        msg = ''
        if winner is othello.Player.LIGHT:
            msg = 'WHIGHT Wins!'
        if winner is othello.Player.DARK:
            msg = 'BLACK Wins!'
        if winner is othello.DRAW:
            msg = 'DRAW!'
        self.screen.create_rectangle(150,535,350,565,outline="#111",fill='#111')
        self.screen.create_text(250,550,anchor="c",font=("Consolas",20), text=msg,fill="#008000")
        self.screen.update()
    def update_score_board(self):
        self.screen.delete('score')
        w_score = self.game.get_score(othello.Player.LIGHT)
        b_score = self.game.get_score(othello.Player.DARK)
        if self.game.next_player == othello.Player.LIGHT:
            w_color = 'green'
            b_color = 'gray'
        else:
            w_color = 'gray'
            b_color = 'green'
        self.screen.create_oval(5,540,25,560,tags="score",fill=w_color,outline=w_color)
        self.screen.create_oval(380,540,400,560,tags="score",fill=b_color,outline=b_color)
        #Pushing text to screen
        self.screen.create_text(30,550,anchor="w", tags="score",font=("Consolas", 50),fill="white",text=w_score)
        self.screen.create_text(400,550,anchor="w", tags="score",font=("Consolas", 50),fill="black",text=b_score)
        self.screen.update()




if __name__ == "__main__":
    gui = GUI()
    gui.startMenu()
    gui.mainloop()
