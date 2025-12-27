from collections import deque
from visualizer.main import Visualizer
from kd_class import KDTree 

def kdtree_vis(points_list, tree=None):
    """
    Tworzy wizualizację KD-Tree używając BitAlgo Visualizer.
    
    Args:
        points_list: lista krotek (x, y) lub obiektów Point
        tree: (opcjonalnie) gotowe drzewo. Jeśli None, zbuduje nowe.
    """
    vis = Visualizer()
    
    # 1. Konwersja punktów na listę krotek (x, y)
    # Obsługuje zarówno obiekty Point (jak u kolegi), jak i krotki
    points_tuples = []
    for p in points_list:
        if hasattr(p, 'x') and hasattr(p, 'y'):
            points_tuples.append((p.x, p.y))
        else:
            points_tuples.append(tuple(p))

    # 2. Budowa drzewa (jeśli nie podano gotowego)
    if tree is None:
        tree = KDTree(points_tuples)

    # 3. Rysowanie wszystkich punktów (niebieskie)
    vis.add_point(points_tuples, color="blue", s=3)

    # 4. Rysowanie granic świata (opcjonalne, ale ładne)
    # Znajdujemy min/max żeby wiedzieć jak duży jest obszar
    if points_tuples:
        xs = [p[0] for p in points_tuples]
        ys = [p[1] for p in points_tuples]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        
        # Margines
        pad = 10
        min_x -= pad; max_x += pad
        min_y -= pad; max_y += pad
        
        # Ramka dookoła wszystkiego
        p1, p2 = (min_x, min_y), (max_x, min_y)
        p3, p4 = (max_x, max_y), (min_x, max_y)
        vis.add_line_segment((p1, p2), color="black")
        vis.add_line_segment((p2, p3), color="black")
        vis.add_line_segment((p3, p4), color="black")
        vis.add_line_segment((p4, p1), color="black")
    else:
        # Domyślne wartości jak pusto
        min_x, max_x, min_y, max_y = 0, 800, 0, 800

    # 5. Rysowanie linii podziału KD-Tree (BFS - poziomami)
    if tree.root:
        queue = deque()
        # Kolejka przechowuje: (węzeł, (min_x, max_x, min_y, max_y) obszaru węzła)
        queue.append((tree.root, (min_x, max_x, min_y, max_y)))

        while queue:
            node, bounds = queue.popleft()
            if node is None:
                continue

            bx_min, bx_max, by_min, by_max = bounds
            px, py = node.point
            
            # Rysujemy linię podziału przechodzącą przez punkt węzła
            if node.axis == 0: # Cięcie pionowe (X)
                # Linia: x=px, od y_min do y_max tego obszaru
                vis.add_line_segment(((px, by_min), (px, by_max)), color="gray", linewidth=1)
                
                # Dodajemy dzieci do kolejki z nowymi granicami
                # Lewe dziecko: x od bx_min do px
                queue.append((node.left, (bx_min, px, by_min, by_max)))
                # Prawe dziecko: x od px do bx_max
                queue.append((node.right, (px, bx_max, by_min, by_max)))
                
            else: # Cięcie poziome (Y)
                # Linia: y=py, od x_min do x_max tego obszaru
                vis.add_line_segment(((bx_min, py), (bx_max, py)), color="gray", linewidth=1)
                
                # Dodajemy dzieci
                # Lewe dziecko (dół): y od by_min do py
                queue.append((node.left, (bx_min, bx_max, by_min, py)))
                # Prawe dziecko (góra): y od py do by_max
                queue.append((node.right, (bx_min, bx_max, py, by_max)))

    return vis