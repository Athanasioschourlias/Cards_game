import Playing_Cards
import tkinter as tk
import PIL
import time
import random
from os.path import join
from tkinter.messagebox import *
path = "."

class CardGameGui(tk.Frame):
    def __init__(self, root):
        ### Game parameteres
        root.title("Cards game V2.0.0")
        root.resizable(width='false', height='false')
        self.d = Playing_Cards.Deck()
        self.table = [] #list with the cards in the table
        self.computer_hand = [] #the cards that computer has
        self.human_hand = [] #the cards that the player has in his hand
        self.what_happend = "start" #what_happens every moment of the game
        self.generate_card_images() #list with the images of the cards of the deck from the sprite sheet
        self.drawn_cards = []
        ###GUI parameters
        self.board_width, self.board_height = 900, 600 #Canvas dimantions
        self.card_width, self.card_height = 80, 120 #Diamentions of the cards
        self.padx, self.pady = 5, 5 #the space between the canvas and the activated areas
        self.f = tk.Frame.__init__(self, root)
        self.f1 = tk.Frame(self.f)
        self.f2 = tk.Frame(self.f, bg = 'black')
        self.f1.pack( fill = 'x')
        self.f2.pack( fill = 'x')
        self.canvas = tk.Canvas(self.f2, width=self.board_width, height=self.board_height, bg='darkgreen')
        self.canvas.pack(side='left', fill =  'x')
        self.canvas.bind("<Button-1>", self.board_event_handler)
        self.b = tk.Button(self.f1, text = "New game ", bg='#efefef', command= self.game_restart)
        self.b.pack(side='left', fill='x')
        self.message = ""
        self.score = [0,0]
        self.score_label = tk.Label(self.f1, text = "Score : Computer {} - You {}".format(self.score[0], self.score[1]), font = 'Arial 14', fg = 'brown')
        self.score_label.pack(side = 'right')


    def game_restart(self):
        self.d = Playing_Cards.Deck()
        self.table = []
        self.computer_hand = [] #the cards that computer has
        self.human_hand = [] #the cards that the player has in his hand
        self.what_happend = "start" #what_happens every moment of the game
        self.create_board()

    def subimage(self, l, t, r, b):
        dst = PhotoImage()
        dst.tk.call(dst, "copy", self.spritsheet, '-from', l, t, r, d, '-to', 0, 0)
        return dst

    def generate_card_images(self):
        #Here we create the images of the cards(80x120 px) from the sprite sheet cards2.gif
        imagefile = join(path,"cards2.gif")
        self.spritesheet = tk.PhotoImage(file = imagefile)
        self.num_sprites = 13
        self.cards = []
        place = 0
        self.images = {}
        for x in 'sdhc':
            self.images [x] = [self.subimage(80*i, 0+place, 80*(i+1), 120+place) for i in range(self.num_sprites)]
            place += 120
        self.card_back = self.subimage(0,place,80,120 + place)

    def create_board(self):
        if self.what_happend == "start":
            self.initial()
        #the area where the cards of the computer are
        comp_startx, comp_starty = self.padx, self.pady
        comp_endx, comp_endy = self.padx + (len(self.computer_hand)+ 1)* self.card_width //2, self.pady + self.card_height
        self.comp_plays_area = (comp_startx, comp_starty, comp_endx, comp_endy)
        #the area of the cards from the player
        human_startx, human_starty = self.padx, self.board_height - self.pady - self.card_height
        human_endx, human_endy = self.padx + (len(self.human_hand)+1) * self.card_width//2, self.board_height - self.pady
        self.human_plays_area = (human_startx, human_starty, human_endx, human_endy)
        #the area of the cards from the deck
        deck_startx,  deck_starty = 800, 230
        self.deck_of_cards_area = (deck_startx,deck_starty, deck_startx+self.card_width,deck_starty+self.card_height)
        #The area if the open cards (table)
        table_startx, table_starty = 360, 230
        self.table_cards_area = (table_startx,table_starty,table_startx+ self.card_width,table_starty+self.card_height)

        #Draw cards
        self.canvas.delete('all')
        self.drawn_cards = []
        self.score_label.config(text = "Score : Computer{} - You{}".format(self.score[0], self.score[1])) 
        if self.d.cards_left() > 0:
            self.drawn_cards.append(self.drawimage((deck_startx, deck_starty), 'bb'))
            self.canvas.create_text(deck_startx, deck_starty - 45, fill = 'white', text = 'Deck: \n Cards:{}'.format(self.d.cards_left()), font = 'Arial 14', anchor = 'nw')
        else:
            self.canvas.create_text(deck_startx-40, deck_starty, fill="white", text = "The cards \nof the deck \n finished" + "\nClick here \nfor the score\nif you dont have an other card \nto throw", font="Arial 12", anchor = 'nw')
        if len(self.table)>= 1:
            card = str(self.table[-1])
            self.drawn_cards.append(self.drawimage((table_startx, table_starty), card ))
        pos = 0
        for c in self.human_hand:
            card = str(c)
            self.drawn_cards.append(self.drawimage((human_startx+ pos*self.card_width//2, human_starty), card))
            pos += 1
        self.canvas.create_text(human_startx, human_starty - 30, fill="white", text = "Player cards:{}".format(len(self.human_hand)), font="Arial 14", anchor = 'nw')
        for item in range(len(self.computer_hand)):
            self.drawn_cards.append(self.drawimage((comp_startx+ item*self.card_width//2, comp_starty), 'bb'))
        self.canvas.create_text(comp_startx, comp_starty+self.card_height + 20, fill="white", text = "Computer cards:{}".format(len(self.computer_hand)),font="Arial 14", anchor ='nw')
        if self.what_happened in [ "deck_finished", "human_wins", "computer_wins", "END"]:
            showinfo("End of the game", self.message)
    
    def board_event_handler(self, event):
        x = event.x
        y = event.y
        if self.what_happend == 'END':
            return 
        else:
            if self.in_area(x,y, self.human_plays_area ):
                # The user has pressed the area of his cards,
                # Serching for the cards the player pressed on
                w = self.card_width//2
                x0 = x-self.human_plays_area[0]
                card_selected = x0//w
                if card_selected >= len(self.human_hand):
                    card_selected = len(self.human_hand) - 1
                # we are calling the function self.human_plays(): Cheking if the action is allowed by the game
                if self.human_plays(str(self.human_hand[card_selected])):
                    if self.what_happened == "human_played": # The action can be executed
                        if len(self.human_hand) == 0:  # If the cards of the player are finished
                            self.what_happened = "human_wins"
                            self.message = self.evaluate() # Final message 
                            self.canvas.after(200, self.create_board)
                            # it returns to redraw the board in the new state
                        else:
                        # the action can be executed but the cards of the player are not finished yet
                            self.computer_plays() # Calling the function Computer_Plays()
                        # Checking if the cards from the computer are finished
                            if len(self.computer_hand) == 0:
                                self.what_happened = "computer_wins"
                                self.message = self.evaluate() # Final message
                                self.canvas.after(200, self.create_board)
                                # it returns to redraw the board in the new state
                            elif self.what_happened == "deck_finished":
                                self.message = self.evaluate()
                                self.canvas.after(200, self.create_board)
                    # For any othe case redraw the Game UI
                    self.canvas.after(200, self.create_board)
            elif self.in_area(x,y, self.deck_of_cards_area ):
                # The user has presse the area of the deck
                if self.human_plays(""): # The player is drawing a new card
                    if self.what_happened =="deck_finished": #If the deck is finished
                        self.message = self.evaluate() # Checking if the game if over
                        self.canvas.after(200, self.create_board)
                    else:
                        self.canvas.after(200, self.create_board)
                        # exit point to  create the board
    def in_area(self, x,y, rect):
        if x>= rect[0] and x <= rect[2] \
            and y >= rect[1] and y <= rect[3]:
            return True
        else:
            return False

    def subimage(self, l, t, r, b):
        print(l,t,r,b)
        dst = tk.PhotoImage()
        dst.tk.call(dst, 'copy', self.spritesheet, '-from', l, t, r, b, '-to', 0, 0)
        return dst

    def drawimage(self, pos, c):
        x = pos[0]
        y = pos[1]
        if c == 'bb':
            self.new_img = self.canvas.create_image(x,y, image = self.card_back)
            self.canvas.itemconfig (self.new_img, anchor = 'nw')
        else:
            sprite = 'A23456789TJQK'.find(c[0].upper())
            symbol = c[1].lower()
            self.new_img = self.canvas.create_image(x,y, image = self.images[symbol][sprite])
            self.canvas.itemconfig (self.new_img, anchor = 'nw')
        return self.new_img
    
    def initial(self):
        self.d.collect()
        self.table = []
        self.computer_hand = []
        self.human_hand = []
        self.d.shuffle()
        print("Collecting the cards...Shaffling the deck...I'm dealing...")
        self.table.append(self.d.Draw())
        print("In the table is", self.table[-1]) ########################## event 5
        for i in range(7):
            self.human_hand.append(self.d.Draw())
            self.computer_hand.append(self.d.Draw())
        if random.random()<0.5:
            print("Throwing a coin......You play first")
            self.what_happened = "computer_played"
        else:
            print("Throwing a coin......The computer plays first")
            self.computer_plays()
            self.what_happened = "human_played"
    
    def computer_plays(self):
        target_val = self.table[-1].value
        target_sym = self.table[-1].symbol
        while True:
            #comp_hand_string = [str(x) for x in self.computer_hand]
            #print("COMPUTER=",comp_hand_string)
            for c in self.computer_hand:
                if c.value ==target_val or c.symbol ==target_sym:
                    print ("The computer throws",c ) ################  event 1
                    self.computer_hand.remove(c)
                    self.table.append(c)
                    self.what_happened = "computer_played"
                    return
            new_card  =  self.d.Draw()
            if new_card  == "empty":
                self.what_happened = "deck_finished"
                return
            else:
                print ("The computer draws a cards from the deck")      ################### event 2
                self.computer_hand.append(new_card)
                time.sleep(1)

    def human_plays(self, sel):
            if sel =="":
                new_card = self.d.Draw()
                print(str(new_card))
                if new_card =="empty":
                    if self.what_happened != 'END' :
                        self.what_happened = "deck_finished"
                    return 1
                else:
                    self.human_hand.append(new_card)
                    human_hand_string = [str(x) for x in self.human_hand]
                    print("HUMAN=",human_hand_string, sel)
                    return 1
            else:
                human_hand_string = [str(x) for x in self.human_hand]
                print("HUMAN=",human_hand_string, sel)
                t = self.table[-1]
                target_val = t.value
                target_sym = t.symbol
                if sel[0] !=  target_val and sel[1] !=  target_sym:
                    print("You can not throw that card ",sel)
                    showinfo("Warning!!!", "You can not make that move!")
                    return 0
                else:
                    print("You throw the",sel) # αυτο δεν χρειαζεται να ανακοινωθει
                    ind = human_hand_string.index(sel)
                    selc = self.human_hand[ind]
                    self.human_hand.remove(selc)
                    self.table.append(selc)
                    self.what_happened = "human_played"
                    return 1

    def evaluate(self):
        out=""
        if self.what_happened =="human_wins":
            out = "Congratulations. YOU WON!!!"
            self.score[1] += 1
            self.score_label.config(text= "Score : Computer {} - Player {}   ".format(self.score[0], self.score[1]))
            self.what_happened = 'END'
        if self.what_happened =="computer_wins":
            out = "The computer beat you"
            self.score[0] += 1
            self.score_label.config(text= "Score : computer {} - Player {}   ".format(self.score[0], self.score[1]))
            self.what_happened = 'END'
        if self.what_happened =="deck_finished":
            ch = len(self.computer_hand)
            if ch == 1: fyl1 = "Card"
            else: fyl1 = "Cards"
            hh = len(self.human_hand)
            if hh == 1: fyl2 = "Card"
            else: fyl2 = "Cards"
            out = "The deck is finished, the computer has "+ "{} {} and you have {} {}\n".format(ch, fyl1, hh, fyl2)
            if ch>hh:
                out += "Congratulations you won!!!"
                self.score[1] += 1
                self.score_label.config(text= "Score : Computer {} - Player {}   ".format(self.score[0], self.score[1]))
                self.what_happened = 'END'
            if ch<hh:
                out += "The computer won."
                self.score[0] += 1
                self.score_label.config(text= "score: Computer{} - Player {}   ".format(self.score[0], self.score[1]))
                self.what_happened = 'END'
            if ch ==hh:
                out+="TIE ( The computer and you have the same number of cards )"
                self.what_happened = 'END'
        return out



# root = tk.Tk()
# app = CardGameGui(root)
# root.mainloop()
def main():
    root = tk.Tk()
    CardGameGui(root)
    root.mainloop()
    
if __name__ == "__main__":
    main()