from math import cos, sin, sqrt

import numpy as np


def project(vertex: np.ndarray, d: float, vww: float, vwh: float, z0=0.01) -> np.ndarray:
    if vertex[2] > 0.01:
        x = ((vertex[0] * d) / vertex[2]) + (vww / 2)
        y = ((vertex[1] * d) / vertex[2]) + (vwh / 2)
    else:
        x = ((vertex[0] * d) / z0) + (vww / 2)
        y = ((vertex[1] * d) / z0) + (vwh / 2)
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


def distance(p1: np.ndarray, p2: np.ndarray) -> float:
    return sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2 + (p2[2] - p1[2]) ** 2)


def min_dist(poly: np.ndarray, point: np.ndarray, cell_size=10) -> float:
    if len(poly) == 3:  # find the closest triangle vertex
        # return np.linalg.norm(point - poly.mean(axis=0))
        return min(np.linalg.norm(point - poly[0]), np.linalg.norm(point - poly[1]), np.linalg.norm(point - poly[2]))
    elif len(poly) == 4:  # split into triangles and find the closest vertex
        x_size = round(np.linalg.norm(poly[0] - poly[1]) / cell_size)
        y_size = round(np.linalg.norm(poly[0] - poly[3]) / cell_size)
        step_x = -(poly[0] - poly[1]) / x_size
        step_y = -(poly[0] - poly[3]) / y_size
        min_d = np.linalg.norm(point - poly[0])
        for i in range(x_size + 1):
            for j in range(y_size + 1):
                min_d = min(min_d, np.linalg.norm(point - (poly[0] + (step_x * i) + (step_y * j))))
        return min_d
    else:  # just calc distance to the centroid
        return np.linalg.norm(point - poly.mean(axis=0))


def split_rectangles(rectangles, colors, cell_size=10):
    triangles = []
    new_colors = []
    for idx in range(len(rectangles)):
        x_size = round(np.linalg.norm(rectangles[idx][0] - rectangles[idx][1]) / cell_size)
        y_size = round(np.linalg.norm(rectangles[idx][0] - rectangles[idx][3]) / cell_size)
        step_x = -(rectangles[idx][0] - rectangles[idx][1]) / x_size
        step_y = -(rectangles[idx][0] - rectangles[idx][3]) / y_size
        for i in range(x_size):
            for j in range(y_size):
                cell = [
                    rectangles[idx][0] + (step_x * i) + (step_y * j),
                    rectangles[idx][0] + (step_x * (i + 1)) + (step_y * j),
                    rectangles[idx][0] + (step_x * (i + 1)) + (step_y * (j + 1)),
                    rectangles[idx][0] + (step_x * i) + (step_y * (j + 1))
                ]
                new_colors.append(colors[idx])
                new_colors.append(colors[idx])
                triangles.append(cell[0:3])
                triangles.append([cell[2], cell[3], cell[0]])
    return np.array(triangles), np.array(new_colors)
