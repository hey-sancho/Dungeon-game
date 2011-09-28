#! /usr/bin/env python
# -*- coding: utf8 -*-
import sys, curses, shutil, ConfigParser

#Initialization
stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
curses.curs_set(0)
stdscr.keypad(1)

#Brushes
brush_top='._\'_'
brush_floor='nmmn'
brush_wall='|'

#Player-related data
player_name='Player'
savefile=player_name+'.sav'
player_x = 1
player_y = 1
player_d = 2
#player_char = 'V' #view
#player_pos = player_x, player_y, player_d

#Draw main window
win_begin_x = 0
win_begin_y = 0
win_height = 24
win_width = 61
win = curses.newwin(win_height, win_width, win_begin_y, win_begin_x)
win.box(0,0)
win.immedok(1)

#Draw stats window
stats_begin_x = 62
stats_begin_y = 0
stats_height = 15
stats_width = 18
stats = curses.newwin(stats_height, stats_width, stats_begin_y, stats_begin_x)
stats.box(0,0)
stats.immedok(1)

#Draw map
OFFSET = 6
mapsize = 64
map_char = '.'
scrmap_begin_x = 62
scrmap_begin_y = 15
scrmap_end_x = 78
scrmap_end_y = 22
#map size is 8x17
scrmap = curses.newpad(mapsize, mapsize)

#TODO: Doesn't work, should scroll map, keeping the player in the center
def center_view(player_axis_value, scrmap_begin_axis, scrmap_end_axis):
    value=0
    a=(player_axis_value-(scrmap_end_axis-scrmap_begin_axis+1))/2
    if a>0:
        value=a
    return value

#TODO: make a border of 3-5 # around map to avoid bugs with render\or map refresh
def load_map(mapfile):
    shutil.copy(mapfile,savefile)
    config = ConfigParser.ConfigParser()
    config.read(savefile)
    player_pos = config.get("Player", "player_x"), config.get("Player", "player_y"), config.get("Player", "player_d") 
    savemap=open(savefile,'r')
    lines=savemap.readlines()
    for y in range(OFFSET, len(lines)):
        try: scrmap.addstr(y-OFFSET,0,lines[y])
        except curses.error: pass
    scrmap.refresh(center_view(player_y, scrmap_begin_y, scrmap_end_y),
                   center_view(player_x, scrmap_begin_x, scrmap_end_x),
                   scrmap_begin_y,scrmap_begin_x, scrmap_end_y,scrmap_end_x)

#-----DRAWING FUNCTIONS-----
# Wall layers:
# 0 - the furthest walls
# 1 - walls in front 
# 2 - nearest walls (left, right)
    
def draw_top_bottom():
    for x in xrange(1, 11):
        win.addnstr(x,1,brush_top*(win_width-2),(win_width-2))
    for x in xrange(1, 10):        
        win.addnstr(win_height-x-1,1,brush_floor*(win_width-2),(win_width-2))

def draw_0_front(pos):  #0,1,2,3,4; 2 <-center
    right=0
    width=12
    if pos > 2:        
        right=1
    elif pos==2:
        width=13
    for y in xrange(7):        
        win.addstr(9+y,12*pos+right,brush_wall*width)   #size 7x12, 7x13 -center

def draw_0_left(pos):   #left -> 0,1,2 <-center; THANKS DEN! =)
    x=12*pos
    if pos==0:
        for y in xrange(7):
            if y in (0,6):
                win.addstr(9+y,x,brush_wall*2)
            elif y in (1,5):
                win.addstr(9+y,x,brush_wall*7)
            else:
                win.addstr(9+y,x,brush_wall*11)    
    elif pos==1:
        for y in xrange(7):
            if y in (0,6):
                win.addstr(9+y,x,brush_wall*2)
            elif y in (1,5):
                win.addstr(9+y,x,brush_wall*5)
            else:
                win.addstr(9+y,x,brush_wall*8)
    else:
        for y in xrange(5):
            win.addstr(10+y,x,brush_wall*(2+2*((y%4-(y-1)%4)+3)/4))    #hehehe

