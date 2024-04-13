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

edges = np.array([[0, 1], [1, 2], [2, 3], [3, 0], [4, 5], [5, 6], [6, 7], [7, 4], [0, 4], [1, 5], [2, 6], [3, 7]])
faces = np.array([[0, 1, 2, 3], [4, 5, 6, 7], [0, 1, 5, 4], [1, 2, 6, 5], [2, 3, 7, 6], [3, 0, 4, 7]])
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

    faces_2d = []
    for i in range(len(cuboids)):
        vertices_2d = []
        for j in range(len(cuboids[i])):
            cuboids[i][j] = rotate(translate(cuboids[i][j], tv), rv)
            vertices_2d.append(project(cuboids[i][j], d, vww, vwh))
        for face in faces:
            face_2d = []
            centroid_z = 0.0
            for vertex in face:
                face_2d.append(vertices_2d[vertex])
                centroid_z = centroid_z + cuboids[i][vertex][2]
            centroid_z = centroid_z / 4.0
            faces_2d.append([face_2d, centroid_z])

    faces_2d.sort(key=lambda x: x[1], reverse=True)
    for face_2d in faces_2d:
        pygame.draw.polygon(screen, bg, face_2d[0])
        pygame.draw.lines(screen, fg, True, face_2d[0], 2)

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
