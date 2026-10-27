import pygame
import animhandler

pygame.init()

screen = pygame.display.set_mode((1600,800))
clock = pygame.time.Clock()

mousepos = pygame.mouse.get_pos()

testrect = pygame.rect.Rect((0,0),(100,100))
dragmode = False

class Building:
    def __init__(self,l,w):
        self.rect = pygame.rect.Rect((mousepos[0],mousepos[1]),(l,w))
        self.append(buildings)
        self.rect.append(buildingrects)

buildings = []
buildingrects = []

running = True
while running:
    screen.fill((0,0,0))
    mousepos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        mouseheld = pygame.mouse.get_pressed()[0]
        if mouseheld:
            for b in buildingrects:
                if b.collidepoint(mousepos):
                    dragmode = True

        if dragmode:
            tilemovepos = (round(mousepos[0], -2),round(mousepos[1], -2))
            for b in buildingrects:
                b.topleft = tilemovepos
                if not mouseheld:
                    dragmode = False
    pygame.draw.rect(screen, "red", testrect)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()