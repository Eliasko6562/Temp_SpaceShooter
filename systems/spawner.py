import random
from entities.enemy import Enemy
from settings import WIDTH, SPAWN_INTERVAL, ENEMY_SPEED, MIN_SPAWN_INTERVAL

class Spawner:
    def __init__(self, game):
        self.game = game
        self.timer = 0
    
    def update(self, dt, total_time):
        self.timer += dt 
        
        if self.timer >= max(MIN_SPAWN_INTERVAL, SPAWN_INTERVAL - total_time * 0.005):
            self.timer = 0
            self.spawn_enemy(total_time)
    
    def spawn_enemy(self, total_time):
        pos = (random.randint(0, WIDTH), 0)

        enemy = Enemy(self.game, pos, size=(25, 25), color=(30, 30, 30), speed=ENEMY_SPEED + total_time)
        self.game.enemies.add(enemy)
        self.game.all_sprites.add(enemy)