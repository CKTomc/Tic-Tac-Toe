# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 13:10:59 2019

@author: khadidja
"""
import pygame as pg,sys
import pygame.locals as pl
import time

xo='x'
winner=None
draw=False
w=500   
h=500
white=(255,150,100)
line_color=(70,10,10)

def game_opening():
    screen.blit(opening,(0,0))
    pg.display.update()
    time.sleep(1)
    screen.fill(white)
    #vertical lines
    pg.draw.line(screen,line_color,(w/3,0),(w/3, h),7)
    pg.draw.line(screen,line_color,(w/3*2,0),(w/3*2, h),7)
    #horizontal lines
    pg.draw.line(screen,line_color,(0,h/3),(w, h/3),7)
    pg.draw.line(screen,line_color,(0,h/3*2),(w, h/3*2),7)
    draw_status()
    
def draw_status():
    global draw
    if winner is None:
        message = xo.upper() + "'s Turn"
    else:
        message = winner.upper() + " won!"
    if draw:
        message = 'Game Draw!'
    font = pg.font.Font(None, 30)
    text = font.render(message, 1, (255, 255, 255))
    # copy the message onto the board
    screen.fill ((0, 0, 0), (0, 500, 600, 100))
    text_rect = text.get_rect(center=(w/2, 600-50))
    #to write the text on the bottom space
    screen.blit(text, text_rect)
    pg.display.update()
    
def check_win():
    global ttt, winner,draw
    # winner through rows?
    for row in range (0,3):
        if ((ttt [row][0] == ttt[row][1] == ttt[row][2]) and(ttt [row][0] is not None)):
            # this row won
            winner = ttt[row][0]
            pg.draw.line(screen, (250,0,0), (0, (row + 1)*h/3 -h/6),\
                              (w, (row + 1)*h/3 - h/6 ), 7)
            break
    #winner through columns?
    for col in range (0, 3):
        if (ttt[0][col] == ttt[1][col] == ttt[2][col]) and (ttt[0][col] is not None):
            #get the winner 
            winner = ttt[0][col]
            #draw winning line
            pg.draw.line (screen, (250,0,0),((col + 1)* w/3 - w/6, 0),\
                          ((col + 1)* w/3 - w/6, h), 7)
            break
    #winner through left diagonal
    if (ttt[0][0] == ttt[1][1] == ttt[2][2]) and (ttt[0][0] is not None):
        winner = ttt[0][0]
        pg.draw.line (screen, (250,70,70), (50, 50), (350, 350), 7)
    #winner through right diagonal?
    if (ttt[0][2] == ttt[1][1] == ttt[2][0]) and (ttt[0][2] is not None):    
        winner = ttt[0][2]
        pg.draw.line (screen, (250,70,70), (350, 50), (50, 350), 7)
        
    if(all([all(row) for row in ttt]) and winner is None ):
        draw = True
    draw_status()
    
def drawxo(row,col):
    global ttt,xo
    if row==1:
        posx = 30
    if row==2:
        posx = w/3 + 30
    if row==3:
        posx = w/3*2 + 30
    if col==1:
        posy = 30
    if col==2:
        posy = h/3 + 30
    if col==3:
        posy = h/3*2 + 30

    ttt[row-1][col-1] = xo
    if(xo == 'x'):
        screen.blit(ximg,(posy,posx))
        xo= 'o'
    else:
        screen.blit(oimg,(posy,posx))
        xo= 'x'
    pg.display.update()
    
def userClick():
    #get x,y coordinates of the mouse click
    x,y = pg.mouse.get_pos()
    #get clicked column
    if(x<w/3):
        col = 1
    elif (x<w/3*2):
        col = 2
    elif(x<w):
        col = 3
    else:
        col = None
    #get clicked row
    if(y<h/3):
        row = 1
    elif (y<h/3*2):
        row = 2
    elif(y<h):
        row = 3
    else:
        row = None
    if(row and col and ttt[row-1][col-1] is None):
        global xo
        #draw  x or o on the corresponding cell 
        drawxo(row,col)
        check_win()

def reset_game():
    global ttt, winner,xo, draw
    time.sleep(5)
    xo = 'x'
    draw = False
    game_opening()
    winner=None
    ttt = [[None]*3,[None]*3,[None]*3]
#3*3 game board
ttt=[[None]*3,[None]*3,[None]*3]
#intialize the game window
pg.init()
fps=30
clock=pg.time.Clock()
screen=pg.display.set_mode((w,h+100),0,32)
pg.display.set_caption("TIC TAC TOE :)")
opening=pg.image.load('xo.png')
ximg=pg.image.load('x.png')
oimg=pg.image.load('o.png')
ximg=pg.transform.scale(ximg,(80,80))
oimg=pg.transform.scale(oimg,(80,80))
opening=pg.transform.scale(opening,(w,h+100))

game_opening()
# run the game loop while window isn't closed by the user
while(True):
    for event in pg.event.get():
        if event.type == pl.QUIT:
            pg.quit()
            sys.exit()
        elif event.type is pl.MOUSEBUTTONDOWN:
            #after a click, draw x or o
            userClick()
            if(winner or draw):
                reset_game()
    pg.display.update()
    clock.tick(fps)