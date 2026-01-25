# Orthogonal Range Search: Quadtree vs. KD-Tree

Projekt dedykowany rozwiązaniu problemu przeszukiwania obszarów ortogonalnych w geometrii obliczeniowej. System implementuje i porównuje dwie kluczowe struktury danych: **Quadtree** (drzewo ćwiartkowe) oraz **KD-Tree** (drzewo k-wymiarowe).

## 🚀 Główne Funkcjonalności
* **Implementacja Struktur Przestrzennych**:
    * **Quadtree**: Rekurencyjny podział przestrzeni na cztery równe ćwiartki (NE, NW, SW, SE) z przechowywaniem punktów wyłącznie w liściach.
    * **KD-Tree**: Binarne drzewo dzielące przestrzeń względem naprzemiennych osi (X/Y) w oparciu o medianę zbioru punktów, co zapewnia zrównoważenie struktury.
* **Silnik Wizualizacji**:
    * Dynamiczne animacje (GIF) prezentujące proces budowy drzew oraz mechanizm "odcinania" (pruning) gałęzi podczas zapytań obszarowych.
    * Wykorzystanie silnika wizualizacyjnego opartego na bibliotece Matplotlib, stworzonego przez koło naukowe BIT.
* **Interfejs Interaktywny**: Notatnik Jupyter umożliwiający ręczne wprowadzanie punktów oraz definiowanie obszarów wyszukiwania za pomocą interaktywnego selektora myszy.
* **Analiza Wydajnościowa**: Kompleksowy moduł benchmarkingu porównujący czasy budowy i zapytań na 6 zróżnicowanych rozkładach danych: jednostajnym, normalnym, prostej ukośnej, kopercie, siatce oraz pierścieniu.

## 🛠️ Wymagania Techniczne
Projekt został zrealizowany i przetestowany przy użyciu interpretera **Python 3.13.5**. Wymagane biblioteki zewnętrzne to:
* `numpy` (2.0.2) – obliczenia numeryczne i generowanie danych.
* `pandas` (2.3.3) – obsługa i agregacja danych.
* `matplotlib` (3.9.4) – wizualizacja struktur i wyników.

## 📂 Struktura Projektu
* `algorithms/kd_tree/` – Implementacja klasy KDTree oraz skrypty wizualizujące.
* `algorithms/quadtree/` – Implementacja drzewa ćwiartkowego z kontrolą głębokości.
* `algorithms/utils/` – Funkcje pomocnicze do generowania testów i wizualizacji wyników końcowych.
* `main.ipynb` – Główny interfejs programu z przygotowanymi scenariuszami testowymi.

## 📈 Wnioski z Analizy
Przeprowadzone testy na zbiorach do **100 000 punktów** wykazały, że:
* **KD-Tree** oferuje bardziej stabilny czas budowy i zapytania, szczególnie w przypadku danych o dużej gęstości (np. rozkład Gaussa) lub złożonej geometrii.
* **Quadtree** wykazuje wysoką skuteczność w "odcinaniu" dużych, pustych obszarów przestrzeni, lecz jego wydajność spada przy silnych zagęszczeniach punktów.

## 👥 Autorzy
* Mikołaj Gaweł
* Mateusz Kursa
