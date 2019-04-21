import pygame
import math

pygame.init()

FPS = 24
SIZE = width, height = 640, 480
SCREEN = pygame.display.set_mode(SIZE)
BULLETS = []
CLOCK = pygame.time.Clock()


class GameObject:
    def __init__(
        self,
        path_to_img,
        width=32,
        height=45,
        speed_x=0,
        speed_y=0,
        angle=0,
        x=0,
        y=0
    ):

        # we keep the original surface to compensate rotation
        # lost of image quality
        print(path_to_img)
        self.orig_surface = pygame.image.load(path_to_img)
        self.orig_surface = pygame.transform.scale(
            self.orig_surface, (width, height)
        )

        self.surface = self.orig_surface.copy()
        self.rect = self.surface.get_rect()

        self.rect.center = (x, y)

        # perform rotation without loosing image quality
        orig_center = self.rect.center
        self.surface = pygame.transform.rotate(self.surface, angle)
        self.rect = self.surface.get_rect(center=orig_center)

        # setting the initial values
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.angle = 0
        self.projection_x = 1
        self.projection_y = 0

    def _perform_move(self):
        self.rect = self.rect.move([self.speed_x, self.speed_y])

    def update(self):
        print('angle: {}'.format(self.angle))
        print('projection_x: {}'.format(self.projection_x))
        print('projection_y: {}'.format(self.projection_y))
        print('speed_x: {}'.format(self.speed_x))
        print('speed_y: {}'.format(self.speed_y))
        print('\n')
        self._perform_move()


class Rocket(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.jet = Jet(
            'assets/jet.png',
            width=20, height=30,
            angle=self.angle,
            x=self.rect.center[0],
            y=self.rect.bottom
        )
        self.is_accelerating = False

    def _perform_move(self):
        super()._perform_move()
        self.jet.rect = self.jet.rect.move([self.speed_x, self.speed_y])

    def _accelerate(self, val):
        self.speed_x += val * self.projection_x
        self.speed_y += val * self.projection_y

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, val):
        if abs(val) == 360:
            self._angle = 0

        else:
            self._angle = val

        if not val % 90:
            self.surface = pygame.transform.rotate(self.orig_surface, val)

    @property
    def rads(self):
        return self.angle * math.pi / 180

    def accept_direction(self, direction):
        if direction == 'right':
            self._accelerate(0)

            self.angle -= 10

            # perform rotation without loosing image quality
            orig_center = self.rect.center
            self.surface = pygame.transform.rotate(self.surface, -10)
            self.rect = self.surface.get_rect(center=orig_center)

        if direction == 'left':
            self._accelerate(0)

            self.angle += 10

            # perform rotation without loosing image quality
            orig_center = self.rect.center
            self.surface = pygame.transform.rotate(self.surface, 10)
            self.rect = self.surface.get_rect(center=orig_center)

        if direction == 'up':
            self._accelerate(1)

            if not self.is_accelerating:
                self.is_accelerating = True

        self.projection_x = -math.sin(self.rads)
        self.projection_y = -math.cos(self.rads)

    def fire(self):
        bullet_speed = 15

        bullet = Bullet(
            'assets/bullet.png',
            width=30, height=20,
            speed_x=self.projection_x * bullet_speed + self.speed_x,
            speed_y=self.projection_y * bullet_speed + self.speed_y,
            angle=self.angle - 90,
            x=self.rect.center[0],
            y=self.rect.center[1]
        )

        BULLETS.append(bullet)


class Bullet(GameObject):
    def exist(self):
        pass


class Jet(GameObject):
    def exist(self):
        pass


rocket = Rocket('assets/rocket.png', angle=-90)

while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                rocket.is_accelerating = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT]:
        rocket.accept_direction('right')

    if keys[pygame.K_LEFT]:
        rocket.accept_direction('left')

    if keys[pygame.K_UP]:
        rocket.accept_direction('up')

    if keys[pygame.K_SPACE]:
        rocket.fire()

    rocket.update()

    CLOCK.tick(FPS)

    SCREEN.fill((0, 0, 0))
    SCREEN.blit(rocket.surface, rocket.rect)

    if rocket.is_accelerating:
        SCREEN.blit(rocket.jet.surface, rocket.jet.rect)

    for bullet in BULLETS:
        SCREEN.blit(bullet.surface, bullet.rect)
        bullet.update()

    pygame.display.flip()
    pygame.event.pump()
