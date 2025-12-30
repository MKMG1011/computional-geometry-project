from collections import deque
from visualizer.main import Visualizer
from algorithms.quadtree.quadtree import QuadTree, Rectangle, Point, build_quadtree
from algorithms.kd_tree.kd_class import KDTree 

def visualize_search_result(points, search_area, found_points, algorithm='quadtree'):
    vis = Visualizer()
    
    k = 4
    k = 4

    xs = [p[0] if isinstance(p, (tuple, list)) else p.x for p in points]
    ys = [p[1] if isinstance(p, (tuple, list)) else p.y for p in points]

    xs += [search_area.x - search_area.w, search_area.x + search_area.w]
    ys += [search_area.y - search_area.h, search_area.y + search_area.h]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    cx = (min_x + max_x) / 2
    cy = (min_y + max_y) / 2
    half = max(max_x - min_x, max_y - min_y) / 2

    pad = 30  
    screen_boundary = Rectangle(cx, cy, half + pad, half + pad)
    min_screen = cx - (half + pad)
    max_screen = cx + (half + pad)

    points_objects = []
    kdtree_points = []
    
    for p_data in points:
        if isinstance(p_data, (tuple, list)):
            p_obj = Point(p_data[0], p_data[1])
            points_objects.append(p_obj)
            kdtree_points.append((p_data[0], p_data[1]))
        else:
            points_objects.append(p_data)
            kdtree_points.append((p_data.x, p_data.y))

    vis_coords = [(p.x, p.y) for p in points_objects]
    vis.add_point(vis_coords, color='blue', s=2)

    bx, by, bw, bh = screen_boundary.x, screen_boundary.y, screen_boundary.w, screen_boundary.h
    p1, p2 = (bx - bw, by - bh), (bx + bw, by - bh)
    p3, p4 = (bx + bw, by + bh), (bx - bw, by + bh)
   

    if algorithm == 'quadtree':
        # Tu używamy build_quadtree, więc boundary oblicza się samo
        qt = build_quadtree(points_objects, capacity=4)

        bx, by, bw, bh = qt.boundary.x, qt.boundary.y, qt.boundary.w, qt.boundary.h
        p1 = (bx - bw, by - bh)
        p2 = (bx + bw, by - bh)
        p3 = (bx + bw, by + bh)
        p4 = (bx - bw, by + bh)

       

        queue = deque([qt])
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

    elif algorithm == 'kdtree':
        min_screen, max_screen = 0, 800
        
        # Ramka ekranu dla KD-Tree (bo ono nie ma boundary w sobie)
        vis.add_line_segment(((0, 0), (800, 0)), color='black')
        vis.add_line_segment(((800, 0), (800, 800)), color='black')
        vis.add_line_segment(((800, 800), (0, 800)), color='black')
        vis.add_line_segment(((0, 800), (0, 0)), color='black')

        tree = KDTree(kdtree_points)
        if tree.root:
            queue = deque([(tree.root, min_screen, max_screen, min_screen, max_screen)])
            kd_lines = []

            while queue:
                node, x_min, x_max, y_min, y_max = queue.popleft()
                
                if node.left is None and node.right is None:
                    continue

                if node.axis == 0: 
                    split = node.split_val
                    kd_lines.append(((split, y_min), (split, y_max)))
                    if node.left:
                        queue.append((node.left, x_min, split, y_min, y_max))
                    if node.right:
                        queue.append((node.right, split, x_max, y_min, y_max))
                else: 
                    split = node.split_val
                    kd_lines.append(((x_min, split), (x_max, split)))
                    if node.left:
                        queue.append((node.left, x_min, x_max, y_min, split))
                    if node.right:
                        queue.append((node.right, x_min, x_max, split, y_max))
            
            vis.add_line_segment(kd_lines, color='lightgray', linewidth=1)

    qx, qy, qw, qh = search_area.x, search_area.y, search_area.w, search_area.h
    q_p1 = (qx - qw, qy - qh)
    q_p2 = (qx + qw, qy - qh)
    q_p3 = (qx + qw, qy + qh)
    q_p4 = (qx - qw, qy + qh)
    
    query_lines = [
        (q_p1, q_p2), (q_p2, q_p3), (q_p3, q_p4), (q_p4, q_p1)
    ]
    vis.add_line_segment(query_lines, color='purple', linewidth=2)

    if found_points:
        found_coords = []
        for p_data in found_points:
            if isinstance(p_data, (tuple, list)):
                found_coords.append((p_data[0], p_data[1]))
            else:
                found_coords.append((p_data.x, p_data.y))
        
        vis.add_point(found_coords, color='green', s=5)

    return vis