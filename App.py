from Playing_Cards import *

#! MAIN PROGRAM
print('THE GAME WITH CARDS v 1.0.0')
print("===========================")
print()
n = int(input("With how many deck you want to play? ")) # TODO I HAVE TO ADD A CHECK IF THE PLAYER ENTERS A NEGATIVE OR AN INVALID VALUE
print("OK, chif we are playing with, ", n , "number of decks")
print()

#Global variables
table= []
computer_hand = []
human_hand = []
what_happend = ""
again = "y"
d = Pack(n)

def Computer_Plays():
    global d, table, computer_hand, human_hand, what_happend
    target_val = table[-1].value
    target_sym = table[-1].symbol
    while True:
        for c in computer_hand:
            if c.value == target_val or c.symbol== target_sym:
                print("THE COMPUTER PlAYS",c)
                computer_hand.remove(c)
                what_happend = "computer_played"
                return
        
        new_card = d.Draw()
        if new_card == "empty":
            what_happend = "Deck_finished"
            return
        else:
            print("THE COMPUTER IS DRAWING A CARD. ")
            computer_hand.append(new_card)
        
def print_info():
    global d, table, computer_hand, human_hand, what_happend
    print()
    print("The deck has ", len(d.content), " cards")
    print("The computer has ", len(computer_hand), " cards")
    print("On the table are ", len(table), " cards")
    print("Your cards are ", len(human_hand))
    HHS = [str(x) for x in human_hand]
    print(HHS)
    print()
    print("Pick the card you want to through")
    print("Press ENTER if you just want to draw an other card")

def human_plays():
    global d, table, computer_hand, human_hand, what_happend
    while True:
        print_info()
        sel = input()
        if sel == "":
            new_card = d.Draw()
            if new_card == "empty":
                what_happend = "deck_finished"
                return
            else:
                human_hand.append(new_card)
        else:
            HHS = [str(x) for x in human_hand]
            if not(sel in HHS):
                print(sel, "??? YOU DO NOT HAVE THAT CARD")
            else:
                t = table[-1]
                target_val = t.value
                target_sym = t.symbol
                if sel[0] != target_val and sel[1] != target_sym:
                    print('You can not through that card', sel)
                else:
                    print("You through the",sel)
                    ind = HHS.index(sel)
                    selc = human_hand[ind]
                    human_hand.remove(selc)
                    table.append(selc)
                    what_happend = "humman_played"
                    return


def initial():
    global d, table, computer_hand, human_hand, what_happend
    print("I'm collecting all the cards...")
    d.collect()
    table = []
    computer_hand = []
    human_hand = []
    print("Im shuffling...")
    d.shuffle()
    print("im dealing the cards around")
    table.append(d.Draw())
    print("On the table is ", table[-1])
    for i in range(7):
        human_hand.append(d.Draw())
        computer_hand.append(d.Draw())
    print("Fliping a coin", end = " ")
    if random.random() < 0.5:
        print("You are playing first")
        what_happend= "computer_played"
    else:
        print("The computer is playing first")
        what_happend = "human_played"

def evaluate():
    global d, table, computer_hand, human_hand, what_happend
    if what_happend == "human_wins":
        print("Congratulationn YOU WON")
    if what_happend == "computer_wins":
        print("The computer WON!!")
    if what_happend == "deck_finised":
        ch = len(computer_hand)
        hh = len(human_hand)
        print("The deck if finished, the computer has ", ch, "cards and the you have", hh)
        if ch > hh:
            print("Congratulations you WON!!")
        if ch < hh:
            print("The computer WON!!")
        if ch==hh:
            print("draw")    
    print()

def next_turn():
    global d, table, computer_hand, human_hand, what_happend
    while True:
        if what_happend == "game_starts":
            initial()
        elif what_happend == "human_played":
            if len(human_hand) == 0:
                what_heppend = "human_wins"
                evaluate()
                break
            print()
            print("--------------------Computers turn--------------------")
            print()
            Computer_Plays()
        elif what_happend == "computer_played": 
            if len(computer_hand)== 0:
                what_happend = "computer_wins"
                evaluate()
                break
            print()
            print("--------------------Your turn-------------------------")
            human_plays()
        elif what_happend == "deck_finished":
            evaluate()
            break


#! MAIN PROGRAM

while again == "y":
    what_happend = "game_starts"
    next_turn()
    print("You want to play agin with me;")
    again = input('type "y" for yes and "n" for no')
print("END OF PROGRAM")

