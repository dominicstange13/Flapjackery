import pygame

pygame.init()

screen = pygame.display.set_mode((1600,800))
clock = pygame.time.Clock()

mousepos = pygame.mouse.get_pos()

testrect = pygame.rect.Rect((0,0),(100,100))
dragmode = False

running = True
while running:
    screen.fill((0,0,0))
    mousepos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        mouseheld = pygame.mouse.get_pressed()[0]
        if mouseheld and testrect.collidepoint(mousepos):
            dragmode = True

        if dragmode:
            tilemovepos = (round(mousepos[0], -2),round(mousepos[1], -2))
            testrect.topleft = tilemovepos
            if not mouseheld:
                dragmode = False
    pygame.draw.rect(screen, "red", testrect)
    pygame.display.flip()
    print(mousepos)
    clock.tick(60)
pygame.quit()