from collections import deque
from visualizer.main import Visualizer

def visualize_kdtree_query2(tree, points_list, query_rect):
    """
    Wizualizacja zapytania KD-Tree (wariant Leaf-Storage).
    
    Kolory punktów (Liści):
    - Niebieski (domyślny): Nieodwiedzone (zaoszczędzone dzięki pruningowi).
    - Zielony: Punkt sprawdzony i leży W ŚRODKU zapytania.
    - Czerwony: Punkt sprawdzony, ale leży POZA zapytaniem (strata czasu).
    
    Animacja obszarów (Węzły wewnętrzne):
    - Pomarańczowy prostokąt: Aktualnie rozważany obszar (węzeł).
    """
    vis = Visualizer()
    
    # 1. TŁO - Punkty i Granice
    points_tuples = []
    for p in points_list:
        points_tuples.append((p.x, p.y) if hasattr(p, 'x') else tuple(p))

    # Obliczanie granic świata dla wizualizacji
    if points_tuples:
        xs = [p[0] for p in points_tuples]
        ys = [p[1] for p in points_tuples]
        min_x, max_x = min(xs) - 20, max(xs) + 20
        min_y, max_y = min(ys) - 20, max(ys) + 20
    else:
        min_x, max_x, min_y, max_y = 0, 800, 0, 800

    root_region = (min_x, max_x, min_y, max_y)

    # Rysujemy wszystkie punkty jako NIEBIESKIE (start)
    vis.add_point(points_tuples, color='blue', s=15)

    # Rysujemy statyczne linie podziału (tło)
    if tree.root:
        lines = []
        queue = deque([(tree.root, root_region)])
        while queue:
            node, bounds = queue.popleft()
            if node is None or node.is_leaf(): continue
            
            bx1, bx2, by1, by2 = bounds
            split = node.split_val
            
            if node.axis == 0: # Pionowa
                lines.append(((split, by1), (split, by2)))
                queue.append((node.left, (bx1, split, by1, by2)))
                queue.append((node.right, (split, bx2, by1, by2)))
            else: # Pozioma
                lines.append(((bx1, split), (bx2, split)))
                queue.append((node.left, (bx1, bx2, by1, split)))
                queue.append((node.right, (bx1, bx2, split, by2)))
        
        vis.add_line_segment(lines, color='lightgray', linewidth=1)

    # Rysujemy prostokąt zapytania (Fioletowy, gruby)
    qx1, qx2, qy1, qy2 = query_rect
    q_lines = [
        ((qx1, qy1), (qx2, qy1)), ((qx2, qy1), (qx2, qy2)),
        ((qx2, qy2), (qx1, qy2)), ((qx1, qy2), (qx1, qy1))
    ]
    vis.add_line_segment(q_lines, color='purple', linewidth=2)

    # ==========================================
    # 2. ANIMACJA ALGORYTMU
    # ==========================================

    def highlight_subtree(node, color):
        """Pomocnicza: koloruje całe poddrzewo (np. na zielono przy INSIDE)."""
        if node is None: return
        if node.is_leaf():
            vis.add_point([node.point], color=color, s=20)
            return
        highlight_subtree(node.left, color)
        highlight_subtree(node.right, color)

    def visit(node, region):
        if node is None:
            return

        # 1. Rysujemy aktualny obszar węzła (Pomarańczowy) - Głowica
        # Wizualizujemy, że algorytm "patrzy" teraz na ten kwadrat
        rx1, rx2, ry1, ry2 = region
        head_rect = [
            ((rx1, ry1), (rx2, ry1)), ((rx2, ry1), (rx2, ry2)),
            ((rx2, ry2), (rx1, ry2)), ((rx1, ry2), (rx1, ry1))
        ]
        head_fig = vis.add_line_segment(head_rect, color='orange', linewidth=2)
        
        # 2. Sprawdzamy LIŚĆ
        if node.is_leaf():
            x, y = node.point
            # Sprawdzenie z Epsilonem
            EPS = tree.eps
            if (qx1 - EPS <= x <= qx2 + EPS) and (qy1 - EPS <= y <= qy2 + EPS):
                # SUKCES -> Zielony
                vis.add_point([node.point], color='green', s=20)
            else:
                # PORAŻKA (był odwiedzony, ale pudło) -> Czerwony
                vis.add_point([node.point], color='red', s=20)
            
            vis.remove_figure(head_fig)
            return

        # 3. Sprawdzamy WĘZEŁ WEWNĘTRZNY
        # Musimy sklasyfikować relację regionu do zapytania (INSIDE/OUTSIDE/INTERSECTS)
        
        # Obliczanie granic dzieci
        split = node.split_val
        if node.axis == 0:
            reg_lc = (rx1, split, ry1, ry2)
            reg_rc = (split, rx2, ry1, ry2)
        else:
            reg_lc = (rx1, rx2, ry1, split)
            reg_rc = (rx1, rx2, split, ry2)

        def classify(reg):
            # Prosta klasyfikacja do wizualizacji (bez skomplikowanego EPS dla przejrzystości)
            r1, r2, s1, s2 = reg
            if r1 >= qx1 and r2 <= qx2 and s1 >= qy1 and s2 <= qy2: return "INSIDE"
            if r2 < qx1 or r1 > qx2 or s2 < qy1 or s1 > qy2: return "OUTSIDE"
            return "INTERSECTS"

        # Rekurencja Lewa
        st_lc = classify(reg_lc)
        if st_lc == "INSIDE":
            # Raportujemy całe poddrzewo na zielono bez wchodzenia
            highlight_subtree(node.left, 'green')
        elif st_lc == "INTERSECTS":
            visit(node.left, reg_lc)
        # else: OUTSIDE -> Pruning (nic nie robimy, zostaje niebieskie)

        # Rekurencja Prawa
        st_rc = classify(reg_rc)
        if st_rc == "INSIDE":
            highlight_subtree(node.right, 'green')
        elif st_rc == "INTERSECTS":
            visit(node.right, reg_rc)

        # Usuwamy pomarańczową głowicę po wyjściu z węzła
        vis.remove_figure(head_fig)

    if tree.root:
        visit(tree.root, root_region)

    return vis