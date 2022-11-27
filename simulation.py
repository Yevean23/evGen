import pygame
from enum import Enum
import random

step = 0.001
width = 600
height = 400

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 255, 0)
PURPLE = (255, 0, 255)
YELLOW = (0, 255, 255)


class Universe:
    def __init__(self, object_properties=None, forces=None, objects=None,
                 forces_independent=True, properties_can_be_zero=False, boundary_collision=True):
        self.forces_independent = forces_independent
        self.object_properties = object_properties
        self.forces = forces if forces else self.create_forces()
        self.objects = objects

    def create_forces(self):
        self.forces = [Force(object_property) for object_property in self.object_properties]

    def create_objects(self):
        self.objects = []

    def net_force(self, obj):
        net_force_d2x = 0
        net_force_d2y = 0
        for tmpObj in self.objects:
            if obj != tmpObj:
                for force in self.forces:
                    f_d2x, f_d2y = force.calculate(obj, tmpObj)
                    net_force_d2x += f_d2x
                    net_force_d2y += f_d2y
        return net_force_d2x, net_force_d2y

    def step(self):
        for obj in self.objects:
            f_d2x, f_d2y = self.net_force(obj)
            obj.d2x = f_d2x
            obj.d2y = f_d2y
            obj.update_location()


class ObjectProperties(Enum):
    MASS = "mass"


mass = ObjectProperties.MASS

import sys

epsilon = sys.float_info.epsilon


class Object:
    def __init__(self, x=0, y=0, dx=0, dy=0, d2x=0, d2y=0, width=3, object_properties={}):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.d2x = d2x
        self.d2y = d2y
        self.width = width
        self.vertical_friction = 1.01
        self.horizontal_friction = 1.05
        self.object_properties = object_properties
        if self.object_properties['mass']:
            self.width = self.object_properties['mass'] / 100

    # util functions
    def distance_to(self, another_object):
        test_distance = (((self.x - another_object.x) ** 2) + ((self.y - another_object.y) ** 2)) ** (1 / 2)
        if test_distance <= (self.width + another_object.width):
            print("collision")

        if test_distance <= epsilon:
            print("Intersection")
            test_distance = epsilon

        return test_distance

    def angle_to(self, another_object):
        ...

    # kinematics
    def update_velocity(self):
        self.dx += self.d2x * step
        self.dy += self.d2y * step

    def update_position(self):
        test_x = self.x + self.dx
        if test_x >= width:
            self.dx = - self.dx / self.vertical_friction
            self.x = width
            test_x = self.x + self.dx
        if test_x <= 0:
            self.dx = - self.dx / self.vertical_friction
            self.x = 0
            test_x = self.x + self.dx
        self.x = test_x
        test_y = self.y + self.dy
        if test_y >= height:
            self.dy = - self.dy
            self.y = height
            test_y = self.y + self.dy
        if test_y <= 0:
            self.dy = - self.dy / self.horizontal_friction
            self.dx = self.dx / self.horizontal_friction
            self.y = 0
            test_y = self.y + self.dy
        self.y = test_y

    def collision_elastic(self, obj1, obj2):
        return ...

    def collision_inelastic(self, obj1, obj2):
        return ...

    def collision_dampened(self, obj1, obj2, dampening_factor=0.5):
        return dampening_factor * self.collision_inelastic(obj1, obj2) \
               + (1 - dampening_factor) * self.collision_elastic(obj1, obj2)

    def update_location(self):
        self.update_velocity()
        self.update_position()


Balls = []
balu = Object(69, 420, 0, 0, 0, -9.8, 3, {"mass": 400, "color": RED})
Balls.append(balu)

for i in range(0, width, 100):
    for j in range(0, height, 100):
        Balls.append(Object(i, j, 0, 0, 0, 0, 3, {"mass": 100, "color": GREEN}))


def reset_balls():
    Balls = []
    balu = Object(420, 69, 0, 0, 0, 0, {"mass": 400, "color": RED})
    Balls.append(balu)

    for i in range(0, width, 100):
        for j in range(0, height, 100):
            Balls.append(Object(i, j, 0, 0, 0, 0, {"mass": 100, "color": GREEN}))
    return Balls, balu


class Force:
    def __init__(self, force_function, d2x, d2y, object_properties):
        self.force_function = force_function
        self.object_properties = object_properties

        self.d2x = d2x
        self.d2y = d2y

    def calculate(self, object1, object2):
        if self.d2y:
            return self.d2x, self.d2y
        tmpfun = self.force_function(object1, object2)
        tmpd2x = tmpfun * math.cos(math.atan2(object1.y - object2.y, object1.x - object2.x))
        tmpd2y = tmpfun * math.sin(math.atan2(object1.y - object2.y, object1.x - object2.x))
        return tmpd2x, tmpd2y


gravity = Force(None, 0, -9.8)


def FG(obj1, obj2):
    return -(obj2.object_properties['mass']) / (obj1.distance_to(obj2))


genGrav = Force(FG)

EG_CONST = 100


def EG(obj1, obj2):
    return EG_CONST * (obj2.object_properties['mass']) / (obj1.distance_to(obj2) ** 2)


elec = Force(EG, 0, 0, [mass])

uni = Universe(mass, [genGrav, elec], Balls)


