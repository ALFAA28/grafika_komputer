x = int(input("masukkan nilai x: "))

if x > 0:
    print("titik dikanan layar.")
elif x < 0:
    print("titik dikiri layar.")
else:
    print("titik ditengah.")
    
print("menampilkan 5 titik:")
for i in range(2, 7):
    print(f"titik ke-{i}")