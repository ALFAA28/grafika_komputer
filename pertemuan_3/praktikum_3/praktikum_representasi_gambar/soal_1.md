
x1, y1 = 0, 0
x2, y2 = 5, 3

- Mendefinisikan titik awal `(x1, y1)` dan titik akhir `(x2, y2)`.
-------------------------------------------------------------------------------------------

n = 10

- Menentukan jumlah segmen interpolasi. Karena `n = 10`, maka akan dihasilkan
  **11 titik** (termasuk titik awal dan akhir).
-------------------------------------------------------------------------------------------

print("Titik-titik koordinat sepanjang garis dari (0,0) ke (5,3):\n")

- Menampilkan judul output.
-------------------------------------------------------------------------------------------

for i in range(n + 1):

- Melakukan perulangan dari `i = 0` hingga `i = 10` (total 11 titik).
-------------------------------------------------------------------------------------------

    t = i / n

- Menghitung rasio interpolasi `t`, yaitu nilai antara 0 dan 1 yang menunjukkan posisi 
  relatif antara titik awal dan akhir.
------------------------------------------------------------------------------------------

    x = x1 + (x2 - x1) * t
    y = y1 + (y2 - y1) * t

- Menghitung koordinat titik ke-i menggunakan rumus interpolasi linier:
  
  x = x_1 + (x_2 - x_1) \cdot t,\quad y = y_1 + (y_2 - y_1) \cdot t
------------------------------------------------------------------------------------------

    print(f"Titik ke-{i}: {{x:.2f}}, {{y:.2f}}")

- Menampilkan koordinat titik ke-i dengan format dua angka di belakang koma.
------------------------------------------------------------------------------------------

Berikut hasil yang akan dicetak:
<img width="610" height="572" alt="Screenshot 2025-10-28 142350" src="https://github.com/user-attachments/assets/6a81a122-00f9-4f50-891f-b06a6bfaf104" />




