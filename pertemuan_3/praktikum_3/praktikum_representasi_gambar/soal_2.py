x1, y1 = 0, 0
x2, y2 = 5, 3

n = 10

print("Titik-titik koordinat sepanjang garis dari (0,0) ke (5,3):\n")
for i in range(n + 1):
    t = i / n  
    x = x1 + (x2 - x1) * t
    y = y1 + (y2 - y1) * t
    print(f"Titik ke-{i}: ({x:.2f}, {y:.2f})")