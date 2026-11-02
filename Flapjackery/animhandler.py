import pygame

pygame.init()
currenttime = pygame.time.get_ticks()

screen = pygame.display.set_mode((1600,800))

mixer1 = pygame.image.load("assets/images/mixer/mixer1.png").convert_alpha()
mixer2 = pygame.image.load("assets/images/mixer/mixer2.png").convert_alpha()
mixer3 = pygame.image.load("assets/images/mixer/mixer3.png").convert_alpha()
mixer4 = pygame.image.load("assets/images/mixer/mixer4.png").convert_alpha()
mixer5 = pygame.image.load("assets/images/mixer/mixer3.png").convert_alpha()
mixer6 = pygame.image.load("assets/images/mixer/mixer2.png").convert_alpha()
mixerframes = [mixer2, mixer3, mixer4, mixer5, mixer6]

press1 = pygame.image.load("assets/images/press/press1.png").convert_alpha()
press2 = pygame.image.load("assets/images/press/press2.png").convert_alpha()
press3 = pygame.image.load("assets/images/press/press3.png").convert_alpha()
press4 = pygame.image.load("assets/images/press/press4.png").convert_alpha()
press5 = pygame.image.load("assets/images/press/press5.png").convert_alpha()
press6 = pygame.image.load("assets/images/press/press6.png").convert_alpha()
pressframes = [press2, press3, press4, press5, press6]

stove1 = pygame.image.load("assets/images/stove/stove1.png").convert_alpha()
stove2 = pygame.image.load("assets/images/stove/stove2.png").convert_alpha()
stove3 = pygame.image.load("assets/images/stove/stove3.png").convert_alpha()
stoveframes = [stove2, stove3]

butter1 = pygame.image.load("assets/images/butter/butter1.png").convert_alpha()
butter2 = pygame.image.load("assets/images/butter/butter2.png").convert_alpha()
butter3 = pygame.image.load("assets/images/butter/butter3.png").convert_alpha()
butter4 = pygame.image.load("assets/images/butter/butter4.png").convert_alpha()
butter5 = pygame.image.load("assets/images/butter/butter5.png").convert_alpha()
butterframes = [butter2, butter3, butter4, butter5]

syrup1 = pygame.image.load("assets/images/syrup/syrup1.png").convert_alpha()
syrup2 = pygame.image.load("assets/images/syrup/syrup2.png").convert_alpha()
syrup3 = pygame.image.load("assets/images/syrup/syrup3.png").convert_alpha()
syrup4 = pygame.image.load("assets/images/syrup/syrup4.png").convert_alpha()
syrup5 = pygame.image.load("assets/images/syrup/syrup5.png").convert_alpha()
syrup6 = pygame.image.load("assets/images/syrup/syrup6.png").convert_alpha()
syrupframes = [syrup2, syrup3, syrup4, syrup5, syrup6]

conveyerup1 = pygame.image.load("assets/images/conveyer/conveyer1.png").convert_alpha()
conveyerup2 = pygame.image.load("assets/images/conveyer/conveyer2.png").convert_alpha()
conveyerup3 = pygame.image.load("assets/images/conveyer/conveyer3.png").convert_alpha()
conveyerup4 = pygame.image.load("assets/images/conveyer/conveyer4.png").convert_alpha()
conveyerup5 = pygame.image.load("assets/images/conveyer/conveyer5.png").convert_alpha()
conveyerup6 = pygame.image.load("assets/images/conveyer/conveyer6.png").convert_alpha()
conveyerup7 = pygame.image.load("assets/images/conveyer/conveyer7.png").convert_alpha()
conveyerupframes = [conveyerup1, conveyerup2, conveyerup3, conveyerup4, conveyerup5, conveyerup6, conveyerup7]

conveyerdown1 = pygame.transform.rotate(conveyerup1, 180)
conveyerdown2 = pygame.transform.rotate(conveyerup2, 180)
conveyerdown3 = pygame.transform.rotate(conveyerup3, 180)
conveyerdown4 = pygame.transform.rotate(conveyerup4, 180)
conveyerdown5 = pygame.transform.rotate(conveyerup5, 180)
conveyerdown6 = pygame.transform.rotate(conveyerup6, 180)
conveyerdown7 = pygame.transform.rotate(conveyerup7, 180)
conveyerdownframes = [conveyerdown1, conveyerdown2, conveyerdown3, conveyerdown4, conveyerdown5, conveyerdown6, conveyerdown7]

