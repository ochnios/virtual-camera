import copy
from math import pi, cos, sin

import numpy as np
import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True


def project(vertex: np.ndarray, d: float) -> np.ndarray:
    if vertex[2] > 0.001:
        x = ((vertex[0] * d) / vertex[2]) + (screen.get_width() / 2)
        y = ((vertex[1] * d) / vertex[2]) + (screen.get_height() / 2)
    else:  # temp workaround for division by 0
        x = ((vertex[0] * d) / 0.001) + (screen.get_width() / 2)
        y = ((vertex[1] * d) / 0.001) + (screen.get_height() / 2)
    return np.array([x, y])


def translate(vertex: np.ndarray, tv: np.ndarray) -> np.ndarray:
    return np.array([vertex[0] + tv[0], vertex[1] + tv[1], vertex[2] + tv[2]])


def rotate(vertex: np.ndarray, rv: np.ndarray) -> np.ndarray:
    rot = np.identity(3)
    x, y, z = rv
    if x != 0:
        rot @= np.array([
            [1, 0, 0],
            [0, cos(x), -sin(x)],
            [0, sin(x), cos(x)]
        ])
    if y != 0:
        rot @= np.array([
            [cos(y), 0, sin(y)],
            [0, 1, 0],
            [-sin(y), 0, cos(y)]
        ])
    if z != 0:
        rot @= np.array([
            [cos(z), -sin(z), 0],
            [sin(z), cos(z), 0],
            [0, 0, 1]
        ])
    return rot @ vertex.transpose()


d = 400  # initial viewport
t = 3  # translation step
r = pi / 64  # rotation step

edges = np.array([[0, 1], [1, 2], [2, 3], [3, 0], [4, 5], [5, 6], [6, 7], [7, 4], [0, 4], [1, 5], [2, 6], [3, 7]])
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

reset = copy.deepcopy(cuboids)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill('black')

    tv = np.array([0, 0, 0], dtype=float)  # translation vector
    rv = np.array([0, 0, 0], dtype=float)  # rotation vector

    keys = pygame.key.get_pressed()
    mods = pygame.key.get_mods()
    if keys[pygame.K_r]:
        cuboids = copy.deepcopy(reset)
    if keys[pygame.K_i]:
        d += 0.1 * d
    if keys[pygame.K_o]:
        d -= 0.1 * d
    if keys[pygame.K_w]:
        tv[2] -= t
    if keys[pygame.K_d]:
        tv[0] -= t
    if keys[pygame.K_s]:
        tv[2] += t
    if keys[pygame.K_a]:
        tv[0] += t
    if keys[pygame.K_SPACE]:
        tv[1] += t
    if mods & pygame.KMOD_SHIFT:
        tv[1] -= t
    if keys[pygame.K_LEFT]:
        if mods & pygame.KMOD_CTRL:
            rv[2] += r
        else:
            rv[1] += r
    if keys[pygame.K_RIGHT]:
        if mods & pygame.KMOD_CTRL:
            rv[2] -= r
        else:
            rv[1] -= r
    if keys[pygame.K_UP]:
        rv[0] -= r
    if keys[pygame.K_DOWN]:
        rv[0] += r

    cuboids_2d = []
    for i in range(len(cuboids)):
        vertices_2d = []
        for j in range(len(cuboids[i])):
            cuboids[i][j] = translate(cuboids[i][j], tv)
            cuboids[i][j] = rotate(cuboids[i][j], rv)
            vertices_2d.append(project(cuboids[i][j], d))
        cuboids_2d.append(vertices_2d)

    for i in range(len(cuboids_2d)):
        for edge_id in edges:
            pygame.draw.aaline(screen, 'white', cuboids_2d[i][edge_id[0]], cuboids_2d[i][edge_id[1]])

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
