from collections import deque
from visualizer.main import Visualizer
from algorithms.kd_tree.kd_class import KDTree 

def kd_build_visualization2(points_list, tree=None):
    """Tworzy wizualizację KD-Tree (wariant Leaf-Storage) używając BitAlgo Visualizer."""
    vis = Visualizer()
    
    # Konwersja na krotki
    points_tuples = []
    for p in points_list:
        points_tuples.append((p.x, p.y) if hasattr(p, 'x') else tuple(p))

    # Budowa drzewa
    if tree is None:
        tree = KDTree(points_tuples)

    # Wyznaczanie granic 
    if points_tuples:
        xs = [p[0] for p in points_tuples]
        ys = [p[1] for p in points_tuples]
        min_x, max_x = min(xs) - 20, max(xs) + 20
        min_y, max_y = min(ys) - 20, max(ys) + 20
        
        # Ramka
        vis.add_line_segment(((min_x, min_y), (max_x, min_y)), color="black")
        vis.add_line_segment(((max_x, min_y), (max_x, max_y)), color="black")
        vis.add_line_segment(((max_x, max_y), (min_x, max_y)), color="black")
        vis.add_line_segment(((min_x, max_y), (min_x, min_y)), color="black")
    else:
        min_x, max_x, min_y, max_y = 0, 800, 0, 800

    # Rysowanie punktów
    vis.add_point(points_tuples, color="blue", s=3)

    # Rysowanie podziałów (BFS)
    if tree.root:
        queue = deque([(tree.root, (min_x, max_x, min_y, max_y))])

        while queue:
            node, (bx_min, bx_max, by_min, by_max) = queue.popleft()
            
            if node is None or node.is_leaf():
                continue

            split = node.split_val
            
            if node.axis == 0: # Oś X
                vis.add_line_segment(((split, by_min), (split, by_max)), color="gray", linewidth=1)
                queue.append((node.left, (bx_min, split, by_min, by_max)))
                queue.append((node.right, (split, bx_max, by_min, by_max)))
            else: # Oś Y
                vis.add_line_segment(((bx_min, split), (bx_max, split)), color="gray", linewidth=1)
                queue.append((node.left, (bx_min, bx_max, by_min, split)))
                queue.append((node.right, (bx_min, bx_max, split, by_max)))

    return vis