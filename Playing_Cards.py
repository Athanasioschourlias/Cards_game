import random
import time

class Card():
    
    def __init__(self, val, sym):
        self.value = val
        self.symbol = sym
        if self.symbol in "sc":
            self.color = 'B'
        else:
            self.color = 'R'
        if self.value in "JQK":
            self.fig = True
        else:
            self.fig = False
        
    def __str__(self):
        return self.value + self.symbol
    
    def detailed_info(self):
        print("Worth: ", self.value, "Symbol: ", self.symbol, "\n", "Color: ", self.color, "Figure: ", self.fig)
    
class Deck():
    Values = "A23456789XJQK" #this is what every card can worth. # TODO: FIgure out a way have a 10 in my deck insted of an X
    Symbols = "shcd" #these are all the symbols the cards can have.
    def __init__(self):
        self.content= []
        self.pile= []
        for s in Deck.Symbols:
            for v in Deck.Values:
                c = Card(v , s)
                self.content.append(c)

    def __str__(self):
        s = ""
        cntr = 0
        for i in self.content:
            s = s + str(i) + ""
            cntr = cntr + 1
            if cntr%13 == 0:
                s = s + '\n'
        if s[-1] != '\n':
            s = s + '\n'
        s = s +str(len(self.content))+"-"+str(len(self.pile))
        return s
    
    def shuffle(self):
        random.shuffle(self.content)
    
    def Draw(self):
        if len(self.content) < 1:
            return "empty"
        c = self.content[0]
        self.content = self.content[1:]
        self.pile.append(c)
        return c
    def collect(self):
        self.content = self.content + self.pile
        self.pile= []
    
        
        