<<<<<<< HEAD

#author: Mahendra Suthar & Piyush Bhutani
#First Game 
import random
import pygame
import time
frame = 4
tme = 2
pygame.init()
win = pygame.display.set_mode((500, 700))
pygame.display.set_caption("Two Car")
i_b = 0
i_c = 0                                  #left lane object counter
obstr = ["box.fw.png" ,"ring.fw.png"]    #obstacle type  ring and box
objcoun_L   = 0                          #similar items added in lane
objlane_L   = 0                          #similar items in lane
objcoun_R   = 0                          #similar items added in lane
objlane_R   = 0
temp_box_L  = []                         #left side object list
temp_box_R  = []                         #right side object list
game_pause      = False
game_start_act  = False
game_over       = False
game_over_conju = False
new_game        = False
run             = True
fileread        = True
scor = 0
ss = 0#to store the score
game_start = True
zx = list(range(190, 250, 20))           #list of possible gap between consecutive obstacles
gap_box_R = random.choice(zx)+30         #intantaneous gap
gap_box_L = random.choice(zx)
black = (200, 200, 0)
#bg = pygame.image.load("background.fw.jpg")
clock = pygame.time.Clock()
class Lines():
    """creates line object"""
    def __init__(self):
        """start points, end points, color, width"""
        self.lines = []
        
    def add_lines(self, start, end, color, width=3):
        """start points, end points, color, width"""
        self.start    = start
        self.end      = end
        self.color    = color
        self.width    = width
        self.line_arg = (self.color,self.start, self.end, self.width)
        self.lines.append(self.line_arg)

    def draw_line(self, win):
        """draws line on window"""
        for j in self.lines:
            pygame.draw.line(win, j[0], j[1], j[2], j[3])
      
class Obstacle():
    """creates obstacles of game"""
    def __init__(self,x,y,z,x_val,y_val):
        self.mov     = True
        self.curt    = True
        self.boxlist = True
        self.x       = x
        self.y       = y
        self.name    = z
        self.image   = pygame.image.load(z)
        self.vel     = 5
        self.ar      = [0,1]
        self.pos_arr = [x_val,y_val]
        self.pos     = 0

    def update_img(self, name):
        """changes image name"""
        self.name  = name
        self.image = pygame.image.load(self.name)

    def update_lane(self, lane):
        self.x   = self.pos_arr[lane]
        self.y   = -60
        self.mov = False
        win.blit(self.image, (self.x, self.y))
        
    def draw(self):
        """puts box on starting"""
        self.y   = -60
        self.pos = random.choice(self.ar)
        self.ar.remove(self.pos)
        self.x   = self.pos_arr[self.pos]
        win.blit(self.image, (self.x, self.y))
    
    def move(self ):
        """moves box randomly in lane"""
        if self.mov  and self.curt:
            self.draw()
            self.mov = False
        if not self.mov:
            self.y += 2
            win.blit(self.image, (self.x, self.y))
            if self.y >= 700:
                self.name  = random.choice(obstr)
                self.image = pygame.image.load(self.name)
                self.mov   = True
                self.curt  = False
                self.y = 0
                if(len(self.ar) == 0):
                    self.ar = [0,1]
              
class Car():
    """creates car object"""
    def __init__(self,x,y,height,width,z):
        self.r      = False                    #to keep car moving to right          
        self.l      = False                    #to keep car moving to left
        self.mov_r  = False                    #true if car is moving to right
        self.mov_l  = False                    #true if car is moving to left
        self.image  = pygame.image.load(z)
        self.x      = x
        self.y      = y
        self.height = height
        self.width  = width
        self.jump   = 2.5

    def draw(self):
        """draws car on window"""
        win.blit(self.image, (self.x,self.y))

    def jumpRight(self, key, y, z):
        """Jumping car to right"""
        if (key and (self.x >= y and self.x < z) \
        or self.r == True) and self.mov_l == False:
            self.mov_r = True
            self.r = True
            if(self.x == z):
                self.r = False
                self.mov_r = False
            else:
                self.x += self.jump
                self.draw()

    def jumpLeft(self, key, y, z):
        """Jumping car to left"""
        if (key and (self.x <= y and self.x > z ) \
        or self.l == True) and self.mov_r == False:
            self.mov_l = True
            self.l = True
            if(self.x == z):
                self.l = False
                self.mov_l = False
            else:
                self.x -= self.jump
                self.draw()
class Foont():
    """creates text object with different fonts and size"""
    def __init__(self, font, size):
        """creates text object"""
        self.text_obj = pygame.font.Font(font, size)

