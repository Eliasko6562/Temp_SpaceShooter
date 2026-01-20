import pygame as pg
from entities.entity import Entity

class Enemy(Entity):
    def __init__(self, game, pos, size, color, speed):
        super().__init__(game, pos, size, color)
        self.speed = speed
        
    def update(self, dt):
        self.pos.y += self.speed * dt
        self.rect.center = self.pos