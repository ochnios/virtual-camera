import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True


def projection(vertex: tuple, d: float) -> tuple:
    if vertex[2] != 0:
        x = ((vertex[0] * d) / vertex[2]) + (screen.get_width() / 2)
        y = ((vertex[1] * d) / vertex[2]) + (screen.get_height() / 2)
    else:  # temp workaround for division by 0
        x = ((vertex[0] * d) / 0.001) + (screen.get_width() / 2)
        y = ((vertex[1] * d) / 0.001) + (screen.get_height() / 2)
    return x, y


def translate(vertex: tuple, t: list) -> tuple:
    return vertex[0] + t[0], vertex[1] + t[1], vertex[2] + t[2]


d = 100

edges = ((0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4), (0, 4), (1, 5), (2, 6), (3, 7))
vertices = [(-50, -50, 100), (50, -50, 100), (50, -50, 150), (-50, -50, 150),
            (-50, 50, 100), (50, 50, 100), (50, 50, 150), (-50, 50, 150)]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill('black')

    t = [0, 0, 0]

    keys = pygame.key.get_pressed()
    mods = pygame.key.get_mods()
    if keys[pygame.K_i]:
        d += 0.1 * d
    if keys[pygame.K_o]:
        d -= 0.1 * d
    if keys[pygame.K_LEFT]:
        t[0] += 5
    if keys[pygame.K_RIGHT]:
        t[0] -= 5
    if keys[pygame.K_UP]:
        if mods & pygame.KMOD_SHIFT:
            t[2] += 5
        else:
            t[1] += 5
    if keys[pygame.K_DOWN]:
        if mods & pygame.KMOD_SHIFT:
            t[2] -= 5
        else:
            t[1] -= 5

    vertices_2d = []
    for idx in range(len(vertices)):
        vertices[idx] = translate(vertices[idx], t)
        vertices_2d.append(projection(vertices[idx], d))

    for edge_id in edges:
        pygame.draw.aaline(screen, 'white', vertices_2d[edge_id[0]], vertices_2d[edge_id[1]])

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
