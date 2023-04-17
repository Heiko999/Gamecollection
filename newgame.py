import math
import pygame
from abc import ABC, abstractmethod

# Define abstract classes for game objects
class GameObject(ABC):
    @abstractmethod
    def draw(self, surface):
        pass

    @abstractmethod
    def update(self):
        pass

# Define concrete implementations of game objects
class Player(GameObject):
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 50)
        self.field_rect = pygame.Rect(0, 0, 800, 800) # Set the boundaries of the game field
    
    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.move_ip(-5, 0)
        if keys[pygame.K_RIGHT]:
            self.rect.move_ip(5, 0)
        if keys[pygame.K_UP]:
            self.rect.move_ip(0, -5)
        if keys[pygame.K_DOWN]:
            self.rect.move_ip(0, 5)

        if not self.field_rect.contains(self.rect):
            self.rect.clamp_ip(self.field_rect)

class Enemy(GameObject):
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 50)
        self.direction = 1
    
    def draw(self, surface):
        pygame.draw.rect(surface, (0, 255, 0), self.rect)

    def update(self):
        if self.rect.right >= 800 or self.rect.left <= 0:
            self.direction = -self.direction
        self.rect.move_ip(self.direction * 5, 0)

class Enemy2(GameObject):
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 50)
        self.direction = 1
    
    def draw(self, surface):
        pygame.draw.rect(surface, (0, 255, 0), self.rect)

    def update(self, player_rect):
        # Calculate the distance between the enemy and the player
        dx = player_rect.centerx - self.rect.centerx
        dy = player_rect.centery - self.rect.centery
        distance = math.sqrt(dx**2 + dy**2)

        # Calculate the direction towards the player
        if distance != 0:
            direction = (dx/distance, dy/distance)
        else:
            direction = (0, 0)

        # Adjust the enemy position based on the direction and speed
        self.rect.move_ip(direction[0]*self.speed, direction[1]*self.speed)

# Define an abstract class for the game controller
class GameController(ABC):
    @abstractmethod
    def handle_events(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def draw(self):
        pass

# Define a concrete implementation of the game controller
class PygameController(GameController):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 800))
        self.clock = pygame.time.Clock()
        self.objects = []

    def add_object(self, obj):
        self.objects.append(obj)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

    def update(self):
        for obj in self.objects:
            obj.update()

    def draw(self):
        self.screen.fill((255, 255, 255))
        for obj in self.objects:
            obj.draw(self.screen)
        pygame.display.flip()
        self.clock.tick(60)

# Define a main function that sets up and runs the game
class thisgame():
    def __init__(self):
        self.controller = PygameController()
        self.player = Player(375, 500)
        self.enemy1 = Enemy(100, 100)
        self.enemy2 = Enemy2(600, 100)
        self.controller.add_object(self.player)
        self.controller.add_object(self.enemy1)
        self.controller.add_object(self.enemy2)
    
    def run(self):
        while True:
            self.controller.handle_events()
            self.controller.update()
            self.controller.draw()


if __name__ == '__main__':
    game = thisgame()
    game.run()
