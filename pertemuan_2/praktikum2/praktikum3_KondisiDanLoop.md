x = int(input("masukkan nilai x: "))

- Program meminta pengguna memasukkan nilai `x` (bilangan bulat).
- Nilai ini akan digunakan untuk menentukan posisi titik secara horizontal.

------------------------------------------------------------------------------------------
if x > 0:
    print("titik dikanan layar.")
elif x < 0:
    print("titik dikiri layar.")
else:
    print("titik ditengah.")
    
- **`if x > 0`** → Jika nilai `x` positif, titik dianggap berada di **kanan layar**.
- **`elif x < 0`** → Jika nilai `x` negatif, titik dianggap berada di **kiri layar**.
- **`else`** → Jika `x` sama dengan nol, titik berada **di tengah layar**.
------------------------------------------------------------------------------------------

print("menampilkan 5 titik:")
for i in range(2, 7):
    print(f"titik ke-{i}")

- `range(2, 7)` menghasilkan angka dari 2 sampai 6 (karena batas atas `range` tidak termasuk).
- Perulangan ini mencetak:
------------------------------------------------------------------------------------------

<img width="764" height="454" alt="image" src="https://github.com/user-attachments/assets/3a11f890-dc19-4b70-84f5-c4442979c3ec" />
