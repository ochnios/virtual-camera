import copy

import numpy as np
import pygame

from calc import translate, rotate, project

vww = 1280  # viewport width
vwh = 720  # viewport height
d = 400  # initial viewport
t = 2  # translation step
r = np.pi / 64  # rotation step
bg = 'white'
fg = 'black'

faces = np.array([[0, 1, 2, 3], [4, 5, 6, 7], [0, 1, 5, 4], [1, 2, 6, 5], [2, 3, 7, 6], [3, 0, 4, 7]], dtype=int)
cuboids = np.array([
    [[-70, -50, 100], [-20, -50, 100], [-20, -50, 150], [-70, -50, 150],
     [-70, 50, 100], [-20, 50, 100], [-20, 50, 150], [-70, 50, 150]],
    [[20, -50, 100], [70, -50, 100], [70, -50, 150], [20, -50, 150],
     [20, 50, 100], [70, 50, 100], [70, 50, 150], [20, 50, 150]],
    [[-70, -50, 190], [-20, -50, 190], [-20, -50, 240], [-70, -50, 240],
     [-70, 50, 190], [-20, 50, 190], [-20, 50, 240], [-70, 50, 240]],
    [[20, -50, 190], [70, -50, 190], [70, -50, 240], [20, -50, 240],
     [20, 50, 190], [70, 50, 190], [70, 50, 240], [20, 50, 240]]
], dtype=float)
n_cuboids = len(cuboids)

polygons = np.zeros((n_cuboids * 6, 4, 3), dtype=float)
for i in range(n_cuboids):
    for j in range(6):
        for k in range(4):
            polygons[i * 6 + j][k] = cuboids[i][faces[j][k]]

polygons_reset = copy.deepcopy(polygons)
d_reset = d

polygons_2d = np.zeros((len(polygons), 4, 2), dtype=float)
centroids = np.zeros(len(polygons), dtype=float)

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
        centroid_z = .0
        for j in range(len(polygons[i])):
            polygons[i][j] = rotate(translate(polygons[i][j], tv), rv)
            polygons_2d[i][j] = project(polygons[i][j], d, vww, vwh)
            centroid_z += polygons[i][j][2]
        centroids[i] = centroid_z / len(polygons[i])

    indices = centroids.argsort()[::-1][:len(centroids)]
    sorted_polygons = polygons_2d[indices]
    for polygon in sorted_polygons:
        pygame.draw.polygon(screen, bg, polygon)
        pygame.draw.lines(screen, fg, True, polygon, 2)

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
