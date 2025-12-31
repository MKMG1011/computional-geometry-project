class Node:
    def __init__(self, point=None, left=None, right=None, split_val=None, axis=None):
        self.point = point
        self.left = left
        self.right = right
        self.split_val = split_val
        self.axis = axis

    def is_leaf(self):
        return self.point is not None

class KDTree:
    def __init__(self, points, eps=1e-9):
        self.eps = eps
        self.root = None
        if not points:
            return
        pts = [(x, y, i) for i, (x, y) in enumerate(points)]

        P_x = sorted(pts, key=lambda p: (p[0], p[1], p[2]))
        P_y = sorted(pts, key=lambda p: (p[1], p[0], p[2]))

        self.root = self._build_rec(P_x, P_y, depth=0)

    def _build_rec(self, P_x, P_y, depth):
        n = len(P_x)
        if n == 0:
            return None
        if n == 1:
            x, y, _ = P_x[0]
            return Node(point=(x, y))  
        axis = depth % 2
        mid = (n - 1) // 2
        if axis == 0:
            split_val = P_x[mid][0]
            P1_x = P_x[:mid + 1]
            P2_x = P_x[mid + 1:]
            left_ids = {p[2] for p in P1_x}
            P1_y = [p for p in P_y if p[2] in left_ids]
            P2_y = [p for p in P_y if p[2] not in left_ids]
        else:
            split_val = P_y[mid][1]
            P1_y = P_y[:mid + 1]
            P2_y = P_y[mid + 1:]

            left_ids = {p[2] for p in P1_y}
            P1_x = [p for p in P_x if p[2] in left_ids]
            P2_x = [p for p in P_x if p[2] not in left_ids]
        left = self._build_rec(P1_x, P1_y, depth + 1)
        right = self._build_rec(P2_x, P2_y, depth + 1)
        return Node(left=left, right=right, split_val=split_val, axis=axis)  

    def query(self, region):
        if self.root is None:
            return []

        x_min, x_max, y_min, y_max = region
        results = []

        inf = float("inf")
        root_region = (-inf, inf, -inf, inf)
        self._search_rec(self.root, (x_min, x_max, y_min, y_max), root_region, results)
        return results

    def _report_subtree(self, node, results):
        if node is None:
            return
        if node.is_leaf():
            results.append(node.point)
            return
        self._report_subtree(node.left, results)
        self._report_subtree(node.right, results)

    _OUTSIDE = 0
    _INSIDE = 1
    _INTERSECTS = 2

    def _classify_region(self, reg, rx_min, rx_max, ry_min, ry_max, split, axis, EPS, is_right_child):
        r_xmin, r_xmax, r_ymin, r_ymax = reg

        if (r_xmin >= rx_min - EPS and r_xmax <= rx_max + EPS and
            r_ymin >= ry_min - EPS and r_ymax <= ry_max + EPS):
            return self._INSIDE

        if (r_xmax < rx_min - EPS or r_xmin > rx_max + EPS or
            r_ymax < ry_min - EPS or r_ymin > ry_max + EPS):
            return self._OUTSIDE
        return self._INTERSECTS

    def _search_rec(self, v, R, region_v, results):
        if v is None:
            return

        rx_min, rx_max, ry_min, ry_max = R
        EPS = self.eps

        if v.is_leaf():
            x, y = v.point
            if (rx_min - EPS <= x <= rx_max + EPS) and (ry_min - EPS <= y <= ry_max + EPS):
                results.append(v.point)
            return

        min_x, max_x, min_y, max_y = region_v
        split = v.split_val

        if v.axis == 0:
            region_lc = (min_x, split, min_y, max_y)
            region_rc = (split, max_x, min_y, max_y)
        else:
            region_lc = (min_x, max_x, min_y, split)
            region_rc = (min_x, max_x, split, max_y)

        status = self._classify_region(region_lc, rx_min, rx_max, ry_min, ry_max, split, v.axis, EPS, is_right_child=False)
        if status == self._INSIDE:
            self._report_subtree(v.left, results)
        elif status == self._INTERSECTS:
            self._search_rec(v.left, R, region_lc, results)

        status = self._classify_region(region_rc, rx_min, rx_max, ry_min, ry_max, split, v.axis, EPS, is_right_child=True)
        if status == self._INSIDE:
            self._report_subtree(v.right, results)
        elif status == self._INTERSECTS:
            self._search_rec(v.right, R, region_rc, results)