def draw(universe, trails_length=1, camera_shake=False):
    displacement = 0
    for obj in universe.objects:
        color = obj.object_properties['color']
        if camera_shake:
            displacement = random.randint(-5, 5)
            color = WHITE
        pygame.draw.circle(screen, color,
                           [obj.x + displacement, height - obj.y + displacement], obj.width, int(obj.width))
        pygame.draw.line(screen, color, [obj.x + displacement, height - obj.y + displacement],
                         [trails_length * (obj.x - obj.dx) + displacement,
                          trails_length * ((height - obj.y) + obj.dy) + displacement], 2)


pygame.init()

# Open a new window
size = (width, height)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("evGEN Alpha | Gravity Physics Demo")

# The loop will carry on until the user exits the game (e.g. clicks the close button).
carryOn = True
import math

# The clock will be used to control how fast the screen updates
clock = pygame.time.Clock()
bounce = 0.1
action_counter = 0

paused = False
godMode = False
show_tooltips = False

bool1 = False
Emitter = []

font = pygame.font.SysFont('Times New Roman', 12)
# -------- Main Program Loop -----------
while carryOn:
    # --- Main event loop
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            carryOn = False  # Flag that we are done so we can exit the while loop

    # --- Game logic should go here

    # --- Drawing code should go here
    # First, clear the screen to white.

    # The you can draw different shapes and lines or add text to your background stage.
    if not paused:
        uni.step()

    if godMode:
        screen.fill(BLACK)
        pygame.draw.circle(screen, WHITE, [0, 0], 100, 100)
        draw(uni, 2, True)

    else:
        screen.fill(WHITE)
        draw(uni, 1, False)

    if show_tooltips:
        textsurface = font.render('Arrow Keys to move around', False, (0, 0, 0))
        screen.blit(textsurface, (0, 0))
        textsurface = font.render('Space to Pause Time', False, (0, 0, 0))
        screen.blit(textsurface, (0, 15))
        textsurface = font.render('P to Spawn Large Balls', False, (0, 0, 0))
        screen.blit(textsurface, (0, 30))
        textsurface = font.render('Left Click to Spawn Medium Balls', False, (0, 0, 0))
        screen.blit(textsurface, (0, 45))
        textsurface = font.render('G to toggle VFX', False, (0, 0, 0))
        screen.blit(textsurface, (0, 60))
        textsurface = font.render('1, 2, 3 to toggle Forces', False, (0, 0, 0))
        screen.blit(textsurface, (0, 75))
        textsurface = font.render('Look Around For Some More Easter Eggs ;)', False, (0, 0, 0))
        screen.blit(textsurface, (0, 90))
        textsurface = font.render('H to Close Help', False, (0, 0, 0))
        screen.blit(textsurface, (0, 105))
    else:
        textsurface = font.render('evGen Alpha Gravity Demo. Press H for Help', False, (0, 0, 0))
        screen.blit(textsurface, (0, 0))

    pygame.display.flip()

    for ball in Emitter:
        ball.object_properties['lifetime'] -= 1
        if ball.object_properties['lifetime'] <= 0:
            Balls.remove(ball)
            Emitter.remove(ball)

    if action_counter > 30:
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            Balls.append(Object(pos[0], height - pos[1], 0, 0, 0, 0, 3, {"mass": 200, "color": BLUE}))
            action_counter = 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            paused = not paused
            action_counter = 0
        if keys[pygame.K_g]:
            godMode = not godMode
            action_counter = 0
        if keys[pygame.K_h]:
            show_tooltips = not show_tooltips
            action_counter = 0
        if keys[pygame.K_b]:
            step /= 10
            action_counter = 0
        if keys[pygame.K_n]:
            step *= 10
            action_counter = 0
        if keys[pygame.K_r]:
            for ball in Balls:
                ball.dx *= -1
                ball.dy *= -1
            action_counter = 0
        if keys[pygame.K_p]:
            ball_em = Object(235, 0, 0, 1, 0, 0, 0, {"mass": 1000, "color": PURPLE, "lifetime": 120})
            Emitter.append(ball_em)
            Balls.append(ball_em)
            action_counter = 0

        mass_scale = 1
        if keys[pygame.K_0]:
            for ball in Balls:
                ball.dx *= 2
                ball.dy *= 2
            action_counter = 0
        if keys[pygame.K_MINUS]:
            for ball in Balls:
                ball.dx /= 2
                ball.dy /= 2
            action_counter = 0

        if keys[pygame.K_1]:
            if not uni.forces.count(gravity):
                uni.forces.append(gravity)
            else:
                uni.forces.remove(gravity)
            action_counter = 0

        if keys[pygame.K_2]:
            if not uni.forces.count(genGrav):
                uni.forces.append(genGrav)
            else:
                uni.forces.remove(genGrav)
            action_counter = 0

        if keys[pygame.K_3]:
            if not uni.forces.count(elec):
                uni.forces.append(elec)
            else:
                uni.forces.remove(elec)
            action_counter = 0

        if keys[pygame.K_RETURN]:
            print("im here")
            Balls = None
            balu = None
            Balls, balu = reset_balls()

        balu.dx += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * 0.05
        balu.dy += (keys[pygame.K_UP] - keys[pygame.K_DOWN]) * 0.05

    # --- Limit to 60 frames per second
    action_counter += 1
    clock.tick(60)

# Once we have exited the main program loop we can stop the game engine:
pygame.quit()
