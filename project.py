import math
import pygame
import random
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
    """
    TODO: Scoreboard class
    """
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
        self.sprite = pygame.transform.scale(self.sprite, [50, 40])
        self.sprite = self.sprite.convert_alpha()
        self.coordinate = [screen_size[0]/2 - self.sprite.get_width()/2, screen_size[1] - 1.5 * self.sprite.get_height()]
        self.Lasers = LaserShots('./images/laser_shot_01.png')

    def update_position(self, x_coordinate, screen_width):

        # Bound x_coordinate to [0.5 *sprite_width, screenwidth - 0.5 *sprite_width]

        x_coordinate = max(x_coordinate, 0.5 * self.sprite.get_width())
        x_coordinate = min(x_coordinate, screen_width - 0.5 * self.sprite.get_width())

        self.coordinate[0]  = x_coordinate
        self.Lasers.update()

    def show(self, screen):
        plot_coordinate = [0, 0]
        plot_coordinate[0] = self.coordinate[0] - self.sprite.get_width()/2
        plot_coordinate[1] = self.coordinate[1] - self.sprite.get_height()/2
        screen.blit(self.sprite, plot_coordinate)
        self.Lasers.show(screen)

    def shoot_laser(self):
        self.Lasers.add_laser([self.coordinate[0], self.coordinate[1] - self.sprite.get_height()/2])

class LaserShots():

    def __init__(self, image_file):
        self.coordinates = []
        self.count = 0
        self.max_count = 2
        self.speed = 2
        self.img = pygame.image.load(image_file)
        self.img = pygame.transform.scale(self.img, [25, 30])

    def add_laser(self, coordinate):
        if self.count < self.max_count:
            self.coordinates.append([coordinate[0], coordinate[1]])
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
        plot_coordinate = [0, 0]
        for coordinate in self.coordinates:
            plot_coordinate[0] = coordinate[0] - self.img.get_width()/2
            plot_coordinate[1] = coordinate[1] - self.img.get_height()/2
            screen.blit(self.img, plot_coordinate)

class Asteroids():
    def __init__(self, image_dir, screen_size):
        self.coordinates = []
        self.asteroid_types = []
        self.speed = 2.0
        self.screen_size = screen_size
        self.drop_coordinate = [0, 0]

        # Load asteroid images
        self.images = []
        for file_name in os.listdir(image_dir):
            try:
                curr_image = pygame.image.load(os.path.join(image_dir, file_name))
                curr_image = pygame.transform.scale_by(curr_image, 0.6)
            except:
                sys.exit("Asteroid images is corrupt!")
            self.images.append(curr_image)

    def update(self, add_new=True):
        num_new_asteroids = random.choices([0, 1, 2], [0.9, 0.099, 0.001])[0]

        i = 0
        while i < len(self.coordinates):
            if self.coordinates[i][1] > self.screen_size[1]:
                self.remove(i)
            else:
                self.coordinates[i][1] += self.speed
                i += 1

        if add_new:
            for i in range(num_new_asteroids):
                # Pick asteroid type randomly
                curr_type = random.randint(0, len(self.images) - 1)

                # Pick drop coordinate randomly
                drop_coordinate = [self.drop_coordinate[0] + random.randint(0, self.screen_size[0]),
                                self.drop_coordinate[1]]
                drop_coordinate[0] = min(drop_coordinate[0], screen_size[0] - self.images[curr_type].get_width()/2)
                drop_coordinate[0] = max(drop_coordinate[0], self.images[curr_type].get_width()/2)

                self.coordinates.append(drop_coordinate)
                self.asteroid_types.append(curr_type)

    def remove(self, i):
        """
        Remove ith asteroid
        """
        if i >= 0 and i < len(self.coordinates):
            self.coordinates.pop(i)
            self.asteroid_types.pop(i)

    def show(self, screen):
        plot_coordinate = [0, 0]
        for i in range(len(self.coordinates)):
            coordinate = self.coordinates[i]
            curr_type = self.asteroid_types[i]
            plot_coordinate[0] = coordinate[0] - self.images[curr_type].get_width()/2
            plot_coordinate[1] = coordinate[1] - self.images[curr_type].get_height()/2
            screen.blit(self.images[curr_type], plot_coordinate)

