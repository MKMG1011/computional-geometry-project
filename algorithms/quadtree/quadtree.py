class Point:
    def __init__(self, x, y, user_data=None):
        self.x = x
        self.y = y
        self.user_data = user_data

class Rectangle:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def contains(self, point):
        return (point.x >= self.x - self.w and
                point.x <= self.x + self.w and
                point.y >= self.y - self.h and
                point.y <= self.y + self.h)

    def intersects(self, range):
        return not (range.x - range.w > self.x + self.w or
                    range.x + range.w < self.x - self.w or
                    range.y - range.h > self.y + self.h or
                    range.y + range.h < self.y - self.h)
    
class QuadTree:
    def __init__(self, boundary, capacity):
        self.boundary = boundary
        self.capacity = capacity
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

        self.northeast = QuadTree(ne, self.capacity)
        self.northwest = QuadTree(nw, self.capacity)
        self.southeast = QuadTree(se, self.capacity)
        self.southwest = QuadTree(sw, self.capacity)
        
        self.divided = True

    def insert(self, point):
        if not self.boundary.contains(point):
            return False

        if len(self.points) < self.capacity:
            self.points.append(point)
            return True
        
        if not self.divided:
            self.subdivide()

        if self.northeast.insert(point): return True
        if self.northwest.insert(point): return True
        if self.southeast.insert(point): return True
        if self.southwest.insert(point): return True
        
        return False

    def query(self, range, found_points):
        if not self.boundary.intersects(range):
            return found_points

        for point in self.points:
            if range.contains(point):
                found_points.append(point)

        if self.divided:
            self.northwest.query(range, found_points)
            self.northeast.query(range, found_points)
            self.southwest.query(range, found_points)
            self.southeast.query(range, found_points)

        return found_points