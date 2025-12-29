from collections import deque
from visualizer.main import Visualizer
from algorithms.quadtree.quadtree import QuadTree, Rectangle, Point

def quadtree_vis(raw_points_list, boundary, k):
    vis = Visualizer()
    
    points_objects = []
    for p_data in raw_points_list:
        if isinstance(p_data, (tuple, list)):
            points_objects.append(Point(p_data[0], p_data[1]))
        else:
            points_objects.append(p_data)

    qt = QuadTree(boundary, k)
    for p in points_objects:
        qt.insert(p)

    vis_coords = [(p.x, p.y) for p in points_objects]
    vis.add_point(vis_coords, color="blue")

    bx, by, bw, bh = boundary.x, boundary.y, boundary.w, boundary.h
    p1, p2 = (bx - bw, by - bh), (bx + bw, by - bh)
    p3, p4 = (bx + bw, by + bh), (bx - bw, by + bh)

    vis.add_line_segment((p1, p2), color="black")
    vis.add_line_segment((p2, p3), color="black")
    vis.add_line_segment((p3, p4), color="black")
    vis.add_line_segment((p4, p1), color="black")

    queue = deque([qt])

    while queue:
        node = queue.popleft()

        if node.divided:
            x, y = node.boundary.x, node.boundary.y
            w, h = node.boundary.w, node.boundary.h

            vis.add_line_segment(((x - w, y), (x + w, y)), color="gray")
            vis.add_line_segment(((x, y - h), (x, y + h)), color="gray")

            queue.append(node.northeast)
            queue.append(node.northwest)
            queue.append(node.southeast)
            queue.append(node.southwest)

    return vis