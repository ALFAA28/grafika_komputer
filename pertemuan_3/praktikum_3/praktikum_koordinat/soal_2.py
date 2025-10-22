
lebar = 10
tinggi = 5
x = 3
y = 2

print("Simulasi Koordinat Layar (10x5):\n")
for row in range(tinggi):
    for col in range(lebar):
        if col == x and row == y:
            print("X", end="")
        else:
            print(".", end="")
    print()  