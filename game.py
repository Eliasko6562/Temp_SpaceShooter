import pygame as pg

from systems.spawner import Spawner
from entities.player import Player

from settings import WIDTH, HEIGHT, FPS

class Game:
    def __init__(self):
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption('Game Arena')
        self.clock = pg.time.Clock()
        
        # ToDo: Inicializace skupiny objektu
        self.all_sprites = pg.sprite.Group()
        
        # ToDo: Vytvoreni objektu hrace
        self.player = Player(game=self, pos=(WIDTH / 2, HEIGHT / 2), size=(50, 50), color=(0, 255, 0))
        self.all_sprites.add(self.player)
        
        # ToDo: Inicializace systemu vytvareni nepratel
        self.enemies = pg.sprite.Group()
        self.spawner = Spawner(self)
        
        #ToDo: Inicializace skupiny projektilu
        self.bullets = pg.sprite.Group()
        
        # Stav hry
        self.game_running = True
        self.app_running = True
        self.score = 0
        self.total_time = 0
        
        # Obrazky entit
        self.ship = pg.image.load("./images/ship.png")
        self.imagerect = self.ship.get_rect()
        
        self.meteorite = pg.image.load("./images/meteorite.png")
        self.meteoriterect = self.meteorite.get_rect()
        
        self.bullet = pg.image.load("./images/bullet2.png")
        self.bulletrect = self.bullet.get_rect()
        
    def run(self):
        self.highscore = 0
        while self.app_running:
            dt = self.clock.tick(FPS) / 1000  # Delta time in seconds.
            self.handle_events()
            if self.game_running:
                self.update(dt)
                self.draw()
            else:
                self.game_over()

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.app_running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.shoot()

    def update(self, dt):
        self.all_sprites.update(dt)
        self.spawner.update(dt, self.total_time)
        self.total_time += dt
        for bullet in self.bullets:
            hits = pg.sprite.spritecollide(bullet, self.enemies, True)
            if hits:
                bullet.kill()
                self.score += len(hits)
                
        if pg.sprite.spritecollide(self.player, self.enemies, dokill=False):
            self.player.kill()
            self.game_running = False

    def draw(self):
        self.screen.fill((30, 30, 30))  # Clear screen with dark gray
        self.all_sprites.draw(self.screen)
        self.imagerect.center = self.player.rect.center
        self.screen.blit(self.ship, self.imagerect)
        for enemy in self.enemies:
            self.meteoriterect.center = enemy.rect.center
            self.screen.blit(self.meteorite, self.meteoriterect)
        for bullet in self.bullets:
            self.bulletrect.center = bullet.rect.center
            self.screen.blit(self.bullet, self.bulletrect)
        self.score_board()
        pg.display.flip()
        
    def game_over(self):
        self.screen.fill((30, 30, 30))
        font = pg.font.SysFont('Arial', 50)
        
        text = font.render('Game Over', True, (255, 0, 0))
        self.screen.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 3 - text.get_height() / 2))
        
        if self.score >= self.highscore:
            self.highscore = self.score
            highscore_text = font.render(f'New Highscore: {self.highscore}', True, (255, 255, 255))
            self.screen.blit(highscore_text, (WIDTH / 2 - highscore_text.get_width() / 2, HEIGHT / 3 + 50))
        else:
            highscore_text = font.render(f'Highscore: {self.highscore}', True, (255, 255, 255))
            self.screen.blit(highscore_text, (WIDTH / 2 - highscore_text.get_width() / 2, HEIGHT / 3 + 50))
            
            score_text = font.render(f'Current Score: {self.score}', True, (255, 255, 255))
            self.screen.blit(score_text, (WIDTH / 2 - score_text.get_width() / 2, HEIGHT / 3 + 100))
        
        time_alive_text = font.render(f'Time Survived: {self.total_time:.1f} s', True, (255, 255, 255))
        self.screen.blit(time_alive_text, (WIDTH / 2 - time_alive_text.get_width() / 2, HEIGHT / 3 + 150))
        
        restart_text = font.render('(r - restart | q - quit', True, (255, 255, 255))
        self.screen.blit(restart_text, (WIDTH / 2 - restart_text.get_width() / 2, HEIGHT / 3 + 250))
        
        keys = pg.key.get_pressed()
        if keys[pg.K_r]:
            print( "Restarting game..." )
            self.__init__()  # Restart the game            
        elif keys[pg.K_q]:
            self.app_running = False
        pg.display.flip()
        
    def score_board(self):
        font = pg.font.SysFont('Arial', 30)
        text = font.render(f'Kills: {self.score}', True, (255,255,255))
        self.screen.blit(text, (50, 50))
        text = font.render(f'Time: {self.total_time:.1f}', True, (255,255,255))
        self.screen.blit(text, (45, 85))
