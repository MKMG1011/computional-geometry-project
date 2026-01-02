from visualizer.main import Visualizer
from algorithms.kd_tree.kd_class import KDTree

def visualize_kdtree_animation(tree, points_list, query_rect):
    vis = Visualizer()
    
    points_tuples = [(p[0], p[1]) for p in points_list]
    if points_tuples:
        xs = [p[0] for p in points_tuples]
        ys = [p[1] for p in points_tuples]
        
        world_min_x, world_max_x = min(xs) - 20, max(xs) + 20
        world_min_y, world_max_y = min(ys) - 20, max(ys) + 20
    else:
        world_min_x, world_max_x, world_min_y, world_max_y = 0, 10, 0, 10

    initial_draw_region = (world_min_x, world_max_x, world_min_y, world_max_y)

    vis.add_point(points_tuples, color='blue', s=20)
    
    qx1, qx2, qy1, qy2 = query_rect
    vis.add_polygon([(qx1, qy1), (qx2, qy1), (qx2, qy2), (qx1, qy2)], color='purple', alpha=0.1)
    vis.add_line_segment([((qx1, qy1), (qx2, qy1)), ((qx2, qy1), (qx2, qy2)), 
                          ((qx2, qy2), (qx1, qy2)), ((qx1, qy2), (qx1, qy1))], color='purple', linewidth=2)

    # Rysowanie statycznej siatki podziałów drzewa KD
    def draw_static_grid(node, region):
        if node is None or node.is_leaf():
            return

        r_xmin, r_xmax, r_ymin, r_ymax = region
        draw_xmin = max(world_min_x, r_xmin)
        draw_xmax = min(world_max_x, r_xmax)
        draw_ymin = max(world_min_y, r_ymin)
        draw_ymax = min(world_max_y, r_ymax)

        split = node.split_val
        
        if node.axis == 0: 
            vis.add_line_segment(((split, draw_ymin), (split, draw_ymax)), color='black', linewidth=1, alpha=0.3)
            draw_static_grid(node.left, (r_xmin, split, r_ymin, r_ymax))
            draw_static_grid(node.right, (split, r_xmax, r_ymin, r_ymax))
        else: 
            vis.add_line_segment(((draw_xmin, split), (draw_xmax, split)), color='black', linewidth=1, alpha=0.3)
            draw_static_grid(node.left, (r_xmin, r_xmax, r_ymin, split))
            draw_static_grid(node.right, (r_xmin, r_xmax, split, r_ymax))

    if tree.root:
        root_region_infinite = (float('-inf'), float('inf'), float('-inf'), float('inf'))
        draw_static_grid(tree.root, root_region_infinite)

    # Funkcja pomocnicza do rysowania prostokąta regionu
    def get_poly_coords(region):
        r_x1, r_x2, r_y1, r_y2 = region
        r_x1 = max(world_min_x, min(world_max_x, r_x1 if r_x1 != float('-inf') else world_min_x))
        r_x2 = max(world_min_x, min(world_max_x, r_x2 if r_x2 != float('inf') else world_max_x))
        r_y1 = max(world_min_y, min(world_max_y, r_y1 if r_y1 != float('-inf') else world_min_y))
        r_y2 = max(world_min_y, min(world_max_y, r_y2 if r_y2 != float('inf') else world_max_y))
        return [(r_x1, r_y1), (r_x2, r_y1), (r_x2, r_y2), (r_x1, r_y2)]

    # Funkcja do raportowania wszystkich punktów w poddrzewie
    def report_subtree_vis(node):
        if node is None: return
        if node.is_leaf():
            vis.add_point([node.point], color='green', s=30)
            return
        report_subtree_vis(node.left)
        report_subtree_vis(node.right)

    def visit(node, region_v):
        if node is None: return

        gray_poly = vis.add_polygon(get_poly_coords(region_v), color='gray', alpha=0.2)
        
        rx_min, rx_max, ry_min, ry_max = query_rect
        EPS = tree.eps

        if node.is_leaf():
            x, y = node.point
            if (rx_min - EPS <= x <= rx_max + EPS) and (ry_min - EPS <= y <= ry_max + EPS):
                vis.add_point([node.point], color='green', s=30)
            vis.remove_figure(gray_poly)
            return

        min_x, max_x, min_y, max_y = region_v
        split = node.split_val

        if node.axis == 0:
            region_lc = (min_x, split, min_y, max_y)
            region_rc = (split, max_x, min_y, max_y)
        else:
            region_lc = (min_x, max_x, min_y, split)
            region_rc = (min_x, max_x, split, max_y)

        
        status_lc = tree._classify_region(region_lc, rx_min, rx_max, ry_min, ry_max,EPS)
        if status_lc == tree._INSIDE:
            gp = vis.add_polygon(get_poly_coords(region_lc), color='green', alpha=0.4)
            report_subtree_vis(node.left)
            vis.remove_figure(gp)
        elif status_lc == tree._INTERSECTS:
            visit(node.left, region_lc)
        else: 
            rp = vis.add_polygon(get_poly_coords(region_lc), color='red', alpha=0.4)
            vis.remove_figure(rp)

        
        status_rc = tree._classify_region(region_rc, rx_min, rx_max, ry_min, ry_max, EPS)
        if status_rc == tree._INSIDE:
            gp = vis.add_polygon(get_poly_coords(region_rc), color='green', alpha=0.4)
            report_subtree_vis(node.right)
            vis.remove_figure(gp)
        elif status_rc == tree._INTERSECTS:
            visit(node.right, region_rc)
        else:
            rp = vis.add_polygon(get_poly_coords(region_rc), color='red', alpha=0.4)
            vis.remove_figure(rp)

        vis.remove_figure(gray_poly)

    if tree.root:
        root_region_infinite = (float('-inf'), float('inf'), float('-inf'), float('inf'))
        visit(tree.root, root_region_infinite)

    return vis

