from math import pi, cos, sin

import numpy
import numpy as np
import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True


def projection(vertex: tuple, d: float) -> tuple:
    if vertex[2] > 0.001:
        x = ((vertex[0] * d) / vertex[2]) + (screen.get_width() / 2)
        y = ((vertex[1] * d) / vertex[2]) + (screen.get_height() / 2)
    else:  # temp workaround for division by 0
        x = ((vertex[0] * d) / 0.001) + (screen.get_width() / 2)
        y = ((vertex[1] * d) / 0.001) + (screen.get_height() / 2)
    return x, y


def translate(vertex: tuple, t: list) -> tuple:
    return vertex[0] + t[0], vertex[1] + t[1], vertex[2] + t[2]


def rotate(vertex: tuple, fi: list) -> tuple:
    rot = numpy.identity(3)
    x, y, z = fi
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
    return (rot @ np.array(vertex).transpose()).tolist()


d = 400
r = pi / 64

edges = ((0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4), (0, 4), (1, 5), (2, 6), (3, 7))
vertices = [(-50, -50, 100), (50, -50, 100), (50, -50, 200), (-50, -50, 200),
            (-50, 50, 100), (50, 50, 100), (50, 50, 200), (-50, 50, 200)]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill('black')

    t = [0, 0, 0]
    fi = [0, 0, 0]

    keys = pygame.key.get_pressed()
    mods = pygame.key.get_mods()
    if keys[pygame.K_i]:
        d += 0.1 * d
    if keys[pygame.K_o]:
        d -= 0.1 * d
    if keys[pygame.K_LEFT]:
        if mods & pygame.KMOD_CTRL:
            fi[2] -= r
        elif mods & pygame.KMOD_SHIFT:
            fi[1] += r
        else:
            t[0] += 5
    if keys[pygame.K_RIGHT]:
        if mods & pygame.KMOD_CTRL:
            fi[2] += r
        elif mods & pygame.KMOD_SHIFT:
            fi[1] -= r
        else:
            t[0] -= 5
    if keys[pygame.K_UP]:
        if mods & pygame.KMOD_CTRL:
            t[2] += 5
        elif mods & pygame.KMOD_SHIFT:
            fi[0] += r
        else:
            t[1] += 5
    if keys[pygame.K_DOWN]:
        if mods & pygame.KMOD_CTRL:
            t[2] -= 5
        elif mods & pygame.KMOD_SHIFT:
            fi[0] -= r
        else:
            t[1] -= 5

    vertices_2d = []
    for idx in range(len(vertices)):
        vertices[idx] = translate(vertices[idx], t)
        vertices[idx] = rotate(vertices[idx], fi)
        vertices_2d.append(projection(vertices[idx], d))

    for edge_id in edges:
        pygame.draw.aaline(screen, 'white', vertices_2d[edge_id[0]], vertices_2d[edge_id[1]])

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
