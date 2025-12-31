from visualizer.main import Visualizer
from algorithms.kd_tree.kd_class import KDTree 

def kd_build_visualization(points_list, tree=None):
    vis = Visualizer()
    
    # 1. Przygotowanie punktów
    points_tuples = []
    for p in points_list:
        points_tuples.append((p.x, p.y) if hasattr(p, 'x') else tuple(p))

    if not points_tuples:
        return vis

    # Ustalanie granic świata
    xs = [p[0] for p in points_tuples]
    ys = [p[1] for p in points_tuples]
    min_x, max_x = min(xs) - 20, max(xs) + 20
    min_y, max_y = min(ys) - 20, max(ys) + 20
    
    # Rysowanie ramki świata
    vis.add_line_segment(((min_x, min_y), (max_x, min_y)), color="black")
    vis.add_line_segment(((max_x, min_y), (max_x, max_y)), color="black")
    vis.add_line_segment(((max_x, max_y), (min_x, max_y)), color="black")
    vis.add_line_segment(((min_x, max_y), (min_x, min_y)), color="black")
    
    vis.add_point(points_tuples, color="blue", s=12)
    
    if tree is None:
        tree = KDTree(points_tuples)
    
    def traverse_dfs(node, bx_min, bx_max, by_min, by_max):
        if node is None or node.is_leaf():
            return

        split = node.split_val
        
        if node.axis == 0: 
            
            vis.add_line_segment(((split, by_min), (split, by_max)), color="red", linewidth=1)
            
            left_bounds = (bx_min, split, by_min, by_max)
            right_bounds = (split, bx_max, by_min, by_max)
        else: 
            
            vis.add_line_segment(((bx_min, split), (bx_max, split)), color="green", linewidth=1)
            
            left_bounds = (bx_min, bx_max, by_min, split)
            right_bounds = (bx_min, bx_max, split, by_max)

        traverse_dfs(node.left, *left_bounds)
        traverse_dfs(node.right, *right_bounds)

    if tree.root:
        traverse_dfs(tree.root, min_x, max_x, min_y, max_y)

    return vis