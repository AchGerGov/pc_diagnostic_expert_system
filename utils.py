# utils.py
import tkinter as tk

class RoundedButton(tk.Canvas):
    """
    Кастомная кнопка с закруглёнными углами и эффектами наведения.
    """
    def __init__(self, master, text, command=None, width=120, height=40, corner_radius=10,
                 bg_color="#B0BEC5", hover_color="#CFD8DC", text_color="#1A237E", font_size=12):
        super().__init__(master, width=width, height=height, highlightthickness=0, bg=master["bg"])
        self.command = command
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.corner_radius = corner_radius
        self.width = width
        self.height = height
        self.font = ("Consolas", font_size, "bold")
        self.text = text
        self.normal_bg = bg_color

        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)

        self.draw_button(bg_color)

    def darker_color(self, color, factor=0.8):
        r, g, b = self.winfo_rgb(color)
        r = int(r * factor / 256)
        g = int(g * factor / 256)
        b = int(b * factor / 256)
        return f"#{r:02x}{g:02x}{b:02x}"

    def draw_button(self, color):
        self.delete("all")
        x0, y0 = 0, 0
        x1, y1 = self.width, self.height
        r = self.corner_radius
        points = [x0+r, y0, x1-r, y0, x1, y0, x1, y0+r, x1, y1-r,
                  x1, y1, x1-r, y1, x0+r, y1, x0, y1, x0, y1-r, x0, y0+r, x0, y0]
        self.create_polygon(points, fill=color, outline=self.darker_color(color, 0.8),
                            width=2, smooth=True)
        self.create_text(self.width//2, self.height//2, text=self.text,
                         fill=self.text_color, font=self.font)

    def on_enter(self, event):
        self.draw_button(self.hover_color)
        self.scale("all", self.width//2, self.height//2, 1.05, 1.05)

    def on_leave(self, event):
        self.scale("all", self.width//2, self.height//2, 1/1.05, 1/1.05)
        self.draw_button(self.normal_bg)

    def on_click(self, event):
        if self.command:
            self.command()
