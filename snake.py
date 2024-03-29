import pygame as pg
from random import randrange, randint

vec2 = pg.math.Vector2
class Snake:
    def __init__(self, game):
        self.game = game
        self.size = game.TILE_SIZE
        self.rect = pg.rect.Rect([0, 0, game.TILE_SIZE - 2, game.TILE_SIZE - 2])
        self.range = (self.size // 2, self.game.WINDOW_SIZE - self.size // 2, self.size)
        self.rect.center = self.get_random_position()
        self.direction = vec2(0, 0)
        self.step_delay = 100  # milliseconds
        self.time = 0
        self.length = 1
        self.segments = []
        self.directions = {pg.K_UP: 1, pg.K_DOWN: 1, pg.K_LEFT: 1, pg.K_RIGHT: 1}
        
    def control(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and self.directions[pg.K_UP]:
                self.direction = vec2(0, -self.size)
                self.directions = {pg.K_UP: 1, pg.K_DOWN: 0, pg.K_LEFT: 1, pg.K_RIGHT: 1}

            if event.key == pg.K_DOWN and self.directions[pg.K_DOWN]:
                self.direction = vec2(0, self.size)
                self.directions = {pg.K_UP: 0, pg.K_DOWN: 1, pg.K_LEFT: 1, pg.K_RIGHT: 1}

            if event.key == pg.K_LEFT and self.directions[pg.K_LEFT]:
                self.direction = vec2(-self.size, 0)
                self.directions = {pg.K_UP: 1, pg.K_DOWN: 1, pg.K_LEFT: 1, pg.K_RIGHT: 0}

            if event.key == pg.K_RIGHT and self.directions[pg.K_RIGHT]:
                self.direction = vec2(self.size, 0)
                self.directions = {pg.K_UP: 1, pg.K_DOWN: 1, pg.K_LEFT: 0, pg.K_RIGHT: 1}

    def delta_time(self):
        time_now = pg.time.get_ticks()
        if time_now - self.time > self.step_delay:
            self.time = time_now
            return True
        return False

    def get_random_position(self):
        return [randrange(*self.range), randrange(*self.range)]

    def check_borders(self):
        if self.rect.left < 0 or self.rect.right > self.game.WINDOW_SIZE:
            if(self.length> SnakeGame.highscore):
                SnakeGame.highscore = self.length
            self.game.new_game()
        if self.rect.top < 0 or self.rect.bottom > self.game.WINDOW_SIZE:
            if(self.length> SnakeGame.highscore):
                SnakeGame.highscore = self.length
            self.game.new_game()

    def check_food(self):
        if self.rect.center == self.game.food.rect.center:
            self.game.food.rect.center = self.get_random_position()
            self.length += self.game.food.foodpoint
            self.game.new_foodtype()

    def check_selfeating(self):
        if len(self.segments) != len(set(segment.center for segment in self.segments)):
            SnakeGame.highscore = self.length
            self.game.new_game()

    def move(self):
        if self.delta_time():
            self.rect.move_ip(self.direction)
            self.segments.append(self.rect.copy())
            self.segments = self.segments[-self.length:]

    def update(self):
        self.check_selfeating()
        self.check_borders()
        self.check_food()
        self.move()

    def draw(self):
        [pg.draw.rect(self.game.screen, 'green', segment) for segment in self.segments]


class Food():
    def __init__(self, game):
        self.game = game
        self.size = game.TILE_SIZE
        self.rect = pg.rect.Rect([0, 0, game.TILE_SIZE - 2, game.TILE_SIZE - 2])
        self.rect.center = self.game.snake.get_random_position()

    def draw(self):
        pg.draw.rect(self.game.screen, self.game.food.color, self.rect)

class Item1(Food):
    def __init__(self, game):
        super().__init__(game)
        self.foodpoint = 1
        self.color = 'red'

class Item2(Food):
    def __init__(self, game):
        super().__init__(game)
        self.foodpoint = 2
        self.color = 'blue'

class Item3(Food):
    def __init__(self, game):
        super().__init__(game)
        self.foodpoint = 3
        self.color = 'yellow'

    

class SnakeGame:
    highscore=0
    def __init__(self):
        pg.init()
        self.WINDOW_SIZE = 800
        self.TILE_SIZE = 50
        self.clock = pg.time.Clock()
        self.new_game()
        self.score = 0
        self.Done = False
        self.score_font = pg.font.SysFont("comicsansms", 35)
        

    def draw_grid(self):
        [pg.draw.line(self.screen, [50] * 3, (x, 0), (x, self.WINDOW_SIZE))
                                             for x in range(0, self.WINDOW_SIZE, self.TILE_SIZE)]
        [pg.draw.line(self.screen, [50] * 3, (0, y), (self.WINDOW_SIZE, y))
                                             for y in range(0, self.WINDOW_SIZE, self.TILE_SIZE)]

    def new_game(self):
        self.snake = Snake(self)
        self.food = Item1(self)

    def new_foodtype(self):
        rando = randint(1,3)
        if rando == 1:
            self.food = Item1(self)
        elif rando == 2:
            self.food = Item2(self)
        elif rando == 3:
            self.food = Item3(self)

    def update(self):
        self.snake.update()
        pg.display.flip()
        self.clock.tick(60)

    def Your_score(self):
        value = self.score_font.render("Your Score: " + str(self.snake.length), True,(255,255,255))
        self.screen.blit(value, [0, 0])
        

    def draw(self):
        self.screen.fill('black')
        self.draw_grid()
        self.food.draw()
        self.snake.draw()
        self.Your_score()

    def check_event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.Done = True
            if event.type == pg.KEYDOWN and (event.key == pg.K_ESCAPE or event.key == pg.K_BACKSPACE):
                self.Done = True
            self.snake.control(event)


    def run(self):
        self.screen = pg.display.set_mode([self.WINDOW_SIZE] * 2)
        while not self.Done:
            self.check_event()
            self.update()
            self.draw()

    def getscore(self):
        return self.score
