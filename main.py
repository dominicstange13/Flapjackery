import pygame
import animhandler as anim
import random

pygame.init()

screen = pygame.display.set_mode((1600,800))
clock = pygame.time.Clock()
currenttime = pygame.time.get_ticks()

mousepos = pygame.mouse.get_pos()
mouserect = pygame.rect.Rect((0,0),(10,10))

testrect = pygame.rect.Rect((0,0),(100,100))
dragmode = False
mouseheld = False
istilefree = True
dragindex = -1

newpancake = 0

inventorybg = pygame.rect.Rect((0,0),(300,400))
gridbox = pygame.image.load("assets/images/gridbox.png")
purchasebuttons = []
inventoryopen = False

cash = 0

def renderui():
    global cash, inventoryopen, inventorybg, purchasebuttons
    cashfont = pygame.font.Font("assets/fonts/mainfont.otf", 48)
    cashcounter = cashfont.render(f"${cash}", True, "yellow2")
    screen.blit(cashcounter, (10,0))
    if inventoryopen:
        for r in range(8):
            for i in range(16):
                screen.blit(gridbox, ((i*100),(r*100)))
        pygame.draw.rect(screen, "gray", inventorybg)
        purchasebuttons.clear()
        iconyvalue = inventorybg.y + 15
        iconxvalue = inventorybg.x + 20
        iconindex = -1
        for _ in range(3):
            for i in range(5):
                if iconindex < (len(anim.defaultframes) - 1):
                    iconindex += 1
                    newpurchasebutton = pygame.transform.scale_by(anim.defaultframes[iconindex], 0.5)
                    newpurchasebuttonrect = newpurchasebutton.get_rect()
                    newpurchasebuttonrect.topleft = (iconxvalue,iconyvalue)
                    purchasebuttons.append(newpurchasebuttonrect)
                    screen.blit(newpurchasebutton, ((iconxvalue,iconyvalue)))
                    iconyvalue += 80
            iconyvalue = inventorybg.y + 15
            iconxvalue += 80

def renderbuildings():
    for b in buildings:
        if not b.working:
            if b.buildingtype <= 4:
                screen.blit(anim.defaultframes[b.buildingtype], (b.rect.topleft))
            else:
                b.playanim(b.buildingtype)
        else:
            if b.buildingtype <= 4:
                b.playanim(b.buildingtype)
            else:
                b.playanim(b.buildingtype + 4)

def placement():
    global dragmode, mouseheld, dragindex
    leftbutton = pygame.mouse.get_pressed()[0]
    if leftbutton:
        for b in buildingrects:
            if b.collidepoint(mousepos) and not mouseheld:
                dragindex = buildingrects.index(b)
                inventoryopen = False
                dragmode = True
        mouseheld = True
    elif not leftbutton:
        mouseheld = False
    if dragmode and round(mousepos[0], -2) <= 1500 and round(mousepos[1], -2) <= 700 and round(mousepos[0], -2) >= 0 and round(mousepos[1], -2) >= 0:
        if buildinggrid[int(round((mousepos[1] / 100)))][int(round((mousepos[0] / 100)))] == -1:
            istilefree = True
        else:
            istilefree = False
        if istilefree:
            tilemovepos = (round(mousepos[0], -2),round(mousepos[1], -2))
            buildinggrid[int((buildingrects[dragindex].y / 100))][int((buildingrects[dragindex].x / 100))] = buildings[dragindex].buildingtype
            buildingrects[dragindex].topleft = tilemovepos
            buildings[dragindex].tile = (int((buildings[dragindex].rect.y / 100)), int((buildings[dragindex].rect.x / 100)))
        if not leftbutton:
            istilefree = True
            dragmode = False
            dragindex = -1

buildings = []
buildingrects = []

buildinggrid = [
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
    ]

