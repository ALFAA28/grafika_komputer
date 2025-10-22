import math

Mengaktifkan modul `math` agar bisa menggunakan fungsi matematika seperti akar kuadrat.
---------------------------------------------------------------------------------------------------

def hitung_jarak(x1, y1, x2, y2):

Membuat fungsi bernama `hitung_jarak` dengan empat parameter: dua titik dalam koordinat kartesius.
---------------------------------------------------------------------------------------------------

    jarak = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

Menghitung jarak antara dua titik menggunakan rumus:
\sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}
---------------------------------------------------------------------------------------------------

    return jarak

Mengembalikan hasil perhitungan jarak ke pemanggil fungsi.
---------------------------------------------------------------------------------------------------

hasil = hitung_jarak(0, 0, 3, 4)

Memanggil fungsi `hitung_jarak` dengan titik pertama di (0, 0) dan titik kedua di (3, 4),
lalu menyimpan hasilnya ke variabel `hasil`.
---------------------------------------------------------------------------------------------------

print(f"jarak antara dua titik: {hasil}")

Menampilkan hasil perhitungan ke layar dalam format teks yang rapi.
---------------------------------------------------------------------------------------------------

Jika dijalankan, program akan mencetak:

jarak antara dua titik: 5.0

Karena jarak antara titik (0, 0) dan (3, 4) adalah:

\sqrt{3^2 + 4^2} = \sqrt{9 + 16} = \sqrt{25} = 5
---------------------------------------------------------------------------------------------------

<img width="842" height="342" alt="image" src="https://github.com/user-attachments/assets/2a18803e-c157-4269-b7cc-a00f3040b969" />
