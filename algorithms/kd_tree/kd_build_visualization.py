from collections import deque
from visualizer.main import Visualizer
from algorithms.kd_tree.kd_class import KDTree 

def kd_build_visualization2(points_list, tree=None):
    """
    Tworzy wizualizację KD-Tree (wariant Leaf-Storage) używając BitAlgo Visualizer.
    """
    vis = Visualizer()
    
    # 1. Konwersja punktów na listę krotek (x, y)
    points_tuples = []
    for p in points_list:
        if hasattr(p, 'x') and hasattr(p, 'y'):
            points_tuples.append((p.x, p.y))
        else:
            points_tuples.append(tuple(p))

    # 2. Budowa drzewa (jeśli nie podano gotowego)
    if tree is None:
        tree = KDTree(points_tuples)

    # 3. Obliczanie granic świata (Bounding Box)
    # Potrzebujemy tego, żeby wiedzieć, dokąd rysować linie podziału
    if points_tuples:
        xs = [p[0] for p in points_tuples]
        ys = [p[1] for p in points_tuples]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        
        # Dodajemy margines (padding), żeby linie nie kończyły się idealnie na punktach skrajnych
        pad = 20
        min_x -= pad; max_x += pad
        min_y -= pad; max_y += pad
        
        # Opcjonalnie: Rysowanie ramki dookoła całego obszaru
        p1, p2 = (min_x, min_y), (max_x, min_y)
        p3, p4 = (max_x, max_y), (min_x, max_y)
        vis.add_line_segment((p1, p2), color="black") # Dół
        vis.add_line_segment((p2, p3), color="black") # Prawa
        vis.add_line_segment((p3, p4), color="black") # Góra
        vis.add_line_segment((p4, p1), color="black") # Lewa
    else:
        min_x, max_x, min_y, max_y = 0, 800, 0, 800

    # 4. Rysowanie wszystkich punktów (na niebiesko)
    vis.add_point(points_tuples, color="blue", s=3)

    # 5. Rysowanie linii podziału KD-Tree (BFS)
    if tree.root:
        queue = deque()
        # Kolejka przechowuje: (węzeł, (min_x, max_x, min_y, max_y) obszaru tego węzła)
        queue.append((tree.root, (min_x, max_x, min_y, max_y)))

        while queue:
            node, bounds = queue.popleft()
            
            # Jeśli węzeł jest pusty lub jest liściem, nie rysujemy linii podziału
            # (Liście w tym wariancie mają punkt, ale nie dzielą już przestrzeni)
            if node is None or node.is_leaf():
                continue

            bx_min, bx_max, by_min, by_max = bounds
            split = node.split_val  # Węzeł wewnętrzny ma split_val
            axis = node.axis        # Oraz oś podziału

            if axis == 0: # Cięcie pionowe (X)
                # Rysujemy linię pionową na x = split
                vis.add_line_segment(((split, by_min), (split, by_max)), color="gray", linewidth=1)
                
                # Dodajemy dzieci do kolejki z zaktualizowanymi granicami X
                # Lewe dziecko: x od obecnego min do split
                queue.append((node.left, (bx_min, split, by_min, by_max)))
                # Prawe dziecko: x od split do obecnego max
                queue.append((node.right, (split, bx_max, by_min, by_max)))
                
            else: # Cięcie poziome (Y)
                # Rysujemy linię poziomą na y = split
                vis.add_line_segment(((bx_min, split), (bx_max, split)), color="gray", linewidth=1)
                
                # Dodajemy dzieci do kolejki z zaktualizowanymi granicami Y
                # Lewe dziecko (dół): y od obecnego min do split
                queue.append((node.left, (bx_min, bx_max, by_min, split)))
                # Prawe dziecko (góra): y od split do obecnego max
                queue.append((node.right, (bx_min, bx_max, split, by_max)))

    return vis