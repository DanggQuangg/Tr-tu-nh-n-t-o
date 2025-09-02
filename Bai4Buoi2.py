x =float(input("Nhập x: "))
k = 1      
cos_x = k  
n = 0
while 1e-10 < abs(k):
    k *= -x**2 / ((2*n+1)*(2*n+2))  
    cos_x += k
    n += 1
print(cos_x)


      
