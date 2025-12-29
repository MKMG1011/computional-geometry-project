# plik zawiera różne generatory do tworzenia sekwencji danych   

import numpy as np

# 1. ROZKŁAD JEDNOSTAJNY (UNIFORM)
def generate_uniform(n, box_min, box_max):
    np.random.seed(101)
    data = np.random.uniform(box_min, box_max, size=(n, 2))
    return [tuple(p) for p in data]

# 2. KLASTRY 
def generate_clusters(n, box_min, box_max, clusters_count=5):
    np.random.seed(102)
    points_per_cluster = n // clusters_count
    data = []
    
    for _ in range(clusters_count):
        
        center = np.random.uniform(box_min + 100, box_max - 100, 2)
        points = np.random.normal(loc=center, scale=40, size=(points_per_cluster, 2))
        data.append(points)
        
    data = np.vstack(data)
    # Wycinamy punkty, które wyleciały poza mapę
    mask = (data[:,0] >= box_min) & (data[:,0] <= box_max) & \
           (data[:,1] >= box_min) & (data[:,1] <= box_max)
    data = data[mask]
    return [tuple(p) for p in data]

# 3. PRZEKĄTNA (DIAGONAL LINE)
def generate_diagonal(n, box_min, box_max, width=20):
    np.random.seed(103)
    x = np.random.uniform(box_min, box_max, n)
    y = x + np.random.uniform(-width, width, n)
    
    data = np.column_stack((x, y))
    mask = (data[:,0] >= box_min) & (data[:,0] <= box_max) & \
           (data[:,1] >= box_min) & (data[:,1] <= box_max)
    data = data[mask]
    return [tuple(p) for p in data]

# 4. OKRĄG 
def generate_circle(n, box_min, box_max):
    np.random.seed(104)
    center = (box_max + box_min) / 2
    radius = (box_max - box_min) / 3
    
    angles = np.random.uniform(0, 2 * np.pi, n)
    x = center + radius * np.cos(angles)
    y = center + radius * np.sin(angles) 
    
    data = np.column_stack((x, y))
    return [tuple(p) for p in data]

# 5. POJEDYNCZY ROZKŁAD NORMALNY (GAUSSIAN CENTER)
def generate_centered_gaussian(n, box_min, box_max):
    np.random.seed(201)
    center = (box_min + box_max) / 2
    std_dev = (box_max - box_min) / 6 
    
    data = np.random.normal(loc=center, scale=std_dev, size=(n, 2))
    
    mask = (data[:,0] >= box_min) & (data[:,0] <= box_max) & \
           (data[:,1] >= box_min) & (data[:,1] <= box_max)
    data = data[mask]
    return [tuple(p) for p in data]

# 6. KWADRAT Z PRZEKĄTNYMI 
def generate_square_with_diagonals(n, box_min, box_max):
    np.random.seed(202)
    
    n_side = n // 6
    n_diag = n // 3
    
    points = []
    
   
    y_rand = np.random.uniform(box_min, box_max, n_side)
    points.append(np.column_stack((np.full(n_side, box_min), y_rand)))
    points.append(np.column_stack((np.full(n_side, box_max), y_rand)))
    
    x_rand = np.random.uniform(box_min, box_max, n_side)
    points.append(np.column_stack((x_rand, np.full(n_side, box_min))))
    points.append(np.column_stack((x_rand, np.full(n_side, box_max))))
    
    x_diag = np.random.uniform(box_min, box_max, n_diag)
    
    points.append(np.column_stack((x_diag, x_diag)))
    
    
    y_diag_2 = box_max - (x_diag - box_min)
    points.append(np.column_stack((x_diag, y_diag_2)))
    
    data = np.vstack(points)
    return [tuple(p) for p in data]

# 7. SIATKA 

def generate_grid(n, box_min, box_max):
    side_count = int(np.sqrt(n))
    
    x = np.linspace(box_min, box_max, side_count)
    y = np.linspace(box_min, box_max, side_count)
    
    xx, yy = np.meshgrid(x, y)
    data = np.column_stack((xx.ravel(), yy.ravel()))
    
    return [tuple(p) for p in data]