class Text():
    """creates text object"""
    def __init__(self, text, color, surface, x, y):
        """creates font object"""
        self.surface = surface
        self.txt = text
        self.color = color
        self.text = surface.render(text, True, color)
        self.rect = self.text.get_rect()
        self.center_x = x
        self.center_y = y
        self.rect.center = (self.center_x, self.center_y)

    def update_col(self, color):
        self.text = self.surface.render(self.txt, True, color)

    def update_txt(self, txt):
        """changes txt"""
        self.txxt = txt
        self.text = self.surface.render(self.txxt, True, self.color)
  
def collision(x, y, x_size, y_size):
    """checks for collision between two objects"""
    if(x.y + x_size[1] >= y.y) and ((x.x + x_size[0] >= y.x) \
                                    and (x.x <= y.x+y_size)): 
        return True
    else:
        return False

gap_box = random.choice(zx)

#setting font and size for different text elements
mainfont_1 = Foont("comic.ttf", 80)
mainfont = Foont("comic.ttf", 60)
secon_1  = Foont("comic.ttf", 40)
secon_2  = Foont("comic.ttf", 35)

#setting up all the text used in game
two_car  = Text("2 Car game"  ,(255,119,0), mainfont.text_obj, 250, 300)
pause    = Text("Game Paused" ,(251, 55, 70), mainfont.text_obj, 250, 300)
over     = Text("Game Over"   , (251, 55, 70), mainfont.text_obj, 250, 300)
play     = Text("Play"        , (255,119,0), secon_1.text_obj, 140, 370 )
quite    = Text("Quit"        , (255,119,0), secon_1.text_obj, 350, 370)
quite_1  = Text("Quit"        , (217, 183, 119), secon_1.text_obj, 373, 370)
contiue  = Text("Continue"    , (217, 183, 119), secon_1.text_obj, 135, 370)
mn_score = Text("Your score is "+ str(scor), (255,119,0), secon_1.text_obj, 220, 430)
score    = Text("Score = "+str(scor), (255,119,0), secon_2.text_obj, 400, 40)
high     = Text("Highscore is ", (255,119,0), secon_1.text_obj, 220, 490)
tame     = Text(str(tme)       ,(255,119,0), mainfont_1.text_obj, 250, 350)

#setting up our main class of lines to 
#to group together
start_lines = Lines()
lane_lines  = Lines()
#this is our lane lines start
lane_lines.add_lines((1, 0), (1, 800), black)
lane_lines.add_lines((498, 0), (498, 800), black)
lane_lines.add_lines((125, 0), (125, 800), black)
lane_lines.add_lines((245, 0), (245, 800), black, 5)
lane_lines.add_lines((255, 0), (255, 800), black, 5)
lane_lines.add_lines((375, 0), (375, 800), black)
#this is our lane lines end

#this is our game start lines
start_lines.add_lines((0, 0), (500, 800), black)
start_lines.add_lines((0, 400), (500, 1200), black)
start_lines.add_lines((0, 700), (500, 0), black)
#this is our game start lines end

#setting up cars
car_1  = Car(30,570,80,60,"car.fw.png")
car_2  = Car(280,570,80,60,"car_1.fw.png")

#setting up obstacles of game
box_1  = Obstacle(0,0,obstr[0],38, 163)
box_2  = Obstacle(0,0,obstr[1],38, 163)
box_3  = Obstacle(0,0,obstr[0],38, 163)
box_4  = Obstacle(0,0,obstr[1],38, 163)
box_5  = Obstacle(0,0,obstr[0],38, 163)
box_6  = Obstacle(0,0,obstr[1],38, 163)
box_21 = Obstacle(0,0,obstr[1],288, 413)
box_22 = Obstacle(0,0,obstr[0],288, 413)
box_23 = Obstacle(0,0,obstr[1],288, 413)
box_24 = Obstacle(0,0,obstr[0],288, 413)
box_25 = Obstacle(0,0,obstr[1],288, 413)
box_26 = Obstacle(0,0,obstr[0],288, 413)

box_L  = [box_1, box_2, box_3, box_4, box_5, box_6]       #left side car obstacle list
box_R  = [box_21, box_22, box_23, box_24, box_25, box_26] #right side car obstacle list
     
