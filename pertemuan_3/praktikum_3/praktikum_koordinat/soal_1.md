
def tentukan_kuadran(x, y):

Mendefinisikan fungsi untuk menentukan posisi titik `(x, y)` dalam sistem koordinat
kartesius.
----------------------------------------------------------------------------------------

    if x > 0 and y > 0:
        return "Kuadran I"

Titik berada di **Kuadran I** jika `x` dan `y` keduanya positif.
----------------------------------------------------------------------------------------

    elif x < 0 and y > 0:
        return "Kuadran II"

Titik berada di **Kuadran II** jika `x` negatif dan `y` positif.
----------------------------------------------------------------------------------------

    elif x < 0 and y < 0:
        return "Kuadran III"

Titik berada di **Kuadran III** jika `x` dan `y` keduanya negatif.
----------------------------------------------------------------------------------------

    elif x > 0 and y < 0:
        return "Kuadran IV"

Titik berada di **Kuadran IV** jika `x` positif dan `y` negatif.
----------------------------------------------------------------------------------------

    elif x == 0 and y == 0:
        return "Titik pusat (origin)"

Titik berada di **pusat koordinat (0, 0)**.
----------------------------------------------------------------------------------------

    elif x == 0:
        return "Garis Y"

Titik berada di **sumbu Y** jika `x = 0` dan `y ≠ 0`.
----------------------------------------------------------------------------------------

    elif y == 0:
        return "Garis X"

Titik berada di **sumbu X** jika `y = 0` dan `x ≠ 0`.
----------------------------------------------------------------------------------------

def main():
    print("Program Menghitung Jarak dan Kuadran Titik\n")

Menampilkan judul program.
----------------------------------------------------------------------------------------

    try:
        x1 = float(input("Masukkan x1: "))
        y1 = float(input("Masukkan y1: "))
        x2 = float(input("Masukkan x2: "))
        y2 = float(input("Masukkan y2: "))

Memasukkan koordinat dua titik: `(x1, y1)` dan `(x2, y2)`. Semua input 
dikonversi ke tipe `float` agar bisa digunakan dalam perhitungan jarak.
----------------------------------------------------------------------------------------

        jarak = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

Menghitung **jarak Euclidean** antara dua titik menggunakan rumus:

\text{jarak} = \sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}
----------------------------------------------------------------------------------------

        kuadran = tentukan_kuadran(x1, y1)

Menentukan kuadran dari titik pertama `(x1, y1)` dengan memanggil fungsi 
`tentukan_kuadran`.
----------------------------------------------------------------------------------------

        print("\n==HASIL==\n")
        print(f"Titik pertama    : ({x1}, {y1})")
        print(f"Titik kedua      : ({x2}, {y2})")
        print(f"Jarak antar titik:  {jarak:.2f}")
        print(f"Titik pertama berada di: {kuadran}")

Menampilkan hasil:
- Koordinat kedua titik
- Jarak antar titik (dibulatkan 2 angka di belakang koma)
- Posisi titik pertama dalam sistem koordinat
----------------------------------------------------------------------------------------

    except ValueError:
        print("Input harus berupa angka. Silakan coba lagi.")

Menangani kesalahan jika input bukan angka, agar program tidak crash.
----------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()

Menjalankan fungsi `main()` hanya jika file ini dijalankan langsung, bukan diimpor 
sebagai modul.
----------------------------------------------------------------------------------------

<img width="814" height="604" alt="image" src="https://github.com/user-attachments/assets/389a7b51-c9e0-486e-ba35-e3100f2dd168" />

----------------------------------------------------------------------------------------
