#!/usr/bin/python3


__author__ = 'Rohit Joshi'


from tkinter import *
from time import sleep
from random import randint,choice
from pygame import mixer

class Obstacle:
    
    def __init__(self,canvas,color,height):
        self.obstacles=[]
        self.canvas=canvas
        x=600
        self.y=0
        self.color=["red","yellow","green","blue"]
        for i in range(3):
            self.new_obstacle(0)
        for log in self.obstacles:
            self.canvas.move(log,x,0)
            x+=300
        self.speed=1
        self.game_over=False
        
    def new_obstacle(self,x):
        color = choice(self.color)
        height = randint(100,300)
        position = randint(0,600-height)
        self.id=self.canvas.create_rectangle(x,position,x+50,position+height,fill=color)   
        self.obstacles.append(self.id)
        
    def draw(self):
        self.collide=False
        for log in self.obstacles:
            self.canvas.move(log,-self.speed,0)
            self.pos=self.canvas.coords(log)        
            if self.pos[2]<=0:
                self.obstacles.remove(log)
                self.canvas.delete(log)
                self.new_obstacle(1150)
                
    

class Coords:
    def __init__(self,x1=0,y1=0,x2=0,y2=0):
        self.x1=x1
        self.y1=y1
        self.x2=x2
        self.y2=y2
    def within_x(self,co1,co2):
        if (co1.x1>co2.x1 and co1.x1<co2.x2)\
                or (co1.x2>co2.x1 and co1.x2<co2.x2)\
                or (co2.x1>co1.x1 and co2.x1<co1.x2)\
                or (co2.x2>co1.x1 and co2.x2<co1.x1):
            return True
        else:
            return False
    def within_y(self,co1,co2):
        if (co1.y1>co2.y1 and co1.y1<co2.y2)\
                or (co1.y2>co2.y1 and co1.y2<co2.y2)\
                or (co2.y1>co1.y1 and co2.y1<co1.y2)\
                or (co2.y2>co1.y1 and co2.y2<co1.y1):
            return True
        else:
            return False
        
class Ball:
    def __init__(self,canvas,color,log):
        self.canvas=canvas
        self.images=[]
        self.i = 0
        for i in range(1,7):
            self.images.append(PhotoImage(file="photos/heli%d.gif"%i))
        self.id=canvas.create_image(200,300,image=self.images[self.i],anchor='nw')
        self.x = 10
        self.y = 10
        self.g = 0.5
        self.canvas.bind_all('<KeyPress>',self.key_pressed)
        self.state=True
        self.collide = False
        self.log = log
        
    def key_pressed(self,event):
        key = event.keysym
        pos=self.canvas.bbox(self.id)
        self.x = 0
        self.y = 0
        if self.state:
            if (key == "Up" or key == "space") and pos[1]>25:
                self.x = 0
                self.y = -10
            elif key == "Down" and pos[3]<575:
                self.x = 0
                self.y = 10
            elif key == "Right" and pos[2]<600:
                self.x = 10
                self.y = 0
            elif key == "Left" and pos[0]>0:
                self.x = -10
                self.y = 0

            # elif key == "enter":
            #     self.pause = True

            self.canvas.move(self.id,self.x,self.y)
            
    def check(self):
        posheli  = self.canvas.bbox(self.id)
        for obs in self.log.obstacles:
            self.pos=self.canvas.coords(obs)
            self.check_collision()
        if posheli[1]<=25 or posheli[3]>=575:
            self.collide = True
        if self.collide==True:
            self.over()
            
    def fall(self):
        if self.pos[3]<600:
            self.canvas.move(self.id,0,self.g)
    def fallfast(self):
        
        self.pos=self.canvas.bbox(self.id)
        if self.pos[3]<600:
            self.canvas.move(self.id,0,4)
            
    def animate(self):
        if self.i<4:
            self.i+=1
        else:
            self.i=0
        self.canvas.itemconfig(self.id,image=self.images[self.i])
        
    def check_collision(self):
        obs=Coords(self.pos[0],self.pos[1],self.pos[2],self.pos[3])
        self.posb=self.canvas.bbox(self.id)
        heli=Coords(self.posb[0],self.posb[1],self.posb[2],self.posb[3])
        if obs.within_x(obs,heli) and obs.within_y(obs,heli):
            self.collide=True
        
        
    def over(self):
        mixer.music.load('sound/crash.ogg')
        mixer.music.play(1,1)
        self.text=self.canvas.create_text(200,200,text="Game Over",font=("times",30))
        tk.update()
        self.state=False
        self.game_over=True
        
class Scorebox:
    def __init__(self,canvas,color):
        self.canvas=canvas
        self.id1=canvas.create_rectangle(0,0,100,60,fill=color)
        self.canvas.move(self.id1,10,35)
        self.h=0
        self.id2=self.canvas.create_text(0,0,text=self.h,font=("Times",20))
        self.canvas.move(self.id2,55,60)  
    def change_score(self):
        self.h=self.h+1
        self.canvas.itemconfig(self.id2,text=self.h)
        
def thorn(canvas):
    x = 0
    while x<600:
        canvas.create_polygon(x,0,x+15,25,x+30,0,fill="black")
        x+=30
    x = 0
    while x<600:
        canvas.create_polygon(x,600,x+15,575,x+30,600,fill="black")
        x+=30


tk=Tk()
tk.title("Heli Fly")
canvas=Canvas(tk,width=600,height=600)
canvas.pack()
tk.update()

def main():
    mixer.init()
    mixer.music.load('sound/fly.ogg')
    mixer.music.play(-1,0.0)

    log=Obstacle(canvas,"green",250)
    ball=Ball(canvas,"red",log)
    score=Scorebox(canvas,"gray")
    thorn(canvas)

    while True:
        if log.game_over==False and ball.state==True:
            log.draw()
            ball.check()
            ball.fall()
            ball.animate()
            tk.update()
            score.change_score()
            sleep(0.01)
        else:
            canvas.itemconfig(ball.id,image=ball.images[5])
            
            while 1:
                pos = canvas.bbox(ball.id)[3]
                ball.fallfast()
                tk.update()
                sleep(0.01)
                if pos>=600:
                    break
            break

    canvas.delete('all')
    sleep(2)
    main()
    tk.mainloop()  


try:
    main()
except TclError:
    print('Game Closed')
