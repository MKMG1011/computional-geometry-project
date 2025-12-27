class Node:
    def __init__(self, point, axis, left=None, right=None, bbox=None):
        self.point = point      # (x, y)
        self.axis = axis        # 0 -> x, 1 -> y
        self.left = left
        self.right = right
        self.bbox = bbox        # (x_min, x_max, y_min, y_max)


def point_in_rect(p, r):
    x, y = p
    x_min, x_max, y_min, y_max = r
    return (x_min <= x <= x_max) and (y_min <= y <= y_max)


def rects_intersect(a, b):
    ax_min, ax_max, ay_min, ay_max = a
    bx_min, bx_max, by_min, by_max = b
    return not (ax_max < bx_min or bx_max < ax_min or ay_max < by_min or by_max < ay_min)


class KDTree:
    """
    Static 2D KD-tree (wersja A):
      - build once, query many
      - budowa O(n log n): presort po x i po y + liniowe partycjonowanie
      - range query z bbox pruning + pruning po osi splitu
      - działa poprawnie także dla duplikatów (używa wewnętrznych id)
    """

    def __init__(self, points):
        self.points = list(points)

        # wewnętrznie: (x, y, id) żeby nie psuły się duplikaty
        pts = [(p[0], p[1], i) for i, p in enumerate(self.points)]
        pts_x = sorted(pts, key=lambda t: (t[0], t[1], t[2]))  # sort po x
        pts_y = sorted(pts, key=lambda t: (t[1], t[0], t[2]))  # sort po y

        self.root = self._build(pts_x, pts_y, depth=0)

    # -------------------- build --------------------

    def _build(self, pts_x, pts_y, depth):
        n = len(pts_x)
        if n == 0:
            return None

        axis = depth % 2
        mid = n // 2

        if axis == 0:
            # pivot z listy posortowanej po x
            px, py, pid = pts_x[mid]
            left_x = pts_x[:mid]
            right_x = pts_x[mid + 1:]

            left_ids = set(t[2] for t in left_x)

            # pts_y dzielone liniowo, zachowując posortowanie po y
            left_y = [t for t in pts_y if t[2] in left_ids]
            right_y = [t for t in pts_y if (t[2] not in left_ids) and (t[2] != pid)]

            node = Node(point=(px, py), axis=axis)
            node.left = self._build(left_x, left_y, depth + 1)
            node.right = self._build(right_x, right_y, depth + 1)
            node.bbox = self._compute_bbox(node)
            return node

        else:
            # pivot z listy posortowanej po y
            px, py, pid = pts_y[mid]
            left_y = pts_y[:mid]
            right_y = pts_y[mid + 1:]

            left_ids = set(t[2] for t in left_y)

            # pts_x dzielone liniowo, zachowując posortowanie po x
            left_x = [t for t in pts_x if t[2] in left_ids]
            right_x = [t for t in pts_x if (t[2] not in left_ids) and (t[2] != pid)]

            node = Node(point=(px, py), axis=axis)
            node.left = self._build(left_x, left_y, depth + 1)
            node.right = self._build(right_x, right_y, depth + 1)
            node.bbox = self._compute_bbox(node)
            return node

    def _compute_bbox(self, node):
        x, y = node.point
        x_min = x_max = x
        y_min = y_max = y

        for ch in (node.left, node.right):
            if ch is None or ch.bbox is None:
                continue
            cx_min, cx_max, cy_min, cy_max = ch.bbox
            x_min = min(x_min, cx_min)
            x_max = max(x_max, cx_max)
            y_min = min(y_min, cy_min)
            y_max = max(y_max, cy_max)

        return (x_min, x_max, y_min, y_max)

    # -------------------- range query --------------------

    def range_query(self, x_min, x_max, y_min, y_max):
        r = (x_min, x_max, y_min, y_max)
        out = []
        self._range_query_node(self.root, r, out)
        return out

    def _range_query_node(self, node, r, out):
        if node is None:
            return

        # 1) bbox pruning
        if node.bbox is not None and not rects_intersect(node.bbox, r):
            return

        # 2) punkt węzła
        if point_in_rect(node.point, r):
            out.append(node.point)

        # 3) pruning po osi splitu
        x_min, x_max, y_min, y_max = r
        px, py = node.point

        if node.axis == 0:
            # split po x = px
            if x_min <= px:
                self._range_query_node(node.left, r, out)
            if px <= x_max:
                self._range_query_node(node.right, r, out)
        else:
            # split po y = py
            if y_min <= py:
                self._range_query_node(node.left, r, out)
            if py <= y_max:
                self._range_query_node(node.right, r, out)

    # -------------------- helpers for visualization --------------------

    def global_bbox(self):
        return None if self.root is None else self.root.bbox

    def split_segments(self):
        """
        Zwraca listę segmentów podziału:
          [ ((x1,y1),(x2,y2), depth), ... ]
        Segmenty są przycięte do regionu węzła.
        """
        if self.root is None:
            return []
        segs = []
        self._collect_segments(self.root, self.root.bbox, depth=0, out=segs)
        return segs

    def _collect_segments(self, node, region, depth, out):
        if node is None:
            return

        x_min, x_max, y_min, y_max = region
        px, py = node.point

        if node.axis == 0:
            # pion: x = px na całej wysokości regionu
            out.append(((px, y_min), (px, y_max), depth))
            left_region = (x_min, px, y_min, y_max)
            right_region = (px, x_max, y_min, y_max)
        else:
            # poziom: y = py na całej szerokości regionu
            out.append(((x_min, py), (x_max, py), depth))
            left_region = (x_min, x_max, y_min, py)
            right_region = (x_min, x_max, py, y_max)

        self._collect_segments(node.left, left_region, depth + 1, out)
        self._collect_segments(node.right, right_region, depth + 1, out)


# --- Przykład użycia (do testów) ---
if __name__ == "__main__":
    punkty = [(2, 3), (5, 4), (9, 6), (4, 7), (8, 1), (7, 2), (4, 2)]
    drzewo = KDTree(punkty)
    
    # Szukamy punktów w prostokącie x=[0, 6], y=[0, 5]
    znalezione = drzewo.range_query(0, 6, 0, 5)
    print(f"Punkty w obszarze: {znalezione}")