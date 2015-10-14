#Simple Memory Match Game

import pygame
from pygame.locals import *

import time
import random
import os, pygame.mixer, pygame.time

#Checks if the cards match using their array indices
def match_check(deck, flipped):
    if deck[6*flipped[0][1]+flipped[0][0]] == deck[6*flipped[1][1]+flipped[1][0]]:
        return deck[6*flipped[0][1]+flipped[0][0]]

#Get mouse position, and check which card it's on using division
def card_check(mouse_pos):
    MouseX = mouse_pos[0]
    MouseY = mouse_pos[1]
    CardX = int(MouseX/125)
    CardY = int(MouseY/181)
    card = (CardX, CardY)
    return card

#Draw the cards. This is used after initializsation and to rehide cards
def card_draw(cards):
    pygame.init()
    DISPLAY_SIZE = (750, 905)
    screen = pygame.display.set_mode(DISPLAY_SIZE)
    
    #Place card images in their appropriate spots by multiplying card width & height
    for i in range(6):
        for j in range(5):
            screen.blit(cards[i+6*j], (i*125,j*181))

#Load the main card images (used in cards_init())
def card_load(char):
    card = "./card_images/%s-spades.png" % char
    card_load = pygame.image.load(card) 
    return card_load

def cards_init():
    cards = []

    #Load images into array
    for i in range(2,11):
        cards.append(card_load(i))
    
    for alpha in ['J', 'Q', 'K', 'A']:
        cards.append(card_load(alpha))
    
    cards.append(card_load('wild'))
    joker_load = pygame.image.load("./card_images/joker.png")
    cards.append(joker_load)

    #Multiply the deck by two so there is one pair of everything
    cards *= 2 #Python is so great - just double the list to duplicate!

    #Shuffle the deck for a new game every time
    random.shuffle(cards)

    return cards

def main(runs):
    DISPLAY_SIZE = (750, 905) 
    GAME_TITLE = "Python Memory Match"
    DESIRED_FPS = 60

    #Setup preliminary pygame stuff
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY_SIZE)
    pygame.display.set_caption(GAME_TITLE)

    fps_clock = pygame.time.Clock()

    card_deck = cards_init() #initialize deck

    #load card-back image for all cards at first, and have matches slowly unveiled
    card_back = pygame.image.load("./card_images/card_back.png")
    visible_deck = []
    for x in range(30):
        visible_deck.append(card_back)

    card_draw(visible_deck)

    game_run = True #run the game
    
    #Ensure the welcome message is displayed only on the first time through
    if runs == 0:
        print "Welcome to Memory Match! Select two cards to flip them and find a match!"
        print "Press 'q' to quit at any time."
    elif runs == 1:
        print "\n\nNew Game"

    #"Global" variables used throughout the while loop
    flips = []
    found = []
    missed = 0
    first_flip = 0
    second_flip = 0
    t = 1

    while game_run:
        user_input = pygame.event.get()
        pressed_key = pygame.key.get_pressed()

        #Retreives all user input
        for event in user_input:
            #But is the input mouse button down?
            if event.type == pygame.MOUSEBUTTONDOWN:
                #Get position of mouse and put it into card_check
                #to figure out which card mouse is on
                mouse_pos = pygame.mouse.get_pos()
                card_select = card_check(mouse_pos)
                #Make sure card has not been selected before
                if card_select not in flips and card_select not in found:
                    flips.append(card_select)
                    #Put the actual value of the card on the screen (vs just the back)
                    if len(flips) <= 2:
                        screen.blit(card_deck[6*card_select[1]+card_select[0]], (125*card_select[0],181*card_select[1]))
                        first_flip = time.time() #first card has been flipped
                    if len(flips) == 2:
                        second_flip = time.time() #second card has been flipped
                        match = match_check(card_deck, flips) #are the two cards a match?
                        if match:
                            #if a match, append coordinates of two cards to found array,
                            #and have them permanently displayed by adding them to the visible deck
                            for i in range(2):
                                found.append(flips[i])
                                visible_deck[6*flips[i][1]+flips[i][0]] = card_deck[6*flips[i][1]+flips[i][0]]
                            print "Matches found: %d/15" % (len(found)/2)
                            t = 0 #Allows user to immediately flip next card
                        else:
                            missed += 1

        #Show the cards only for one second
        if len(flips) >= 2 and time.time() - second_flip > t:
            t = 1
            card_draw(visible_deck)
            flips = []

        #If the user is slow, the card gets flipped back
        elif len(flips) == 1 and time.time() - first_flip > 3:
            card_draw(visible_deck)
            flips = []
            #Unsure if misseses += 1 belongs here - balance question

        #This comes before quitting to avoid video errors
        pygame.display.flip()
        fps_clock.tick(DESIRED_FPS)

        if pressed_key[K_q]:
            game_run = False

        if len(found) == 30:
            found.append("WIN")
            print "YOU WIN!"
            print "Score: %d misses" % missed
            print "\nPlay again? (y/n)" #no raw_input to avoid wrong characters
            runs = 2

        if runs == 2: #Win mode of main
            if pressed_key[K_y]:
                main(1)
            elif pressed_key[K_n]:
                game_run = False

    pygame.quit()

main(0) #Three modes of main: first run (0), not first run (1), win (2)
