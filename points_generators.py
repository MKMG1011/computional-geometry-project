# plik zawiera różne generatory do tworzenia sekwencji danych   

import numpy as np
import random
def generate_uniform_points(left, right, n=10**5):
    random.seed(2137)
    points = np.random.uniform(left, right, size=(n, 2))
    return [tuple(point) for point in points]

def generate_normal_points(mean, std, n=10**5):
    random.seed(2137)
    points = np.random.normal(mean, std, size=(n, 2))
    return [tuple(point) for point in points]

def generate_collinear_points(a, b, n=100, x_range=1000):
    random.seed(2137)
    points = []
    vect = (b[0] - a[0], b[1] - a[1])
    if vect[0] == 0: t_start, t_end = -x_range, x_range
    else: t_start, t_end = (-x_range - a[0]) / vect[0], (x_range - a[0]) / vect[0]
    t_min, t_max = min(t_start, t_end), max(t_start, t_end)
    t_factor = np.random.uniform(t_min, t_max, n)
    for t in t_factor:
        x = a[0] + vect[0] * t
        y = a[1] + vect[1] * t
        points.append((x, y))
    return [tuple(point) for point in points]

def generate_square_points(a, b, c, d, axis_n, diag_n):
    random.seed(2137)
    points = [a, b, c, d]
    vects = [(b, a), (d, a), (c, a), (b, d)] # axis1, axis2, diag1, diag2 vectors logic simplified
    # Re-using previous logic but compact
    # Actually let's just stick to the reliable previous implementation logic
    res_points = []
    # Axis
    for start, end in [(a,b), (a,d)]:
        dx, dy = end[0]-start[0], end[1]-start[1]
        ts = np.random.uniform(0, 1, axis_n)
        for t in ts: res_points.append((start[0]+dx*t, start[1]+dy*t))
    # Diagonals
    for start, end in [(a,c), (d,b)]:
        dx, dy = end[0]-start[0], end[1]-start[1]
        ts = np.random.uniform(0, 1, diag_n)
        for t in ts: res_points.append((start[0]+dx*t, start[1]+dy*t))
    return res_points

def generate_grid_points(n=100):
    random.seed(2137)
    return [(i, j) for i in range(n) for j in range(n)]

def generate_clustered_points(cluster_centers, cluster_std, points_per_cluster):
    random.seed(2137)
    points = []
    for center in cluster_centers:
        cluster_points = np.random.normal(center, cluster_std, size=(points_per_cluster, 2))
        points.extend(cluster_points)
    return [tuple(point) for point in points]

def generate_spiral_points(n, center=(500, 500), max_radius=450, turns=4):
    random.seed(2137)
    theta = np.linspace(0, turns * 2 * np.pi, n)
    noise = np.random.normal(0, 5, n)
    r = (theta / (turns * 2 * np.pi)) * max_radius + noise
    x = center[0] + r * np.cos(theta)
    y = center[1] + r * np.sin(theta)
    data = np.column_stack((x, y))
    return [tuple(p) for p in data]