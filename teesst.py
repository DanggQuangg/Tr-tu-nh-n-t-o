import tkinter as tk
from tkinter import messagebox

# ===== Helpers =====
def grid_pos(widget):
    info = widget.grid_info()
    return int(info["row"]), int(info["column"])

def make_tile(frame, number):
    """Tạo 1 nút trong frame và gán command truyền chính nút đó vào handler."""
    btn = tk.Button(frame, text=str(number))
    btn.config(command=lambda b=btn: btnclicked(b))
    btn.pack(fill="both", expand=True)
    return btn

def is_win():
    """
    Thắng khi:
      - frames[0..7] đều có 1 nút, text lần lượt '1'..'8'
      - frames[8] (ô cuối) phải trống
    """
    for idx, f in enumerate(frames):
        kids = f.winfo_children()
        if idx < 8:
            if not kids:
                return False
            if kids[0].cget("text") != str(idx + 1):
                return False
        else:
            # idx == 8: ô cuối cùng phải trống
            if kids:
                return False
    return True

# ===== Events =====
def btnclicked(btn):
    # Frame hiện tại của nút được bấm
    cur_frame = btn.master

    # Tìm frame trống (không có widget con)
    empty = next(f for f in frames if not f.winfo_children())

    # Vị trí lưới
    r1, c1 = grid_pos(cur_frame)
    r2, c2 = grid_pos(empty)

    # Chỉ cho phép di chuyển nếu kề nhau theo 4 hướng (Manhattan distance = 1)
    if abs(r1 - r2) + abs(c1 - c2) == 1:
        number = btn["text"]
        # Xoá nút cũ và tạo lại ở frame trống (Tkinter không đổi parent trực tiếp)
        btn.destroy()
        make_tile(empty, number)

        # Cập nhật màu: ô trống mới là cur_frame
        cur_frame.config(bg="white")
        empty.config(bg="lightgrey")

        # Sau khi di chuyển hợp lệ, kiểm tra thắng
        if is_win():
            messagebox.showinfo("Thông báo", "Bạn đã thắng!")
    else:
        # Không kề nhau: nháy màu cảnh báo nhẹ
        flash(cur_frame, to="orange", back="lightgrey")

def flash(frame, to="orange", back="lightgrey", ms=150):
    old = frame.cget("bg")
    frame.config(bg=to)
    frame.after(ms, lambda: frame.config(bg=back if back is not None else old))

# ===== UI =====
root = tk.Tk()
root.title("8 puzzles")
root.geometry("600x600")

# Khai báo trước để handler dùng
frames = []

# Chia 3x3 giãn đều
for i in range(3):
    root.grid_rowconfigure(i, weight=1)
    root.grid_columnconfigure(i, weight=1)

# Tạo 8 ô có button (1..8)
for i in range(8):
    frame = tk.Frame(root, bg="lightgrey", borderwidth=1, relief="solid")
    frame.grid(row=i // 3, column=i % 3, sticky="nsew")
    frames.append(frame)
    make_tile(frame, i + 1)

# Ô trống ban đầu tại (2,2)
empty_frame = tk.Frame(root, bg="white", borderwidth=1, relief="solid")
empty_frame.grid(row=2, column=2, sticky="nsew")
frames.append(empty_frame)

root.mainloop()
