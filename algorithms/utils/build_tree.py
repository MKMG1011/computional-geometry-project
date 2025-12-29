from algorithms.quadtree.quadtree import QuadTree, Rectangle, Point, build_quadtree
from algorithms.quadtree.quadtree_visualization import quadtree_vis
from algorithms.quadtree.quadtree_query_visualization import visualize_quadtree_query



from algorithms.kd_tree.kd_class import *
from algorithms.kd_tree.kd_build_visualization import *
from algorithms.kd_tree.kd_query_visualization import * 


def build_tree(algorithm, points_list, k=4):

    if algorithm == 'quadtree':
        return build_quadtree(points_list, Rectangle(400, 400, 400, 400), capacity=4)

    elif algorithm == "kdtree":
        return KDTree(points_list)
    
    return None

def get_points_in_area(algorithm, points_list, search_area, k=4):

    tree = build_tree(algorithm, points_list, k)

    if algorithm == 'quadtree':
        found_points = []
        tree.query(search_area, found_points)
        return found_points

    elif algorithm == "kdtree":
        min_x = search_area.x - search_area.w
        max_x = search_area.x + search_area.w
        min_y = search_area.y - search_area.h
        max_y = search_area.y + search_area.h
        
        region = (min_x, max_x, min_y, max_y)
        
        found_tuples = tree.query(region)
        
        return [Point(pt[0], pt[1]) for pt in found_tuples]