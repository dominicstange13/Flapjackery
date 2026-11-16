import pygame
import animhandler as anim
originalpcframes = anim.pcframes.copy()
originalanimframes = [frames.copy() for frames in anim.animframes]
originaldefaultframes = anim.defaultframes.copy()
import random

pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("assets/sounds/music.wav")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.25)

screen = pygame.display.set_mode((1600,800))
pygame.display.set_caption("Flapjackery")
lasticonswitch = 0
windowlogoindex = 0
clock = pygame.time.Clock()
currenttime = pygame.time.get_ticks()
scalefactor = 1 # if >1: must be 1 doubled a set # of times (2, 4, etc); if <1: must be 1 divided in half a set # of times (0.5, 0.25, etc)
gridsize = (1 / scalefactor) * 100

mousepos = pygame.mouse.get_pos()
mouserect = pygame.rect.Rect((0,0),(10,10))

testrect = pygame.rect.Rect((0,0),(gridsize,gridsize)) # represents one "tile"
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
gridbox = pygame.transform.scale_by(gridbox, (1 / scalefactor))
purchasebuttons = []
inventoryopen = False

cash = 0

def scaleframes():
    global gridbox
    size = int(gridsize)
    gridboxoriginal = pygame.image.load("assets/images/gridbox.png")
    gridbox = pygame.transform.scale(gridboxoriginal, (size, size))
    for i in range(len(anim.pcframes)): # pancake loaded conveyer frames
        anim.pcframes[i] = pygame.transform.scale(originalpcframes[i], (size, size))
    for a in range(len(anim.animframes)): # working building frames
        for i in range(len(anim.animframes[a])):
            anim.animframes[a][i] = pygame.transform.scale(originalanimframes[a][i], (size, size))
    for i in range(len(anim.defaultframes)): # non-working building frames
        anim.defaultframes[i] = pygame.transform.scale(originaldefaultframes[i], (size, size))
    for b in buildingrects:
        b.width = size
        b.height = size
    for i in range(len(pancakeimages)): # pancake images
        pancakeimages[i] = pygame.image.load(f"assets/images/pancake/pancake{i+1}.png")
        pancakeimages[i] = pygame.transform.scale_by(pancakeimages[i], (1 / scalefactor))
    for b in buildings:
        b.rect.topleft = (b.tile[1] * gridsize, b.tile[0] * gridsize)
    for p in pancakes:
        p.rect.topleft = (p.tile[1] * gridsize, p.tile[0] * gridsize)
        p.rect.size = (size, size)

def renderui():
    global cash, inventoryopen, inventorybg, purchasebuttons
    cashfont = pygame.font.Font("assets/fonts/mainfont.otf", 48)
    cashcounter = cashfont.render(f"${cash}", True, "yellow2")
    screen.blit(cashcounter, (10,0))
    if inventoryopen:
        for r in range(int(8 * scalefactor)):
            for i in range(int(16 * scalefactor)):
                screen.blit(gridbox, ((i*gridsize),(r*gridsize)))
        pygame.draw.rect(screen, "gray", inventorybg)
        purchasebuttons.clear()
        iconyvalue = inventorybg.y + 15
        iconxvalue = inventorybg.x + 20
        iconindex = -1
        for _ in range(3):
            for i in range(5):
                if iconindex < (len(anim.iconframes) - 1):
                    iconindex += 1
                    newpurchasebutton = pygame.transform.scale_by(anim.iconframes[iconindex], 0.5)
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
            if b.buildingtype <= 5:
                screen.blit(anim.defaultframes[b.buildingtype], (b.rect.topleft))
            else:
                for c in buildings:
                    if c.buildingtype > 5 and c.pancakeloaded and (any(i.collidepoint(c.collisionposses[0]) for i in pancakerects) or c.tilecollisions[0] - c.tilecollisions[1] != 1) and c.tilecollisions[0] != -1:
                        screen.blit(anim.pcframes[c.buildingtype - 6], (c.rect.topleft))
                    elif c.buildingtype > 5 and c.pancakeloaded and c.tilecollisions[0] == -1:
                        screen.blit(anim.pcframes[c.buildingtype - 6], (c.rect.topleft))
                    elif c.buildingtype > 5 and not c.pancakeloaded:
                        b.playanim(b.buildingtype)
        else:
            if b.buildingtype <= 5:
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
    if dragmode and (round(mousepos[0] / gridsize) * gridsize) <= (1600 - gridsize) and (round(mousepos[1] / gridsize) * gridsize) <= (800 - gridsize) and (round(mousepos[0] / gridsize) * gridsize) >= 0 and (round(mousepos[1] / gridsize) * gridsize) >= 0:
        # ^^^check if mouse is out of bounds
        gridx = int(round(mousepos[0] / gridsize))
        gridy = int(round(mousepos[1] / gridsize))                                                               
        if buildinggrid[gridy][gridx] == -1 and not any(p.collidepoint(gridx, gridy) for p in pancakerects):
            istilefree = True
        else:
            istilefree = False
        if istilefree:
            tilemovepos = ((round(mousepos[0] / gridsize) * gridsize),(round(mousepos[1] / gridsize) * gridsize))
            buildinggrid[int((buildingrects[dragindex].y / gridsize))][int((buildingrects[dragindex].x / gridsize))] = buildings[dragindex].buildingtype
            buildingrects[dragindex].topleft = tilemovepos
            buildings[dragindex].tile = (int((buildings[dragindex].rect.y / gridsize)), int((buildings[dragindex].rect.x / gridsize)))
        if not leftbutton:
            istilefree = True
            dragmode = False
            dragindex = -1

