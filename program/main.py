
# import pygame module in this program 
import pygame
from classes import *

pygame.init()

winx = 900
winy = 900

quantity = 30

win = pygame.display.set_mode((winx, winy))
  
pygame.display.set_caption("Rock Paper Scissors Wargame")
  
# object current co-ordinates 
x = 200
y = 200
  
# dimensions of the object 
width = 20
height = 20
  
# velocity / speed of movement
vel = 10
  
# Indicates pygame is running
run = True

group = EntityGroup()
clock = pygame.time.Clock()
counter = quantity
while counter != 0:
    group.add(Rock(group,random.randrange(0,winx),random.randrange(0,winy)),0)
    counter-=1
counter = quantity
while counter != 0:
    group.add(Paper(group,random.randrange(0,winx),random.randrange(0,winy)),1)
    counter-=1
counter = quantity
while counter != 0:
    group.add(Scissors(group,random.randrange(0,winx),random.randrange(0,winy)),2)
    counter-=1
  
def renderScores():
    font = pygame.font.SysFont('arial', 20)
    rocks = font.render("Rocks: " + str(len(group.rocks)), True, (0, 0, 0))
    papers = font.render("Papers: " + str(len(group.papers)), True, (0, 0, 0))
    scissors = font.render("Scissors: " + str(len(group.scissors)), True, (0, 0, 0))
    win.blit(rocks, (0,0))
    win.blit(papers, (0,20))
    win.blit(scissors, (0,40))

# infinite loop 
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:      
            run = False

    win.fill("WHITE")
    
    group.draw(win)
    group.update()
    renderScores()
    clock.tick(60)
    pygame.display.update()
  
# closes the pygame window 
pygame.quit()
