from abc import ABC, abstractclassmethod
import pygame
import random
import time


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([50, 50])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 2
        self.rect.y = SCREEN_HEIGHT - 75
        self.speed = 10

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        

        #Keep the player within the screen bounds
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

class Context:
    def __init__(self, strategy):
        self.strategy = strategy

    def setStrategy(self, strategy):
        self.strategy = strategy

    def executeStrategy(self):
        return self.strategy.execute()

class EnemyMode(ABC):
    @abstractclassmethod
    def execute(self):
        pass

#Defining the fast enemy mode
class FastEnemyMode(EnemyMode):
    def execute(self):
        Enemy.speedscale = 6

#Defining the slow enemy mode
class SlowEnemyMode(EnemyMode):
    def execute(self):
        Enemy.speedscale = 1


class Enemy(pygame.sprite.Sprite):
    speedscale = 1
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([30, 30])
        self.image.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -50)
        self.speed = random.randint(1, 3) + Enemy.speedscale

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -50)
            self.speed = random.randint(1, 3) + Enemy.speedscale


#Defining the game class
class skyfallGame:
    highscore = 0
    def __init__(self):
        pygame.init()
        self.start_time = time.time()
        self.context = Context(SlowEnemyMode())
        self.player = Player()
        self.context.setStrategy(SlowEnemyMode())
        #Creates a sprite group for the player and enemies
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        #Creates a sprite group for the enemies
        self.enemy_sprites = pygame.sprite.Group()
        #Creates some enemies and add them to the enemy sprite group
        for i in range(10):
            enemy = Enemy()
            self.enemy_sprites.add(enemy)
            self.all_sprites.add(enemy)
            self.context.executeStrategy()
            enemy.update()
        self.done = False
        self.clock = pygame.time.Clock()
        self.score = 0

        #Set the game over screen
        self.game_over = False
        self.game_over_text = None

    def set_enemy_Mode(self, enemy_Mode):
        self.enemy_Mode = enemy_Mode

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            elif event.type == pygame.KEYDOWN:
                if self.game_over and event.key == pygame.K_RETURN:
                    self.restart_game()
                if event.key == pygame.K_1:
                    self.context.setStrategy(FastEnemyMode())
                if event.key == pygame.K_2:
                    self.context.setStrategy(SlowEnemyMode())
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_BACKSPACE:
                    self.done = True

    def update(self):
        if not self.game_over:
            self.all_sprites.update()
            self.collision_score_update()
            

    def collision_score_update(self):
            if pygame.sprite.spritecollide(self.player, self.enemy_sprites, False):
                self.game_over = True
                font = pygame.font.SysFont("Arial", 48)
                self.game_over_text = font.render("GAME OVER", True, WHITE)
                if self.score > skyfallGame.highscore:
                    skyfallGame.highscore = self.score

    def draw(self):
        #Draw everything to the screen
        self.screen.fill(BLACK)
        
        if not self.game_over:
            font = pygame.font.SysFont("Arial", 24)
            screenscore = round(self.score)
            score_text = font.render("Score: " + str(screenscore), True, WHITE)
            self.all_sprites.draw(self.screen)
            self.screen.blit(score_text, (10, 10))
        else:
            #Draw the game over text
            self.screen.blit(self.game_over_text, (SCREEN_WIDTH // 2 - self.game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - self.game_over_text.get_height() // 2))

            #Draw the restart text
            font = pygame.font.SysFont("Arial", 24)
            restart_text = font.render("Press Enter to Restart", True, WHITE)
            restart_text2 = font.render("GameModeChange:", True, WHITE)
            restart_text3 = font.render("Press 1 for fast and 2 for slow", True, WHITE)
            self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + self.game_over_text.get_height() // 2 + 0))
            self.screen.blit(restart_text2, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + self.game_over_text.get_height() // 2 + 50))
            self.screen.blit(restart_text3, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + self.game_over_text.get_height() // 2 + 100))
        pygame.display.flip()

    def scorepoints(self):
        elapsed_time = time.time() - self.start_time
        self.score = round(elapsed_time)
        


    def run(self):
        self.screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        #Game loop
        while not self.done:
            self.handle_events()
            self.update()
            self.scorepoints()
            self.draw()
            #Set the FPS of the game
            self.clock.tick(60)
    
    def restart_game(self):
        self.score = 0
        self.start_time = time.time()
        self.game_over = False
        self.game_over_text = None
        for enemy in self.enemy_sprites:
            enemy.kill()

        #Creates some new enemies and add them to the sprite groups
        for i in range(10):
            enemy = Enemy()
            self.enemy_sprites.add(enemy)
            self.all_sprites.add(enemy)
            self.context.executeStrategy()
            enemy.update()
        #Resets the player position
        self.player.rect.centerx = SCREEN_WIDTH // 2
        self.run()

