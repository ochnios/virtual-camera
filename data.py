import numpy as np

import calc

faces = np.array([[0, 1, 2, 3], [4, 5, 6, 7], [0, 1, 5, 4], [1, 2, 6, 5], [2, 3, 7, 6], [3, 0, 4, 7]], dtype=int)
faces_colors = np.array(
    [[245, 85, 26], [125, 188, 57], [7, 92, 191], [249, 248, 84], [54, 201, 240], [91, 26, 255]], dtype=int)
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


def cuboids_as_rectangles() -> tuple[np.ndarray, np.ndarray]:
    rectangles = np.zeros((n_cuboids * 6, 4, 3), dtype=float)
    colors = np.zeros((n_cuboids * 6, 3), dtype=int)
    for i in range(n_cuboids):
        for j in range(6):
            colors[i * 6 + j] = faces_colors[(i * 6 + j) % 6]
            for k in range(4):
                rectangles[i * 6 + j][k] = cuboids[i][faces[j][k]]
    return rectangles, colors


def cuboids_as_triangles(cell_size=10) -> tuple:
    rectangles, colors = cuboids_as_rectangles()
    triangles = []
    new_colors = []
    for idx in range(len(rectangles)):
        x_size = round(calc.distance(rectangles[idx][0], rectangles[idx][1]) / cell_size)
        y_size = round(calc.distance(rectangles[idx][0], rectangles[idx][3]) / cell_size)
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
