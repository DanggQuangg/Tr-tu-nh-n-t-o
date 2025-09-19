import tkinter as tk
from PIL import Image, ImageTk
import random

class GreedyQueens:
    def __init__(self, n=8):
        self.n = n
        self.reset()
        self.last_pos = None

    def reset(self):
        self.queens = []
        self.row = 0
        self.last_pos = None

    def conflicts(self, row, col):
        cnt = 0
        for (r, c) in self.queens:
            if c == col or abs(r - row) == abs(c - col):
                cnt += 1
        return cnt

    def step(self):
        if self.row >= self.n:
            return False  


        scores = []
        for c in range(self.n):
            cnt = self.conflicts(self.row, c)
            scores.append((cnt, c))

        min_conf = min(scores)[0]
        candidates = [c for (cnt, c) in scores if cnt == min_conf]
        chosen_col = random.choice(candidates)

        self.queens.append((self.row, chosen_col))
        self.last_pos = (self.row, chosen_col)
        self.row += 1
        return True

    def current_positions(self):
        return self.queens[:]

def taobanco_fixed(r, title, size=520):
    frame = tk.LabelFrame(r, text=title, padx=8, pady=8)
    frame.grid_propagate(False)
    banco = tk.Frame(frame, height=size, width=size, bg="white")
    banco.pack(fill="both", expand=True)
    cells = [[None for _ in range(8)] for _ in range(8)]
    for i in range(8):
        banco.grid_columnconfigure(i, weight=1, uniform="o")
        banco.grid_rowconfigure(i, weight=1, uniform="o")
        for j in range(8):
            color = "black" if (i + j) % 2 else "white"
            cell = tk.Frame(banco, bg=color, borderwidth=1, relief="solid")
            cell.grid(row=i, column=j, sticky="nsew")
            cell.grid_propagate(False)
            cells[i][j] = cell
    return frame, banco, cells


def veoco_fixed(cells, queens=None, queenimg=None, highlight=None):
    for i in range(8):
        for j in range(8):
            for w in cells[i][j].winfo_children():
                w.destroy()
            cells[i][j]["highlightbackground"] = "black"
            cells[i][j]["highlightthickness"] = 1

    queens = set(queens or [])
    for (i,j) in queens:
        if queenimg is not None:
            tk.Label(cells[i][j], image=queenimg, bg=cells[i][j]["bg"]).pack(expand=True)
        else:
            fg = "white" if cells[i][j]["bg"] == "black" else "black"
            tk.Label(cells[i][j], text="Q", font=("Arial",28,"bold"), fg=fg, bg=cells[i][j]["bg"]).pack(expand=True)

    if highlight:
        i,j = highlight
        cells[i][j]["highlightbackground"] = "yellow"
        cells[i][j]["highlightthickness"] = 3


root = tk.Tk()
root.title("8 Hậu – Greedy Algorithm")

khungtrai, bancotrai, cells_trai = taobanco_fixed(root, "Bàn cờ (Greedy)")
khungtrai.grid(row=0, column=0, padx=10, pady=10)

hau = ImageTk.PhotoImage(Image.open("queen.jpg").resize((56, 56)))

solver = GreedyQueens(n=8)
veoco_fixed(cells_trai, queens=[], queenimg=hau)

delay = 500
running = False

def buoc_tiep():
    global running
    running = True
    def run_step():
        global running
        if not running:
            return
        veoco_fixed(cells_trai, queens=solver.current_positions(), queenimg=hau, highlight=solver.last_pos)
        if solver.step():
            root.after(delay, run_step)
        else:
            running = False
            btn_buoc.config(text="Đã xong")
    run_step()

def lam_moi():
    global running, solver
    running = False
    solver = GreedyQueens(n=8)
    veoco_fixed(cells_trai, queens=[], queenimg=hau)
    btn_buoc.config(text="Bắt đầu")

def tang_toc():
    global delay
    delay = 100

toolbar = tk.Frame(root)
toolbar.grid(row=1, column=0, pady=(0,10))

btn_buoc = tk.Button(toolbar, text="Bắt đầu", command=buoc_tiep)
btn_buoc.pack(side="left", padx=5)

btn_tangtoc = tk.Button(toolbar, text="Tăng tốc", command=tang_toc)
btn_tangtoc.pack(side="left", padx=5)

btn_lammoi = tk.Button(toolbar, text="Làm mới", command=lam_moi)
btn_lammoi.pack(side="left", padx=5)

root.minsize(600,600)
root.mainloop()
