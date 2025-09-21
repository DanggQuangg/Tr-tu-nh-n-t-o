import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, UnidentifiedImageError
import random, os

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

def fitness(state):
    return 1.0 / (1 + cost(state))

def tournament_selection(pop, k=3):
    selected = random.sample(pop, min(k, len(pop)))
    selected.sort(key=lambda x: cost(x))
    return selected[0]

def uniform_crossover(p1, p2):
    n = len(p1)
    return [p1[i] if random.random() < 0.5 else p2[i] for i in range(n)]

def mutation(state, mut_rate):
    n = len(state)
    new = state[:]
    for i in range(n):
        if random.random() < mut_rate:
            old = new[i]
            new[i] = random.randint(0, n-1)
            if n > 1 and new[i] == old:
                new[i] = (old + 1) % n
    return new


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
                lbl = tk.Label(cells[row][col], image=queenimg, bg=cells[row][col]["bg"])
                lbl.image = queenimg
                lbl.pack(expand=True)
            else:
                color = cells[row][col]["bg"]
                fg = "white" if color == "black" else "black"
                tk.Label(cells[row][col], text="Q", font=("Arial",28,"bold"), fg=fg, bg=color).pack(expand=True)

    if highlight:
        i, j = highlight
        if 0 <= i < n and 0 <= j < n:
            cells[i][j]["highlightbackground"] = "yellow"
            cells[i][j]["highlightthickness"] = 3

def draw_thumbnail(canvas, x, y, size, state, queenimg=None):
    n = len(state)
    cell = size // n
    canvas.create_rectangle(x, y, x+size, y+size, fill="grey90", outline="black")
    for i in range(n):
        for j in range(n):
            color = "black" if (i + j) % 2 else "white"
            canvas.create_rectangle(x+j*cell, y+i*cell, x+(j+1)*cell, y+(i+1)*cell, fill=color, outline="")
    for row, col in enumerate(state):
        cx = x + col*cell + cell/2
        cy = y + row*cell + cell/2
        r = cell*0.28
        canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill="red", outline="black")
    canvas.create_rectangle(x, y, x+size, y+size, outline="black", width=1)


N = 4
root = tk.Tk()
root.title(f"{N} Hậu – Genetic Algorithm")
root.grid_columnconfigure(0, weight=1, uniform="khung")
root.grid_columnconfigure(1, weight=1, uniform="khung")
root.grid_rowconfigure(0, weight=1)

khungtrai, _, cells_trai = taobanco_fixed(root, "Best của quần thể", n=N)
khungphai, _, cells_phai = taobanco_fixed(root, "Cá thể được chọn", n=N)
khungtrai.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
khungphai.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

queen_img = None
try:
    if os.path.exists("queen.jpg"):
        queen_img = ImageTk.PhotoImage(Image.open("queen.jpg").resize((64,64)))
    elif os.path.exists("queen.png"):
        queen_img = ImageTk.PhotoImage(Image.open("queen.png").resize((64,64)))
except (UnidentifiedImageError, Exception):
    queen_img = None

frame_pop = tk.LabelFrame(root, text="Quần thể (nhấn vào thumbnail để chọn)", padx=5, pady=5)
frame_pop.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=(0,10))
frame_pop.grid_columnconfigure(0, weight=1)
pop_canvas = tk.Canvas(frame_pop, height=140)
h_scroll = ttk.Scrollbar(frame_pop, orient="horizontal", command=pop_canvas.xview)
pop_canvas.configure(xscrollcommand=h_scroll.set)
h_scroll.pack(side="bottom", fill="x")
pop_canvas.pack(side="left", fill="both", expand=True)
thumb_frame = tk.Frame(pop_canvas)
pop_canvas.create_window((0,0), window=thumb_frame, anchor="nw")

def update_thumb_scrollregion():
    thumb_frame.update_idletasks()
    pop_canvas.configure(scrollregion=pop_canvas.bbox("all"))

frame_log = tk.LabelFrame(root, text="Log chạy thuật toán (Generations)", padx=5, pady=5)
frame_log.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=10, pady=(0,10))
columns = ("Gen", "BestCost", "AvgCost", "BestFitness")
tree = ttk.Treeview(frame_log, columns=columns, show="headings", height=8)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100, anchor="center")
tree.pack(fill="both", expand=True)

toolbar = tk.Frame(root)
toolbar.grid(row=3, column=0, columnspan=2, pady=(5,10))

tk.Label(toolbar, text="Population:").pack(side="left")
entry_pop = tk.Entry(toolbar, width=5)
entry_pop.insert(0, "20")
entry_pop.pack(side="left", padx=4)

tk.Label(toolbar, text="Crossover%:").pack(side="left")
entry_cx = tk.Entry(toolbar, width=5)
entry_cx.insert(0, "80")
entry_cx.pack(side="left", padx=4)

tk.Label(toolbar, text="Mutation%:").pack(side="left")
entry_mut = tk.Entry(toolbar, width=5)
entry_mut.insert(0, "10")
entry_mut.pack(side="left", padx=4)

