import pygame
import math

screen_width = 1500
screen_height = 800


class Car:
    def __init__(self, car_file, map_file, pos):
        # inital properties of the car
        self.surface = pygame.image.load(car_file)
        self.map = pygame.image.load(map_file)
        self.surface = pygame.transform.scale(self.surface, (100, 100))
        self.rotate_surface = self.surface
        self.pos = pos
        self.angle = 90
        self.speed = 0
        self.center = [self.pos[0] + 50, self.pos[1] + 50]
        self.radars = []
        self.is_alive = True
        self.target = [1349, 148]  # target location
        self.prev_distance = 0
        self.cur_distance = 0
        self.goal = False
        self.check_flag = False
        self.distance = 0
        self.time_spent = 0
        len = 40
        left_top = [self.center[0] + math.cos(math.radians(360 - (self.angle + 30)))
                    * len, self.center[1] + math.sin(math.radians(360 - (self.angle + 30))) * len]
        right_top = [self.center[0] + math.cos(math.radians(360 - (self.angle + 150)))
                     * len, self.center[1] + math.sin(math.radians(360 - (self.angle + 150))) * len]
        left_bottom = [self.center[0] + math.cos(math.radians(360 - (self.angle + 210)))
                       * len, self.center[1] + math.sin(math.radians(360 - (self.angle + 210))) * len]
        right_bottom = [self.center[0] + math.cos(math.radians(360 - (self.angle + 330)))
                        * len, self.center[1] + math.sin(math.radians(360 - (self.angle + 330))) * len]
        # To calculate the position of four white circles around the car
        self.four_points = [left_top, right_top, left_bottom, right_bottom]

        # check the radar(green lines) in four directions(-90,-45,0,45,90)
        for d in range(-90, 120, 45):
            self.check_radar(d)

    def draw(self, screen):
        screen.blit(self.rotate_surface, self.pos)

    def draw_collision(self, screen):
        for i in range(4):
            x = int(self.four_points[i][0])
            y = int(self.four_points[i][1])
            # drawing four white circles around the car
            pygame.draw.circle(screen, (255, 255, 255), (x, y), 5)

    def draw_radar(self, screen):
        for r in self.radars:
            pos, dist = r
            # to draw the radars (green lines and green dots)
            pygame.draw.line(screen, (0, 255, 0), self.center, pos, 1)
            pygame.draw.circle(screen, (0, 255, 0), pos, 5)

    # If one of the four white circles around the car contact the white pixel(i.e. not the track), car is crashed.
    def check_collision(self):
        self.is_alive = True
        for p in self.four_points:
            if self.map.get_at((int(p[0]), int(p[1]))) == (255, 255, 255, 255):
                self.is_alive = False
                break

    # calculate where the radars are contacting the white pixel in the given angle and store it in radars array
    def check_radar(self, degree):
        len = 0
        x = int(
            self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * len)
        y = int(
            self.center[1] + math.sin(math.radians(360 - (self.angle + degree))) * len)

        while not self.map.get_at((x, y)) == (255, 255, 255, 255) and len < 300:
            len = len + 1
            x = int(
                self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * len)
            y = int(
                self.center[1] + math.sin(math.radians(360 - (self.angle + degree))) * len)

        dist = int(
            math.sqrt(math.pow(x - self.center[0], 2) + math.pow(y - self.center[1], 2)))
        self.radars.append([(x, y), dist])

    def update(self):  # update the car properties after every action
        # check speed
        self.speed -= 0.5
        if self.speed > 10:
            self.speed = 10
        if self.speed < 1:
            self.speed = 1

        # if car is near the target, mark the game as done
        if get_distance(self.target, self.pos) < 150:
            self.goal = True

        # check position
        self.rotate_surface = rot_center(self.surface, self.angle)
        self.pos[0] += math.cos(math.radians(360 - self.angle)) * self.speed
        if self.pos[0] < 20:
            self.pos[0] = 20
        elif self.pos[0] > screen_width - 60:
            self.pos[0] = screen_width - 60

        self.distance += self.speed
        self.time_spent += 1
        self.pos[1] += math.sin(math.radians(360 - self.angle)) * self.speed
        if self.pos[1] < 20:
            self.pos[1] = 20
        elif self.pos[1] > screen_height - 60:
            self.pos[1] = screen_height - 60

        # caculate 4 collision points
        self.center = [int(self.pos[0]) + 50, int(self.pos[1]) + 50]
        len = 40
        left_top = [self.center[0] + math.cos(math.radians(360 - (self.angle + 30)))
                    * len, self.center[1] + math.sin(math.radians(360 - (self.angle + 30))) * len]
        right_top = [self.center[0] + math.cos(math.radians(360 - (self.angle + 150)))
                     * len, self.center[1] + math.sin(math.radians(360 - (self.angle + 150))) * len]
        left_bottom = [self.center[0] + math.cos(math.radians(360 - (self.angle + 210)))
                       * len, self.center[1] + math.sin(math.radians(360 - (self.angle + 210))) * len]
        right_bottom = [self.center[0] + math.cos(math.radians(360 - (self.angle + 330)))
                        * len, self.center[1] + math.sin(math.radians(360 - (self.angle + 330))) * len]
        self.four_points = [left_top, right_top, left_bottom, right_bottom]


class PyGame2D:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 30)
        # 100,150 is the cars intial position
        self.car = Car('car.png', 'test.png', [100, 550])
        self.game_speed = 60
        self.mode = 0

    def action(self, action):  # if the action taken is 0 or 1 or 2
        if action == 0:
            self.car.speed += 2
        if action == 1:
            self.car.angle += 5
        elif action == 2:
            self.car.angle -= 5

        self.car.update()  # upon every action, update the car properties
        # upon completion of every action, check whether the car is outside the track(grey) or not
        self.car.check_collision()
        # redraw the radars
        self.car.radars.clear()
        for d in range(-90, 120, 45):
            self.car.check_radar(d)

    def evaluate(self):
        '''
        Reward function
        '''
        reward = 0
        if not self.car.is_alive:
            # depends upon the distance between the car and the target
            reward = -(get_distance(self.car.target, self.car.pos))

        elif self.car.goal:
            reward = 10000

        return reward

    def is_done(self):
        if not self.car.is_alive or self.car.goal:
            self.car.distance = 0
            return True
        return False

    def observe(self):
        # return state
        radars = self.car.radars
        ret = [0, 0, 0, 0, 0, int(self.car.pos[0]/10), int(self.car.pos[1]/10)]
        # ret [0,1,2,3,4] saves the length of the 5 radars(green lines)
        for i, r in enumerate(radars):
            ret[i] = int(r[1] / 3)

        return tuple(ret)

    def view(self):
        # draw game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        self.screen.blit(self.car.map, (0, 0))

        if self.mode == 1:
            self.screen.fill((0, 0, 0))

        self.car.radars.clear()
        for d in range(-90, 120, 45):
            self.car.check_radar(d)

        rect_size = 60
        pygame.Surface.fill(self.screen, (255, 0, 0), rect=(self.car.target[0]-int(
            rect_size/2), self.car.target[1]-int((rect_size/2)), rect_size, rect_size))
        # draw the four white dots around the car
        self.car.draw_collision(self.screen)
        self.car.draw_radar(self.screen)  # draw the green lines
        self.car.draw(self.screen)

        pygame.display.flip()
        self.clock.tick(self.game_speed)


def get_distance(p1, p2):  # distance function
    return math.sqrt(math.pow((p1[0] - p2[0]), 2) + math.pow((p1[1] - p2[1]), 2))


def rot_center(image, angle):  # function to change the image by a certain degree
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image
