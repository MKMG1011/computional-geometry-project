import random
import pprint

def solve_brute_force(points, rect_tuple):
    cx, cy, w, h = rect_tuple
    found = []
    for p in points:
        px, py = p
        if (cx - w <= px <= cx + w) and (cy - h <= py <= cy + h):
            found.append(p)
    return sorted(found)

def generate_test_file():
    tests = []
    random.seed(42)

    for _ in range(20):
        n = random.randint(10, 100)
        points = [(round(random.uniform(0, 1000), 2), round(random.uniform(0, 1000), 2)) for _ in range(n)]
        
        cx = round(random.uniform(200, 800), 2)
        cy = round(random.uniform(200, 800), 2)
        w = round(random.uniform(50, 150), 2)
        h = round(random.uniform(50, 150), 2)
        rect = (cx, cy, w, h)
        
        expected = solve_brute_force(points, rect)
        
        tests.append({
            "P": points,
            "R": rect,
            "RES": expected
        })

    with open("test_data.py", "w") as f:
        f.write("# Plik wygenerowany automatycznie. Nie edytowac recznie.\n\n")
        f.write("TEST_DATA = ")
        f.write(pprint.pformat(tests))

if __name__ == "__main__":
    generate_test_file()
    print("Wygenerowano plik test_data.py")