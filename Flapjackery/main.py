import pygame
import animhandler as anim
import random

pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("assets/sounds/music.wav")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.25)

screen = pygame.display.set_mode((1600,800))
pygame.display.set_caption("Flapjackery")
pygame.display.set_icon(anim.syrup6)
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
pancakes = []
pancakerects = []
pancake1 = pygame.image.load("assets/images/pancake/pancake1.png").convert_alpha()
pancake2 = pygame.image.load("assets/images/pancake/pancake2.png").convert_alpha()
pancake3 = pygame.image.load("assets/images/pancake/pancake3.png").convert_alpha()
pancakeimages = [pancake1, pancake2, pancake3]

inventorybg = pygame.rect.Rect((0,0),(300,400))
gridbox = pygame.image.load("assets/images/gridbox.png").convert_alpha()
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
                for c in buildings:
                    if c.buildingtype > 4 and c.pancakeloaded and (any(i.collidepoint(c.collisionposses[0]) for i in pancakerects) or c.tilecollisions[0] - c.tilecollisions[1] != 1) and c.tilecollisions[0] != -1:
                        screen.blit(anim.pcframes[c.buildingtype - 5], (c.rect.topleft))
                    elif c.buildingtype > 4 and c.pancakeloaded and c.tilecollisions[0] == -1:
                        screen.blit(anim.pcframes[c.buildingtype - 5], (c.rect.topleft))
                    elif c.buildingtype > 4 and not c.pancakeloaded:
                        b.playanim(b.buildingtype)
        else:
            if b.buildingtype <= 4:
                b.playanim(b.buildingtype)
            else:
                b.playanim(b.buildingtype + 4)

