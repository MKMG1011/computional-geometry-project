from collections import deque
from visualizer.main import Visualizer
from algorithms.quadtree.quadtree import QuadTree, Point, build_quadtree

def visualize_quadtree_query(raw_points_list, query_rect, k=4):
    vis = Visualizer()

    # 1. Budujemy drzewo automatycznie (samo oblicza granice)
    qt_root = build_quadtree(raw_points_list, capacity=k)

    # 2. Rysujemy punkty
    vis_points = []
    for p in raw_points_list:
        if isinstance(p, (tuple, list)):
            vis_points.append(p)
        else:
            vis_points.append((p.x, p.y))
            
    vis.add_point(vis_points, color='blue')

    # 3. Rysujemy główną ramkę (pobraną z drzewa)
    bx, by, bw, bh = qt_root.boundary.x, qt_root.boundary.y, qt_root.boundary.w, qt_root.boundary.h
    p1 = (bx - bw, by - bh)
    p2 = (bx + bw, by - bh)
    p3 = (bx + bw, by + bh)
    p4 = (bx - bw, by + bh)

    vis.add_line_segment((p1, p2), color='black')
    vis.add_line_segment((p2, p3), color='black')
    vis.add_line_segment((p3, p4), color='black')
    vis.add_line_segment((p4, p1), color='black')

    # 4. Rysujemy siatkę
    queue = deque([qt_root])
    grid_lines = []

    while queue:
        node = queue.popleft()
        if node.divided:
            nx, ny = node.boundary.x, node.boundary.y
            nw, nh = node.boundary.w, node.boundary.h
            grid_lines.append(((nx - nw, ny), (nx + nw, ny)))
            grid_lines.append(((nx, ny - nh), (nx, ny + nh)))
            
            queue.append(node.northeast)
            queue.append(node.northwest)
            queue.append(node.southeast)
            queue.append(node.southwest)
            
    vis.add_line_segment(grid_lines, color='lightgray', linewidth=1)

    # 5. Rysujemy prostokąt zapytania
    qx, qy, qw, qh = query_rect.x, query_rect.y, query_rect.w, query_rect.h
    q_p1 = (qx - qw, qy - qh)
    q_p2 = (qx + qw, qy - qh)
    q_p3 = (qx + qw, qy + qh)
    q_p4 = (qx - qw, qy + qh)
    
    query_lines = [
        (q_p1, q_p2), (q_p2, q_p3), (q_p3, q_p4), (q_p4, q_p1)
    ]
    vis.add_line_segment(query_lines, color='purple', linewidth=2)

    # 6. Animacja
    def visit(node):
        if not node.boundary.intersects(query_rect):
            return

        # Sprawdzamy punkty TYLKO w liściach (bo to wersja leaf-only)
        for p in node.points:
            head = vis.add_point([(p.x, p.y)], color='orange', s=30, zorder=20)
            
            if query_rect.contains(p):
                vis.add_point([(p.x, p.y)], color='green', s=30, zorder=10)
            else:
                vis.add_point([(p.x, p.y)], color='red', s=30, zorder=10)
            
            vis.remove_figure(head)

        if node.divided:
            visit(node.northwest)
            visit(node.northeast)
            visit(node.southwest)
            visit(node.southeast)

    visit(qt_root)
    
    return vis