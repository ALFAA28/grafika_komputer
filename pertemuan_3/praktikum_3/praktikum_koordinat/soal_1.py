import math

def tentukan_kuadran(x, y):
    if x > 0 and y > 0:
        return "Kuadran I"
    elif x < 0 and y > 0:
        return "Kuadran II"
    elif x < 0 and y < 0:
        return "Kuadran III"
    elif x > 0 and y < 0:
        return "Kuadran IV"
    elif x == 0 and y == 0:
        return "Titik pusat (origin)"
    elif x == 0:
        return "Garis Y"
    elif y == 0:
        return "Garis X"

def main():
    print("Program Menghitung Jarak dan Kuadran Titik\n")

    try:
        x1 = float(input("Masukkan x1: "))
        y1 = float(input("Masukkan y1: "))
        x2 = float(input("Masukkan x2: "))
        y2 = float(input("Masukkan y2: "))

        jarak = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        kuadran = tentukan_kuadran(x1, y1)

        print("\n==HASIL==\n")
        print(f"Titik pertama    : ({x1}, {y1})")
        print(f"Titik kedua      : ({x2}, {y2})")
        print(f"Jarak antar titik:  {jarak:.2f}")
        print(f"Titik pertama berada di: {kuadran}")

    except ValueError:
        print("Input harus berupa angka. Silakan coba lagi.")

if __name__ == "__main__":
    main()