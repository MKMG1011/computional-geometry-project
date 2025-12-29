from collections import deque
from visualizer.main import Visualizer
from algorithms.quadtree.quadtree import build_quadtree

def quadtree_vis(raw_points_list, k=4):
    vis = Visualizer()
    
    qt = build_quadtree(raw_points_list, k)

    vis_points = []
    for p in raw_points_list:
        if isinstance(p, (tuple, list)):
            vis_points.append(p)
        else:
            vis_points.append((p.x, p.y))
            
    vis.add_point(vis_points, color="blue")

    bx, by, bw, bh = qt.boundary.x, qt.boundary.y, qt.boundary.w, qt.boundary.h
    p1 = (bx - bw, by - bh)
    p2 = (bx + bw, by - bh)
    p3 = (bx + bw, by + bh)
    p4 = (bx - bw, by + bh)

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