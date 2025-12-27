import math

class Node:
    """
    Pojedynczy element drzewa.
    Przechowuje punkt (x, y), oś podziału oraz linki do dzieci.
    """
    def __init__(self, point, axis, left=None, right=None):
        self.point = point  # Krotka (x, y)
        self.axis = axis    # 0 dla X, 1 dla Y
        self.left = left    # Lewe dziecko (mniejsze od point)
        self.right = right  # Prawe dziecko (większe od point)

class KDTree:
    def __init__(self, points):
        """
        Tworzy drzewo na podstawie listy punktów.
        """
        # Główny korzeń drzewa
        self.root = self._build_tree(points, depth=0)

    def _build_tree(self, points, depth):
        """
        Rekurencyjna funkcja budująca drzewo.
        Dzieli zbiór punktów na pół, wybierając medianę.
        """
        if not points:
            return None

        # 1. Wybierz oś podziału (0 = X, 1 = Y) na podstawie głębokości
        axis = depth % 2

        # 2. Posortuj punkty względem wybranej osi
        # Dzięki temu łatwo znajdziemy środek (medianę)
        # key=lambda p: p[axis] oznacza: sortuj po X jeśli axis=0, po Y jeśli axis=1
        points.sort(key=lambda p: p[axis])

        # 3. Wybierz środkowy element (Mediana)
        mid = len(points) // 2
        median_point = points[mid]

        # 4. Stwórz węzeł i rekurencyjnie zbuduj dzieci
        # Wszystko przed środkiem idzie do lewego, wszystko po środku do prawego
        return Node(
            point=median_point,
            axis=axis,
            left=self._build_tree(points[:mid], depth + 1),
            right=self._build_tree(points[mid + 1:], depth + 1)
        )

    def search_range(self, x_min, x_max, y_min, y_max):
        """
        Publiczna metoda do wyszukiwania punktów w prostokącie.
        """
        results = []
        # Definiujemy obszar szukania jako [x_min, x_max] x [y_min, y_max]
        range_bounds = (x_min, x_max, y_min, y_max)
        self._search_recursive(self.root, range_bounds, results)
        return results

    def _search_recursive(self, node, bounds, results):
        """
        Wewnętrzna funkcja rekurencyjna do przeszukiwania drzewa.
        To tutaj dzieje się magia "odcinania" (pruning).
        """
        if node is None:
            return

        x_min, x_max, y_min, y_max = bounds
        px, py = node.point
        axis = node.axis

        # 1. Sprawdź, czy AKTUALNY punkt węzła leży w szukanym prostokącie
        if x_min <= px <= x_max and y_min <= py <= y_max:
            results.append(node.point)

        # 2. Decyzja: Gdzie iść dalej? (Logika odcinania gałęzi)
        
        # Pobieramy współrzędną punktu, która decyduje o podziale (x lub y)
        current_val = px if axis == 0 else py
        
        # Pobieramy granice szukanego obszaru dla tej osi
        # Jeśli axis=0 (X), to interesuje nas x_min i x_max
        search_min = x_min if axis == 0 else y_min
        search_max = x_max if axis == 0 else y_max

        # ZASADA 1: Idź w LEWO tylko jeśli obszar szukania przecina się z lewą stroną
        # Czyli: początek szukanego obszaru (search_min) musi być mniejszy lub równy linii podziału
        if search_min <= current_val:
            self._search_recursive(node.left, bounds, results)

        # ZASADA 2: Idź w PRAWO tylko jeśli obszar szukania przecina się z prawą stroną
        # Czyli: koniec szukanego obszaru (search_max) musi być większy lub równy linii podziału
        if search_max >= current_val:
            self._search_recursive(node.right, bounds, results)

# --- Przykład użycia (do testów) ---
if __name__ == "__main__":
    punkty = [(2, 3), (5, 4), (9, 6), (4, 7), (8, 1), (7, 2)]
    drzewo = KDTree(punkty)
    
    # Szukamy punktów w prostokącie x=[0, 6], y=[0, 5]
    znalezione = drzewo.search_range(0, 6, 0, 5)
    print(f"Punkty w obszarze: {znalezione}")