tk.Label(toolbar, text="Delay(ms):").pack(side="left")
entry_delay = tk.Entry(toolbar, width=6)
entry_delay.insert(0, "600")
entry_delay.pack(side="left", padx=4)

btn_start = tk.Button(toolbar, text="Bắt đầu", width=10)
btn_start.pack(side="left", padx=6)
btn_step = tk.Button(toolbar, text="1 Generation", width=12)
btn_step.pack(side="left", padx=6)
btn_stop = tk.Button(toolbar, text="Dừng", width=8)
btn_stop.pack(side="left", padx=6)

lbl_info = tk.Label(toolbar, text="Gen:0  BestCost:?  AvgCost:?")
lbl_info.pack(side="left", padx=12)

population = []
pop_size = 20
crossover_rate = 0.8
mutation_rate = 0.1
delay_ms = 600
running = False
generation = 0
selected_child = None

def init_population():
    global population, generation, selected_child
    population = [random_state(N) for _ in range(pop_size)]
    generation = 0
    selected_child = None
    refresh_ui()

def evaluate_population():
    costs = [cost(ind) for ind in population]
    fits = [fitness(ind) for ind in population]
    return costs, fits

def refresh_ui():
    costs, fits = evaluate_population()
    best_idx = min(range(len(population)), key=lambda i: costs[i])
    best = population[best_idx]
    best_cost = costs[best_idx]
    avg_cost = sum(costs)/len(costs)
    best_fit = fits[best_idx]

    veoco_fixed(cells_trai, best, queen_img)
    if selected_child:
        veoco_fixed(cells_phai, selected_child, queen_img)
    else:
        veoco_fixed(cells_phai, None, queen_img)

    lbl_info.config(text=f"Gen:{generation}  BestCost:{best_cost}  AvgCost:{avg_cost:.2f}")

    for widget in thumb_frame.winfo_children():
        widget.destroy()

    thumb_w = 80
    spacing = 8
    mini = tk.Canvas(thumb_frame, width=(thumb_w+spacing)*len(population)+spacing, height=thumb_w+10)
    mini.pack(side="left")
    def on_click(event):
        idx = int(event.x // (thumb_w + spacing))
        if 0 <= idx < len(population):
            select_individual(idx)
    mini.bind("<Button-1>", on_click)

    for i, ind in enumerate(population):
        x = spacing + i*(thumb_w+spacing)
        y = 5
        draw_thumbnail(mini, x, y, thumb_w, ind, queen_img)
        mini.create_text(x + thumb_w/2, y + thumb_w + 8, text=f"c={cost(ind)}", anchor="n", font=("Arial",8))

    update_thumb_scrollregion()
    tree.insert("", "end", values=(generation, best_cost, f"{avg_cost:.2f}", f"{best_fit:.4f}"))

def select_individual(idx):
    global selected_child
    selected_child = population[idx][:]
    veoco_fixed(cells_phai, selected_child, queen_img)

def run_generation():
    global population, generation, selected_child
    new_pop = []
    costs, _ = evaluate_population()
    elite_idx = min(range(len(population)), key=lambda i: costs[i])
    elite = population[elite_idx][:]
    new_pop.append(elite)

    while len(new_pop) < pop_size:
        p1 = tournament_selection(population, k=3)
        p2 = tournament_selection(population, k=3)
        if random.random() < crossover_rate:
            child = uniform_crossover(p1, p2)
        else:
            child = p1[:]
        child = mutation(child, mutation_rate)
        new_pop.append(child)

    population = new_pop
    generation += 1
    selected_child = random.choice(population)[:]
    refresh_ui()

def start_run():
    global running, pop_size, crossover_rate, mutation_rate, delay_ms
    try:
        p = int(entry_pop.get())
        cx = float(entry_cx.get())/100.0
        mu = float(entry_mut.get())/100.0
        d = int(entry_delay.get())
    except:
        p, cx, mu, d = 20, 0.8, 0.1, 600
    if p < 2: p = 2
    if d < 10: d = 10
    pop_size, crossover_rate, mutation_rate, delay_ms = p, cx, mu, d
    init_population()
    running = True
    btn_start.config(text="Đang chạy")
    auto_step()

def auto_step():
    global running
    if not running:
        return
    run_generation()
    costs, _ = evaluate_population()
    if 0 in costs:
        running = False
        btn_start.config(text="Đã tìm được nghiệm (dừng)")
        return
    root.after(delay_ms, auto_step)

def stop_run():
    global running
    running = False
    btn_start.config(text="Bắt đầu")

def step_once():
    global pop_size, crossover_rate, mutation_rate
    try:
        p = int(entry_pop.get())
        cx = float(entry_cx.get())/100.0
        mu = float(entry_mut.get())/100.0
    except:
        p, cx, mu = pop_size, crossover_rate, mutation_rate
    if p != pop_size:
        pop_size = p
        init_population()
    crossover_rate = cx
    mutation_rate = mu
    run_generation()

btn_start.config(command=start_run)
btn_stop.config(command=stop_run)
btn_step.config(command=step_once)

delay_ms = int(entry_delay.get())
init_population()
root.minsize(900, 720)
root.mainloop()