def placement():
    global dragmode, mouseheld, dragindex, inventoryopen
    leftbutton = pygame.mouse.get_pressed()[0]
    if leftbutton and not inventoryopen:
        for b in buildingrects:
            if b.collidepoint(mousepos) and not mouseheld:
                dragindex = buildingrects.index(b)
                inventoryopen = False
                dragmode = True
        mouseheld = True
    elif not leftbutton:
        mouseheld = False
    if dragmode and round(mousepos[0], -2) <= 1500 and round(mousepos[1], -2) <= 700 and round(mousepos[0], -2) >= 0 and round(mousepos[1], -2) >= 0:
        gridx = int(round(mousepos[0] / 100))
        gridy = int(round(mousepos[1] / 100))
        if buildinggrid[gridy][gridx] == -1 and not any(p.collidepoint(gridx, gridy) for p in pancakerects):
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
        self.nearbyconveyers = []
        self.nextmovepoint = 0
        self.pancakeloaded = False
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
                self.currentframeindex = 1
                self.workcycle = True
                self.working = False
            self.currentframe = self.animlist[self.currentframeindex - 1]
            self.lastswitchedframe = currenttime
        screen.blit(self.currentframe, (self.rect.topleft))

    def work(self):
        self.tilecollisions = []
        self.collisionposses = []
        if any(i.colliderect(self.rect) for i in pancakerects):
            self.pancakeloaded = True
        else:
            self.pancakeloaded = False
        if self.buildingtype <= 4:
            try:
                self.tilecollisions.append(buildinggrid[self.tile[0] - 1][self.tile[1]])
                self.collisionposses.append((int((self.rect.x)), int((self.rect.y - 100))))
            except IndexError:
                pass
            try:
                self.tilecollisions.append(buildinggrid[self.tile[0] + 1][self.tile[1]])
                self.collisionposses.append((int((self.rect.x)), int((self.rect.y + 100))))
            except IndexError:
                pass
            try:
                self.tilecollisions.append(buildinggrid[self.tile[0]][self.tile[1] - 1])
                self.collisionposses.append((int((self.rect.x - 100)), int((self.rect.y))))
            except IndexError:
                pass
            try:
                self.tilecollisions.append(buildinggrid[self.tile[0]][self.tile[1] + 1])
                self.collisionposses.append((int((self.rect.x + 100)), int((self.rect.y))))
            except IndexError:
                pass
        else:
            if self.buildingtype == 5:
                try:
                    self.tilecollisions.append(buildinggrid[self.tile[0] - 1][self.tile[1]])
                    self.collisionposses.append((int((self.rect.x)), int((self.rect.y - 100))))
                    self.tilecollisions.append(buildinggrid[self.tile[0] + 1][self.tile[1]])
                    self.collisionposses.append((int((self.rect.x)), int((self.rect.y + 100))))
                except IndexError:
                    pass
            elif self.buildingtype == 6:
                try:
                    self.tilecollisions.append(buildinggrid[self.tile[0] + 1][self.tile[1]])
                    self.collisionposses.append((int((self.rect.x)), int((self.rect.y + 100))))
                    self.tilecollisions.append(buildinggrid[self.tile[0] - 1][self.tile[1]])
                    self.collisionposses.append((int((self.rect.x)), int((self.rect.y - 100))))
                except IndexError:
                    pass
            elif self.buildingtype == 7:
                try:
                    self.tilecollisions.append(buildinggrid[self.tile[0]][self.tile[1] - 1])
                    self.collisionposses.append((int((self.rect.x - 100)), int((self.rect.y))))
                    self.tilecollisions.append(buildinggrid[self.tile[0]][self.tile[1] + 1])
                    self.collisionposses.append((int((self.rect.x + 100)), int((self.rect.y))))
                except IndexError:
                    pass
            elif self.buildingtype == 8:
                try:
                    self.tilecollisions.append(buildinggrid[self.tile[0]][self.tile[1] + 1])
                    self.collisionposses.append((int((self.rect.x + 100)), int((self.rect.y))))
                    self.tilecollisions.append(buildinggrid[self.tile[0]][self.tile[1] - 1])
                    self.collisionposses.append((int((self.rect.x - 100)), int((self.rect.y))))
                except IndexError:
                    pass
        self.movedpancake = False
        if self.workcycle:
            self.workcycle = False
            self.nearbyconveyers = []
            self.tilecollisionindex = 0

            for t in self.tilecollisions: # detect conveyers
                if t > 4:
                    self.nearbyconveyers.append(self.collisionposses[self.tilecollisionindex])
                self.tilecollisionindex += 1

            for p in pancakes: # move the pancake (to a conveyer)
                availableconveyers = [c for c in self.nearbyconveyers if c != p.previousconveyer]
                if self.rect.topleft == p.rect.topleft and len(availableconveyers) > 0 and self.movedpancake == False:
                    try:
                        self.nextmovepoint = availableconveyers[random.randint(0,(len(availableconveyers)-1))]
                        if not any(i.collidepoint(self.nextmovepoint) for i in pancakerects):
                            p.rect.topleft = self.nextmovepoint
                            p.stage = self.buildingtype
                            self.movedpancake = True
                        else:
                            self.working = False
                    except ValueError:
                        try:
                            if not any(i.collidepoint(self.nextmovepoint) for i in pancakerects):
                                p.rect.topleft = availableconveyers[0]
                                p.stage = self.buildingtype
                                self.movedpancake = True
                            else:
                                self.working = False
                        except:
                            pass

        if not self.working and any(n > 4 for n in self.tilecollisions): # update conveyers
            self.nearbyconveyers = []
            for i, t in enumerate(self.tilecollisions):
                if t > 4:
                    self.nearbyconveyers.append(self.collisionposses[i])

            if self.buildingtype == 0: # mixers (pancake origin)
                for t in self.nearbyconveyers:
                    if any(p.collidepoint(t) for p in pancakerects):
                        pass
                    else:
                        newpancake = Pancake(self.rect.x, self.rect.y)
                        newpancake.tile = self.tile
                        self.working = True

            elif self.buildingtype != 0 and self.buildingtype < 5: # check work (all other buildings)
                for p in pancakerects:
                    if p.colliderect(self.rect):
                        self.working = True

        elif self.buildingtype > 4: # conveyers
            for c in self.collisionposses:
                for p in pancakerects:
                    if p.colliderect(self.rect) and not any(i.collidepoint(self.collisionposses[0]) for i in pancakerects) and self.tilecollisions[0] != -2 and (self.tilecollisions[0] != -1 or pancakes[pancakerects.index(p)].stage > 1):
                        if (self.tilecollisions[0] > -1 and self.tilecollisions[0] < 5 and self.tilecollisions[0] - self.tilecollisions[1] == 1) or self.tilecollisions[0] == -1:
                            self.working = True
                            pancakes[pancakerects.index(p)].previousconveyer = self.rect.topleft
                            p.topleft = c

class Pancake():
    def __init__(self, x, y):
        self.rect = pygame.rect.Rect((x,y),(100,100))
        self.tile = (int((self.rect.y / 100)), int((self.rect.x / 100)))
        self.stage = 0
        self.value = 0
        self.previousconveyer = None
        pancakes.append(self)
        pancakerects.append(self.rect)

    def delete(self):
        pancakes.remove(self)
        pancakerects.remove(self.rect)

    def collect(self):
        global cash
        self.value = self.stage * 5
        cash += self.value
        self.delete()

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
    for p in pancakes:
        if not any(p.rect.colliderect(b) for b in buildingrects):
            buildinggrid[int((p.rect.y / 100))][int((p.rect.x / 100))] = -2

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
                        inventoryopen = False
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and not inventoryopen and any(p.collidepoint(mousepos) for p in pancakerects):
            for p in pancakes:
                if p.rect.collidepoint(mousepos) and not any(p.rect.colliderect(b) for b in buildings) and p.stage > 1:
                    p.collect()

    placement()
    for b in buildings:
        b.work()
    if not inventoryopen:
        purchasebuttons.clear()
    renderbuildings()
    #for p in pancakerects: # temporary lines for hitbox rendering for debug -- maybe add as a toggleable feature?
        #screen.blit(gridbox, p)
    renderui()
    for p in pancakes:
        if not any(p.rect.colliderect(b) for b in buildingrects):
            if p.stage > 1:
                screen.blit(pancakeimages[p.stage - 2], (p.rect))
            else:
                p.delete()
    pygame.display.flip()
    clock.tick(60)
pygame.quit()