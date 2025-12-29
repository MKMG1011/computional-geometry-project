from collections import deque
from visualizer.main import Visualizer
from algorithms.quadtree import QuadTree, Rectangle

def quadtree_vis(points_list, boundary, k):
    vis = Visualizer()
    #boundary = Rectangle(400, 400, 400, 400)
    qt = QuadTree(boundary, k)

    for p in points_list:
        qt.insert(p)

    all_points_tuples = [(p.x, p.y) for p in points_list]
    vis.add_point(all_points_tuples, color="blue")
    
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