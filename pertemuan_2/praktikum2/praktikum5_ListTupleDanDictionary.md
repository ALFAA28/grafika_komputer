titik = [(0,0), (50,50), (100,0)]

- Membuat sebuah **list** berisi tiga **tuple**.
- Masing-masing tuple mewakili koordinat `(x, y)` dari sebuah titik.
- Contoh:
  - Titik 1: (0, 0)
  - Titik 2: (50, 50)
  - Titik 3: (100, 0)
-----------------------------------------------------------------------------------------

print("tampilkan koordinat yang sudah dimasukkan!!")

- Menampilkan teks sebagai judul atau pengantar sebelum daftar titik dicetak.
-----------------------------------------------------------------------------------------

for i, (x, y) in enumerate(titik, start=1):
    print(f"{i}. koordinat: (x: {x}, y: {y})")

- Melakukan perulangan pada list `titik` menggunakan `enumerate()`
 agar setiap titik diberi nomor urut mulai dari 1.
- `x` dan `y` diambil langsung dari tuple.
- Hasil cetakan:

  1. koordinat: (x: 0, y: 0)
  2. koordinat: (x: 50, y: 50)
  3. koordinat: (x: 100, y: 0)
-----------------------------------------------------------------------------------------

pusat = (0,0)

- Membuat sebuah **tuple** bernama `pusat` yang menyimpan koordinat pusat
 (biasanya titik asal dalam sistem koordinat kartesius).
- Tuple bersifat **immutable** (tidak bisa diubah setelah dibuat), cocok
 untuk nilai tetap seperti titik pusat.
-----------------------------------------------------------------------------------------

print("nilai pusat:", pusat)

- Menampilkan isi tuple `pusat` ke layar.
- Output:

  nilai pusat: (0, 0)
-----------------------------------------------------------------------------------------

<img width="848" height="382" alt="image" src="https://github.com/user-attachments/assets/c2c07210-3c65-4104-b4ed-df2126b72d99" />

-----------------------------------------------------------------------------------------

a = int(input("masukkan titik x:"))

Memasukkan nilai koordinat X, lalu mengubahnya menjadi bilangan bulat.
-----------------------------------------------------------------------------------------

b = int(input("masukkan titik y:"))

Memasukkan nilai koordinat Y, juga dikonversi menjadi bilangan bulat.
-----------------------------------------------------------------------------------------

c = input("masukkan warna:")

Memasukkan warna titik sebagai teks (string).
-----------------------------------------------------------------------------------------

titik = {"x": a, "y": b, "warna": c}

Membuat sebuah **dictionary** bernama `titik` yang menyimpan tiga informasi:
- `"x"` → nilai koordinat X
- `"y"` → nilai koordinat Y
- `"warna"` → warna titik
-----------------------------------------------------------------------------------------

print(f"titik ({titik['x']}, {titik['y']}) berewarna {titik['warna']}.")

Menampilkan informasi titik dengan format yang rapi menggunakan *f-string*, mengambil 
nilai dari dictionary berdasarkan kunci.
-----------------------------------------------------------------------------------------

Jika pengguna memasukkan:

masukkan titik x: 5
masukkan titik y: 5
masukkan warna: hitam

Maka output-nya adalah:

titik (5, 5) berewarna hitam.
-----------------------------------------------------------------------------------------

<img width="848" height="356" alt="image" src="https://github.com/user-attachments/assets/09ab1493-5166-4742-a996-5a9b181d0517" />

-----------------------------------------------------------------------------------------