buildings = []
buildingrects = []

class Building:
    def __init__(self, buildingtype, gridx, gridy):
        self.rect = pygame.rect.Rect(((gridx * gridsize),(gridy * gridsize)),(gridsize,gridsize))
        self.buildingtype = buildingtype
        self.working = False
        self.workcycle = False
        self.nextstage = False
        self.currentframe = anim.defaultframes[buildingtype]
        self.currentframeindex = 0
        self.lastswitchedframe = 0
        self.animloops = 1
        self.loopspercycle = 1
        self.nearbyconveyers = []
        self.nextmovepoint = 0
        self.pancakeloaded = False
        self.tile = (int((self.rect.y / gridsize)), int((self.rect.x / gridsize)))
        buildinggrid[int((self.rect.y / gridsize))][int((self.rect.x / gridsize))] = self.buildingtype
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
                if self.animloops < self.loopspercycle:
                    self.animloops += 1
                else:
                    self.animloops = 1
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
        if self.buildingtype <= 5:
            try:
                self.tilecollisions.append(buildinggrid[self.tile[0] - 1][self.tile[1]])
                self.collisionposses.append((int((self.rect.x)), int((self.rect.y - gridsize))))
            except IndexError:
                pass
            try:
                self.tilecollisions.append(buildinggrid[self.tile[0] + 1][self.tile[1]])
                self.collisionposses.append((int((self.rect.x)), int((self.rect.y + gridsize))))
            except IndexError:
                pass
            try:
                self.tilecollisions.append(buildinggrid[self.tile[0]][self.tile[1] - 1])
                self.collisionposses.append((int((self.rect.x - gridsize)), int((self.rect.y))))
            except IndexError:
                pass
            try:
                self.tilecollisions.append(buildinggrid[self.tile[0]][self.tile[1] + 1])
                self.collisionposses.append((int((self.rect.x + gridsize)), int((self.rect.y))))
            except IndexError:
                pass
        else:
            if self.buildingtype == 6:
                try:
                    self.tilecollisions.append(buildinggrid[self.tile[0] - 1][self.tile[1]])
                    self.collisionposses.append((self.rect.x, self.rect.y - gridsize))
                except IndexError:
                    pass
                try:
                    self.tilecollisions.append(buildinggrid[self.tile[0] + 1][self.tile[1]])
                    self.collisionposses.append((self.rect.x, self.rect.y + gridsize))
                except IndexError:
                    self.tilecollisions.append(-1)
            elif self.buildingtype == 7:
                try:
                    self.tilecollisions.append(buildinggrid[self.tile[0] + 1][self.tile[1]])
                    self.collisionposses.append((self.rect.x, self.rect.y + gridsize))
                except IndexError:
                    self.tilecollisions.append(-1)
                try:
                    self.tilecollisions.append(buildinggrid[self.tile[0] - 1][self.tile[1]])
                    self.collisionposses.append((self.rect.x, self.rect.y - gridsize))
                except IndexError:
                    self.tilecollisions.append(-1)
            elif self.buildingtype == 8:
                try:
                    self.tilecollisions.append(buildinggrid[self.tile[0]][self.tile[1] - 1])
                    self.collisionposses.append((self.rect.x - gridsize, self.rect.y))
                except IndexError:
                    pass
                try:
                    self.tilecollisions.append(buildinggrid[self.tile[0]][self.tile[1] + 1])
                    self.collisionposses.append((self.rect.x + gridsize, self.rect.y))
                except IndexError:
                    self.tilecollisions.append(-1)
            elif self.buildingtype == 9:
                try:
                    self.tilecollisions.append(buildinggrid[self.tile[0]][self.tile[1] + 1])
                    self.collisionposses.append((self.rect.x + gridsize, self.rect.y))
                except IndexError:
                    pass
                try:
                    self.tilecollisions.append(buildinggrid[self.tile[0]][self.tile[1] - 1])
                    self.collisionposses.append((self.rect.x - gridsize, self.rect.y))
                except IndexError:
                    self.tilecollisions.append(-1)
        self.movedpancake = False
        if self.workcycle:
            self.workcycle = False
            self.nearbyconveyers = []
            self.tilecollisionindex = 0

            if self.buildingtype == 5:
                for p in pancakes:
                    if pancakerects[pancakes.index(p)].colliderect(self.rect):
                        p.collect()

            for t in self.tilecollisions: # detect conveyers
                if t > 5:
                    if self.buildingtype <= 5:
                        self.nearbyconveyers.append(self.collisionposses[self.tilecollisionindex])
                    else:
                        if self.collisionposses[self.tilecollisions.index(t)] == self.collisionposses[0]:
                            self.nearbyconveyers.append(self.collisionposses[0])
                        else:
                            pass
                self.tilecollisionindex += 1

            for p in pancakes: # move the pancake (to a conveyer)
                self.availableconveyers = [c for c in self.nearbyconveyers if c != p.previousconveyer]
                if self.rect.topleft == p.rect.topleft and len(self.availableconveyers) > 0 and self.movedpancake == False:
                    try:
                        self.nextmovepoint = self.availableconveyers[random.randint(0,(len(self.availableconveyers)-1))]
                        if not any(i.collidepoint(self.nextmovepoint) for i in pancakerects):
                            p.rect.topleft = self.nextmovepoint
                            if self.buildingtype <= 5:
                                p.stage = self.buildingtype
                            self.movedpancake = True
                        else:
                            self.working = False
                    except ValueError:
                        try:
                            if not any(i.collidepoint(self.nextmovepoint) for i in pancakerects):
                                p.rect.topleft = self.availableconveyers[0]
                                if self.buildingtype <= 5:
                                    p.stage = self.buildingtype
                                self.movedpancake = True
                            else:
                                self.working = False
                        except:
                            pass

        if self.buildingtype <= 5 and not self.working and any(n > 5 for n in self.tilecollisions): # update conveyers
            self.nearbyconveyers = []
            for i, t in enumerate(self.tilecollisions):
                if t > 5:
                    self.nearbyconveyers.append(self.collisionposses[i])

            if self.buildingtype == 0: # mixers (pancake origin)
                for t in self.nearbyconveyers:
                    if any(p.collidepoint(t) for p in pancakerects):
                        pass
                    else:
                        newpancake = Pancake(self.rect.x, self.rect.y)
                        newpancake.tile = self.tile
                        self.working = True

            elif self.buildingtype != 0 and self.buildingtype <= 5: # check work (all other buildings)
                for p in pancakerects:
                    if p.colliderect(self.rect):
                        self.working = True

        elif self.buildingtype > 5: # conveyers
            for c in self.collisionposses:
                for p in pancakerects:
                    if p.colliderect(self.rect) and not any(i.collidepoint(self.collisionposses[0]) for i in pancakerects) and self.tilecollisions[0] != -2 and (self.tilecollisions[0] != -1 or pancakes[pancakerects.index(p)].stage > 1):
                        if (self.tilecollisions[0] > -1 and self.tilecollisions[0] < 5 and self.tilecollisions[0] - pancakes[pancakerects.index(p)].stage == 1) or self.tilecollisions[0] == -1 or (self.tilecollisions[0] == 5 and pancakes[pancakerects.index(p)].stage > 1):
                            self.working = True
                            pancakes[pancakerects.index(p)].previousconveyer = self.rect.topleft
                            p.topleft = c

    def delete(self):
        buildings.remove(self)
        buildingrects.remove(self.rect)