while run:
    """game main loop all thingd happen in this 
       loop"""
    pygame.time.delay(4)
    for event in pygame.event.get():
         if event.type == pygame.QUIT:
            run = False
         if event.type == pygame.KEYDOWN:
             if event.key == pygame.K_SPACE:
                 game_pause = True          
    keys = pygame.key.get_pressed()
    car_1.jumpRight(keys[pygame.K_d], 30, 155)
    car_1.jumpLeft(keys[pygame.K_a], 155, 30)
    car_2.jumpRight(keys[pygame.K_RIGHT], 280, 405)
    car_2.jumpLeft(keys[pygame.K_LEFT], 405, 280)
    while game_start_act:
        """this is our game_start loop
           it runs only one time in 
           game"""
        win.fill((4, 4, 0))
        lane_lines.draw_line(win)
        tame.update_txt(str(tme))
        win.blit(tame.text, tame.rect)
        if tme == -1:
            tme = 2
            game_start_act = False
            pygame.display.update()
            break
        tme -= 1
        pygame.display.update()
        time.sleep(1)
        
    while game_start:

        win.fill((4, 4, 0))
        start_lines.draw_line(win)
        win.blit(two_car.text, two_car.rect)
        win.blit(play.text, play.rect)
        win.blit(quite.text, quite.rect)
        for event in pygame.event.get():
            z = pygame.mouse.get_pos()
            if (play.rect.collidepoint(z)):
                play.update_col((55,255,0)) 
                if (pygame.mouse.get_pressed()[0] == 1):
                    game_start = False
            else:
                play.update_col((255,119,0)) 
            if (quite.rect.collidepoint(z)):
                quite.update_col((255,0,0))
                if (pygame.mouse.get_pressed()[0] == 1):
                    game_start = False
                    run = False
                    break
            else:
                quite.update_col((255,119,0))
        pygame.display.update()
        
    while game_pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_pause = False
                run = False
            z = pygame.mouse.get_pos()
            if (contiue.rect.collidepoint(z)):
                contiue.update_col((26, 224, 152))
                if (pygame.mouse.get_pressed()[0] == 1):
                    game_pause = False
            else:
                contiue.update_col((217, 183, 119)) 
            if (quite_1.rect.collidepoint(z)):
                quite_1.update_col((155, 120, 203)) 
                if (pygame.mouse.get_pressed()[0] == 1):
                    run = False
                    game_pause = False
            else:
                quite_1.update_col((217, 183, 119)) 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_pause = False
        win.fill((4, 4, 0))
        lane_lines.draw_line(win)
        win.blit(pause.text, pause.rect)
        win.blit(contiue.text, contiue.rect)
        win.blit(quite_1.text, quite_1.rect)
        pygame.display.update()

    while game_over:
        if fileread:
            ##print("yess")
            scoree = open("score.txt","r")
            while True:
                scoreline = scoree.readline()
                if len(scoreline) == 0:
                    break
                sce = scoreline.split()
                ss = int(sce[2])
                ##print(sce)
                if ss < scor:
                    ss = scor
                else:
                    ss = int(sce[2])
                sc = open("score.txt","w")
                sc.write("highscore is "+str(ss))
                sc.close()
            scoree.close()
            high.update_txt("Highscore is "+str(ss))
            fileread = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = False
                run = False
                scor = 0
            z = pygame.mouse.get_pos()
            if (contiue.rect.collidepoint(z)):
                contiue.update_col((26, 224, 152))
                if (pygame.mouse.get_pressed()[0] == 1):
                    game_over = False
                    game_over_conju = True
                    new_game = True
                    scor = 0
                    fileread = True
            else:
                contiue.update_col((217, 183, 119))
            if (quite_1.rect.collidepoint(z)):
                quite_1.update_col((155, 120, 203))
                if (pygame.mouse.get_pressed()[0] == 1):
                    run = False
                    game_over = False
                    scor = 0
                    break
            else:
                quite_1.update_col((217, 183, 119))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_pause = False 
        mn_score.update_txt("Your score is "+ str(scor))# = conti.render("Your score is "+ str(scor) , True, (255,119,0))
        win.fill((4, 4, 0))
        lane_lines.draw_line(win)
        win.blit(high.text, high.rect)
        win.blit(mn_score.text, mn_score.rect)
        win.blit(quite_1.text, quite_1.rect)
        win.blit(contiue.text, contiue.rect)
        win.blit(over.text, over.rect)
        pygame.display.update()
        
    if not game_over and game_over_conju:
        for j in box_L:
            j.y = -60
            j.mov = True
            j.curt = True
            j.boxlist = True
            j.ar = [0,1]
        for k in box_R:
            k.y = -60
            k.mov = True
            k.curt = True
            k.boxlist = True
            k.ar = [0,1]
        temp_box_L.clear()                     
        temp_box_R.clear()
        i_b = 0
        i_c = 0
        game_over_conju = False
        car_1.x = 30
        car_2.x = 280
        game_start_act = True
        continue
    
    win.fill((4, 4, 0))
    lane_lines.draw_line(win)
    car_1.draw()
    car_2.draw()
    
    if box_L[i_b].y > gap_box_L:
        i_b += 1
        if i_b == 6:
            i_b = 0
        oldbox_L = box_L[i_b-1].name
        oldlane_L = box_L[i_b-1].pos
        box_L[i_b].update_img(random.choice(obstr))
        new_box_L = box_L[i_b].name
        newlane_L = box_L[i_b].pos
        #print(oldbox_L)
        #print(new_box_L)
        if new_box_L == oldbox_L:
            objcoun_L += 1
            if objcoun_L == 3:
                if new_box_L == "box.fw.png":
                    new_box_L = "ring.fw.png"
                    box_L[i_b].update_img(new_box_L)
                else:
                    new_box_L = "box.fw.png"
                    box_L[i_b].update_img(new_box_L)
                objcoun_L = 0
        else:
            objcoun_L = 0
        #print("changed"+new_box_L)
        #print(objcoun_L)
        if newlane_L == oldlane_L:
            objlane_L += 1
            if objlane_L == 3:
                if newlane_L == 0:
                    newlane_L = 1
                    box_L[i_b].update_lane(newlane_L)
                else:
                    newlane_L = 0
                    box_L[i_b].update_lane(newlane_L)
        else:
            objlane_L = 0 
        gap_box_L = random.choice(zx)   
    if box_L[i_b].boxlist:
        temp_box_L.append(box_L[i_b])
        box_L[i_b].boxlist = False
        
    for j in temp_box_L:
        j.move()
        if collision(j, car_1, (50, 50), 60):
            #print("collision"+j.name)
            if j.name == "box.fw.png":
                game_over = True
                j.y = 850
                break
            else:
                scor += 1
            j.y = 850
            j.curt = False
        else:
            if j.name == "ring.fw.png" and j.y == 690:
                game_over = True
                break
    if len(temp_box_L) > 0 and temp_box_L[0].curt == False:
        temp_box_L[0].curt = True
        temp_box_L[0].y = -60
        temp_box_L[0].boxlist = True
        temp_box_L.remove(temp_box_L[0])
        
    if box_R[i_c].y > gap_box_R:
        i_c += 1
        if i_c == 6:
            i_c = 0
        oldbox_R = box_R[i_c-1].name
        oldlane_R = box_R[i_c-1].pos
        box_R[i_c].update_img(random.choice(obstr))
        new_box_R = box_R[i_c].name
        newlane_R = box_R[i_c].pos
        #print(oldbox_L)
        #print(new_box_L)
        if new_box_R == oldbox_R:
            objcoun_R += 1
            if objcoun_R == 3:
                if new_box_R == "box.fw.png":
                    new_box_R = "ring.fw.png"
                    box_R[i_c].update_img(new_box_R)
                else:
                    new_box_R = "box.fw.png"
                    box_R[i_c].update_img(new_box_R)
                objcoun_R = 0
        else:
            objcoun_R = 0
        #print("changed"+new_box_L)
        #print(objcoun_L)
        if newlane_R == oldlane_R:
            objlane_R += 1
            if objlane_R == 3:
                if newlane_R == 0:
                    newlane_R = 1
                    box_R[i_c].update_lane(newlane_R)
                else:
                    newlane_R = 0
                    box_R[i_c].update_lane(newlane_R)
        else:
            objlane_R = 0   
    if box_R[i_c].boxlist:
        temp_box_R.append(box_R[i_c])
        box_R[i_c].boxlist = False

    for k in temp_box_R:
        k.move()
        if collision(k, car_2, (50, 50), 60):
            #print("collision"+j.name)
            if k.name == "box.fw.png":
                game_over = True
                k.y = 850
                break
            else:
                scor += 1
            k.y = 850
            k.curt = False
        else:
            if k.name == "ring.fw.png" and k.y == 690:
                game_over = True
                break
    if len(temp_box_R) > 0 and temp_box_R[0].curt == False:
        temp_box_R[0].curt = True
        temp_box_R[0].y = -60
        temp_box_R[0].boxlist = True
        temp_box_R.remove(temp_box_R[0])
        gap_box_R = random.choice(zx)
        
    score.update_txt("Score = "+str(scor))
    win.blit(score.text, score.rect)
    if scor > 40:
        frame = 3
    if scor > 60:
        frame = 2
    ##clock.tick(120)
    pygame.display.update()
