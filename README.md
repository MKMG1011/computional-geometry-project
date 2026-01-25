# Orthogonal Range Search: Quadtree vs. KD-Tree

[cite_start]Projekt dedykowany rozwiązaniu problemu przeszukiwania obszarów ortogonalnych w geometrii obliczeniowej[cite: 1, 12, 13]. [cite_start]System implementuje i porównuje dwie kluczowe struktury danych: **Quadtree** (drzewo ćwiartkowe) oraz **KD-Tree** (drzewo k-wymiarowe)[cite: 18, 19, 22].

## 🚀 Główne Funkcjonalności
* **Implementacja Struktur Przestrzennych**:
    * [cite_start]**Quadtree**: Rekurencyjny podział przestrzeni na cztery równe ćwiartki (NE, NW, SW, SE) z przechowywaniem punktów wyłącznie w liściach[cite: 19, 21, 63].
    * [cite_start]**KD-Tree**: Binarne drzewo dzielące przestrzeń względem naprzemiennych osi (X/Y) w oparciu o medianę zbioru punktów, co zapewnia zrównoważenie struktury[cite: 22, 23, 24].
* **Silnik Wizualizacji**:
    * [cite_start]Dynamiczne animacje (GIF) prezentujące proces budowy drzew oraz mechanizm "odcinania" (pruning) gałęzi podczas zapytań obszarowych[cite: 478, 489, 2095].
    * [cite_start]Wykorzystanie silnika wizualizacyjnego opartego na bibliotece Matplotlib, stworzonego przez koło naukowe BIT[cite: 43, 56, 367].
* [cite_start]**Interfejs Interaktywny**: Notatnik Jupyter umożliwiający ręczne wprowadzanie punktów oraz definiowanie obszarów wyszukiwania za pomocą interaktywnego selektora myszy[cite: 61, 1965, 1966, 1978].
* [cite_start]**Analiza Wydajnościowa**: Kompleksowy moduł benchmarkingu porównujący czasy budowy i zapytań na 6 zróżnicowanych rozkładach danych: jednostajnym, normalnym, prostej ukośnej, kopercie, siatce oraz pierścieniu [cite: 2183, 2184-2193].

## 🛠️ Wymagania Techniczne
[cite_start]Projekt został zrealizowany i przetestowany przy użyciu interpretera **Python 3.13.5**[cite: 26, 31]. [cite_start]Wymagane biblioteki zewnętrzne to[cite: 26]:
* [cite_start]`numpy` (2.0.2) – obliczenia numeryczne i generowanie danych[cite: 27, 32].
* [cite_start]`pandas` (2.3.3) – obsługa i agregacja danych[cite: 28, 33].
* [cite_start]`matplotlib` (3.9.4) – wizualizacja struktur i wyników[cite: 29, 35].

## 📂 Struktura Projektu
* [cite_start]`algorithms/kd_tree/` – Implementacja klasy KDTree oraz skrypty wizualizujące[cite: 49].
* [cite_start]`algorithms/quadtree/` – Implementacja drzewa ćwiartkowego z kontrolą głębokości[cite: 50, 177].
* [cite_start]`algorithms/utils/` – Funkcje pomocnicze do generowania testów i wizualizacji wyników końcowych[cite: 51, 52].
* [cite_start]`main.ipynb` – Główny interfejs programu z przygotowanymi scenariuszami testowymi[cite: 1871, 1872].

## 📈 Wnioski z Analizy
[cite_start]Przeprowadzone testy na zbiorach do **100 000 punktów** wykazały, że[cite: 2599, 2636, 2835]:
* [cite_start]**KD-Tree** oferuje bardziej stabilny czas budowy i zapytania, szczególnie w przypadku danych o dużej gęstości (np. rozkład Gaussa) lub złożonej geometrii[cite: 2822, 2823, 2833].
* [cite_start]**Quadtree** wykazuje wysoką skuteczność w "odcinaniu" dużych, pustych obszarów przestrzeni, lecz jego wydajność spada przy silnych zagęszczeniach punktów[cite: 2832, 2834, 2840].

## 👥 Autorzy
* [cite_start]Mikołaj Gaweł [cite: 4]
* [cite_start]Mateusz Kursa [cite: 5]

---
[cite_start]*Projekt zrealizowany w ramach przedmiotu Algorytmy Geometryczne (AGH, styczeń 2026)[cite: 6].*
