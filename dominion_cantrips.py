#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 04:47:16 2020

@author: maxzli


Dominion starting build analyzer, basic

"""

import random

input1 = int(input("how many deck go-throughs, besides first one? "))

input2 = []
for index in range(input1):
    temp = int(input("how many terminal actions bought during deck go-through #" + str(index+1)+"? "))
    assert temp >=0 and temp < 5, "input should be positive integer less than 5"
    input2.append(temp)

### could create a matrix across first three rounds, of options 0, 1, and 2 ???
### accounted for action collision that occurs between rounds
### accounted for withholding of action cards and non-action cards between decks


# # input1 = 4
# input2 = [2, 1, 1]
# input1 = len(input2)

pos = []
for i in range(input1):
    pos.append(0)

pos2 = pos[:]
wasted = pos[:]

total = 100000 # number of trials


for j in range(total):
    termActs = 0
    excessActionsPrev = 0 # actions that bled over until next deck
    L = []
    for i in range(10):
        L.append(i)
    if j == 0:
        print("\ndeck go-through #1 deck size:", len(L))
        cardsPlayed = len(L)
        print("total number of cards played after deck # 1:" + str(cardsPlayed)+"\n")


    oldExcess = 0
    newExcess = 0

    for deck in range(2, input1+2):
        termActs += input2[deck-2] # running total of terminal actions
        
    
        # for i in range(int((len(L)+oldExcess)/5)): # account for split across rounds
        for i in range(int((len(L))/5)): # account for split across rounds, don't need to consider oldExcess
            L.append(len(L))
            
        oldExcess = newExcess # excess of round t-2 determines how many cards in this deck
        
        if j == 0:
            print("excess of " + str(newExcess) + " before " + str(deck) + " deck go-throughs")
        
        newExcess = len(L)%5 # excess of round t-1 determines how many cards this deck will buy (how many rounds)
    
        ### counter for shortage across rounds counts the actions during partial round as part of the latter round
    
        if j == 0:
            print("deck go-through #"+ str(deck) + " deck size:", str(len(L))) # how many cards in each time going through deck
    
            cardsPlayed+= (len(L) - oldExcess)
            print("total number of cards played after deck #" + str(deck)+ ": " + str(cardsPlayed)+"\n")
        
            

    
        actions = [] # reset positions of terminal actions
        excessActionsNew = 0
        L2 = random.sample(L[0:len(L)-oldExcess], len(L)-oldExcess) # sample only the cards in discard pile
        heldActions = excessActionsPrev # how many Actions were left in the last part of the deck?
        # if heldActions>0:
        #     print(heldActions)
        
        if oldExcess != 0:
            for l in range(termActs - heldActions): # how many terminal actions this round? append positions
                if L2.index(l) < 5-oldExcess:
                    excessActionsPrev += 1    
                elif L2.index(l) > len(L2)-1-newExcess:
                    excessActionsNew += 1
                else:
                    actions.append(int((L2.index(l)+oldExcess)/5))

        if oldExcess == 0:
            for l in range (termActs - heldActions):
                if L2.index(l) > len(L2)-1-newExcess:
                    excessActionsNew += 1 # how many actions are preserved here
                else:
                    actions.append(int((L2.index(l)/5)))
        # if excessActionsPrev == 3: # just checking our specific case of wasted initial overlap
        #     pos2[deck-2] += 1
        if excessActionsPrev > 0: # here it is the total number of actions
            excessActionsPrev -= 1 # here it is the wasted number of actions
        waste = len(actions) - len(set(actions)) + excessActionsPrev

        excessActionsPrev = excessActionsNew # reset excessActionsPrev for the next deck
        
        if waste > 0:
            pos[deck-2] += 1
        if waste > 1:
            pos2[deck-2] += 1
        wasted[deck-2] += waste
                
pos = [x / total for x in pos] # probability this round of at least one collision
pos2 = [x / total for x in pos2] # probability this round of at least two terminal actions being wasted
wasted = [x / total for x in wasted] # average number of terminal action cards wasted per deck go-through

for x in range(1, len(wasted)): # to estimate cumulative wasted cards
    wasted[x] += wasted[x-1]    
        
print(pos)
print(pos2)
print(wasted)