pygame.quit()
=======

#author: Mahendra Suthar & Piyush Bhutani
#First Game 
import random
import pygame
import time
frame = 4
tme = 2
pygame.init()
win = pygame.display.set_mode((500, 700))
pygame.display.set_caption("Two Car")
i_b = 0
i_c = 0                                  #left lane object counter
obstr = ["box.fw.png" ,"ring.fw.png"]    #obstacle type  ring and box
objcoun_L   = 0                          #similar items added in lane
objlane_L   = 0                          #similar items in lane
objcoun_R   = 0                          #similar items added in lane
objlane_R   = 0
temp_box_L  = []                         #left side object list
temp_box_R  = []                         #right side object list
game_pause      = False
game_start_act  = False
game_over       = False
game_over_conju = False
new_game        = False
run             = True
fileread        = True
scor = 0
ss = 0#to store the score
game_start = True
zx = list(range(190, 250, 20))           #list of possible gap between consecutive obstacles
gap_box_R = random.choice(zx)+30         #intantaneous gap
gap_box_L = random.choice(zx)
black = (200, 200, 0)
#bg = pygame.image.load("background.fw.jpg")
clock = pygame.time.Clock()
class Lines():
    """creates line object"""
    def __init__(self):
        """start points, end points, color, width"""
        self.lines = []
        
    def add_lines(self, start, end, color, width=3):
        """start points, end points, color, width"""
        self.start    = start
        self.end      = end
        self.color    = color
        self.width    = width
        self.line_arg = (self.color,self.start, self.end, self.width)
        self.lines.append(self.line_arg)

    def draw_line(self, win):
        """draws line on window"""
        for j in self.lines:
            pygame.draw.line(win, j[0], j[1], j[2], j[3])
      
