class Point:
    def __init__(self, x, y, user_data=None):
        self.x = x
        self.y = y
        self.user_data = user_data  # Opcjonalne dane (np. nazwa punktu)

class Rectangle:
    def __init__(self, x, y, w, h):
        self.x = x  # Środek prostokąta (x)
        self.y = y  # Środek prostokąta (y)
        self.w = w  # Połowa szerokości (od środka do krawędzi)
        self.h = h  # Połowa wysokości (od środka do krawędzi)

    # Sprawdza, czy punkt leży w tym prostokącie
    def contains(self, point):
        return (point.x >= self.x - self.w and
                point.x <= self.x + self.w and
                point.y >= self.y - self.h and
                point.y <= self.y + self.h)

    # Sprawdza, czy ten prostokąt przecina się z innym (potrzebne do wyszukiwania)
    def intersects(self, range):
        return not (range.x - range.w > self.x + self.w or
                    range.x + range.w < self.x - self.w or
                    range.y - range.h > self.y + self.h or
                    range.y + range.h < self.y - self.h)
    
class QuadTree:
    def __init__(self, boundary, capacity):
        self.boundary = boundary  # Obiekt Rectangle określający granice tego węzła
        self.capacity = capacity  # Ile punktów mieści się zanim podzielimy węzeł (np. 4)
        self.points = []          # Lista punktów w tym węźle
        self.divided = False      # Czy węzeł został już podzielony?
        
        # Dzieci (na początku puste)
        self.northeast = None
        self.northwest = None
        self.southeast = None
        self.southwest = None

    # --- KROK 1: DZIELENIE (SUBDIVIDE) ---
    # Tworzy 4 dzieci (ćwiartki) wewnątrz obecnego prostokąta
    def subdivide(self):
        x = self.boundary.x
        y = self.boundary.y
        w = self.boundary.w
        h = self.boundary.h

        # Tworzymy nowe granice dla ćwiartek (w/2, h/2 to nowe wymiary)
        ne = Rectangle(x + w/2, y - h/2, w/2, h/2)
        nw = Rectangle(x - w/2, y - h/2, w/2, h/2)
        se = Rectangle(x + w/2, y + h/2, w/2, h/2)
        sw = Rectangle(x - w/2, y + h/2, w/2, h/2)

        self.northeast = QuadTree(ne, self.capacity)
        self.northwest = QuadTree(nw, self.capacity)
        self.southeast = QuadTree(se, self.capacity)
        self.southwest = QuadTree(sw, self.capacity)
        
        self.divided = True

    # --- KROK 2: WSTAWIANIE (INSERT) ---
    def insert(self, point):
        # 1. Jeśli punkt nie mieści się w granicach tego węzła, ignorujemy go
        if not self.boundary.contains(point):
            return False

        # 2. Jeśli mamy miejsce w obecnym węźle i nie jest on podzielony, dodajemy punkt tutaj
        if len(self.points) < self.capacity:
            self.points.append(point)
            return True
        
        # 3. Jeśli brakuje miejsca, musimy podzielić węzeł (jeśli jeszcze nie podzielony)
        if not self.divided:
            self.subdivide()

        # 4. Próbujemy dodać punkt do jednego z dzieci (rekurencja)
        # Punkt trafi tylko do jednego z nich, bo return zadziała przy pierwszym sukcesie
        if self.northeast.insert(point): return True
        if self.northwest.insert(point): return True
        if self.southeast.insert(point): return True
        if self.southwest.insert(point): return True
        
        return False

# --- KROK 3: WYSZUKIWANIE (QUERY) ---
    # Zwraca listę punktów znajdujących się w zadanym obszarze (range)
    def query(self, range, found_points):
        # 1. Optymalizacja: Jeśli obszar przeszukiwania nie przecina się z tym węzłem,
        # to w tym węźle na pewno nie ma szukanych punktów. Koniec.
        if not self.boundary.intersects(range):
            return found_points

        # 2. Sprawdź punkty znajdujące się w tym węźle
        for point in self.points:
            if range.contains(point):
                found_points.append(point)

        # 3. Jeśli węzeł jest podzielony, szukaj rekurencyjnie u dzieci
        if self.divided:
            self.northwest.query(range, found_points)
            self.northeast.query(range, found_points)
            self.southwest.query(range, found_points)
            self.southeast.query(range, found_points)

        return found_points

