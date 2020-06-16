import pygame
import neat
import random
import tkinter as tk
import os
from tkinter import messagebox
class Snake :
    body = []
    turns = {}
    def __init__(self,color,pos):
        super().__init__()
        self.color=color
        self.head=cube(pos)
        self.body.append(self.head)
        self.dirnx=0
        self.dirny=1
    def move(self):
        for event in pygame.event.get() :
            if event.type ==pygame.QUIT :
                pygame.quit()
            keys = pygame.key.get_pressed()
            for key in keys :
                if keys[pygame.K_LEFT]:
                    dirnx=-1
                    dirny=0
                    self.dirnx=dirnx
                    self.dirny=dirny
                    self.turns[self.head.pos[:]]=[self.dirnx,self.dirny]
                elif keys[pygame.K_RIGHT]:
                    dirnx=1
                    dirny=0
                    self.dirnx=dirnx
                    self.dirny=dirny
                    self.turns[self.head.pos[:]]=[self.dirnx,self.dirny]
                elif keys[pygame.K_UP]:
                    dirny=-1
                    dirnx=0
                    self.dirnx=dirnx
                    self.dirny=dirny
                    self.turns[self.head.pos[:]]=[self.dirnx,self.dirny]
                elif keys[pygame.K_DOWN]:
                    dirny=1
                    dirnx=0
                    self.dirnx=dirnx
                    self.dirny=dirny
                    self.turns[self.head.pos[:]]=[self.dirnx,self.dirny]
        for i,c in enumerate(self.body) :
            p=c.pos[:]
            if p in self.turns :
                turn = self.turns[p]
                c.move(turn[0],turn[1])
                if i==len(self.body)-1:
                    self.turns.pop(p)
            else:
                if c.dirnx==-1 and c.pos[0]<=0 : c.pos = (c.rows-1 , c.pos[1])
                elif c.dirnx==1 and c.pos[0]>=c.rows-1 : c.pos = (0, c.pos[1])
                elif c.dirny==-1 and c.pos[1]<=0 : c.pos = (c.pos[0] , c.rows -1)
                elif c.dirny==1 and c.pos[1]>=c.rows-1 : c.pos = (c.pos[0] , 0)
                else :
                    c.move(c.dirnx,c.dirny)
    def reset(self,pos):
        self.head=cube(pos)
        self.body=[]
        self.body.append(self.head)
        self.turns={}
        self.dirnx=0
        self.dirny=0
    def addCube(self):
        tail=self.body[-1]
        dx,dy=tail.dirnx,tail.dirny
        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1,tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1,tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0],tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0],tail.pos[1]+1)))
 
        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy
    def draw(self,surface):
        for i,c in enumerate(self.body):
            c.draw(surface)
class cube :
    w=500
    rows=20
    def __init__(self,start , dirnx=1,dirny=0,color=(255,0,0)):
        super().__init__()
        self.pos = start
        self.dirnx=dirnx
        self.dirny=dirny
        self.color=color
    def move(self,dirnx,dirny):
        self.dirnx=dirnx
        self.dirny=dirny
        self.pos=(self.pos[0]+self.dirnx,self.pos[1]+self.dirny)
    def draw(self,surface):
        dis=self.w//self.rows
        i=self.pos[0]
        j=self.pos[1]
        pygame.draw.rect(surface,self.color,(i*dis+1,j*dis+1,dis+2,dis+2))
def drawGrid(surface,rows,width):
    sizeBetween = width // rows
    x=0
    y=0
    for l in range(rows):
        x=x+sizeBetween
        y=y+sizeBetween

        pygame.draw.line(surface,(255,255,255),(x,0),(x,width))
        pygame.draw.line(surface,(255,255,255),(0,y),(width,y))

def redrawWindow (surface) :
    global rows , width , s , snack
    surface.fill((0,0,0))
    s.draw(surface)
    snack.draw(surface)
    drawGrid(surface,rows,width)
    pygame.display.update()
def randomSnack(rows,item):
    positions=item.body
    while True :
        x=random.randrange(rows)
        y=random.randrange(rows)
        if len(list(filter(lambda x: x.pos==(x,y),positions))) > 0 :
            continue
        else :
            break
    return x,y
def message_box(subject,content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass 
def run (config_path) :
    config=neat.config.Config(neat.DefaultGenome,neat.DefaultReproduction,
    neat.DefaultSpeciesSet , neat.DefaultStagnation , config_path
    )
    p= neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    winner = p.run(main,50)
def main(genomes,config):
    global width,rows,s , snack
    nets=[]
    ge=[]
    snakes=[]
    for _,g in genomes :
        net = neat.nn.FeedForwardNetwork.create(g,config)
        nets.append(net)
        snakes.append(Snake((255,0,0),(10,10)))
        g.fitness= 0
        ge.append(g)
    width=500
    rows=20
    surface=pygame.display.set_mode((width,width))
    s=Snake((255,0,0),(10,10))
    snack=cube(randomSnack(rows,s),color=(0,255,0))
    flag=True
    clock = pygame.time.Clock()
    while flag :
        pygame.time.delay(50)
        clock.tick(10)
        for x,s in enumerate(snakes) :
            s.move()
            ge[x].fitness += 0.2
            output = nets[x].activate()
            if output[0] > 0.5 :
                bird.jump()
        s.move()
        if s.body[0].pos==snack.pos :
            s.addCube()
            snack=cube(randomSnack(rows,s),color=(0,255,0))
        if s.body[0].pos in list(map(lambda x : x.pos,s.body[1:])):
            print('Score: ',len(s.body))
            message_box('You lost','Play again ... Score : {}'.format(len(s.body)))
            s.reset((10,10))
            break

        redrawWindow(surface)
    pass
if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir,"config.txt")
    run(config_path)