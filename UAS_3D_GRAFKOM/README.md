# Playing With Pet Simulator

Simulasi bermain dan berjalan-jalan dengan hewan peliharaan 3D. Proyek UAS Grafika Komputer.

## Fitur Utama
1.  **Karakter 3D**: Bermain sebagai George dengan animasi berjalan yang lucu.
2.  **Pilihan Hewan**:
    -   **Anjing, Kucing, Kelinci**: Hewan darat yang lucu.
    -   **Naga**: Hewan spesial yang **bisa terbang**! Ketinggian terbang menyesuaikan ukuran.
3.  **Interaksi**:
    -   Lempar dan pungut bola.
    -   Hewan akan mengejar dan mengambil bola dengan posisi mulut yang akurat.
    -   **Giant Mode**: Tekan 'G' untuk membesarkan hewan menjadi raksasa!
    -   **Mirror Mode**: Tekan 'M' untuk memunculkan bayangan cermin.

## Kontrol
| Tombol | Fungsi |
| :--- | :--- |
| **WASD** | Bergerak (Jalan/Lari) |
| **Mouse** | Mengarahkan pandangan |
| **Klik Kiri** | Lempar Bola |
| **Klik Kanan** | Panggil Hewan Kembali |
| **E** | Ambil Bola (jika dekat) |
| **G** | Ubah Ukuran Hewan (Normal / Raksasa) |
| **M** | Mode Cermin (Mirror) |
| **C** | Ganti Kamera (FPS / TPS) |
| **ESC** | Pause / Menu Utama |

## Pengaturan Aset (Untuk Developer)
Anda bisa mengatur posisi bola di mulut hewan atau ketinggian terbang secara manual di file `main.py` bagian `pet_assets`:
-   `mouth_pos`: Posisi bola di mulut (Normal).
-   `mouth_pos_giant`: Posisi bola di mulut (Raksasa).
-   `game_y_offset`: Ketinggian terbang dari lantai (Normal).
-   `game_y_offset_giant`: Ketinggian terbang dari lantai (Raksasa).

## Cara Menjalankan
Pastikan Python dan modul Ursina terinstall.
```bash
pip install ursina
python main.py
```
