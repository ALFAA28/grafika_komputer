
lebar = 10
tinggi = 5
x = 3
y = 2

- `lebar = 10` → jumlah kolom dalam grid.
- `tinggi = 5` → jumlah baris dalam grid.
- `x = 3`, `y = 2` → posisi titik yang akan ditandai dengan huruf **"X"** pada
  koordinat `(3, 2)`.
-----------------------------------------------------------------------------------------

print("Simulasi Koordinat Layar (10x5):\n")

Menampilkan judul simulasi sebelum mencetak grid.
-----------------------------------------------------------------------------------------

for row in range(tinggi):
    for col in range(lebar):

- Perulangan luar (`row`) berjalan dari 0 sampai 4 (total 5 baris).
- Perulangan dalam (`col`) berjalan dari 0 sampai 9 (total 10 kolom).
-----------------------------------------------------------------------------------------

        if col == x and row == y:
            print("X", end="")

- Jika posisi saat ini sama dengan `(x, y)`, maka cetak `"X"` sebagai penanda titik.
-----------------------------------------------------------------------------------------

        else:
            print(".", end="")

- Jika bukan titik yang ditandai, cetak `"."` sebagai latar kosong.
-----------------------------------------------------------------------------------------

    print()

- Setelah satu baris selesai, pindah ke baris berikutnya.
-----------------------------------------------------------------------------------------

<img width="810" height="430" alt="image" src="https://github.com/user-attachments/assets/daabda26-23b4-4896-a652-bb60ced7ae10" />

-----------------------------------------------------------------------------------------
