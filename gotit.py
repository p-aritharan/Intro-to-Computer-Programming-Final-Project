import pygame
import random

#Adding colors to make the game look more lively and to differentiate between the different pieces available
#Took the code for each color from the website below
#https://www.rapidtables.com/web/color/RGB_Color.html
class colors:
    black,blue,lime,aqua,red,magenta,yellow,white = [(r,g,b) for r in (0,255) for g in (0,255) for b in (0,255)]

#There are two ways to write functions, using def and lambda
#Taken from #https://pythonconquerstheuniverse.wordpress.com/2011/08/29/lambda_tutorial/
#Here’s an example. You can build a function in the normal way, using def, like this:
# 1
# def square_root(x): return math.sqrt(x)
# or you can use lambda:
# 1
# square_root = lambda x: math.sqrt(x)

#used pygame database for help with using text in the game
#https://www.pygame.org/docs/ref/font.html
# still trying to add text to the game
class fonts:
    default    = lambda size: pygame.font.Font(None, size)
class key:
    state = lambda key: pygame.key.get_pressed()[eval('pygame.K_'+key)]
    #Checks for keyup events
    up    = lambda key: [0 for event in main.event if event.type==pygame.KEYUP and event.key==eval('pygame.K_'+key)]
    #Checks for keydown events
    down  = lambda key: [0 for event in main.event if event.type==pygame.KEYDOWN and event.key==eval('pygame.K_'+key)]


def exitgame(): pygame.quit()

#Sets up the classes for the different pieces of the game to help start it.
class setup:
    def __init__(self, size, title, fps):
        pygame.init()
        self.screen, self.fullscreen, self.clock, self.fps = pygame.display.set_mode(size), False, pygame.time.Clock(), fps

    def events(self):
        
        pygame.display.flip()
        self.clock.tick(self.fps)
        self.screen.fill(colors.white)
        if pygame.event.get(pygame.QUIT): exitgame()
        self.event = pygame.event.get()

      

def center(a,b): return (a[0]-b[0]/2,a[1]-b[1]/2)

class grid:
    def __init__(self, gs, ps, ms, speed):
        self.active = False
        self.gs, self.ps, self.ms, self.speed = gs, ps, ms, speed
        self.rect = pygame.Rect(0, 0, ms[0]+gs[0]*(ps[0]+ms[0]), ms[1]+gs[1]*(ps[1]+ms[1]))

