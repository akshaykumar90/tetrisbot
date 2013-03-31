import win32api, win32con
import time
import ImageGrab

from gamedata import *

# columns hold the top-most empty row index (0-based)
columns = [0]*MAX_COL;

rows = []
for _ in range(MAX_ROW):
    rows.append([0]*MAX_COL)

game_over = False

def moveRight():
    win32api.keybd_event(win32con.VK_RIGHT, 0x4d, 0, 0)
    time.sleep(.1)
    win32api.keybd_event(win32con.VK_RIGHT, 0x4d, win32con.KEYEVENTF_KEYUP, 0)

def moveLeft():
    win32api.keybd_event(win32con.VK_LEFT, 0x4b, 0, 0)
    time.sleep(.1)
    win32api.keybd_event(win32con.VK_LEFT, 0x4b, win32con.KEYEVENTF_KEYUP, 0)

def rotateRight():
    win32api.keybd_event(0x58, 0x2d, 0, 0)
    time.sleep(.1)
    win32api.keybd_event(0x58, 0x2d, win32con.KEYEVENTF_KEYUP, 0)

def rotateLeft():
    win32api.keybd_event(0x5a, 0x2c, 0, 0)
    time.sleep(.1)
    win32api.keybd_event(0x5a, 0x2c, win32con.KEYEVENTF_KEYUP, 0)

def drop():
    win32api.keybd_event(win32con.VK_SPACE, 0x39, 0, 0)
    time.sleep(.1)
    win32api.keybd_event(win32con.VK_SPACE, 0x39, win32con.KEYEVENTF_KEYUP, 0)

def leftClick():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

def mousePos(cord):
    win32api.SetCursorPos((cord[0], cord[1]))

def get_cords():
    x,y = win32api.GetCursorPos()
    print x,y

def save_screenshot():
    im = ImageGrab.grab(box_play_area)
    im.save('play_area__' + str(int(time.time())) + '.png', 'PNG')

def check(start, shape):
    ls = len(shape)
    cols = columns[start:start+ls]
    for i in range(ls):
        d = cols[i] - shape[i]
        feasible = True
        voids = 0
        for j in range(ls):
            empty = shape[j]+d - cols[j]
            feasible &= empty >= 0
            voids += empty
        if feasible:
            return (d,voids)

def pos(p):
    lowest_row = MAX_ROW
    least_voids = 100
    best_shape = best_col = -1
    for k,s in enumerate(shapes[p]):
        span = len(s)
        for i in range(MAX_COL-span+1):
            base,voids = check(i, s)
            if voids < least_voids:
                lowest_row = base
                least_voids = voids
                best_shape = k
                best_col = i
            elif voids == least_voids and base < lowest_row:
                lowest_row = base
                best_shape = k
                best_col = i
            else:
                pass

    return (best_shape,best_col,lowest_row)

def rowFilled(row):
    return all([c == 1 for c in rows[row]])

def printGrid():
    for i in range(MAX_ROW):
        print rows[MAX_ROW-i-1]

def printCols():
    print columns

def guideBlock(piece, si, sc):
    if si == 1:
        rotateRight()
    elif si == 2:
        rotateRight()
        rotateRight()
    elif si == 3:
        rotateLeft()
    else:
        pass

    init_col = init[piece][si]
    moves = abs(sc-init_col)
    if sc < init_col:
        move_func = moveLeft
    else:
        move_func = moveRight
    for _ in range(moves):
        move_func()
    drop()

def updateGrid(piece, shape_index, start_col, lowest_row):
    global game_over
    highest_row = lowest_row
    
    # update rows first
    shape = shapes[piece][shape_index]
    hs = height[piece][shape_index]
    for i,offset in enumerate(shape):
        col = start_col+i
        for j in range(hs[i]):
            row = lowest_row+offset+j
            rows[row][col] = 1
            if row > highest_row:
                highest_row = row
        columns[col] = row+1
        if columns[col] >= MAX_ROW:
            game_over = True

    # check for filled rows and update cols if applicable
    rows_deleted = 0
    for r in range(highest_row,lowest_row-1,-1):
        if rowFilled(r):
            print "Row %d complete!" % (r,)
            del rows[r] # remove this row
            rows_deleted += 1
            rows.append([0]*MAX_COL) # add an empty row

    if rows_deleted > 0:
        # update columns with new values
        for c in range(MAX_COL):
            columns[c] -= rows_deleted
            tr = columns[c]
            while tr>=0 and rows[tr][c] == 0:
                tr -= 1
            columns[c] = tr+1

def playGame():
    global game_over

    # Click on play game on start screen
    mousePos(play_game)
    leftClick()

    # Grab the first block
    # Little tricky because right after screen transition
    time.sleep(1.2)
    im = ImageGrab.grab(box_cur_block)
    color = im.getpixel(cur_block)

    cnt = 0
    tot = 0
    while True:
        if game_over:
            break
        
        time.sleep(.3) # required, for keeping the game in sync
        
        prev_color = color
        if color in colors:
            piece = colors[color]
            tot += 1
            print "Saw a " + piece
        else:
            print "Unknown color!"
            break
        
        # Grab the next block
        im = ImageGrab.grab(box_next_block)
        color = im.getpixel(next_block)

        # HACK - checking for game over
        # if the next block has not changed for five times straight
        # the game is already over
        if color == prev_color:
            cnt += 1
            if cnt > 5:
                game_over = True
        else:
            cnt = 0
        
        si,sc,lr = pos(piece)
        print si,sc,lr
        guideBlock(piece, si, sc)
        updateGrid(piece,si,sc,lr)

if __name__ == "__main__":
    playGame()
