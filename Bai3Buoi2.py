import numpy as np

a = input("Nhập các số cách nhau bằng dấu cách: ")
arr = np.array(list(map(int, a.split())))
delta = 0 
if len(arr) == 3:
    delta = arr[1]**2 - 4*arr[0]*arr[2]
if delta < 0:
    print("Phương trình vô nghiệm", delta, arr[1], arr[0], arr[2])
else:
    x1 = (-arr[1] + delta**0.5)/((len(arr)-1)*arr[0])
    x2 = (-arr[1] - delta**0.5)/((len(arr)-1)*arr[0])
    print("x1 =", x1)
    if(x1 != x2):
        print("x2 =", x2)
