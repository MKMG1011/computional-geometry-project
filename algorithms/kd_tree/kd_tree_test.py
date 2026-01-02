from algorithms.kd_tree.kd_class import KDTree
from test_data import TEST_DATA

def run_kdtree_tests():
    print("rozpoczynam testy kdtree")
    passed = 0
    total = len(TEST_DATA)

    for i, case in enumerate(TEST_DATA):
        points = case["P"]
        rect = case["R"]
        expected = case["RES"]

        cx, cy, w, h = rect
        region = (cx - w, cx + w, cy - h, cy + h)

        tree = KDTree(points)
        result_raw = tree.query(region)
        
        result = sorted(result_raw)

        if result == expected:
            print(f"Test {i+1}/{total}: ZALICZONY")
            passed += 1
        else:
            print(f"Test {i+1}/{total}: BŁĄD!")
            print(f"   Oczekiwano: {len(expected)}, Otrzymano: {len(result)}")

    print(f"\nWynik KD-Tree: {passed}/{total} zaliczonych.\n")

if __name__ == "__main__":
    run_kdtree_tests()