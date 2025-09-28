import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import random, math

def random_state(n=4):
    return [random.randint(0, n-1) for _ in range(n)]

def cost(state):
    n = len(state)
    conflicts = 0
    for i in range(n):
        for j in range(i+1, n):
            if state[i] == state[j] or abs(state[i]-state[j]) == abs(i-j):
                conflicts += 1
    return conflicts

def neighbor(state):
    n = len(state)
    new_state = state[:]
    row = random.randint(0, n-1)
    new_col = random.randint(0, n-1)
    while new_col == new_state[row]:
        new_col = random.randint(0, n-1)
    new_state[row] = new_col
    return new_state, row, new_col

def taobanco_fixed(r, title, n=4, size=360):
    frame = tk.LabelFrame(r, text=title, padx=8, pady=8)
    frame.grid_propagate(False)
    banco = tk.Frame(frame, height=size, width=size, bg="white")
    banco.pack(fill="both", expand=True)
    cells = [[None for _ in range(n)] for _ in range(n)]
    for i in range(n):
        banco.grid_columnconfigure(i, weight=1, uniform="o")
        banco.grid_rowconfigure(i, weight=1, uniform="o")
        for j in range(n):
            color = "black" if (i + j) % 2 else "white"
            cell = tk.Frame(banco, bg=color, borderwidth=1, relief="solid")
            cell.grid(row=i, column=j, sticky="nsew")
            cell.grid_propagate(False)
            cells[i][j] = cell
    return frame, banco, cells

def veoco_fixed(cells, state=None, queenimg=None, highlight=None):
    n = len(cells)
    for i in range(n):
        for j in range(n):
            for w in cells[i][j].winfo_children():
                w.destroy()
            cells[i][j]["highlightbackground"] = "black"
            cells[i][j]["highlightthickness"] = 1

    if state:
        for row, col in enumerate(state):
            if queenimg:
                tk.Label(cells[row][col], image=queenimg, bg=cells[row][col]["bg"]).pack(expand=True)
            else:
                color = cells[row][col]["bg"]
                fg = "white" if color == "black" else "black"
                tk.Label(cells[row][col], text="Q", font=("Arial",28,"bold"), fg=fg, bg=color).pack(expand=True)

    if highlight:
        i, j = highlight
        cells[i][j]["highlightbackground"] = "yellow"
        cells[i][j]["highlightthickness"] = 3


root = tk.Tk()
root.title("4 Hậu – Simulated Annealing")
root.grid_columnconfigure(0, weight=1, uniform="khung")
root.grid_columnconfigure(1, weight=1, uniform="khung")
root.grid_rowconfigure(0, weight=1)

khungtrai, _, cells_trai = taobanco_fixed(root, "Bàn cờ hiện tại", n=4)
khungphai, _, cells_phai = taobanco_fixed(root, "Bàn cờ SA", n=4)
khungtrai.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
khungphai.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

hau = ImageTk.PhotoImage(Image.open("queen.jpg").resize((64, 64)))

state = random_state(4)
veoco_fixed(cells_trai, state, hau)
veoco_fixed(cells_phai, state, hau)

running = False
delay = 800
T = 10.0
alpha = 0.95
step_count = 0

frame_log = tk.LabelFrame(root, text="Log chạy thuật toán", padx=5, pady=5)
frame_log.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

columns = ("Step", "Cost", "DeltaE", "Accept", "Row", "Col")
tree = ttk.Treeview(frame_log, columns=columns, show="headings", height=8)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=80, anchor="center")
tree.pack(fill="both", expand=True)

def run_step():
    global state, T, running, step_count
    if not running:
        return

    step_count += 1
    current_cost = cost(state)
    new_state, row, col = neighbor(state)
    new_cost = cost(new_state)
    deltaE = new_cost - current_cost

    accept = False
    if deltaE <= 0:
        accept = True
    else:
        p = math.exp(-deltaE / T)
        if random.random() < p:
            accept = True

    if accept:
        state = new_state

    veoco_fixed(cells_trai, state, hau, highlight=(row, state[row]))
    veoco_fixed(cells_phai, state, hau)
    lbl_info.config(text=f"T={T:.2f}, cost={cost(state)}, ΔE={deltaE}")

    tree.insert("", "end", values=(step_count, cost(state), deltaE, "Yes" if accept else "No", row, state[row]))

    # Giảm T
    T *= alpha
    if T < 0.001 or cost(state) == 0:
        running = False
        btn_start.config(text="Đã dừng")
        return

    root.after(delay, run_step)

def start():
    global running, T, alpha, state, step_count
    try:
        T0 = float(entry_T.get())
        a = float(entry_alpha.get())
    except:
        T0, a = 10.0, 0.95
    state = random_state(4)
    veoco_fixed(cells_trai, state, hau)
    veoco_fixed(cells_phai, state, hau)
    lbl_info.config(text=f"Khởi tạo: cost={cost(state)}")
    btn_start.config(text="Đang chạy")
    reset_Ta(T0, a)
    step_count = 0
    for i in tree.get_children():
        tree.delete(i)  
    running = True
    run_step()

def reset_Ta(T0, a):
    global T, alpha
    T = T0
    alpha = a

def stop():
    global running
    running = False
    btn_start.config(text="Bắt đầu")

toolbar = tk.Frame(root)
toolbar.grid(row=1, column=0, columnspan=2, pady=(5,5))

tk.Label(toolbar, text="T ban đầu:").pack(side="left")
entry_T = tk.Entry(toolbar, width=6)
entry_T.insert(0, "10")
entry_T.pack(side="left", padx=5)

tk.Label(toolbar, text="Alpha:").pack(side="left")
entry_alpha = tk.Entry(toolbar, width=6)
entry_alpha.insert(0, "0.95")
entry_alpha.pack(side="left", padx=5)

btn_start = tk.Button(toolbar, text="Bắt đầu", command=start)
btn_start.pack(side="left", padx=5)

btn_stop = tk.Button(toolbar, text="Dừng", command=stop)
btn_stop.pack(side="left", padx=5)

lbl_info = tk.Label(toolbar, text="Thông tin")
lbl_info.pack(side="left", padx=15)

root.minsize(800,700)
root.mainloop()
