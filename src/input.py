import pygame

# Encapsulates input from keyboard and (eventually) mouse
class InputHandler:
    def keyDown(self, key):
        keys = pygame.key.get_pressed()
        return keys[key]
        