conveyerleft1 = pygame.transform.rotate(conveyerup1, 90)
conveyerleft2 = pygame.transform.rotate(conveyerup2, 90)
conveyerleft3 = pygame.transform.rotate(conveyerup3, 90)
conveyerleft4 = pygame.transform.rotate(conveyerup4, 90)
conveyerleft5 = pygame.transform.rotate(conveyerup5, 90)
conveyerleft6 = pygame.transform.rotate(conveyerup6, 90)
conveyerleft7 = pygame.transform.rotate(conveyerup7, 90)
conveyerleftframes = [conveyerleft1, conveyerleft2, conveyerleft3, conveyerleft4, conveyerleft5, conveyerleft6, conveyerleft7]

conveyerright1 = pygame.transform.rotate(conveyerup1, 270)
conveyerright2 = pygame.transform.rotate(conveyerup2, 270)
conveyerright3 = pygame.transform.rotate(conveyerup3, 270)
conveyerright4 = pygame.transform.rotate(conveyerup4, 270)
conveyerright5 = pygame.transform.rotate(conveyerup5, 270)
conveyerright6 = pygame.transform.rotate(conveyerup6, 270)
conveyerright7 = pygame.transform.rotate(conveyerup7, 270)
conveyerrightframes = [conveyerright1, conveyerright2, conveyerright3, conveyerright4, conveyerright5, conveyerright6, conveyerright7]

pcup1 = pygame.image.load("assets/images/pc/pc1.png").convert_alpha()
pcup2 = pygame.image.load("assets/images/pc/pc2.png").convert_alpha()
pcup3 = pygame.image.load("assets/images/pc/pc3.png").convert_alpha()
pcup4 = pygame.image.load("assets/images/pc/pc4.png").convert_alpha()
pcup5 = pygame.image.load("assets/images/pc/pc5.png").convert_alpha()
pcup6 = pygame.image.load("assets/images/pc/pc6.png").convert_alpha()
pcup7 = pygame.image.load("assets/images/pc/pc7.png").convert_alpha()
pcupframes = [pcup1, pcup2, pcup3, pcup4, pcup5, pcup6, pcup7]

pcdown1 = pygame.transform.rotate(pcup1, 180)
pcdown2 = pygame.transform.rotate(pcup2, 180)
pcdown3 = pygame.transform.rotate(pcup3, 180)
pcdown4 = pygame.transform.rotate(pcup4, 180)
pcdown5 = pygame.transform.rotate(pcup5, 180)
pcdown6 = pygame.transform.rotate(pcup6, 180)
pcdown7 = pygame.transform.rotate(pcup7, 180)
pcdownframes = [pcdown1, pcdown2, pcdown3, pcdown4, pcdown5, pcdown6, pcdown7]

pcleft1 = pygame.transform.rotate(pcup1, 90)
pcleft2 = pygame.transform.rotate(pcup2, 90)
pcleft3 = pygame.transform.rotate(pcup3, 90)
pcleft4 = pygame.transform.rotate(pcup4, 90)
pcleft5 = pygame.transform.rotate(pcup5, 90)
pcleft6 = pygame.transform.rotate(pcup6, 90)
pcleft7 = pygame.transform.rotate(pcup7, 90)
pcleftframes = [pcleft1, pcleft2, pcleft3, pcleft4, pcleft5, pcleft6, pcleft7]

pcright1 = pygame.transform.rotate(pcup1, 270)
pcright2 = pygame.transform.rotate(pcup2, 270)
pcright3 = pygame.transform.rotate(pcup3, 270)
pcright4 = pygame.transform.rotate(pcup4, 270)
pcright5 = pygame.transform.rotate(pcup5, 270)
pcright6 = pygame.transform.rotate(pcup6, 270)
pcright7 = pygame.transform.rotate(pcup7, 270)
pcrightframes = [pcright1, pcright2, pcright3, pcright4, pcright5, pcright6, pcright7]

defaultframes = [mixer1, press1, stove1, butter1, syrup1, conveyerup3, conveyerdown3, conveyerleft3, conveyerright3]
animframes = [mixerframes, pressframes, stoveframes, butterframes, syrupframes, conveyerupframes, conveyerdownframes, conveyerleftframes, conveyerrightframes, pcupframes, pcdownframes, pcleftframes, pcrightframes]