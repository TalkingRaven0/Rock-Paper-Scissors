import pygame
import random

h = 20
w = 20

class EntityGroup:
    def __init__(self):
        super().__init__()
        self.rocks = []
        self.papers = []
        self.scissors = []

    def add(self,obj,group):
        if group == 0:
            self.rocks.append(obj)
        elif group == 1:
            self.papers.append(obj)
        elif group == 2:
            self.scissors.append(obj)
    
    def draw(self,screen):
        for obj in self.rocks:
            obj.draw(screen)
        for obj in self.papers:
            obj.draw(screen)
        for obj in self.scissors:
            obj.draw(screen)
    
    def update(self):
        for obj in self.rocks:
            obj.update()
        for obj in self.papers:
            obj.update()
        for obj in self.scissors:
            obj.update()

    def get_from_grp(self,group):
        if group == 0 and len(self.rocks)!=0:
            index = random.randint(0,len(self.rocks)-1)
            return self.rocks[index]
        if group == 1 and len(self.papers)!=0:
            index = random.randint(0,len(self.papers)-1)
            return self.papers[index]
        if group == 2 and len(self.scissors)!=0:
            index = random.randint(0,len(self.scissors)-1)
            return self.scissors[index]

    def remove_from_grp(self,group,target):
        if group == 0:
            self.rocks.remove(target)
        if group == 1:
            self.papers.remove(target)
        if group == 2:
            self.scissors.remove(target)

    def return_group(self,group):
        if group == 0:
            return self.rocks
        if group == 1:
            return self.papers
        if group == 2:
            return self.scissors
            

# Object Interface
class Iobject(pygame.sprite.Sprite):
    def draw(self, screen):
        self.x=clamp(self.x,0,screen.get_width()-w)
        self.y=clamp(self.y,0,screen.get_height()-h)
        screen.blit(self.image,(self.x,self.y))

    def go_to(self, obj):
        if (obj==None):
            return
        pos = (obj.x,obj.y)
        dir = ( pos[0] - self.x, pos[1] - self.y )
        dir = normalize(dir)
        self.x+=dir[0]
        self.y+=dir[1]

    def die(self):
        self.grpEntity.remove_from_grp(self.grp,self)
        if self.prey is not None:
            self.prey.predators.remove(self)
        self.kill()

    def transform(self):
        self.die()
        convert = self.enemy(self.grpEntity,self.x,self.y)
        self.grpEntity.add(convert,self.egrp)
        for pred in self.predators:
            if isinstance(pred, type(None)):
                break
            pred.prey=None
    
    def detect(self):
        self.rect.update(self.x,self.y,w,h)
        for obj in self.grpEntity.return_group(self.egrp):
            collided = pygame.sprite.collide_rect(self,obj)
            if collided:
                self.transform()
                return
        #collided = pygame.sprite.collide_rect(self,self.prey)
        #if collided:
        #    self.transform()
        #    return

    def update(self):
        if self.freeze > 0:
            self.freeze-=1
            return
        #self.firstAI()
        #self.cowardAI()
        #self.efficientAI()
        #self.cowardEfficientAI()
        #self.smartCowardAI()
        self.SmartcowardEfficientAI()
        self.detect()

    ## AI LOOPS ##

    def firstAI(self):
        # Picks Random Target
        if self.prey == None:
            self.prey = self.grpEntity.get_from_grp(self.target)
            if self.prey is not None:
                self.prey.predators.append(self)
        else:
            self.go_to(self.prey)

    def efficientAI(self):
        # Picks Closest Target
        closestPrey = (9999,None)
        if closestPrey[1] is None:
            for prey in self.grpEntity.return_group(self.target):
                if prey is None:
                    closestPrey = (0,None)
                    break
                dist = abs(self.x - prey.x) + abs(self.y-prey.y)
                if dist < closestPrey[0]:
                    closestPrey = (dist,prey)
            self.go_to(closestPrey[1])

    def cowardEfficientAI(self):
        # Picks Closest Target but avoids Closest Threat
        closestPred = (9999,None)
        for pred in self.grpEntity.return_group(self.egrp):
            if pred is None:
                closestPred = (0,None)
                break
            dist = abs(self.x - pred.x) + abs(self.y-pred.y)
            if dist < closestPred[0]:
                closestPred = (dist,pred)
        if closestPred[1] is not None:
            pos = (closestPred[1].x,closestPred[1].y)
            dir = ( pos[0] - self.x, pos[1] - self.y )
            dir = normalize(dir)
            self.x-=dir[0]*1.1
            self.y-=dir[1]*1.1
        closestPrey = (9999,None)
        if closestPrey[1] is None:
            for prey in self.grpEntity.return_group(self.target):
                if prey is None:
                    closestPrey = (0,None)
                    break
                dist = abs(self.x - prey.x) + abs(self.y-prey.y)
                if dist < closestPrey[0]:
                    closestPrey = (dist,prey)
            self.go_to(closestPrey[1])

    def SmartcowardEfficientAI(self):
        # Chase Closest Target or avoids Closest Threat if in certain distance
        closestPred = (9999,None)
        for pred in self.grpEntity.return_group(self.egrp):
            if pred is None:
                closestPred = (0,None)
                break
            dist = abs(self.x - pred.x) + abs(self.y-pred.y)
            if dist < closestPred[0]:
                closestPred = (dist,pred)
        if closestPred[1] is not None and closestPred[0] < 100:
            pos = (closestPred[1].x,closestPred[1].y)
            dir = ( pos[0] - self.x, pos[1] - self.y )
            dir = normalize(dir)
            self.x-=dir[0]*0.9
            self.y-=dir[1]*0.9
        else:
            closestPrey = (9999,None)
            if closestPrey[1] is None:
                for prey in self.grpEntity.return_group(self.target):
                    if prey is None:
                        closestPrey = (0,None)
                        break
                    dist = abs(self.x - prey.x) + abs(self.y-prey.y)
                    if dist < closestPrey[0]:
                        closestPrey = (dist,prey)
                self.go_to(closestPrey[1])
    
    def cowardAI(self):
        # Picks Random Target but avoids chasing Threats
        closestPred = (9999,None)
        for pred in self.predators:
            if pred is None:
                closestPred = (0,None)
                break
            dist = abs(self.x - pred.x) + abs(self.y-pred.y)
            if dist < closestPred[0]:
                closestPred = (dist,pred)
            
        if closestPred[1] is not None:
            pos = (closestPred[1].x,closestPred[1].y)
            dir = ( pos[0] - self.x, pos[1] - self.y )
            dir = normalize(dir)
            self.x-=dir[0]
            self.y-=dir[1]

        if self.prey is None:
            self.prey = self.grpEntity.get_from_grp(self.target)
            if self.prey is not None:
                self.prey.predators.append(self)
        else:
            self.go_to(self.prey)

    def smartCowardAI(self):
        # Picks Closest Target and only avoids chasing threat if at certain distance
        closestPred = (9999,None)
        for pred in self.predators:
            if pred is None:
                closestPred = (0,None)
                break
            dist = abs(self.x - pred.x) + abs(self.y-pred.y)
            if dist < closestPred[0]:
                closestPred = (dist,pred)
            
        if closestPred[1] is not None and closestPred[0] < 200:
            pos = (closestPred[1].x,closestPred[1].y)
            dir = ( pos[0] - self.x, pos[1] - self.y )
            dir = normalize(dir)
            self.x-=dir[0]
            self.y-=dir[1]

        if self.prey is None:
            self.prey = self.grpEntity.get_from_grp(self.target)
            if self.prey is not None:
                self.prey.predators.append(self)
        else:
            self.go_to(self.prey)


