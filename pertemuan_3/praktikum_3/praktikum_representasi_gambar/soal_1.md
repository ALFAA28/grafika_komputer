
    lebar = 10

    tinggi = 10

- Menentukan ukuran grid: 10 kolom (`lebar`) dan 10 baris (`tinggi`).
-----------------------------------------------------------------------------------------

    for y in range(tinggi):
        for x in range(lebar):

- Dua perulangan bersarang (`nested loop`) digunakan untuk menjelajahi setiap posisi
  `(x, y)` dalam grid.
- `y` mewakili baris (vertikal), dan `x` mewakili kolom (horizontal).
-----------------------------------------------------------------------------------------

     if x == 4 and y == 6:
         print("x", end=" ")

- Mengecek apakah posisi saat ini adalah `(4, 6)`.
- Jika ya, cetak `"x"` sebagai penanda titik khusus.
-----------------------------------------------------------------------------------------

        else:
            print(".", end=" ")

- Jika bukan titik `(4, 6)`, cetak `"."` sebagai latar kosong.
-----------------------------------------------------------------------------------------

    print()

- Setelah satu baris selesai dicetak, pindah ke baris berikutnya.
-----------------------------------------------------------------------------------------

Program akan mencetak grid seperti ini:
<img width="610" height="572" alt="Screenshot 2025-10-28 142350" src="https://github.com/user-attachments/assets/56dba284-7805-467a-9753-b88d6e5c1e82" />

