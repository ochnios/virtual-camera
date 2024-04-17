import copy

import numpy as np
import pygame

import calc
import data

vww = 1280  # viewport width
vwh = 720  # viewport height
d = 400  # initial viewport
t = 3  # translation step
r = np.pi / 64  # rotation step
bg = 'white'
fg = 'black'
cam = np.zeros(3)

polygons, colors = data.cuboids_as_rectangles()
# polygons, colors = data.cuboids_as_triangles()
polygons_2d = np.zeros((len(polygons), len(polygons[0]), 2), dtype=float)
order = np.zeros(len(polygons), dtype=float)

polygons_reset = copy.deepcopy(polygons)
d_reset = d

pygame.init()
pygame.display.set_caption('VCAM with Painters Algorithm')
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
        polygons = copy.deepcopy(polygons_reset)
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

    for i in range(len(polygons)):
        for j in range(len(polygons[i])):
            polygons[i][j] = calc.rotate(calc.translate(polygons[i][j], tv), rv)
            polygons_2d[i][j] = calc.project(polygons[i][j], d, vww, vwh, 1)
        order[i] = calc.rect_min_dist(polygons[i], cam, 3)  # nearest point approach
        # order[i] = calc.distance(polygons[i].mean(axis=0), np.zeros(3))  # centroid distance approach
        # order[i] = polygons[i].mean(axis=0)[2] / 4  # z approach

    indices = order.argsort()[::-1][:len(order)]
    for i in indices:
        pygame.draw.polygon(screen, tuple(colors[i]), polygons_2d[i])
        pygame.draw.lines(screen, fg, True, polygons_2d[i], 1)

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
