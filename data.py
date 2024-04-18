import numpy as np

edges = np.array([[0, 1], [1, 2], [2, 3], [3, 0], [4, 5], [5, 6], [6, 7], [7, 4], [0, 4], [1, 5], [2, 6], [3, 7]])
faces = np.array([[0, 1, 2, 3], [4, 5, 6, 7], [0, 1, 5, 4], [1, 2, 6, 5], [2, 3, 7, 6], [3, 0, 4, 7]])
faces_colors = np.array([[245, 85, 26], [125, 188, 57], [7, 92, 191], [249, 248, 84], [54, 201, 240], [91, 26, 255]])
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


def cuboids_as_rectangles() -> tuple[np.ndarray, np.ndarray]:
    n_cuboids = len(cuboids)
    rectangles = np.zeros((n_cuboids * 6, 4, 3), dtype=float)
    colors = np.zeros((n_cuboids * 6, 3), dtype=int)
    for i in range(n_cuboids):
        for j in range(6):
            colors[i * 6 + j] = faces_colors[(i * 6 + j) % 6]
            for k in range(4):
                rectangles[i * 6 + j][k] = cuboids[i][faces[j][k]]
    return rectangles, colors


def just_rectangles() -> tuple:
    rectangles = np.array([
        [[-30, -60, 120], [30, -60, 120], [30, 40, 100], [-30, 40, 100]],
        [[-30, -80, 120], [30, -80, 120], [30, 20, 100], [-30, 20, 100]]
    ], dtype=float)
    print(rectangles)
    colors = np.array([[0, 0, 255], [255, 0, 0]])
    return rectangles, colors
