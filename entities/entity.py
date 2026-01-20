import pygame as pg

class Entity(pg.sprite.Sprite):
    def __init__(self, game, pos, size, color):
        super().__init__()
        self.game = game
        
        self.image = pg.Surface(size)
        self.image.fill(color)

        self.pos = pg.Vector2(pos)
        self.rect = self.image.get_rect(center=pos)
        
    def update(self, dt):
        pass