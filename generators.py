import random
import numpy as np

def gen_uniform(n, low=-100, high=100):
    """Rozkład jednostajny w zdefiniowanym kwadracie."""
    return [(random.uniform(low, high), random.uniform(low, high)) for _ in range(n)]

def gen_gauss(n, mu=0, sigma=10):
    """Rozkład normalny (Gauss) ze środkiem w mu i odchyleniem sigma."""
    return [(random.gauss(mu, sigma), random.gauss(mu, sigma)) for _ in range(n)]

def gen_line_yx(n, low=-100, high=100):
    """Punkty idealnie współliniowe na prostej y=x."""
    v = np.linspace(low, high, n)
    return list(zip(v, v))

def gen_envelope(n, low=-100, high=100, diag_ratio=0.6):
    """Koperta: Przekątne (diag_ratio) + boki ramki (reszta)."""
    diag_n = int(diag_ratio * n)
    side_n = n - diag_n
    pts = []
    # Przekątne
    v = np.linspace(low, high, diag_n // 2)
    for x in v:
        pts.extend([(x, x), (x, -x)])
    # Boki
    for i in range(side_n):
        side = i % 4
        if side == 0: pts.append((random.uniform(low, high), low))    # dół
        elif side == 1: pts.append((random.uniform(low, high), high)) # góra
        elif side == 2: pts.append((low, random.uniform(low, high)))  # lewo
        else: pts.append((high, random.uniform(low, high)))           # prawo
    return pts[:n]

def gen_grid(n, low=-100, high=100):
    """Punkty w regularnej siatce (grid)."""
    s = int(np.ceil(np.sqrt(n)))
    v = np.linspace(low, high, s)
    return [(x, y) for x in v for y in v][:n]

def gen_ring(n, radius=80):
    """Punkty na obwodzie koła o zadanym promieniu."""
    a = np.linspace(0, 2 * np.pi, n)
    return [(radius * np.cos(t), radius * np.sin(t)) for t in a]