class Building:
    def __init__(self, buildingtype, gridx, gridy):
        self.rect = pygame.rect.Rect(((gridx * 100),(gridy * 100)),(100,100))
        self.buildingtype = buildingtype
        self.working = False
        self.workcycle = False
        self.nextstage = False
        self.currentframe = anim.defaultframes[buildingtype]
        self.currentframeindex = 0
        self.lastswitchedframe = 0
        self.tile = (int((self.rect.y / 100)), int((self.rect.x / 100)))
        buildinggrid[int((self.rect.y / 100))][int((self.rect.x / 100))] = self.buildingtype
        buildings.append(self)
        buildingrects.append(self.rect)

    def playanim(self, framelist):
        self.framecd = 100
        self.animlist = anim.animframes[framelist]
        if currenttime - self.lastswitchedframe >= self.framecd:
            if self.currentframeindex <= (len(self.animlist) - 1):
                self.currentframeindex += 1
            else:
                self.currentframeindex = 0
                self.workcycle = True
            self.currentframe = self.animlist[self.currentframeindex - 1]
            self.lastswitchedframe = currenttime
        screen.blit(self.currentframe, (self.rect.topleft))

    def work(self):
        self.tilecollisions = []
        self.collisionposses = []
        if self.buildingtype <= 4:
            try:
                self.tilecollisions.append(buildinggrid[self.tile[0] - 1][self.tile[1]])
            except IndexError:
                pass
            try:
                self.tilecollisions.append(buildinggrid[self.tile[0] + 1][self.tile[1]])
            except IndexError:
                pass
            try:
                self.tilecollisions.append(buildinggrid[self.tile[0]][self.tile[1] - 1])
            except IndexError:
                pass
            try:
                self.tilecollisions.append(buildinggrid[self.tile[0]][self.tile[1] + 1])
            except IndexError:
                pass
        else:
            if self.buildingtype == 5:
                try:
                    self.tilecollisions.append(buildinggrid[self.tile[0] - 1][self.tile[1]])
                except IndexError:
                    pass
        if self.buildingtype <= 4:
            if self.buildingtype == 0 and not self.working:
                newpancake = Pancake()
                newpancake.tile = self.tile
                self.working = True
                if self.workcycle:
                    self.workcycle = False
                    for t in self.tilecollisions:
                        self.nearbyconveyers = []
                        if t > 4:
                            self.nearbyconveyers.append(t)
                    try:
                        self.nearbyconveyers[random.randint(0,len(self.nearbyconveyers.index(max(self.nearbyconveyers))))]
                    except IndexError:
                        pass
        else:
            self.working = True
            if self.workcycle:
                self.workcycle = False
                self.working = False

class Pancake():
    def __init__(self):
        self.rect = pygame.rect.Rect((0,0),(100,100))
        self.tile = (int((self.rect.y / 100)), int((self.rect.x / 100)))

running = True
while running:
    screen.fill((20,20,20))
    currenttime = pygame.time.get_ticks()
    mousepos = pygame.mouse.get_pos()
    mouserect.center = mousepos
    renderbuildings()
    
    buildinggrid = [
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
    ]
    for b in buildings:
        buildinggrid[int((b.rect.y / 100))][int((b.rect.x / 100))] = b.buildingtype

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            buildingcollisions = mouserect.collidelist(buildingrects)
            if buildingcollisions == -1:
                inventorybg.topright = (mousepos[0],mousepos[1])
                if inventorybg.topright[0] < 300:
                    inventorybg.topright = (300,inventorybg.topright[1])
                if inventorybg.topright[1] > 400:
                    inventorybg.topright = (inventorybg.topright[0], 400)
                placepos = (int((mousepos[0] / 100))),(int((mousepos[1] / 100)))
                inventoryopen = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and inventoryopen:
            if not inventorybg.collidepoint(mousepos):
                inventoryopen = False
            else:
                for p in purchasebuttons:
                    if p.collidepoint(mousepos):
                        if inventoryopen:
                            newbuilding = Building(purchasebuttons.index(p),placepos[0],placepos[1])
                            newbuilding.work()
                        inventoryopen = False
    placement()
    if not inventoryopen:
        purchasebuttons.clear()
    renderbuildings()
    renderui()
    pygame.display.flip()
    clock.tick(60)
pygame.quit()