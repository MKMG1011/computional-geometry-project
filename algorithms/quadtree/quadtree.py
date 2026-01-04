import math

class Point:
    def __init__(self, x, y, user_data=None):
        self.x = x
        self.y = y
        self.user_data = user_data
    
    def __repr__(self):
        return f"({self.x:.1f}, {self.y:.1f})"

class Rectangle:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def contains(self, point):
        return (self.x - self.w <= point.x <= self.x + self.w and
                self.y - self.h <= point.y <= self.y + self.h)

    def intersects(self, other):
        return not (other.x - other.w > self.x + self.w or
                    other.x + other.w < self.x - self.w or
                    other.y - other.h > self.y + self.h or
                    other.y + other.h < self.y - self.h)

    @classmethod
    def from_points(cls, points, padding=10):
        if not points:
            return cls(400, 400, 400, 400)
        
        min_x = min(p.x for p in points)
        max_x = max(p.x for p in points)
        min_y = min(p.y for p in points)
        max_y = max(p.y for p in points)
        
        width = (max_x - min_x) / 2 + padding
        height = (max_y - min_y) / 2 + padding
        center_x = min_x + width - padding/2
        center_y = min_y + height - padding/2

        max_dim = max(width, height)
        return cls(center_x, center_y, max_dim, max_dim)

class QuadTree:
    def __init__(self, boundary, capacity=4, depth=0, max_depth=20):
        self.boundary = boundary
        self.capacity = capacity
        self.depth = depth
        self.max_depth = max_depth
        self.points = []
        self.divided = False
        
        self.northeast = None
        self.northwest = None
        self.southeast = None
        self.southwest = None

    def subdivide(self):
        x = self.boundary.x
        y = self.boundary.y
        w = self.boundary.w
        h = self.boundary.h

        ne = Rectangle(x + w/2, y - h/2, w/2, h/2)
        nw = Rectangle(x - w/2, y - h/2, w/2, h/2)
        se = Rectangle(x + w/2, y + h/2, w/2, h/2)
        sw = Rectangle(x - w/2, y + h/2, w/2, h/2)

        self.northeast = QuadTree(ne, self.capacity, self.depth + 1, self.max_depth)
        self.northwest = QuadTree(nw, self.capacity, self.depth + 1, self.max_depth)
        self.southeast = QuadTree(se, self.capacity, self.depth + 1, self.max_depth)
        self.southwest = QuadTree(sw, self.capacity, self.depth + 1, self.max_depth)
        
        self.divided = True

    def insert(self, point):
        if not self.boundary.contains(point):
            return False

        if self.divided:
            return self._insert_into_children(point)

        self.points.append(point)

        if len(self.points) > self.capacity and self.depth < self.max_depth:
            self.subdivide()
            while self.points:
                p = self.points.pop()
                self._insert_into_children(p)
            
        return True

    def _insert_into_children(self, point):
        if self.northeast.insert(point): return True
        if self.northwest.insert(point): return True
        if self.southeast.insert(point): return True
        if self.southwest.insert(point): return True
        return False

    def query(self, range_rect, found_points):
        if not self.boundary.intersects(range_rect):
            return found_points

        for point in self.points:
            if range_rect.contains(point):
                found_points.append(point)

        if self.divided:
            self.northwest.query(range_rect, found_points)
            self.northeast.query(range_rect, found_points)
            self.southwest.query(range_rect, found_points)
            self.southeast.query(range_rect, found_points)

        return found_points

def build_quadtree(points_list, capacity=4, max_depth=10):
    points_objects = []
    for p in points_list:
        if isinstance(p, (tuple, list)):
            points_objects.append(Point(p[0], p[1]))
        else:
            points_objects.append(p)
            
    optimal_boundary = Rectangle.from_points(points_objects)
    
    qt = QuadTree(optimal_boundary, capacity, 0, max_depth)
    for p in points_objects:
        qt.insert(p)

    return qt