def update_interactions(playerSpaceShip: SpaceShip, enemyAsteroids: Asteroids):
    """
    Update laser shot - asteroid, spaceship - asteroid interactions
    """
    i = 0
    remove_asteroids_id = []
    while i < len(playerSpaceShip.Lasers.coordinates):
        c1 = playerSpaceShip.Lasers.coordinates[i]
        j = 0
        while j < len(enemyAsteroids.coordinates):
            c2 = enemyAsteroids.coordinates[j]
            asteroid_type = enemyAsteroids.asteroid_types[j]
            if abs(c1[0]-c2[0]) <= enemyAsteroids.images[asteroid_type].get_width()/2 and abs(c1[1]-c2[1]) <= enemyAsteroids.images[asteroid_type].get_height()/2:
                enemyAsteroids.remove(j)
                continue
            j += 1
        i += 1

    c1 = playerSpaceShip.coordinate
    j = 0
    while j < len(enemyAsteroids.coordinates):
        # The widths need correction based on actual asteroid coverage
        #xl_2 = enemyAsteroids.coordinates[j][0] - enemyAsteroids.img.get_width()/2
        #xr_2 = enemyAsteroids.coordinates[j][0] - enemyAsteroids.img.get_width()/2
        c2 = enemyAsteroids.coordinates[j]
        asteroid_type = enemyAsteroids.asteroid_types[j]
        if abs(c1[0] - c2[0]) <= 0.4 * (playerSpaceShip.sprite.get_width() + enemyAsteroids.images[asteroid_type].get_width()):
           if abs(c1[1] - c2[1]) <= 0.15 * (playerSpaceShip.sprite.get_height() + enemyAsteroids.images[asteroid_type].get_height()):
               return 1
        j += 1

    return 0