class Obstacle():
    """creates obstacles of game"""
    def __init__(self,x,y,z,x_val,y_val):
        self.mov     = True
        self.curt    = True
        self.boxlist = True
        self.x       = x
        self.y       = y
        self.name    = z
        self.image   = pygame.image.load(z)
        self.vel     = 5
        self.ar      = [0,1]
        self.pos_arr = [x_val,y_val]
        self.pos     = 0

    def update_img(self, name):
        """changes image name"""
        self.name  = name
        self.image = pygame.image.load(self.name)

    def update_lane(self, lane):
        self.x   = self.pos_arr[lane]
        self.y   = -60
        self.mov = False
        win.blit(self.image, (self.x, self.y))
        
    def draw(self):
        """puts box on starting"""
        self.y   = -60
        self.pos = random.choice(self.ar)
        self.ar.remove(self.pos)
        self.x   = self.pos_arr[self.pos]
        win.blit(self.image, (self.x, self.y))
    
    def move(self ):
        """moves box randomly in lane"""
        if self.mov  and self.curt:
            self.draw()
            self.mov = False
        if not self.mov:
            self.y += 2
            win.blit(self.image, (self.x, self.y))
            if self.y >= 700:
                self.name  = random.choice(obstr)
                self.image = pygame.image.load(self.name)
                self.mov   = True
                self.curt  = False
                self.y = 0
                if(len(self.ar) == 0):
                    self.ar = [0,1]
              
class Car():
    """creates car object"""
    def __init__(self,x,y,height,width,z):
        self.r      = False                    #to keep car moving to right          
        self.l      = False                    #to keep car moving to left
        self.mov_r  = False                    #true if car is moving to right
        self.mov_l  = False                    #true if car is moving to left
        self.image  = pygame.image.load(z)
        self.x      = x
        self.y      = y
        self.height = height
        self.width  = width
        self.jump   = 2.5

    def draw(self):
        """draws car on window"""
        win.blit(self.image, (self.x,self.y))

    def jumpRight(self, key, y, z):
        """Jumping car to right"""
        if (key and (self.x >= y and self.x < z) \
        or self.r == True) and self.mov_l == False:
            self.mov_r = True
            self.r = True
            if(self.x == z):
                self.r = False
                self.mov_r = False
            else:
                self.x += self.jump
                self.draw()

    def jumpLeft(self, key, y, z):
        """Jumping car to left"""
        if (key and (self.x <= y and self.x > z ) \
        or self.l == True) and self.mov_r == False:
            self.mov_l = True
            self.l = True
            if(self.x == z):
                self.l = False
                self.mov_l = False
            else:
                self.x -= self.jump
                self.draw()
class Foont():
    """creates text object with different fonts and size"""
    def __init__(self, font, size):
        """creates text object"""
        self.text_obj = pygame.font.Font(font, size)

