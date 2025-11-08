import tkinter as tk

window = tk.Tk()
window.title("Traffic Signals on Four Roads")
window.geometry("950x700")

canvas = tk.Canvas(window, width=900, height=650, bg='white')
canvas.pack()

SIGNAL_COLORS = ['red', 'yellow', 'green']
SIGNAL_POSITIONS = [(90, 40), (270, 40), (450, 40), (630, 40)]
signal_width = 80
light_radius = 35
vertical_separation = 50
road_length = 340
road_width = 60

# Store all ovals for each signal
signals = []  # Each element: [red_oval, yellow_oval, green_oval]

def draw_traffic_signal(x, y):
    # Signal box
    rect_height = light_radius * 6
    canvas.create_rectangle(x, y, x + signal_width, y + rect_height, fill='black', outline='black')
    xc = x + signal_width // 2
    spacing = light_radius // 2
    ovals = []
    for idx, color in enumerate(SIGNAL_COLORS):
        cy = y + spacing + idx * (light_radius * 2 + spacing)
        oval = canvas.create_oval(
            xc - light_radius, cy - light_radius,
            xc + light_radius, cy + light_radius,
            fill='grey', outline='black', width=3
        )
        ovals.append(oval)
    return ovals, x + signal_width // 2, y + rect_height + vertical_separation

def draw_road(cx, top, road_index):
    bottom = top + road_length
    canvas.create_rectangle(
        cx - road_width // 2, top,
        cx + road_width // 2, bottom,
        fill='#272727', outline='#272727'
    )
    # Draw road label in white, centered
    canvas.create_text(cx, top + road_length // 2, text=f'road {road_index}', font=('Arial', 15), fill="white")

for i, (x, y) in enumerate(SIGNAL_POSITIONS):
    ovals, mid_x, road_start_y = draw_traffic_signal(x, y)
    draw_road(mid_x, road_start_y, i + 1)
    signals.append(ovals)

current_signal = [0]  # Using list for mutability in nested functions
current_light = [0]   # Same reason
TIMINGS = [20000, 20000, 20000]  # 20s each

def reset_all():
    for s in signals:
        for oval in s:
            canvas.itemconfig(oval, fill='grey')

def run_signals():
    reset_all()
    active = current_signal[0]
    light = current_light[0]
    # Light up appropriate oval
    canvas.itemconfig(signals[active][light], fill=SIGNAL_COLORS[light])
    next_light = light + 1
    if next_light < 3:
        current_light[0] = next_light
        window.after(TIMINGS[light], run_signals)
    else:
        current_light[0] = 0
        current_signal[0] = (active + 1) % 4
        window.after(TIMINGS[2], run_signals)

run_signals()
window.mainloop()
