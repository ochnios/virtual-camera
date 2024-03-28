import numpy as np
import pygame
from math import sin, cos
from point import Point

# Thanks to https://en.wikipedia.org/wiki/3D_projection
# https://en.wikipedia.org/wiki/Euler_angles#Tait%E2%80%93Bryan_angles
# https://en.wikipedia.org/wiki/Camera_matrix

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

p1 = Point(10, 10, 10)
p2 = Point(15, 10, 10)
cam = Point(0, 0, 0)
ang = Point(0, 0, 0)
e = Point(0, 0, 0)

m1 = np.array([
    [1, 0, 0],
    [0, cos(ang.x), sin(ang.x)],
    [0, -sin(ang.x), cos(ang.x)]
])

m2 = np.array([
    [cos(ang.y), 0, -sin(ang.y)],
    [0, 1, 0],
    [sin(ang.y), 0, cos(ang.y)]
])

m3 = np.array([
    [cos(ang.z), sin(ang.z), 0],
    [-sin(ang.z), cos(ang.z), 0],
    [0, 0, 1]
])

m4 = np.array([
    [p1.x - cam.x],
    [p1.y - cam.y],
    [p1.z - cam.z]
])

m5 = np.array([
    [p2.x - cam.x],
    [p2.y - cam.y],
    [p2.z - cam.z]
])

d = Point(*(m1 @ m2 @ m3 @ m4))
print(d)
b = Point((e.z / d.z) * d.x + e.x, (e.z / d.z) * d.y + e.y)
print(b)

d = Point(*(m1 @ m2 @ m3 @ m5))
print(d)
b = Point((e.z / d.z) * d.x + e.x, (e.z / d.z) * d.y + e.y)
print(b)

pygame.quit()

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill('white')
    pygame.draw.circle(screen, 'red', player_pos, 50)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player_pos.y -= 300 * dt
    if keys[pygame.K_DOWN]:
        player_pos.y += 300 * dt
    if keys[pygame.K_LEFT]:
        player_pos.x -= 300 * dt
    if keys[pygame.K_RIGHT]:
        player_pos.x += 300 * dt

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()