# Import module
import random
import sys
import pygame
from pygame.locals import *




# program where the game starts
class flappy:
    score_flappy = 0
    def __init__(self):
            # For initializing modules of pygame library
        pygame.init()
        # All the Game Variables
        self.window_width = 600
        self.window_height = 499

        # set height and width of window
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        self.elevation = self.window_height * 0.8
        self.game_images = {}
        self.framepersecond = 32
        self.pipeimage = 'gamedump/pipe.png'
        self.background_image = 'gamedump/background.jpg'
        self.birdplayer_image = 'gamedump/bird.png'
        self.sealevel_image = 'gamedump/base.jfif'
        self.framepersecond_clock = pygame.time.Clock()
        self.done = False
        # Sets the title on top of game window
        pygame.display.set_caption('Flappy Bird Game')

        # Load all the images which we will use in the game

        # images for displaying score
        self.game_images['scoreimages'] = (
            pygame.image.load('gamedump/0.png').convert_alpha(),
            pygame.image.load('gamedump/1.png').convert_alpha(),
            pygame.image.load('gamedump/2.png').convert_alpha(),
            pygame.image.load('gamedump/3.png').convert_alpha(),
            pygame.image.load('gamedump/4.png').convert_alpha(),
            pygame.image.load('gamedump/5.png').convert_alpha(),
            pygame.image.load('gamedump/6.png').convert_alpha(),
            pygame.image.load('gamedump/7.png').convert_alpha(),
            pygame.image.load('gamedump/8.png').convert_alpha(),
            pygame.image.load('gamedump/9.png').convert_alpha()
        )
        self.game_images['flappybird'] = pygame.image.load(
            self.birdplayer_image).convert_alpha()
        self.game_images['sea_level'] = pygame.image.load(
            self.sealevel_image).convert_alpha()
        self.game_images['background'] = pygame.image.load(
            self.background_image).convert_alpha()
        self.game_images['pipeimage'] = (pygame.transform.rotate(pygame.image.load(
            self.pipeimage).convert_alpha(), 180), pygame.image.load(
        self.pipeimage).convert_alpha())

        print("WELCOME TO THE FLAPPY BIRD GAME")
        print("Press space or enter to start the game")

        # Here starts the main game

        while not self.done:

            # sets the coordinates of flappy bird

            horizontal = int(self.window_width/5)
            vertical = int(
                (self.window_height - self.game_images['flappybird'].get_height())/2)
            ground = 0
            while not self.done:
                for event in pygame.event.get():

                    # if user clicks on cross button, close the game
                    if event.type == QUIT or (event.type == KEYDOWN and \
                                            event.key == K_ESCAPE):
                        self.done = True
                        break

                    # If the user presses space or
                    # up key, start the game for them
                    elif event.type == KEYDOWN and (event.key == K_SPACE or\
                                                    event.key == K_UP):
                        self.game()

                    # if user doesn't press anykey Nothing happen
                    else:
                        self.window.blit(self.game_images['background'], (0, 0))
                        self.window.blit(self.game_images['flappybird'],
                                    (horizontal, vertical))
                        self.window.blit(self.game_images['sea_level'], (ground, self.elevation))
                        pygame.display.update()
                        self.framepersecond_clock.tick(self.framepersecond)


    def game(self):
        self.score_flappy = 0
        horizontal = int(self.window_width/5)
        vertical = int(self.window_width/2)
        ground = 0
        mytempheight = 100
        

        # Generating two pipes for blitting on window
        first_pipe = self.createPipe()
        second_pipe = self.createPipe()

        # List containing lower pipes
        down_pipes = [
            {'x': self.window_width+300-mytempheight,
            'y': first_pipe[1]['y']},
            {'x': self.window_width+300-mytempheight+(self.window_width/2),
            'y': second_pipe[1]['y']},
        ]

        # List Containing upper pipes
        up_pipes = [
            {'x': self.window_width+300-mytempheight,
            'y': first_pipe[0]['y']},
            {'x': self.window_width+200-mytempheight+(self.window_width/2),
            'y': second_pipe[0]['y']},
        ]

        # pipe velocity along x
        pipeVelX = -4

        # bird velocity
        bird_velocity_y = -9
        bird_Max_Vel_Y = 10
        bird_Min_Vel_Y = -8
        birdAccY = 1

        bird_flap_velocity = -8
        bird_flapped = False
        while not self.done:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    self.done = True
                if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                    if vertical > 0:
                        bird_velocity_y = bird_flap_velocity
                        bird_flapped = True

            # This function will return true
            # if the flappybird is crashed
            game_over = self.isGameOver(horizontal,
                                vertical,
                                up_pipes,
                                down_pipes)
            if game_over:
                return

            # check for score_flappy
            playerMidPos = horizontal + self.game_images['flappybird'].get_width()/2
            for pipe in up_pipes:
                pipeMidPos = pipe['x'] + self.game_images['pipeimage'][0].get_width()/2
                if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                    self.score_flappy += 1
                    print(f"Your self.score_flappy is {self.score_flappy}")

            if bird_velocity_y < bird_Max_Vel_Y and not bird_flapped:
                bird_velocity_y += birdAccY

            if bird_flapped:
                bird_flapped = False
            playerHeight = self.game_images['flappybird'].get_height()
            vertical = vertical + \
                min(bird_velocity_y, self.elevation - vertical - playerHeight)

            # move pipes to the left
            for upperPipe, lowerPipe in zip(up_pipes, down_pipes):
                upperPipe['x'] += pipeVelX
                lowerPipe['x'] += pipeVelX

            # Add a new pipe when the first is
            # about to cross the leftmost part of the screen
            if 0 < up_pipes[0]['x'] < 5:
                newpipe = self.createPipe()
                up_pipes.append(newpipe[0])
                down_pipes.append(newpipe[1])

            # if the pipe is out of the screen, remove it
            if up_pipes[0]['x'] < -self.game_images['pipeimage'][0].get_width():
                up_pipes.pop(0)
                down_pipes.pop(0)

            # Lets blit our game images now
            self.window.blit(self.game_images['background'], (0, 0))
            for upperPipe, lowerPipe in zip(up_pipes, down_pipes):
                self.window.blit(self.game_images['pipeimage'][0],
                            (upperPipe['x'], upperPipe['y']))
                self.window.blit(self.game_images['pipeimage'][1],
                            (lowerPipe['x'], lowerPipe['y']))

            self.window.blit(self.game_images['sea_level'], (ground, self.elevation))
            self.window.blit(self.game_images['flappybird'], (horizontal, vertical))

            # Fetching the digits of score.
            numbers = [int(x) for x in list(str(self.score_flappy))]
            width = 0

            # finding the width of score images from numbers.
            for num in numbers:
                width += self.game_images['scoreimages'][num].get_width()
            Xoffset = (self.window_width - width)/1.1

            # Blitting the images on the window.
            for num in numbers:
                self.window.blit(self.game_images['scoreimages'][num],
                            (Xoffset, self.window_width*0.02))
                Xoffset += self.game_images['scoreimages'][num].get_width()

            # Refreshing the game window and displaying the score.
            pygame.display.update()
            self.framepersecond_clock.tick(self.framepersecond)


    def isGameOver(self,horizontal, vertical, up_pipes, down_pipes):
        if vertical > self.elevation - 25 or vertical < 0:
            return True

        for pipe in up_pipes:
            pipeHeight = self.game_images['pipeimage'][0].get_height()
            if(vertical < pipeHeight + pipe['y'] and\
            abs(horizontal - pipe['x']) < self.game_images['pipeimage'][0].get_width()):
                return True

        for pipe in down_pipes:
            if (vertical + self.game_images['flappybird'].get_height() > pipe['y']) and\
            abs(horizontal - pipe['x']) < self.game_images['pipeimage'][0].get_width():
                return True
        return False


    def createPipe(self):
        offset = self.window_height/3
        pipeHeight = self.game_images['pipeimage'][0].get_height()
        y2 = offset + \
            random.randrange(
                0, int(self.window_height - self.game_images['sea_level'].get_height() - 1.2 * offset))
        pipeX = self.window_width + 10
        y1 = pipeHeight - y2 + offset
        pipe = [
            # upper Pipe
            {'x': pipeX, 'y': -y1},

            # lower Pipe
            {'x': pipeX, 'y': y2}
        ]
        return pipe
    

# https://www.geeksforgeeks.org/how-to-make-flappy-bird-game-in-pygame/
    



