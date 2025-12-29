from collections import deque
from visualizer.main import Visualizer
from algorithms.quadtree.quadtree import QuadTree, Rectangle

def visualize_quadtree_query(points_list, query_rect, k):
    vis = Visualizer()

    screen_boundary = Rectangle(400, 400, 400, 400)
    qt_root = QuadTree(screen_boundary, k)

    for p in points_list:
        qt_root.insert(p)

    all_points_tuples = [(p.x, p.y) for p in points_list]
    vis.add_point(all_points_tuples, color='blue')

    queue = deque([qt_root])
    grid_lines = []
    
    bx, by, bw, bh = screen_boundary.x, screen_boundary.y, screen_boundary.w, screen_boundary.h
    p1, p2 = (bx - bw, by - bh), (bx + bw, by - bh)
    p3, p4 = (bx + bw, by + bh), (bx - bw, by + bh)
    vis.add_line_segment(((p1, p2)), color='black')
    vis.add_line_segment(((p2, p3)), color='black')
    vis.add_line_segment(((p3, p4)), color='black')
    vis.add_line_segment(((p4, p1)), color='black')

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

    qx, qy, qw, qh = query_rect.x, query_rect.y, query_rect.w, query_rect.h
    q_p1 = (qx - qw, qy - qh)
    q_p2 = (qx + qw, qy - qh)
    q_p3 = (qx + qw, qy + qh)
    q_p4 = (qx - qw, qy + qh)
    
    query_lines = [
        (q_p1, q_p2), (q_p2, q_p3), (q_p3, q_p4), (q_p4, q_p1)
    ]
    vis.add_line_segment(query_lines, color='purple', linewidth=2)

    def visit(node):
        if not node.boundary.intersects(query_rect):
            return

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