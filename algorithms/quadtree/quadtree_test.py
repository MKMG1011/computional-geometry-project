from algorithms.quadtree.quadtree import Rectangle, Point, build_quadtree
from test_data import TEST_DATA

def run_quadtree_tests():
    print("rozpoczynam test quadtree")
    passed = 0
    total = len(TEST_DATA)

    for i, case in enumerate(TEST_DATA):
        points_tuples = case["P"]
        rect_tuple = case["R"]
        expected = case["RES"]

        points_objs = [Point(p[0], p[1]) for p in points_tuples]
        qt = build_quadtree(points_objs, capacity=4)
        
        q_rect = Rectangle(rect_tuple[0], rect_tuple[1], rect_tuple[2], rect_tuple[3])
        
        found_objs = []
        qt.query(q_rect, found_objs)
        
        result = sorted([(p.x, p.y) for p in found_objs])
        
        if result == expected:
            print(f"Test {i+1}/{total}: ZALICZONY")
            passed += 1
        else:
            print(f"Test {i+1}/{total}: BŁĄD!")
            print(f"   Oczekiwano: {len(expected)}, Otrzymano: {len(result)}")

    print(f"\nWynik Quadtree: {passed}/{total} zaliczonych.\n")

if __name__ == "__main__":
    run_quadtree_tests()