def draw_0_right(pos):   #right-> 0,1,2 <-center
    x=61-12*pos
    if pos==0:
        for y in xrange(7):
            if y in (0,6):
                win.addstr(9+y,x-2,brush_wall*2)
            elif y in (1,5):
                win.addstr(9+y,x-7,brush_wall*7)    
            else:    
                win.addstr(9+y,x-11,brush_wall*11)
    elif pos==1:
        for y in xrange(7):
            if y in (0,6):
                win.addstr(9+y,x-2,brush_wall*2)
            elif y in (1,5):
                win.addstr(9+y,x-5,brush_wall*5)    
            else:    
                win.addstr(9+y,x-8,brush_wall*8)
    else:
        for y in xrange(5):
            if y in (0,4):
                win.addstr(10+y,x-2,brush_wall*2)
            else:    
                win.addstr(10+y,x-4,brush_wall*4)

def draw_1_front(pos): # 0,1,2; 1 <-center
    if pos==0:
        for y in xrange(11):
            win.addstr(7+y,1,brush_wall*15)
    elif pos==1:
        for y in xrange(11):
            win.addstr(7+y,16,brush_wall*29)
    else:
        for y in xrange(11):
            win.addstr(7+y,45,brush_wall*15)
        
def draw_1_left(pos): # left-> 0,1 <-center
    if pos==0:
        for y in xrange(11):
            if y in (0,10):
                win.addstr(7+y,1,brush_wall*5)
            elif y in (1,9):
                win.addstr(7+y,1,brush_wall*9)
            else:
                win.addstr(7+y,1,brush_wall*11)
    else:
        for y in xrange(11):
            if y in (0,10):
                win.addstr(7+y,16,brush_wall*3)
            elif y in (1,9):
                win.addstr(7+y,16,brush_wall*6)
            else:
                win.addstr(7+y,16,brush_wall*8)

def draw_1_right(pos): #right-> 0,1 <-center
    x=61-15*pos-1
    if pos==0:
        for y in xrange(11):
            if y in (0,10):
                win.addstr(7+y,x-5,brush_wall*5)
            elif y in (1,9):
                win.addstr(7+y,x-9,brush_wall*9)
            else:
                win.addstr(7+y,x-11,brush_wall*11)
    else:
        for y in xrange(11):
            if y in (0,10):
                win.addstr(7+y,x-3,brush_wall*3)
            elif y in (1,9):
                win.addstr(7+y,x-6,brush_wall*6)
            else:
                win.addstr(7+y,x-8,brush_wall*8)

def draw_2_left(): # left wall
    for y in xrange(2,win_height-1):
        if y in (2,22):
            win.addstr(y,1,brush_wall*3)
        elif y in (3,21):
            win.addstr(y,1,brush_wall*6)
        elif y in (4,20):
            win.addstr(y,1,brush_wall*9)
        elif y in (5,19):
            win.addstr(y,1,brush_wall*12)
        else:
            win.addstr(y,1,brush_wall*15)

def draw_2_right(): #right wall
    x=60
    for y in xrange(2,win_height-1):
        if y in (2,22):
            win.addstr(y,x-3,brush_wall*3)
        elif y in (3,21):
            win.addstr(y,x-6,brush_wall*6)
        elif y in (4,20):
            win.addstr(y,x-9,brush_wall*9)
        elif y in (5,19):
            win.addstr(y,x-12,brush_wall*12)
        else:
            win.addstr(y,x-15,brush_wall*15)

#------VIEW PARSING------
#TODO: write parsing of the map to render the view in first person
#View is supposed to be like this:
# #RAAAAAL#
# ##RAAAL## 
# ###R@L###
# @ - player position
# R - only right side of wallblock is seen, or unseen (if block exists) 
# L - same, but left side
# A - seen, can be everything (front wall or a corridor, etc)
# # - unseen
# View is rendered from far to near, drawing a block+it's wall (left or right) if it exists on the map (sides will be redrawn as front walls if next adjacent block exists)
# Also it parses left walls then right walls, and then front (vertical line from player)
def parse_cell(x,y,d):
    pass
    