def demo(SpaceWarsBackground, PlayerSpaceShip):

    background_scroll_speed = 0.3

    while True:
        time = clock.tick(200)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    PlayerSpaceShip.shoot_laser()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return

        SpaceWarsBackground.update_coordinate(background_scroll_speed, time)
        SpaceWarsBackground.show(SpaceWarsScreen)

        # Display space ship
        x, y = pygame.mouse.get_pos()
        PlayerSpaceShip.update_position(x, screen_size[0])
        PlayerSpaceShip.show(SpaceWarsScreen)

        # Display game info
        font_large = pygame.font.Font(pygame.font.get_default_font(), 15)
        font_small = pygame.font.Font(pygame.font.get_default_font(), 10)
        progress_text = "PRESS ENTER TO START"
        text = font_large.render(progress_text, True, (255, 255, 255))
        textRect = text.get_rect()
        SpaceWarsScreen.blit(text, (screen_size[0]//2 - textRect[2]//2, screen_size[1]//2))

        progress_text = "MOVE - MOUSE"
        text = font_small.render(progress_text, True, (255, 255, 255))
        textRect = text.get_rect()
        SpaceWarsScreen.blit(text, (screen_size[0]//2 - textRect[2]//2, screen_size[1]//2 + 2 * textRect[3]))

        progress_text = "SHOOT - LEFT MOUSE BUTTON"
        text = font_small.render(progress_text, True, (255, 255, 255))
        textRect = text.get_rect()
        SpaceWarsScreen.blit(text, (screen_size[0]//2 - textRect[2]//2, screen_size[1]//2 + 4 * textRect[3]))

        pygame.display.update()

    return

def run_level(SpaceWarsBackground, PlayerSpaceShip):

    font_small = pygame.font.Font(pygame.font.get_default_font(), 12)
    font_large = pygame.font.Font(pygame.font.get_default_font(), 15)

    EnemyAsteroids = Asteroids('./images/asteroids', screen_size)
    asteroid_refresh_at_counter = 10
    asteroid_refresh_counter = 0
    asteroid_initial_speed = EnemyAsteroids.speed 
    asteroid_acceleration = 0.005 # d(speed)/d(progress)

    background_scroll_speed = 0.3
    distance_traversed = 0

    game_active = True
    mission_accomplished = False
    while True:

        time = clock.tick(200)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if game_active and event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    PlayerSpaceShip.shoot_laser()
            if not game_active and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return

        SpaceWarsBackground.update_coordinate(background_scroll_speed, time)
        SpaceWarsBackground.show(SpaceWarsScreen)

        # Update progress
        if game_active:
            distance_traversed += background_scroll_speed * time
       
        progress = min(int(distance_traversed/250), 100)
        if progress == 100:
            game_active = False
            mission_accomplished = True
            background_scroll_speed = 0
            game_active = False
            EnemyAsteroids.speed = 0
            asteroid_refresh_at_counter = 0

        # Display space ship
        if game_active:
            x, y = pygame.mouse.get_pos()
            PlayerSpaceShip.update_position(x, screen_size[0])
        PlayerSpaceShip.show(SpaceWarsScreen)

        # Update asteroid shower
        asteroid_refresh_counter += 1
        if asteroid_refresh_counter == asteroid_refresh_at_counter:
            asteroid_refresh_counter = 0
            EnemyAsteroids.update(add_new=True)
        else:
            EnemyAsteroids.update(add_new=False)

        EnemyAsteroids.show(SpaceWarsScreen)

        # Show game end graphics
        if not game_active:
            # Display End Game
            if mission_accomplished:
                display_text = "MISSION ACCOMPLISHED"
            else:
                display_text = "MISSION FAILED"

            text = font_large.render(display_text, True, (255, 255, 255))
            textRect = text.get_rect()
            SpaceWarsScreen.blit(text,
                                 (screen_size[0]//2 - textRect[2]//2,
                                  screen_size[1]//2))

            text = font_small.render("PRESS ENTER TO CONTINUE", True,
                                     (255, 255, 255))
            textRect = text.get_rect()
            SpaceWarsScreen.blit(text,
                                 (screen_size[0]//2 - textRect[2]//2,
                                 screen_size[1]//2 + textRect[3] * 2))

        # Update speed for progressive difficulty
        if game_active:
            EnemyAsteroids.speed = asteroid_initial_speed + \
                                   asteroid_acceleration * progress


        # Display Progress
        progress_text = 'PROGRESS ' + str(progress).rjust(3) + "%"
        text = font_small.render(progress_text, True, (255, 255, 255))
        textRect = text.get_rect()
        SpaceWarsScreen.blit(text, (5, 5))

        pygame.display.update()

        if game_active and update_interactions(PlayerSpaceShip, EnemyAsteroids):
            background_scroll_speed = 0
            game_active = False
            EnemyAsteroids.speed = 0
            asteroid_refresh_at_counter = 0

def main():
    """
    Main game loop
    """
    # Create game entities
    SpaceWarsBackground = ScrollingBackground(screen_size,
                            './images/BackdropBlackLittleSparkBlack.png')

    PlayerSpaceShip = SpaceShip('./images/spaceship_01.png', screen_size)
    
    while True:
        demo(SpaceWarsBackground, PlayerSpaceShip)
        run_level(SpaceWarsBackground, PlayerSpaceShip)


if __name__ == "__main__":

    # Create pygame session
    pygame.init()
    pygame.mouse.set_visible(0)
    pygame.display.set_caption('Galactic Glide')
    pygame_icon = pygame.image.load('./images/spaceship_01.png')
    pygame.display.set_icon(pygame_icon)
    
    clock = pygame.time.Clock()

    # Create screen
    screen_size = (250, 500)
    SpaceWarsScreen = pygame.display.set_mode(screen_size)

    # Call game loop
    main()