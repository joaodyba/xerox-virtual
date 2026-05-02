import tkinter as tk
import pyautogui
import time
from PIL import Image
import mss
import numpy as np
import keyboard
import img2pdf
import os

# ==============================
# CONFIG
# ==============================

CHANGE_THRESHOLD = 5
CHECK_INTERVAL = 0.4
TIMEOUT = 10

# ==============================
# SNIPPING TOOL
# ==============================

class SnippingTool:
    def __init__(self):
        self.start_x = None
        self.start_y = None
        self.temp_rect = None
        self.text = None
        self.region = None

        self.root = tk.Toplevel()
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-alpha", 0.25)
        self.root.attributes("-topmost", True)
        self.root.overrideredirect(True)

        self.canvas = tk.Canvas(self.root, bg="black", cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)

        self.root.bind("<Escape>", lambda e: self.cancel())
        self.root.bind("<Return>", lambda e: self.confirm())

    def cancel(self):
        self.region = None
        self.root.destroy()

    def confirm(self):
        if self.temp_rect:
            x1, y1, x2, y2 = self.canvas.coords(self.temp_rect)
            self.region = {
                "left": int(min(x1, x2)),
                "top": int(min(y1, y2)),
                "width": int(abs(x2 - x1)),
                "height": int(abs(y2 - y1)),
            }
        self.root.destroy()

    def on_press(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def on_drag(self, event):
        if self.temp_rect:
            self.canvas.delete(self.temp_rect)
        if self.text:
            self.canvas.delete(self.text)

        x1, y1 = self.start_x, self.start_y
        x2, y2 = event.x, event.y

        self.temp_rect = self.canvas.create_rectangle(
            x1, y1, x2, y2,
            outline="white", width=2
        )

        w, h = abs(x2 - x1), abs(y2 - y1)

        self.text = self.canvas.create_text(
            x1 + 80, y1 - 10,
            text=f"{w} x {h}",
            fill="white",
            font=("Arial", 12, "bold")
        )

    def run(self):
        self.root.grab_set()
        self.root.focus_force()
        self.root.wait_window()
        return self.region


# ==============================
# GUI PRINCIPAL
# ==============================

class ControlGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Xerox Automático")
        self.root.geometry("320x300")
        self.root.attributes("-topmost", True)

        self.region = None
        self.click_pos = None
        self.result = None

        tk.Label(self.root, text="Xerox Automático", font=("Arial", 14, "bold")).pack(pady=10)

        self.area_label = tk.Label(self.root, text="Área: não selecionada")
        self.area_label.pack()

        tk.Button(self.root, text="Selecionar área", command=self.select_area).pack(pady=5)

        self.button_label = tk.Label(self.root, text="Botão: não definido")
        self.button_label.pack()

        tk.Button(self.root, text="Capturar botão", command=self.capture_button).pack(pady=5)

        tk.Label(self.root, text="Quantidade de páginas:").pack()
        self.pages_entry = tk.Entry(self.root)
        self.pages_entry.pack()

        tk.Button(self.root, text="Iniciar", command=self.start).pack(pady=15)

    def select_area(self):
        self.root.withdraw()
        selector = SnippingTool()
        self.region = selector.run()
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()

        self.area_label.config(text="Área OK" if self.region else "Área cancelada")

    def capture_button(self):
        self.root.withdraw()
        time.sleep(3)
        self.click_pos = pyautogui.position()
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()

        self.button_label.config(text=f"Botão: {self.click_pos}")

    def start(self):
        try:
            pages = int(self.pages_entry.get())

            if not self.region or not self.click_pos:
                return

            self.result = {
                "region": self.region,
                "click": self.click_pos,
                "pages": pages
            }

            self.root.destroy()
        except:
            pass

    def run(self):
        self.root.mainloop()
        return self.result


# ==============================
# DETECÇÃO DE ESTABILIDADE
# ==============================

def image_difference(img1, img2):
    arr1 = np.array(img1)
    arr2 = np.array(img2)
    return (np.abs(arr1 - arr2) > 10).mean() * 100


def wait_for_stable(sct, region, previous):
    start = time.time()
    last = previous
    stable = 0

    while True:
        if keyboard.is_pressed("esc"):
            return None

        shot = sct.grab(region)
        img = Image.frombytes("RGB", shot.size, shot.rgb)

        diff = image_difference(last, img)

        if diff > CHANGE_THRESHOLD:
            stable = 0
            last = img
        else:
            stable += 1

        if stable >= 3:
            return img

        if time.time() - start > TIMEOUT:
            return img

        time.sleep(CHECK_INTERVAL)


# ==============================
# MAIN
# ==============================

gui = ControlGUI()
config = gui.run()

if not config:
    exit()

region = config["region"]
click_x, click_y = config["click"]
repeticoes = config["pages"]

sct = mss.mss()
screenshots = []

time.sleep(2)

first = sct.grab(region)
prev = Image.frombytes("RGB", first.size, first.rgb)
screenshots.append(prev)

for i in range(repeticoes):
    if keyboard.is_pressed("esc"):
        break

    pyautogui.moveTo(click_x, click_y)
    pyautogui.click()

    img = wait_for_stable(sct, region, prev)
    if img is None:
        break

    if image_difference(prev, img) < 1:
        continue

    screenshots.append(img)
    prev = img

# ==============================
# PDF COM IMG2PDF
# ==============================

temp_files = []

for i, img in enumerate(screenshots):
    path = f"temp_{i}.png"
    img.save(path)
    temp_files.append(path)

with open("resultado.pdf", "wb") as f:
    f.write(img2pdf.convert(temp_files))

for f in temp_files:
    os.remove(f)

print("PDF gerado com sucesso!")