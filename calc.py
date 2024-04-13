from math import cos, sin

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
