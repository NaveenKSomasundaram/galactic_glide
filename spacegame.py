import pygame
import sys

import os

from pygame.locals import *

class ScrollingBackground():
    """
    Scrolling Background class
    """
    
    def __init__(self, screen_size, image_file):

        self.img = pygame.image.load(image_file)
        self.screen_height = self.img.get_height() + 5
        self.screen_width = screen_size[0]
        self.scroll_direction = 'vertical'  
        self.coordinate = [0, 0]
        self.duplicate_coordinate = [0, 0]

    @property
    def img(self):
        return self._img 
    
    @img.setter
    def img(self, image_file):
        print(type(image_file), 'bingo')

        self._img = image_file
        """
        if os.path.isfile(image_file):
            self._img = pygame.image.load(image_file)
        else:
            sys.exist(f'Background file{image_file} is missing.')    
        """

    @property
    def screen_height(self):
        return self._screen_height

    @screen_height.setter
    def screen_height(self, screen_height):
        self._screen_height = screen_height

    def update_coordinate(self, scroll_speed=10, time_delta=1):
        if self.scroll_direction == "vertical":
            self.coordinate[1] += (scroll_speed * time_delta)  % (2 * self.screen_height) 
            self.duplicate_coordinate[1] = (self.coordinate[1] + self.screen_height) % (2 * self.screen_height)

            self.coordinate[1]  -= self.screen_height
            self.duplicate_coordinate[1] -= self.screen_height

        else:
            self.coordinate[0] += (scroll_speed * time_delta)  % (2 * self.screen_width) 
            self.duplicate_coordinate[0] = (self.coordinate[0] + self.screen_width) % (2 * self.screen_width)

            self.coordinate[0]  -= self.screen_width
            self.duplicate_coordinate[0] -= self.screen_width

            
    def show(self, screen):
        # Show image 1
        screen.blit(self.img, self.coordinate)

        # Show image 1 duplicate
        
        screen.blit(self.img, self.duplicate_coordinate)

class ScoreBoard():

    def __init__(self):
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.text = self.font.render('GeeksForGeeks', True, green, blue)


    def update(self):
        pass

    def show(self):
        pass    
        
class SpaceShip():
    
    def __init__(self, image_file, screen_size):

        self.sprite = pygame.image.load(image_file)
        self.sprite = pygame.transform.scale(self.sprite, [65, 50])
        self.sprite = self.sprite.convert_alpha()
        self.coordinate = [screen_size[0]/2 - self.sprite.get_width()/2, screen_size[1] - 1.5 * self.sprite.get_height()]
        self.Lasers = LaserShots('./images/bullet_1.png')
        
    def update_position(self, x_coordinate, screen_width):
        
        # Bound x_coordinate to [0.5 *sprite_width, screenwidth - 0.5 *sprite_width]
    
        x_coordinate = max(x_coordinate, 0.5 * self.sprite.get_width())
        x_coordinate = min(x_coordinate, screen_width - 0.5 * self.sprite.get_width())

        self.coordinate[0]  = x_coordinate - self.sprite.get_width()/2

        self.Lasers.update()

        
        
        
    def show(self, screen):
        screen.blit(self.sprite, self.coordinate)
        self.Lasers.show(screen)

    def shoot_laser(self):
        self.Lasers.add_laser([self.coordinate[0] + self.sprite.get_width()/2, self.coordinate[1]])

class LaserShots():

    def __init__(self, image_file):
        self.coordinates = []
        self.count = 0
        self.speed = 30
        self.img = pygame.image.load(image_file)
        self.img = pygame.transform.scale(self.img, [25, 30])
        
    def add_laser(self, coordinate):
        if self.count < 100:
            self.coordinates.append([coordinate[0] - self.img.get_width()/2, coordinate[1]])
            self.count += 1

    def update(self):
        i = 0
        while i < len(self.coordinates):
            self.coordinates[i][1] -= self.speed

            if self.coordinates[i][1] < -100:
                self.coordinates.pop(i)
            else:
                i += 1
        self.count = len(self.coordinates) 
        
    def show(self, screen):
        for coordinate in self.coordinates:
            screen.blit(self.img, coordinate)
        
        
if __name__ == "__main__":

    pygame.init()  # initialize pygame

    clock = pygame.time.Clock()

    screen_size = (200, 500)

    SpaceWarsScreen = pygame.display.set_mode(screen_size)


    # Load the background image here. Make sure the file exists!

    SpaceWarsBackground = ScrollingBackground(screen_size, './images/BackdropBlackLittleSparkBlack.png')
    PlayerSpaceShip = SpaceShip('./images/ship_2.png', screen_size)

    pygame.mouse.set_visible(0)

    pygame.display.set_caption('Space Age Game')


    # fix indentation

    while True:

        time = clock.tick(60)/1000

        #screen.blit(bg, (0, 0))

        x, y = pygame.mouse.get_pos()


        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONUP:
                PlayerSpaceShip.shoot_laser()


        SpaceWarsBackground.update_coordinate(200, time)

        SpaceWarsBackground.show(SpaceWarsScreen)

        #SpaceWarsScreen.blit(bg_test, [0, 0])


        font = pygame.font.Font(pygame.font.get_default_font(), 15)
        text = font.render('SCORE', True, (255, 255, 255))
        textRect = text.get_rect()
        SpaceWarsScreen.blit(text, textRect)

        #
        x, y = pygame.mouse.get_pos()

        PlayerSpaceShip.update_position(x, screen_size[0])

        PlayerSpaceShip.show(SpaceWarsScreen)
        
        pygame.display.update()