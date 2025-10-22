#list
#titik = [(0,0), (50,50), (100,0)]

#print("tampilkan koordinat yang sudah dimasukkan!!")
#for i, (x, y) in enumerate(titik, start=1):
#    print(f"{i}. koordinat: (x: {x}, y: {y})")
    
#tuple
#pusat = (0,0)

#print("nilai pusat:", pusat)

#dictionary
a = int(input("masukkan titik x:"))
b = int(input("masukkan titik y:"))
c = input("masukkan warna:")

titik = {"x": a, "y": b, "warna": c}

print(f"titik ({titik['x']}, {titik['y']}) berewarna {titik['warna']}.")