#TODO: Will recieve parameters after cell\view parsing and draw
def draw_cell(left,right,front):
    #draw_front(front)
    #draw_sides(left,right)        
    draw_top_bottom()
    
#-----DRAWING FUNCTIONS TESTS-----    
#    draw_0_front(0)
#    draw_0_front(1)
#    draw_0_front(2)
#    draw_0_front(3)
#    draw_0_front(4)
#    draw_0_left(0)
#    draw_0_left(1)
#    draw_0_left(2)
#    draw_0_right(0)
#    draw_0_right(1)
#    draw_0_right(2)
#    draw_1_front(0)
#    draw_1_front(1)
#    draw_1_front(2)
#    draw_1_left(0)    
#    draw_1_left(1)
#    draw_1_right(0)
#    draw_1_right(1)
#    draw_2_left()
#    draw_2_right()  

#------PLAYER MOVEMENT------
def get_player_char(direction):
    charlist=['^','>','v','<']
    return charlist[direction]

def turn_player(clockwise):
    global player_x; global player_y; global player_d
    
    if not clockwise:
        player_d=(player_d-1)%4
    else: player_d=(player_d+1)%4
    draw_player_pos(player_x, player_y, get_player_char(player_d))
    
def move_player(direction, backward):
    global player_x; global player_y
    
    if direction==0:    #North
        x_off, y_off = 0, -1        
    elif direction==1:  #East
        x_off, y_off = 1, 0
    elif direction==2:  #South
        x_off, y_off = 0, 1
    else:               #West
        x_off, y_off = -1, 0
        
    if not backward:
        new_x, new_y = player_x+x_off, player_y+y_off
    else:
        new_x, new_y = player_x-x_off, player_y-y_off
    
    char=chr(scrmap.inch(new_y, new_x))
    if char=='.':     
        draw_player_pos(new_x, new_y, get_player_char(direction))
        
def draw_player_pos(new_x, new_y, player_char):    
    global player_x; global player_y; global map_char
    
    if new_x!=player_x or new_y!=player_y:  #if NEW COORD - move, else - turn
        scrmap.addch(player_y, player_x, map_char)  #put old map char
        map_char=chr(scrmap.inch(new_y,new_x))  #remember new map char
    
    scrmap.addch(new_y, new_x, player_char) #put player char
    player_x, player_y = new_x, new_y   #change player_pos
    
#TODO: make stats look pretty :3
def update_stats():
    stats.addstr(1,1,"Position:")
    stats.addstr(1,11, '%s %s %s' % (player_x, player_y, player_d))

#TODO: Maybe change the key to exit, currently - escape
def get_key(key):
    global player_d

    if key==curses.KEY_LEFT:
        turn_player(0)
    elif key==curses.KEY_RIGHT:    
        turn_player(1)
    elif key==curses.KEY_UP:
        move_player(player_d,0)
    elif key==curses.KEY_DOWN:
        move_player(player_d,1)
    elif key==27:
        curses.nocbreak()
        stdscr.keypad(0)
        curses.echo()
        curses.endwin()
        sys.exit(0)
    
#-----MAIN PROGRAM-----

#TODO: make refresh work correctly. stdscr grabs keys correctly, but doesn't refresh win at start
load_map('level1.map')
while 1:
    key=stdscr.getch()
    stats.addstr(2,1,'keycode: '+str(key)) 
    get_key(key)
    scrmap.refresh(center_view(player_y, scrmap_begin_y, scrmap_end_y),
                   center_view(player_x, scrmap_begin_x, scrmap_end_x),
                   scrmap_begin_y,scrmap_begin_x, scrmap_end_y,scrmap_end_x)
    update_stats()
    draw_cell(0,0,1) 

#update_stats()
#win.getch()
