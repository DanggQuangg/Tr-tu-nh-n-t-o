import tkinter as tk
from PIL import Image, ImageTk
import os

# =========================
# Solver: Backtracking từng bước (để có hành vi đặt/QUAY LUI theo nút bấm)
# =========================
class StepBacktracking:
    def __init__(self, n=8):
        self.n = n
        self.reset()

    def reset(self):
        n = self.n
        self.cols = [-1] * n          # cols[r] = cột đặt ở hàng r; -1 nếu chưa đặt
        self.used_cols = set()
        self.used_d1 = set()          # r - c
        self.used_d2 = set()          # r + c
        self.r = 0                    # hàng hiện tại (số hậu đã đặt)
        self.next_col = [0] * n       # cột sẽ thử tiếp theo ở từng hàng

    def current_positions(self):
        # trả về danh sách (r, c) các hậu đã đặt tới thời điểm hiện tại
        return [(i, self.cols[i]) for i in range(self.r) if self.cols[i] != -1]

    def step(self):
        """
        Thực hiện 1 bước:
          - Nếu còn cột hợp lệ ở hàng r -> đặt hậu (tiến lên).
          - Nếu hết cột ở hàng r -> QUAY LUI (lùi 1 hàng, thử cột kế tiếp lần sau).
        Trả về True nếu trạng thái thay đổi, False nếu đứng yên (đã lùi tới r=0 và hết chọn).
        """
        n = self.n

        # Nếu đã có đủ 8 hậu, coi như chuẩn bị tìm nghiệm khác -> lùi 1 bước
        if self.r == n:
            self.r -= 1
            c_old = self.cols[self.r]
            self.used_cols.remove(c_old)
            self.used_d1.remove(self.r - c_old)
            self.used_d2.remove(self.r + c_old)
            self.cols[self.r] = -1
            self.next_col[self.r] = c_old + 1
            return True

        # Tìm cột hợp lệ ở hàng r bắt đầu từ next_col[r]
        c = self.next_col[self.r]
        while c < n and (
            (c in self.used_cols) or
            ((self.r - c) in self.used_d1) or
            ((self.r + c) in self.used_d2)
        ):
            c += 1

        if c < n:
            # Đặt hậu tại (r, c)
            self.cols[self.r] = c
            self.used_cols.add(c)
            self.used_d1.add(self.r - c)
            self.used_d2.add(self.r + c)
            self.r += 1
            if self.r < n:
                self.next_col[self.r] = 0
            return True
        else:
            # Hết cột hợp lệ ở hàng r -> QUAY LUI nếu có thể
            if self.r == 0:
                return False
            self.r -= 1
            c_old = self.cols[self.r]
            self.used_cols.remove(c_old)
            self.used_d1.remove(self.r - c_old)
            self.used_d2.remove(self.r + c_old)
            self.cols[self.r] = -1
            self.next_col[self.r] = c_old + 1
            return True

# =========================
# GUI helpers
# =========================
def taobanco(r, title, size=520):
    frame = tk.LabelFrame(r, text=title, padx=8, pady=8)
    frame.grid_propagate(False)
    banco = tk.Frame(frame, height=size, width=size, bg="white")
    banco.pack(fill="both", expand=True)
    for i in range(8):
        banco.grid_columnconfigure(i, weight=1, uniform="o")
        banco.grid_rowconfigure(i, weight=1, uniform="o")
    return frame, banco

def veoco(banco, queens=None, queenimg=None):
    for w in banco.winfo_children():
        w.destroy()
    queens = set(queens or [])
    for i in range(8):
        for j in range(8):
            color = "black" if (i + j) % 2 else "white"
            cell = tk.Frame(banco, bg=color, borderwidth=1, relief="solid")
            cell.grid(row=i, column=j, sticky="nsew")
            cell.grid_propagate(False)
            if (i, j) in queens:
                if queenimg is not None:
                    tk.Label(cell, image=queenimg, bg=color).pack(expand=True)
                else:
                    fg = "white" if color == "black" else "black"
                    tk.Label(cell, text="Q", font=("Arial", 28, "bold"), fg=fg, bg=color).pack(expand=True)

# =========================
# Nút bấm
# =========================
def buoc_tiep():
    # B1: snapshot trước khi bấm -> vẽ lên bàn trái
    prev_pos = solver.current_positions()
    veoco(bancotrai, queens=prev_pos, queenimg=hau)

    # B2: thực hiện 1 bước (đặt thêm hoặc quay lui)
    changed = solver.step()

    # B3: vẽ trạng thái sau khi bấm -> bàn phải
    cur_pos = solver.current_positions()
    veoco(bancophai, queens=cur_pos, queenimg=hau)

    # Cập nhật nhãn nút cho dễ hiểu
    if solver.r == 8:
        btn_buoc.config(text="Bước tiếp (đang ở nghiệm, bấm sẽ quay lui)")
    else:
        btn_buoc.config(text="Bước tiếp")

def lam_moi():
    solver.reset()
    veoco(bancotrai, queens=[], queenimg=hau)
    veoco(bancophai, queens=[], queenimg=hau)
    btn_buoc.config(text="Bước tiếp")

# =========================
# Main GUI
# =========================
root = tk.Tk()
root.title("8 Hậu – Nhấn nút: đặt & quay lui từng bước")
root.grid_columnconfigure(0, weight=1, uniform="khung")
root.grid_columnconfigure(1, weight=1, uniform="khung")
root.grid_rowconfigure(0, weight=1)

khungtrai, bancotrai = taobanco(root, "Trước khi bấm (snapshot)")
khungphai, bancophai = taobanco(root, "Sau khi bấm (đi 1 bước)")
khungtrai.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
khungphai.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

# Ảnh hậu (nếu không có file, dùng chữ "Q")

hau = ImageTk.PhotoImage(Image.open("queen.jpg").resize((56, 56)))


solver = StepBacktracking(n=8)
veoco(bancotrai, queens=[], queenimg=hau)
veoco(bancophai, queens=[], queenimg=hau)

toolbar = tk.Frame(root)
toolbar.grid(row=1, column=0, columnspan=2, pady=(0, 10))

btn_buoc = tk.Button(toolbar, text="Bước tiếp", command=buoc_tiep)
btn_buoc.pack(side="left", padx=5)

btn_lammoi = tk.Button(toolbar, text="Làm mới", command=lam_moi)
btn_lammoi.pack(side="left", padx=5)

root.minsize(900, 700)
root.mainloop()
