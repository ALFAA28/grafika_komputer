x = int(input("masukkan titik x: "))
- Program meminta pengguna memasukkan nilai koordinat X.
- `input()` menerima data dalam bentuk string, lalu `int()` mengubahnya menjadi bilangan bulat.

y = int(input("masukkan titik y: "))
- Sama seperti sebelumnya, tapi untuk koordinat Y.

warna = input("masukkan warna titik: ")
- Program meminta pengguna memasukkan warna titik.
- Warna biasanya berupa teks (string).

print(f"titik berada di ({x}, {y}) dan berwarna {warna}.")
- Menggunakan **f-string** untuk mencetak hasil dengan format yang rapi.
- Nilai `x`, `y`, dan `warna` langsung dimasukkan ke dalam string.

Jika pengguna memasukkan:
masukkan titik x: 5
masukkan titik y: 5
masukkan warna titik: hijau

Maka output-nya adalah:
titik berada di (5, 5) dan berwarna hijau.

<img width="848" height="296" alt="image" src="https://github.com/user-attachments/assets/0a5281fa-d014-4c01-b4a6-5aaf18cae023" />