class Rock(Iobject):
    def __init__(self,grpEntity:EntityGroup,x=0,y=0):
        super().__init__()
        self.image = pygame.image.load('resources/rock.png')
        self.image = pygame.transform.scale(self.image,(w,h))
        self.x = x
        self.y = y
        self.prey = None
        self.rect = pygame.Rect(self.x,self.y,w,h)
        self.grp = 0
        self.enemy = Paper
        self.egrp = 1
        self.target= 2
        self.grpEntity=grpEntity
        self.freeze = False
        self.predators=[]

class Paper(Iobject):
    def __init__(self,grpEntity,x=0,y=0):
        super().__init__()
        self.image = pygame.image.load('resources/paper.png')
        self.image = pygame.transform.scale(self.image,(w,h))
        self.x = x
        self.y = y
        self.prey = None
        self.rect = pygame.Rect(self.x,self.y,w,h)
        self.grp = 1
        self.enemy = Scissors
        self.egrp = 2
        self.target=0
        self.grpEntity=grpEntity
        self.freeze = False
        self.predators=[]

class Scissors(Iobject):
    def __init__(self, grpEntity,x=0,y=0):
        super().__init__()
        self.image = pygame.image.load('resources/scissors.png')
        self.image = pygame.transform.scale(self.image,(w,h))
        self.x = x
        self.y = y
        self.prey = None
        self.rect = pygame.Rect(self.x,self.y,50,50)
        self.grp = 2
        self.enemy = Rock
        self.egrp = 0
        self.target = 1
        self.grpEntity = grpEntity
        self.freeze = False
        self.predators=[]

#### Helper Functions #####

def normalize(coords):
    total = abs(coords[0]) + abs(coords[1])
    if total == 0:
        return (0,0)
    newx = coords[0]/total
    newy = coords[1]/total
    pos = (newx,newy)
    return pos

def clamp(n, smallest, largest): 
    return max(smallest, min(n, largest))
