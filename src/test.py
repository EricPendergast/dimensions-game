import pygame

pygame.init()
screen = pygame.display.set_mode((400, 300))
done = False

counter = 0
x = 0

while not done:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    
    pygame.draw.rect(screen, (255,255,255), pygame.Rect(x,0,50,50))
    
    pressed = pygame.key.get_pressed()
    
    if pressed[pygame.K_0]: ++x
    # render to the screen
    pygame.display.flip()
