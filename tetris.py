import pygame
import random

colors = [
    (0, 0, 0),
    (120, 37, 179),
    (100, 179, 179),
    (80, 34, 22),
    (80, 134, 22),
    (180, 34, 22),
    (180, 34, 122),
]


class Figure:
    x = 0
    y = 0

    figures = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],
        [[4, 5, 9, 10], [2, 6, 5, 9]],
        [[6, 7, 9, 10], [1, 5, 6, 10]],
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        [[1, 2, 5, 6]],
    ]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(self.figures) - 1)
        self.color = random.randint(1, len(colors) - 1)
        self.rotation = 0

    def image(self):
        return self.figures[self.type][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.figures[self.type])


class Tetris:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (128, 128, 128)

    size = (400, 500)
    screen = None
    score_tetris = 0
    state = "start"
    field = []
    height = 0
    width = 0
    x = 100
    y = 60
    zoom = 20
    figure = None
    done = False
    clock = pygame.time.Clock()
    fps = 25
    counter = 0

    def __init__(self, height, width):
        pygame.init()
        
        self.height = height
        self.width = width
        self.field = []
        self.score_tetris = 0
        self.state = "start"
        self.done = False
        self.pressing_down = False
        
    
    def new_figure(self):
        self.figure = Figure(3, 0)

    def intersects(self):
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if i + self.figure.y > self.height - 1 or \
                            j + self.figure.x > self.width - 1 or \
                            j + self.figure.x < 0 or \
                            self.field[i + self.figure.y][j + self.figure.x] > 0:
                        intersection = True
        return intersection

    def break_lines(self):
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1 - 1][j]
        self.score_tetris += lines ** 2

    def go_space(self):
        if self.state == "gameover":
            return
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

    def go_down(self):
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze()

    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.color
        self.break_lines()
        self.new_figure()
        if self.intersects():
            self.state = "gameover"

    def go_side(self, dx):
        old_x = self.figure.x
        self.figure.x += dx
        if self.intersects():
            self.figure.x = old_x

    def rotate(self):
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():
            self.figure.rotation = old_rotation

    def run(self):
        self.screen = pygame.display.set_mode(self.size)
        for i in range(self.height):
            new_line = []
            for j in range(self.width):
                new_line.append(0)
            self.field.append(new_line)

        while not self.done:
            if self.figure is None:
                self.new_figure()
            self.counter += 1
            if self.counter > 100000:
                self.counter = 0

            if ((self.counter % 5) == 0) or self.pressing_down:
                if self.state == "start":
                    self.go_down()
                    self.pressing_down = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.rotate()
                    if event.key == pygame.K_DOWN:
                        self.pressing_down = True
                    if event.key == pygame.K_LEFT:
                        self.go_side(-1)
                    if event.key == pygame.K_RIGHT:
                        self.go_side(1)
                    if event.key == pygame.K_SPACE:
                        self.go_space()
                    if event.key == pygame.K_ESCAPE:
                        self.done = True

            if not self.done:
                self.screen.fill(self.WHITE)
                
                for i in range(self.height):
                    for j in range(self.width):
                        pygame.draw.rect(self.screen, self.GRAY, [self.x + self.zoom * j, self.y + self.zoom * i, self.zoom, self.zoom], 1)
                        if self.field[i][j] > 0:
                            pygame.draw.rect(self.screen, colors[self.field[i][j]],
                                            [self.x + self.zoom * j + 1, self.y + self.zoom * i + 1, self.zoom - 2, self.zoom - 1])

                if self.figure is not None:
                    for i in range(4):
                        for j in range(4):
                            p = i * 4 + j
                            if p in self.figure.image():
                                pygame.draw.rect(self.screen, colors[self.figure.color],
                                                [self.x + self.zoom * (j + self.figure.x) + 1,
                                                self.y + self.zoom * (i + self.figure.y) + 1,
                                                self.zoom - 2, self.zoom - 2])

                font = pygame.font.SysFont('Calibri', 25, True, False)
                font1 = pygame.font.SysFont('Calibri', 65, True, False)
                text = font.render("Score: " + str(self.score_tetris), True, self.BLACK)
                text_game_over = font1.render("Game Over", True, (255, 125, 0))
                text_game_over1 = font1.render("Press ESC", True, (255, 215, 0))

                self.screen.blit(text, [0, 0])
                if self.state == "gameover":
                    self.screen.blit(text_game_over, [20, 200])
                    self.screen.blit(text_game_over1, [25, 265])

                pygame.display.flip()
                self.clock.tick(self.fps)
