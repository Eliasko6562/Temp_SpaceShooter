import pygame as pg
from entities.entity import Entity
from settings import BULLET_SPEED, BULLET_LIFETIME

class Bullet(Entity):
    def __init__(self, game, pos):
        super().__init__(game, pos, size=(5,5), color=(0, 255, 255))
        self.timer = 0
        
    def update(self, dt):
        self.timer += dt
        
        if self.timer >= BULLET_LIFETIME:
            self.kill()
        
        self.pos.y -= BULLET_SPEED * dt
        self.rect.center = self.pos
        
    