class Pancake():
    def __init__(self, x, y):
        self.rect = pygame.rect.Rect((x,y),(gridsize,gridsize))
        self.tile = (int((self.rect.y / gridsize)), int((self.rect.x / gridsize)))
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
    pygame.display.set_icon(anim.logoframes[windowlogoindex])
    currenttime = pygame.time.get_ticks()
    mousepos = pygame.mouse.get_pos()
    mouserect.center = mousepos
    buildinggrid = [[-1] * int(128) for _ in range(int(64))]

    for b in buildings:
        gridy = int(b.rect.y / gridsize)
        gridx = int(b.rect.x / gridsize)
        if 0 <= gridy < len(buildinggrid) and 0 <= gridx < len(buildinggrid[0]):
            buildinggrid[gridy][gridx] = b.buildingtype

    for p in pancakes:
        if not any(p.rect.colliderect(b) for b in buildingrects):
            buildinggrid[int((p.rect.y / gridsize))][int((p.rect.x / gridsize))] = -2

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 3: # open inventory
            buildingcollisions = mouserect.collidelist(buildingrects)
            if buildingcollisions == -1:
                inventorybg.topright = (mousepos[0],mousepos[1])
                if inventorybg.topright[0] < 300:
                    inventorybg.topright = (300,inventorybg.topright[1])
                if inventorybg.topright[1] > 400:
                    inventorybg.topright = (inventorybg.topright[0], 400)
                placepos = (int((mousepos[0] / gridsize))),(int((mousepos[1] / gridsize)))
                inventoryopen = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and inventoryopen:
            if not inventorybg.collidepoint(mousepos): # exit inventory
                inventoryopen = False
            else:
                for p in purchasebuttons:
                    if p.collidepoint(mousepos): # buy building from inventory screen
                        if inventoryopen:
                            newbuilding = Building(purchasebuttons.index(p),placepos[0],placepos[1])
                        inventoryopen = False
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and not inventoryopen and any(p.collidepoint(mousepos) for p in pancakerects): # pancake is clicked
            for p in pancakes:
                if p.rect.collidepoint(mousepos) and not any(p.rect.colliderect(b) for b in buildings) and p.stage > 1:
                    p.collect()
        elif event.type == pygame.KEYDOWN: # delete buildings
            if event.key == pygame.K_BACKSPACE:
                for b in buildings:
                    if b.rect.collidepoint(mousepos):
                        b.delete()
        #elif event.type == pygame.MOUSEWHEEL:
            #if event.y > 0: # scrolling up (zooming in)
                #if scalefactor > 0.25:
                    #scalefactor /= 2
            #elif event.y < 0: # scrolling down (zooming out)
                    #if scalefactor < 8:
                        #scalefactor *= 2

            #gridsize = (1 / scalefactor) * 100
            #scaleframes()

    placement()
    for b in buildings:
        b.work()
    if not inventoryopen:
        purchasebuttons.clear()
    for p in pancakes:
        if not any(p.rect.colliderect(b) for b in buildingrects):
            if p.stage > 1:
                screen.blit(pancakeimages[p.stage - 2], (p.rect))
            else:
                p.delete()
    renderbuildings()
    for p in pancakerects: # temporary lines for hitbox rendering for debug -- maybe add as a toggleable feature?
        screen.blit(gridbox, p)
    renderui()
    pygame.display.flip()
    if currenttime - lasticonswitch >= 100: # animate logo at the top of the window (w attention to detail am i right?)
        if windowlogoindex >= 4:
            windowlogoindex = 0
        else:
            windowlogoindex += 1
        lasticonswitch = currenttime
    clock.tick(60)
pygame.quit()