#used this youtube video to learn how to code the shapes
#https://www.youtube.com/watch?v=kF6ki_rR8Fw
        self.shapes = '02.45/1010/22._33/_33.22/464._4/5.5.52/_6._6.56'.split('/')
        # self.shape_colors = [colors.red,colors.orange,colors.lime,colors.lblue,colors.yellow,colors.blue,colors.lpurple]
        self.shape_colors = [colors.red,colors.red,colors.red,colors.red,colors.red,colors.red,colors.red]

        self.resetgame()
        self.movespeed = 8
        self.movedelay = 0

    def resetgame(self):
        self.tiles, self.colors = [], []
        self.pos, self.orient = [self.gs[0]//2,0], 0
        self.game_over, self.score, self.lines, self.frame = False, 0, 0, 0
        self.current, self.next = random.randrange(len(self.shapes)), [random.randrange(len(self.shapes)) for i in range(4)]

    def convert(self,s,o,pos=(0,0)):
        s = s.split('.')
        h,w = len(s)-1,len(max(s))-1
        return [(pos[0]+([x,h-y,w-x,y][o])-1,pos[1]+([y,x,h-y,w-x][o])-h-1) for y in range(len(s)) for x in range(len(s[y])) if s[y][x]!='_']

    def get_colors(self,current,i=None):
        body = self.convert(self.shapes[current],0)
        x,y = min(body,key=lambda i:i[0])[0], min(body,key=lambda i:i[1])[1]
        if i!=None: return int(self.shapes[current].split('.')[body[i][1]-y][body[i][0]-x])
        else: return [int(self.shapes[current].split('.')[row-y][col-x]) for col,row in body]

    def run(self, up, down, left, right):
        self.active = 0
        if key.state("UP"): self.rect.y-=self.speed
        if key.state("DOWN"): self.rect.y+=self.speed
        if key.state("LEFT"): self.rect.x-=self.speed
        if key.state("RIGHT"): self.rect.x+=self.speed

        if not self.game_over:
            self.fallspeed = 12 if key.state(down) else 3

            self.body = self.convert(self.shapes[self.current],self.orient,self.pos)

  #the following code makes the block fall down immediately
            if key.down("SPACE"):
                while not any([(i[0],i[1]+1) in self.tiles or i[1]>self.gs[1]-2 for i in self.body]):
                    self.pos[1]+=1
                    self.body = self.convert(self.shapes[self.current],self.orient,self.pos)

            left_key = key.state(left) and all([(i[0]-1,i[1]) not in self.tiles and i[0]>0 and i[0]<self.gs[0] for i in self.body])
            right_key = key.state(right) and all([(i[0]+1,i[1]) not in self.tiles and i[0]>-2 and i[0]<self.gs[0]-1 for i in self.body])

            if self.movedelay: self.movedelay-=1
            if left_key ^ right_key:
                l,r = key.down(left), key.down(right)
                if l or r: self.movedelay = main.fps//3
                self.pos[0] = self.pos[0] + (-1 if l else 1 if r else 0)
                if not (self.frame%(main.fps//self.movespeed) or self.movedelay): self.pos[0] = self.pos[0] + (-1 if left_key else 1 if right_key else 0)
                self.body = self.convert(self.shapes[self.current],self.orient,self.pos)

            rotated_tiles = self.convert(self.shapes[self.current],(self.orient+1)%4,self.pos)
            rotate_valid = all([i not in self.tiles and i[0]>=0 and i[0]<self.gs[0] and i[1]<self.gs[1] for i in rotated_tiles])
            if key.down(up) and rotate_valid: self.orient, self.body = (self.orient+1)%4, self.convert(self.shapes[self.current],(self.orient+1)%4,self.pos)

            if self.frame%(main.fps//self.fallspeed)==0:
                if any([(i[0],i[1]+1) in self.tiles or i[1]>self.gs[1]-2 for i in self.body]):
                    if all([i>=0 for tile in self.body for i in tile]):
                        # self.score+=25
                        self.tiles+=self.body
                        self.colors+=self.get_colors(self.current)
                            
                        self.pos, self.orient, self.current, self.next = [self.gs[0]//2,0], 0, self.next[0], self.next[1:]+[random.randrange(len(self.shapes))]
                        lines = [y for y in range(self.gs[1]) if len([0 for x in range(self.gs[0]) if (x,y) in self.tiles])==self.gs[0]]
                        self.lines, self.score = self.lines+len(lines), self.score+len(lines)*150

                        for y in lines:
                            for x in range(self.gs[0]): del self.colors[self.tiles.index((x,y))]; del self.tiles[self.tiles.index((x,y))]
                            self.tiles = [(i[0],i[1]+1) if i[1]<y else i for i in self.tiles]

                    else: self.game_over = True
                else: self.pos[1]+=1

            self.frame = (self.frame+1)%main.fps


#this is the background for our game
    def draw_background(self,rect,color1,color2,color3):
        pygame.draw.rect(main.screen, color1, (rect.x-6,rect.y-6,rect.width+12,rect.height+12))
        # this draws the black box in which the blocks fall down
        for i in range(0,rect.width+10,10): pygame.draw.line(main.screen, color2, (rect.left+i,rect.top),(rect.left+(i-rect.height if i>rect.height else 0),rect.top+i if i<rect.height else rect.bottom),4)
        for i in range(-1,rect.height,10): pygame.draw.line(main.screen, color2, (rect.right,rect.bottom-i),(rect.right-i if i<rect.width else rect.left,rect.bottom-(i-rect.width if i>rect.width else 0)),4)
        pygame.draw.rect(main.screen, color3, (rect.x-6,rect.y-6,rect.width+12,rect.height+12), 6)

#draws the game blocks
    def draw_tile(self,tile,color,pos=None):
        if not pos: pos = self.rect.topleft
        x,y,w,h = pygame.Rect((pos[0]+tile[0]*(self.ps[0]+self.ms[0])+self.ms[0], pos[1]+tile[1]*(self.ps[1]+self.ms[1])+self.ms[1]), self.ps)
        pygame.draw.rect(main.screen, colors.black, (x-self.ms[0],y-self.ms[1],w+self.ms[0]*2,h+self.ms[1]*2))
        pygame.draw.rect(main.screen, color, (x,y,w,h))


    def draw(self):
        self.active = True if type(self.active)==int else False
        
        self.draw_background(self.rect,colors.white,colors.white,colors.black)
        [self.draw_tile(i,self.shape_colors[self.get_colors(self.current,self.body.index(i))]) for i in self.body if i[0]>=0 and i[0]<self.gs[0] and i[1]>=0 and i[1]<self.gs[1]]
        [self.draw_tile(self.tiles[i],self.shape_colors[self.colors[i]]) for i in range(len(self.tiles))]

        for z in range(len(self.next)):
            tiles = self.convert(self.shapes[self.next[z]],0)
            [self.draw_tile(tiles[i],self.shape_colors[self.get_colors(self.next[z],i)],(self.rect.right+50,self.rect.y+120+(z*100))) for i in range(len(tiles))]


main = setup((600,600),"Tetris",60)

tetris = grid((10,20),(24,24),(4,4),10)
tetris.rect.center = main.screen.get_rect().center

while True:
    main.events()
    tetris.run("w","s","a","d")
    tetris.draw()
