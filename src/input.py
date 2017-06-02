import pygame

class InputHandler:
    def keyDown(self, key):
        keys = pygame.key.get_pressed()
        return keys[key]
        
