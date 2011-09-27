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
#stats.refresh()

#Draw map
OFFSET = 6
mapsize = 64
map_char = '.'
scrmap_begin_x = 62
scrmap_begin_y = 15
scrmap_end_x = 78
scrmap_end_y = 22
#size 8x17
scrmap = curses.newpad(mapsize, mapsize)

def center_view(player_axis_value, scrmap_begin_axis, scrmap_end_axis):
    value=0
    a=(player_axis_value-(scrmap_end_axis-scrmap_begin_axis+1))/2
    if a>0:
        value=a
    return value

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
# 0 - the furthest walls
# 1 - far walls 
# 0 - nearest walls (left, right and front)
    
def draw_top_bottom():
    for x in xrange(1, 11):
        win.addnstr(x,1,brush_top*(win_width-2),(win_width-2))
    for x in xrange(1, 10):        
        win.addnstr(win_height-x-1,1,brush_floor*(win_width-2),(win_width-2))

def draw_0_front(pos):  #0,1,2,3,4, 2 -center
    right=0
    width=12
    if pos > 2:        
        right=1
    elif pos==2:
        width=13
    for y in xrange(7):        
        win.addstr(9+y,12*pos+right,brush_wall*width)   #size 7x12, 7x13 -center

def draw_0_left(pos):   #left- 0,1,2 -center; THANKS DEN! =)
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
            win.addstr(10+y,x,brush_wall*(2+2*((y%4-(y-1)%4)+3)/4))    #hehehehehehehehehehehe

def draw_0_right(pos):   #right- 0,1,2 -center
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

def draw_1_front():
    pass

def draw_1_left():
    pass

def draw_1_right():
    pass

def draw_2_front():
    for y in xrange(11):
        win.addstr(7+y,16,brush_wall*29)

def draw_2_left():
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

def draw_2_right():
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

def draw_cell(left,right,front):
    #draw_front(front)
    #draw_sides(left,right)        
    draw_top_bottom()
    draw_0_front(0)
    draw_0_front(1)
    draw_0_front(3)
#    draw_0_left(0)
#    draw_0_left(1)
    draw_0_left(2)
#    draw_0_right(0)
#    draw_0_right(1)
    draw_0_right(2)
#    draw_2_front()
#    draw_2_left()
    draw_2_right()  

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
    
    if new_x!=player_x or new_y!=player_y: #if NEW COORD - move, else - turn
        scrmap.addch(player_y, player_x, map_char) #put old map char
        map_char=chr(scrmap.inch(new_y,new_x)) #remember new map char
    
    scrmap.addch(new_y, new_x, player_char) #put player char
    player_x, player_y = new_x, new_y #change player_pos
    
            
def parse_cell(x,y,d):
    pass
    

def update_stats():
    stats.addstr(1,1,"Position:")
    stats.addstr(1,11, '%s %s %s' % (player_x, player_y, player_d))

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
    
#MAIN PROGRAM    
load_map('level1.map')
while 1:
 #   win.refresh()
    key=stdscr.getch()
    stats.addstr(2,1,chr(scrmap.inch(player_y,player_x))) #
    stats.addstr(3,1,str(key)) 
    get_key(key)
    scrmap.refresh(center_view(player_y, scrmap_begin_y, scrmap_end_y),
                   center_view(player_x, scrmap_begin_x, scrmap_end_x),
                   scrmap_begin_y,scrmap_begin_x, scrmap_end_y,scrmap_end_x)
    update_stats()
    draw_cell(0,0,1) 
#    win.refresh

#
#update_stats()
#win.getch()
#TODO
#DRAW -ALL- THE THINGS:
#draw_0_front OK!
#draw_0_left OK!
#draw_0_right OK!
#draw_1_front 
#draw_1_left 
#draw_1_right
#draw_2_front() OK!
#draw_2_left() OK!
#draw_2_right() OK! 

#center player on map
#refresh everything
