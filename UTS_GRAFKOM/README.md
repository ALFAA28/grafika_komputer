1. Judul Proyek
"Aplikasi Game Dino Runner dengan Implementasi Algoritma Grafika Dasar"

2. Konsep Grafika yang Digunakan
Aplikasi ini menerapkan empat konsep utama dalam grafika komputer:
   1) Sistem Koordinat Karstesian & Raster: Pengaturan posisi objek berdasarkan sumbu X (horizontal) dan sumbu Y (vertikal) di dalam canvas.
   2) Representasi Objek:
    - Raster: Menggunakan gambar (sprite) dalam format .png untuk karakter utama.
    - Vektor (Poligon): Menggunakan kumpulan koordinat titik untuk membentuk rintangan.
   3) Animasi Sprite: Pengolahan urutan gambar (frame) untuk menciptakan efek gerakan lari dan lompat pada karakter.
   4) Deteksi Tabrakan (Collision Detection): Menggunakan perhitungan jarak Euclidean untuk mendeteksi interaksi antara karakter dengan koin atau rintangan.
      
3. Algoritma yang Dipakai
Sesuai dengan kriteria tugas, aplikasi ini mengimplementasikan algoritma berikut secara manual:

A. Algoritma Pembentukan Garis (Bresenham)
Digunakan untuk menggambar garis tanah dan sisi-sisi pada rintangan poligon. Algoritma ini dipilih karena efisiensinya dalam menentukan piksel pada layar menggunakan operasi bilangan bulat (integer).

  - Lokasi Kode: Fungsi draw_line(self, x0, y0, x1, y1, color).

B. Algoritma Pembentukan Lingkaran (Midpoint Circle)
Digunakan untuk menggambar item koin emas. Algoritma ini menggunakan parameter keputusan untuk menentukan koordinat piksel lingkaran dengan prinsip simetri 8 oktan.

  - Lokasi Kode: Fungsi draw_midpoint_circle(self, xc, yc, r, color).

C. Algoritma Gambar Poligon
Digunakan untuk membentuk rintangan dengan variasi bentuk (segi empat dan duri). Rintangan direpresentasikan sebagai list koordinat vertex yang kemudian dihubungkan menggunakan fungsi garis.

  - Lokasi Kode: Variabel self.obs_polygon_data dan logika looping di dalam game_loop.

D. Transformasi Geometris 2D
Implementasi transformasi dilakukan pada karakter utama:

  - Translasi: Pergerakan karakter melompat (sumbu Y) dan bergerak kiri-kanan (sumbu X).

  - Rotasi: Karakter berputar saat melakukan lompatan.

  - Skala: Karakter dapat membesar/mengecil (tombol 'S') dengan titik pusat (anchor) tetap di kaki.

  - Refleksi (Mirroring): Karakter berbalik arah saat bergerak ke kiri atau ke kanan.

4. Cara Menjalankan Program
Prasyarat:
  1) Pastikan sudah menginstall Python
  2) Install library Pillow (PIL) untuk pemrosesan gambar:
    - pip install Pillow
  3) Pastikan struktur folder aset gambar sebagai berikut:
     <img width="320" height="212" alt="image" src="https://github.com/user-attachments/assets/c0b35c67-2c93-440a-9bb2-3cc794ca0a63" />

 Langkah-Langkah:
  1) Buka terminal atau editor kode (seperti Thonny atau VS Code).
  2) Jalankan file utama:
    - python dino_run.py
  3) Kontrol Permainan:
    - Space: Melompat.
    - Panah Kiri / Kanan: Bergerak horizontal.
    - S: Mengubah skala (ukuran) karakter.

Tampilan Game:
<img width="1614" height="876" alt="image" src="https://github.com/user-attachments/assets/dc7a781d-59d5-4cc7-9553-20c82ca940cb" />

<img width="1616" height="896" alt="image" src="https://github.com/user-attachments/assets/fd0d3840-1962-4c0a-aba4-d30d6291dbdb" />

<img width="1610" height="870" alt="image" src="https://github.com/user-attachments/assets/b2bf5f1f-3d47-442e-9361-bd1d0d441588" />

<img width="1602" height="860" alt="image" src="https://github.com/user-attachments/assets/ae46ba8e-0bec-43bd-bf9f-007ea77c23d3" />


