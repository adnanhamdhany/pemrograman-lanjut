def mystery(n, m):
    p = 0
    e = 0
    while e < n:
        p = p + 1
        e = e + m
    return p

# Contoh pemanggilan
print(mystery(4, 3)) 
