from collections import deque
from visualizer.main import Visualizer

def visualize_kdtree_query(tree, points_list, query_rect):
    """
    Wizualizacja KD-Tree (GIF).
    - Niebieski: Nieodwiedzone (zaoszczędzone dzięki pruningowi)
    - Czerwony: Odwiedzone, ale odrzucone (złe współrzędne) - NA STAŁE
    - Zielony: Zaakceptowane - NA STAŁE
    - Pomarańczowy: Aktualna głowica
    """
    vis = Visualizer()
    
    # ==========================================
    # 1. TŁO (Elementy statyczne)
    # ==========================================
    
    # Konwersja punktów
    all_points_tuples = []
    for p in points_list:
        coords = (p.x, p.y) if hasattr(p, 'x') else tuple(p)
        all_points_tuples.append(coords)

    # Granice
    if all_points_tuples:
        xs = [p[0] for p in all_points_tuples]
        ys = [p[1] for p in all_points_tuples]
        min_x, max_x = min(xs)-10, max(xs)+10
        min_y, max_y = min(ys)-10, max(ys)+10
    else:
        min_x, max_x, min_y, max_y = 0, 800, 0, 800

    # WSZYSTKIE punkty na początku są NIEBIESKIE
    vis.add_point(all_points_tuples, color='blue', s=10)

    # Linie podziału (szare)
    if tree.root:
        lines = []
        queue = deque([(tree.root, (min_x, max_x, min_y, max_y))])
        
        while queue:
            node, (bx1, bx2, by1, by2) = queue.popleft()
            if not node: continue
            
            px, py = node.point
            if node.axis == 0: # Pionowa
                lines.append(((px, by1), (px, by2)))
                queue.append((node.left, (bx1, px, by1, by2)))
                queue.append((node.right, (px, bx2, by1, by2)))
            else: # Pozioma
                lines.append(((bx1, py), (bx2, py)))
                queue.append((node.left, (bx1, bx2, by1, py)))
                queue.append((node.right, (bx1, bx2, py, by2)))
        
        vis.add_line_segment(lines, color='lightgray', linewidth=1)

    # Prostokąt zapytania (czerwony)
    qx1, qx2, qy1, qy2 = query_rect
    rect_lines = [
        ((qx1, qy1), (qx2, qy1)), ((qx2, qy1), (qx2, qy2)),
        ((qx2, qy2), (qx1, qy2)), ((qx1, qy2), (qx1, qy1))
    ]
    vis.add_line_segment(rect_lines, color='purple', linewidth=2)

    # ==========================================
    # 2. ANIMACJA 
    # ==========================================
    
    def is_in_rect(p, r):
        return r[0] <= p[0] <= r[1] and r[2] <= p[1] <= r[3]

    def intersects(bbox, r):
        return not (bbox[1] < r[0] or r[1] < bbox[0] or bbox[3] < r[2] or r[3] < bbox[2])

    def visit(node):
        if node is None:
            return

        # --- KROK 1: GŁOWICA (Pomarańczowa) ---
        # Pojawia się nad niebieskim punktem
        head_fig = vis.add_point([(node.point[0], node.point[1])], color='orange', s=30, zorder=20)
        
        # Sprawdzamy Pruning (czy odcinamy gałąź)
        pruned = False
        if node.bbox and not intersects(node.bbox, query_rect):
            pruned = True
            # Tutaj kończymy. Punkty w tym poddrzewie zostaną NIEBIESKIE 
            # (bo algorytm tam w ogóle nie wejdzie - to jest oszczędność).

        # --- KROK 2: WERYFIKACJA PUNKTU ---
        if not pruned and not getattr(node, 'deleted', False):
            if is_in_rect(node.point, query_rect):
                # SUKCES: Zaznaczamy na ZIELONO (na stałe)
                # Przykryje niebieski
                vis.add_point([(node.point[0], node.point[1])], color='green', s=30, zorder=10)
            else:
                # PORAŻKA: Punkt był sprawdzany, ale jest poza zakresem -> CZERWONY (na stałe)
                # Przykryje niebieski. To pokazuje, że algorytm tu był i zmarnował czas.
                vis.add_point([(node.point[0], node.point[1])], color='red', s=30, zorder=10)

        # Rekurencja
        if not pruned:
            px, py = node.point
            val = px if node.axis == 0 else py
            r_min = query_rect[0] if node.axis == 0 else query_rect[2]
            r_max = query_rect[1] if node.axis == 0 else query_rect[3]

            if r_min <= val:
                visit(node.left)
            if r_max >= val:
                visit(node.right)

        # --- KROK 3: USUNIĘCIE GŁOWICY ---
        # Pomarańczowa kropka znika, odsłaniając pod spodem albo Zielony, albo Czerwony.
        vis.remove_figure(head_fig)

    if tree.root:
        visit(tree.root)
        
    return vis