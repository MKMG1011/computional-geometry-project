import math

class Node:
    def __init__(self, point, axis, left=None, right=None, bbox=None, deleted=False):
        self.point = point      
        self.axis = axis        
        self.left = left
        self.right = right
        self.bbox = bbox        
        self.deleted = deleted  
class KDTree:

    """
    KD-Tree z obsługą:
    - Build: O(N log N) (presorting)
    - Query: O(sqrt(N)) (pruning)
    - Insert: O(log N)
    - Delete: O(log N) (lazy)
    - Rebuild: O(N log N)
    """
    def __init__(self, points=None):
        self.root = None
        if points:
            self.build(points)
    
    def _point_in_rect(self, p, r):
        x, y = p
        x_min, x_max, y_min, y_max = r
        return (x_min <= x <= x_max) and (y_min <= y <= y_max)

    def _rects_intersect(self, a, b):
        ax_min, ax_max, ay_min, ay_max = a
        bx_min, bx_max, by_min, by_max = b
        return not (ax_max < bx_min or bx_max < ax_min or ay_max < by_min or by_max < ay_min)
    
    def build(self, points):
        """Buduje drzewo od zera (presorting)."""
        points = list(points)
        pts = [(p[0], p[1], i) for i, p in enumerate(points)]
        
        pts_x = sorted(pts, key=lambda t: (t[0], t[1], t[2]))
        pts_y = sorted(pts, key=lambda t: (t[1], t[0], t[2]))
        
        self.root = self._build_rec(pts_x, pts_y, depth=0)

    def rebuild(self):
        """Zbiera wszystkie aktywne punkty i buduje drzewo na nowo (czyści 'deleted')."""
        active_points = self.get_all_points()
        self.build(active_points)

    def _build_rec(self, pts_x, pts_y, depth):
        n = len(pts_x)
        if n == 0: return None
        axis = depth % 2
        mid = n // 2

        if axis == 0:
            px, py, pid = pts_x[mid]
            left_x = pts_x[:mid]
            right_x = pts_x[mid + 1:]
            
            left_ids = set(t[2] for t in left_x)
            left_y = [t for t in pts_y if t[2] in left_ids]
            right_y = [t for t in pts_y if (t[2] not in left_ids) and (t[2] != pid)]
        else:
            px, py, pid = pts_y[mid]
            left_y = pts_y[:mid]
            right_y = pts_y[mid + 1:]
            
            left_ids = set(t[2] for t in left_y)
            left_x = [t for t in pts_x if t[2] in left_ids]
            right_x = [t for t in pts_x if (t[2] not in left_ids) and (t[2] != pid)]

        node = Node(point=(px, py), axis=axis)
        node.left = self._build_rec(left_x, left_y, depth + 1)
        node.right = self._build_rec(right_x, right_y, depth + 1)
        node.bbox = self._compute_bbox(node)
        return node

    def _compute_bbox(self, node):
        x, y = node.point
        x_min, x_max, y_min, y_max = x, x, y, y
        for ch in (node.left, node.right):
            if ch and ch.bbox:
                cx1, cx2, cy1, cy2 = ch.bbox
                x_min, x_max = min(x_min, cx1), max(x_max, cx2)
                y_min, y_max = min(y_min, cy1), max(y_max, cy2)
        return (x_min, x_max, y_min, y_max)

    # --- INSERT (O(log N)) ---
    def insert(self, point):
        """Dodaje punkt do drzewa (bez rebalansu)."""
        def _insert_rec(node, point, depth):
            if node is None:
                new_node = Node(point, depth % 2)
                new_node.bbox = (point[0], point[0], point[1], point[1])
                return new_node
            
            bx1, bx2, by1, by2 = node.bbox
            node.bbox = (min(bx1, point[0]), max(bx2, point[0]),
                         min(by1, point[1]), max(by2, point[1]))

            axis = node.axis
            if point[axis] < node.point[axis]:
                node.left = _insert_rec(node.left, point, depth + 1)
            else:
                node.right = _insert_rec(node.right, point, depth + 1)
            return node

        self.root = _insert_rec(self.root, point, 0)

    
    def delete(self, point):
        """Oznacza punkt jako usunięty (Lazy Deletion)."""
        node = self._find_node(self.root, point)
        if node:
            node.deleted = True

    def _find_node(self, node, point):
        if node is None: return None
        if node.point == point and not node.deleted: return node
        
        axis = node.axis
        if point[axis] < node.point[axis]:
            return self._find_node(node.left, point)
        elif point[axis] > node.point[axis]:
             return self._find_node(node.right, point)
        else:
            res = self._find_node(node.right, point)
            if res: return res
            return self._find_node(node.left, point)

    def range_query(self, x_min, x_max, y_min, y_max):
        r = (x_min, x_max, y_min, y_max)
        out = []
        self._range_query_rec(self.root, r, out)
        return out

    def _range_query_rec(self, node, r, out):
        if node is None: return


        if node.bbox and not self._rects_intersect(node.bbox, r):
            return

        
        if not node.deleted and self._point_in_rect(node.point, r):
            out.append(node.point)
           

        px, py = node.point
        axis = node.axis
        
       
        val = px if axis == 0 else py
        r_min = r[0] if axis == 0 else r[2]
        r_max = r[1] if axis == 0 else r[3]

        if r_min <= val:
            self._range_query_rec(node.left, r, out)
        if r_max >= val:
            self._range_query_rec(node.right, r, out)

    def get_all_points(self):
        """Zwraca listę wszystkich aktywnych punktów (do rebuilda)."""
        pts = []
        def _collect(node):
            if not node: return
            if not node.deleted: pts.append(node.point)
            _collect(node.left)
            _collect(node.right)
        _collect(self.root)
        return pts

if __name__ == "__main__":
    punkty = [(2, 3), (5, 4), (9, 6), (4, 7), (8, 1), (7, 2), (4, 2)]
    drzewo = KDTree(punkty)
    
    # Szukamy punktów w prostokącie x=[0, 6], y=[0, 5]
    znalezione = drzewo.range_query(0, 6, 0, 5)
    print(f"Punkty w obszarze: {znalezione}")