class Text():
    """creates text object"""
    def __init__(self, text, color, surface, x, y):
        """creates font object"""
        self.surface = surface
        self.txt = text
        self.color = color
        self.text = surface.render(text, True, color)
        self.rect = self.text.get_rect()
        self.center_x = x
        self.center_y = y
        self.rect.center = (self.center_x, self.center_y)

    def update_col(self, color):
        self.text = self.surface.render(self.txt, True, color)

    def update_txt(self, txt):
        """changes txt"""
        self.txxt = txt
        self.text = self.surface.render(self.txxt, True, self.color)
  
def collision(x, y, x_size, y_size):
    """checks for collision between two objects"""
    if(x.y + x_size[1] >= y.y) and ((x.x + x_size[0] >= y.x) \
                                    and (x.x <= y.x+y_size)): 
        return True
    else:
        return False

gap_box = random.choice(zx)

#setting font and size for different text elements
mainfont_1 = Foont("comic.ttf", 80)
mainfont = Foont("comic.ttf", 60)
secon_1  = Foont("comic.ttf", 40)
secon_2  = Foont("comic.ttf", 35)

#setting up all the text used in game
two_car  = Text("2 Car game"  ,(255,119,0), mainfont.text_obj, 250, 300)
pause    = Text("Game Paused" ,(251, 55, 70), mainfont.text_obj, 250, 300)
over     = Text("Game Over"   , (251, 55, 70), mainfont.text_obj, 250, 300)
play     = Text("Play"        , (255,119,0), secon_1.text_obj, 140, 370 )
quite    = Text("Quit"        , (255,119,0), secon_1.text_obj, 350, 370)
quite_1  = Text("Quit"        , (217, 183, 119), secon_1.text_obj, 373, 370)
contiue  = Text("Continue"    , (217, 183, 119), secon_1.text_obj, 135, 370)
mn_score = Text("Your score is "+ str(scor), (255,119,0), secon_1.text_obj, 220, 430)
score    = Text("Score = "+str(scor), (255,119,0), secon_2.text_obj, 400, 40)
high     = Text("Highscore is ", (255,119,0), secon_1.text_obj, 220, 490)
tame     = Text(str(tme)       ,(255,119,0), mainfont_1.text_obj, 250, 350)

#setting up our main class of lines to 
#to group together
start_lines = Lines()
lane_lines  = Lines()
#this is our lane lines start
lane_lines.add_lines((1, 0), (1, 800), black)
lane_lines.add_lines((498, 0), (498, 800), black)
lane_lines.add_lines((125, 0), (125, 800), black)
lane_lines.add_lines((245, 0), (245, 800), black, 5)
lane_lines.add_lines((255, 0), (255, 800), black, 5)
lane_lines.add_lines((375, 0), (375, 800), black)
#this is our lane lines end

#this is our game start lines
start_lines.add_lines((0, 0), (500, 800), black)
start_lines.add_lines((0, 400), (500, 1200), black)
start_lines.add_lines((0, 700), (500, 0), black)
#this is our game start lines end

#setting up cars
car_1  = Car(30,570,80,60,"car.fw.png")
car_2  = Car(280,570,80,60,"car_1.fw.png")

#setting up obstacles of game
box_1  = Obstacle(0,0,obstr[0],38, 163)
box_2  = Obstacle(0,0,obstr[1],38, 163)
box_3  = Obstacle(0,0,obstr[0],38, 163)
box_4  = Obstacle(0,0,obstr[1],38, 163)
box_5  = Obstacle(0,0,obstr[0],38, 163)
box_6  = Obstacle(0,0,obstr[1],38, 163)
box_21 = Obstacle(0,0,obstr[1],288, 413)
box_22 = Obstacle(0,0,obstr[0],288, 413)
box_23 = Obstacle(0,0,obstr[1],288, 413)
box_24 = Obstacle(0,0,obstr[0],288, 413)
box_25 = Obstacle(0,0,obstr[1],288, 413)
box_26 = Obstacle(0,0,obstr[0],288, 413)

box_L  = [box_1, box_2, box_3, box_4, box_5, box_6]       #left side car obstacle list
box_R  = [box_21, box_22, box_23, box_24, box_25, box_26] #right side car obstacle list
     
