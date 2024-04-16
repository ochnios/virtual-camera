import copy

import numpy as np
import pygame

from calc import translate, rotate, project
from data import edges, cuboids

vww = 1280  # viewport width
vwh = 720  # viewport height
d = 400  # initial viewport
t = 2  # translation step
r = np.pi / 64  # rotation step
bg = 'white'
fg = 'black'

cuboids_reset = copy.deepcopy(cuboids)
d_reset = d

pygame.init()
pygame.display.set_caption('VCAM')
screen = pygame.display.set_mode((vww, vwh))
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(bg)

    tv = np.array([0, 0, 0], dtype=float)  # translation vector
    rv = np.array([0, 0, 0], dtype=float)  # rotation vector

    keys = pygame.key.get_pressed()
    mods = pygame.key.get_mods()
    if keys[pygame.K_ESCAPE]:
        running = False
    if keys[pygame.K_r]:
        cuboids = copy.deepcopy(cuboids_reset)
        d = d_reset
    # zoom
    if keys[pygame.K_i] and d <= 5000:
        d += 0.1 * d
    if keys[pygame.K_o] and d >= 1:
        d -= 0.1 * d
    # translations
    if keys[pygame.K_w]:
        tv[2] -= t
    if keys[pygame.K_a]:
        tv[0] += t
    if keys[pygame.K_s]:
        tv[2] += t
    if keys[pygame.K_d]:
        tv[0] -= t
    # rotations
    if keys[pygame.K_SPACE]:
        tv[1] += t
    if mods & pygame.KMOD_SHIFT:
        tv[1] -= t
    if keys[pygame.K_LEFT]:
        rv[1] += r
    if keys[pygame.K_RIGHT]:
        rv[1] -= r
    if keys[pygame.K_UP]:
        rv[0] -= r
    if keys[pygame.K_DOWN]:
        rv[0] += r
    if keys[pygame.K_q]:
        rv[2] += r
    if keys[pygame.K_e]:
        rv[2] -= r

    cuboids_2d = []
    for i in range(len(cuboids)):
        vertices_2d = []
        for j in range(len(cuboids[i])):
            cuboids[i][j] = rotate(translate(cuboids[i][j], tv), rv)
            vertices_2d.append(project(cuboids[i][j], d, vww, vwh))
        cuboids_2d.append(vertices_2d)

    for i in range(len(cuboids_2d)):
        for edge in edges:
            pygame.draw.aaline(screen, fg, cuboids_2d[i][edge[0]], cuboids_2d[i][edge[1]])

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
