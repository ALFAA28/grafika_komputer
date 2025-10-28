
    print("Simulasi Koordinat Layar (10x5):")

Menampilkan judul atau keterangan bahwa program akan mensimulasikan tampilan layar 
berukuran 10 kolom dan 5 baris.
-----------------------------------------------------------------------------------------

    for y in range(0, 5):

Melakukan perulangan sebanyak 5 kali (dari `y = 0` hingga `y = 4`) untuk mewakili 
**baris** pada layar.
-----------------------------------------------------------------------------------------

    for x in range(0, 10):

Perulangan di dalam (`nested loop`) sebanyak 10 kali (dari `x = 0` hingga `x = 9`) untuk 
mewakili **kolom** pada setiap baris.
-----------------------------------------------------------------------------------------

        print("x", end="")

Mencetak huruf `"x"` tanpa pindah baris (`end=""` mencegah `print()` membuat baris baru). 
Ini membuat deretan `"x"` dalam satu baris.
-----------------------------------------------------------------------------------------

    print()

Setelah satu baris selesai dicetak, baris ini membuat **pindah ke baris baru**, agar 
baris berikutnya dimulai di bawahnya.
-----------------------------------------------------------------------------------------

<img width="748" height="356" alt="image" src="https://github.com/user-attachments/assets/75302065-e48c-4a2c-8a84-4e0964701082" />

-----------------------------------------------------------------------------------------