while run:
    """game main loop all thingd happen in this 
       loop"""
    pygame.time.delay(4)
    for event in pygame.event.get():
         if event.type == pygame.QUIT:
            run = False
         if event.type == pygame.KEYDOWN:
             if event.key == pygame.K_SPACE:
                 game_pause = True          
    keys = pygame.key.get_pressed()
    car_1.jumpRight(keys[pygame.K_d], 30, 155)
    car_1.jumpLeft(keys[pygame.K_a], 155, 30)
    car_2.jumpRight(keys[pygame.K_RIGHT], 280, 405)
    car_2.jumpLeft(keys[pygame.K_LEFT], 405, 280)
    while game_start_act:
        """this is our game_start loop
           it runs only one time in 
           game"""
        win.fill((4, 4, 0))
        lane_lines.draw_line(win)
        tame.update_txt(str(tme))
        win.blit(tame.text, tame.rect)
        if tme == -1:
            tme = 2
            game_start_act = False
            pygame.display.update()
            break
        tme -= 1
        pygame.display.update()
        time.sleep(1)
        
    while game_start:

        win.fill((4, 4, 0))
        start_lines.draw_line(win)
        win.blit(two_car.text, two_car.rect)
        win.blit(play.text, play.rect)
        win.blit(quite.text, quite.rect)
        for event in pygame.event.get():
            z = pygame.mouse.get_pos()
            if (play.rect.collidepoint(z)):
                play.update_col((55,255,0)) 
                if (pygame.mouse.get_pressed()[0] == 1):
                    game_start = False
            else:
                play.update_col((255,119,0)) 
            if (quite.rect.collidepoint(z)):
                quite.update_col((255,0,0))
                if (pygame.mouse.get_pressed()[0] == 1):
                    game_start = False
                    run = False
                    break
            else:
                quite.update_col((255,119,0))
        pygame.display.update()
        
    while game_pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_pause = False
                run = False
            z = pygame.mouse.get_pos()
            if (contiue.rect.collidepoint(z)):
                contiue.update_col((26, 224, 152))
                if (pygame.mouse.get_pressed()[0] == 1):
                    game_pause = False
            else:
                contiue.update_col((217, 183, 119)) 
            if (quite_1.rect.collidepoint(z)):
                quite_1.update_col((155, 120, 203)) 
                if (pygame.mouse.get_pressed()[0] == 1):
                    run = False
                    game_pause = False
            else:
                quite_1.update_col((217, 183, 119)) 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_pause = False
        win.fill((4, 4, 0))
        lane_lines.draw_line(win)
        win.blit(pause.text, pause.rect)
        win.blit(contiue.text, contiue.rect)
        win.blit(quite_1.text, quite_1.rect)
        pygame.display.update()

    while game_over:
        if fileread:
            ##print("yess")
            scoree = open("score.txt","r")
            while True:
                scoreline = scoree.readline()
                if len(scoreline) == 0:
                    break
                sce = scoreline.split()
                ss = int(sce[2])
                ##print(sce)
                if ss < scor:
                    ss = scor
                else:
                    ss = int(sce[2])
                sc = open("score.txt","w")
                sc.write("highscore is "+str(ss))
                sc.close()
            scoree.close()
            high.update_txt("Highscore is "+str(ss))
            fileread = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = False
                run = False
                scor = 0
            z = pygame.mouse.get_pos()
            if (contiue.rect.collidepoint(z)):
                contiue.update_col((26, 224, 152))
                if (pygame.mouse.get_pressed()[0] == 1):
                    game_over = False
                    game_over_conju = True
                    new_game = True
                    scor = 0
                    fileread = True
            else:
                contiue.update_col((217, 183, 119))
            if (quite_1.rect.collidepoint(z)):
                quite_1.update_col((155, 120, 203))
                if (pygame.mouse.get_pressed()[0] == 1):
                    run = False
                    game_over = False
                    scor = 0
                    break
            else:
                quite_1.update_col((217, 183, 119))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_pause = False 
        mn_score.update_txt("Your score is "+ str(scor))# = conti.render("Your score is "+ str(scor) , True, (255,119,0))
        win.fill((4, 4, 0))
        lane_lines.draw_line(win)
        win.blit(high.text, high.rect)
        win.blit(mn_score.text, mn_score.rect)
        win.blit(quite_1.text, quite_1.rect)
        win.blit(contiue.text, contiue.rect)
        win.blit(over.text, over.rect)
        pygame.display.update()
        
    if not game_over and game_over_conju:
        for j in box_L:
            j.y = -60
            j.mov = True
            j.curt = True
            j.boxlist = True
            j.ar = [0,1]
        for k in box_R:
            k.y = -60
            k.mov = True
            k.curt = True
            k.boxlist = True
            k.ar = [0,1]
        temp_box_L.clear()                     
        temp_box_R.clear()
        i_b = 0
        i_c = 0
        game_over_conju = False
        car_1.x = 30
        car_2.x = 280
        game_start_act = True
        continue
    
    win.fill((4, 4, 0))
    lane_lines.draw_line(win)
    car_1.draw()
    car_2.draw()
    
    if box_L[i_b].y > gap_box_L:
        i_b += 1
        if i_b == 6:
            i_b = 0
        oldbox_L = box_L[i_b-1].name
        oldlane_L = box_L[i_b-1].pos
        box_L[i_b].update_img(random.choice(obstr))
        new_box_L = box_L[i_b].name
        newlane_L = box_L[i_b].pos
        #print(oldbox_L)
        #print(new_box_L)
        if new_box_L == oldbox_L:
            objcoun_L += 1
            if objcoun_L == 3:
                if new_box_L == "box.fw.png":
                    new_box_L = "ring.fw.png"
                    box_L[i_b].update_img(new_box_L)
                else:
                    new_box_L = "box.fw.png"
                    box_L[i_b].update_img(new_box_L)
                objcoun_L = 0
        else:
            objcoun_L = 0
        #print("changed"+new_box_L)
        #print(objcoun_L)
        if newlane_L == oldlane_L:
            objlane_L += 1
            if objlane_L == 3:
                if newlane_L == 0:
                    newlane_L = 1
                    box_L[i_b].update_lane(newlane_L)
                else:
                    newlane_L = 0
                    box_L[i_b].update_lane(newlane_L)
        else:
            objlane_L = 0 
        gap_box_L = random.choice(zx)   
    if box_L[i_b].boxlist:
        temp_box_L.append(box_L[i_b])
        box_L[i_b].boxlist = False
        
    for j in temp_box_L:
        j.move()
        if collision(j, car_1, (50, 50), 60):
            #print("collision"+j.name)
            if j.name == "box.fw.png":
                game_over = True
                j.y = 850
                break
            else:
                scor += 1
            j.y = 850
            j.curt = False
        else:
            if j.name == "ring.fw.png" and j.y == 690:
                game_over = True
                break
    if len(temp_box_L) > 0 and temp_box_L[0].curt == False:
        temp_box_L[0].curt = True
        temp_box_L[0].y = -60
        temp_box_L[0].boxlist = True
        temp_box_L.remove(temp_box_L[0])
        
    if box_R[i_c].y > gap_box_R:
        i_c += 1
        if i_c == 6:
            i_c = 0
        oldbox_R = box_R[i_c-1].name
        oldlane_R = box_R[i_c-1].pos
        box_R[i_c].update_img(random.choice(obstr))
        new_box_R = box_R[i_c].name
        newlane_R = box_R[i_c].pos
        #print(oldbox_L)
        #print(new_box_L)
        if new_box_R == oldbox_R:
            objcoun_R += 1
            if objcoun_R == 3:
                if new_box_R == "box.fw.png":
                    new_box_R = "ring.fw.png"
                    box_R[i_c].update_img(new_box_R)
                else:
                    new_box_R = "box.fw.png"
                    box_R[i_c].update_img(new_box_R)
                objcoun_R = 0
        else:
            objcoun_R = 0
        #print("changed"+new_box_L)
        #print(objcoun_L)
        if newlane_R == oldlane_R:
            objlane_R += 1
            if objlane_R == 3:
                if newlane_R == 0:
                    newlane_R = 1
                    box_R[i_c].update_lane(newlane_R)
                else:
                    newlane_R = 0
                    box_R[i_c].update_lane(newlane_R)
        else:
            objlane_R = 0   
    if box_R[i_c].boxlist:
        temp_box_R.append(box_R[i_c])
        box_R[i_c].boxlist = False

    for k in temp_box_R:
        k.move()
        if collision(k, car_2, (50, 50), 60):
            #print("collision"+j.name)
            if k.name == "box.fw.png":
                game_over = True
                k.y = 850
                break
            else:
                scor += 1
            k.y = 850
            k.curt = False
        else:
            if k.name == "ring.fw.png" and k.y == 690:
                game_over = True
                break
    if len(temp_box_R) > 0 and temp_box_R[0].curt == False:
        temp_box_R[0].curt = True
        temp_box_R[0].y = -60
        temp_box_R[0].boxlist = True
        temp_box_R.remove(temp_box_R[0])
        gap_box_R = random.choice(zx)
        
    score.update_txt("Score = "+str(scor))
    win.blit(score.text, score.rect)
    if scor > 40:
        frame = 3
    if scor > 60:
        frame = 2
    ##clock.tick(120)
    pygame.display.update()
pygame.quit()
>>>>>>> 92424fdf6ca3c238a3bb797b93b6440cebc64d3e
