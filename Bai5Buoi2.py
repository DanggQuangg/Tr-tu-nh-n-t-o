bang_diem = {}
no_mon = {}
n = input("Nhập số lượng SV: ")
for i in range(int(n)):
    mssv = input("Nhập MSSV: ")
    so_mon = input("Nhập số lượng môn học: ")
    mon = {}
    no_mon[mssv] = []
    for j in range(int(so_mon)):
        ten_mon = input("Nhập tên môn học: ")
        diem = float(input("Nhập điểm: "))
        if diem < 5:
            no_mon[mssv] += ten_mon
        mon[ten_mon] = diem
    bang_diem[mssv] = mon
print("Bảng điểm của sinh viên là: " ,bang_diem)
print("Danh sách sinh viên nợ môn là: ", no_mon)
    
