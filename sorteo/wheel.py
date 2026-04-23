# =============================================================================
#  sorteo/wheel.py
#  Pantalla de la ruleta de puntos
# =============================================================================

import math
import random
import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox

from .constants import (
    BG_MAIN, BG_CARD, BG_HEADER,
    BTN_PRIMARY, BTN_REVEAL, BTN_REVEAL_H,
    TEXT_DARK, TEXT_LIGHT, TEXT_MUTED, ACCENT_GOLD,
    SLOT_TEXT, TEAM_COLORS,
)

# Valores y colores de las secciones de la ruleta
WHEEL_SECTIONS = [10, 25, 50, 100, 200, 50]
WHEEL_COLORS   = TEAM_COLORS[:len(WHEEL_SECTIONS)]


class WheelMixin:
    """Mixin con la pantalla y la animación de la ruleta de puntos."""

    # =========================================================================
    #  PANTALLA 3 — RULETA DE PUNTOS
    # =========================================================================

    def show_wheel_screen(self):
        """Muestra la pantalla de la ruleta para ganar puntos."""
        self._clear()

        hdr = tk.Frame(self.container, bg=BG_HEADER, pady=12)
        hdr.pack(fill="x")
        tk.Label(hdr, text="🎡  RULETA DE PUNTOS",
                 font=self.f_header, bg=BG_HEADER, fg=ACCENT_GOLD).pack()

        body = tk.Frame(self.container, bg=BG_MAIN, padx=30, pady=20)
        body.pack(fill="both", expand=True)

        # ── Panel izquierdo: lista de estudiantes ─────────────────────────
        left_panel = tk.Frame(body, bg=BG_MAIN, width=250)
        left_panel.pack(side="left", fill="both", padx=(0, 20))

        tk.Label(left_panel, text="Selecciona un Estudiante:",
                 font=self.f_title, bg=BG_MAIN, fg=TEXT_DARK).pack(pady=10)

        recent_students = set(self.students) if self.students else set()
        lb_data = self.db.get_leaderboard(100)
        all_students = list(recent_students) + [
            s[0] for s in lb_data if s[0] not in recent_students
        ]

        lb_frame = tk.Frame(left_panel, bg=BG_CARD,
                            highlightbackground="#CED4DA", highlightthickness=1)
        lb_frame.pack(fill="both", expand=True, pady=(0, 10))

        scrollbar = tk.Scrollbar(lb_frame)
        scrollbar.pack(side="right", fill="y")

        self.student_listbox = tk.Listbox(
            lb_frame, yscrollcommand=scrollbar.set,
            font=self.f_body, bg=BG_CARD, fg=TEXT_DARK,
            relief="flat", bd=3, activestyle="none",
            selectmode="single", selectforeground=TEXT_LIGHT,
            selectbackground=BTN_PRIMARY,
        )
        self.student_listbox.pack(fill="both", expand=True)
        scrollbar.config(command=self.student_listbox.yview)

        for student in all_students[:30]:
            self.student_listbox.insert("end", student)
        if all_students:
            self.student_listbox.select_set(0)

        # ── Panel derecho: ruleta visual ──────────────────────────────────
        right_panel = tk.Frame(body, bg=BG_MAIN)
        right_panel.pack(side="right", fill="both", expand=True)

        tk.Label(right_panel, text="🎯 Gira la Ruleta",
                 font=self.f_title, bg=BG_MAIN, fg=TEXT_DARK).pack(pady=(0, 15))

        self.wheel_canvas = tk.Canvas(
            right_panel, width=300, height=300,
            bg=BG_CARD, highlightbackground="#DEE2E6", highlightthickness=1,
        )
        self.wheel_canvas.pack(pady=(0, 20))
        self._draw_wheel()

        self.wheel_result_frame = tk.Frame(right_panel, bg=BG_MAIN)
        self.wheel_result_frame.pack(fill="x", pady=10)

        tk.Label(self.wheel_result_frame, text="Puntos obtenidos:",
                 font=self.f_body, bg=BG_MAIN, fg=TEXT_DARK).pack()

        self.wheel_result_lbl = tk.Label(
            self.wheel_result_frame, text="—",
            font=tkfont.Font(family="Helvetica", size=32, weight="bold"),
            bg=BG_MAIN, fg=ACCENT_GOLD,
        )
        self.wheel_result_lbl.pack(pady=5)

        btn_frame = tk.Frame(right_panel, bg=BG_MAIN)
        btn_frame.pack(fill="x", pady=10)

        self.btn_spin_wheel = self._make_btn(
            btn_frame, "🎪   GIRAR RULETA",
            self.spin_wheel, color=BTN_REVEAL, hover=BTN_REVEAL_H,
            px=40, py=14, font=self.f_btn,
        )
        self.btn_spin_wheel.pack(fill="x")

        # ── Top 5 rápido ──────────────────────────────────────────────────
        tk.Label(body, text="🏆 Top 5",
                 font=self.f_name, bg=BG_MAIN, fg=TEXT_DARK).pack(pady=(20, 10))

        lb_quick = self.db.get_leaderboard(5)
        if lb_quick:
            medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]
            for rank, (name, points, _) in enumerate(lb_quick, 1):
                tk.Label(body,
                         text=f"{medals[rank - 1]}  {name}  →  {points} pts",
                         font=self.f_body, bg=BG_MAIN, fg=TEXT_DARK).pack()

        tk.Frame(body, height=0, bg=BG_MAIN).pack(pady=10)
        self._make_btn(body, "← Volver al Menú",
                       self.show_main_menu,
                       color="#6C757D", hover="#495057", px=20, py=8,
                       font=self.f_body).pack()

    def _show_wheel_from_sorteo(self):
        """Navega a la ruleta desde la pantalla de fin de sorteo."""
        self.show_wheel_screen()

    # =========================================================================
    #  DIBUJO Y ANIMACIÓN
    # =========================================================================

    def _draw_wheel(self):
        """Dibuja la ruleta estática con las secciones configuradas."""
        canvas = self.wheel_canvas
        canvas.delete("all")

        cx, cy = 150, 150
        radius = 120
        section_angle = 360 / len(WHEEL_SECTIONS)
        angle = 0

        self.wheel_sections = []

        for i, (points, color) in enumerate(zip(WHEEL_SECTIONS, WHEEL_COLORS)):
            angle_end = angle + section_angle

            # Polígono aproximado de cada sector
            x1 = cx + radius * 0.2 * math.cos(math.radians(angle))
            y1 = cy + radius * 0.2 * math.sin(math.radians(angle))
            x2 = cx + radius * math.cos(math.radians(angle))
            y2 = cy + radius * math.sin(math.radians(angle))
            x3 = cx + radius * math.cos(math.radians(angle_end))
            y3 = cy + radius * math.sin(math.radians(angle_end))
            x4 = cx + radius * 0.2 * math.cos(math.radians(angle_end))
            y4 = cy + radius * 0.2 * math.sin(math.radians(angle_end))

            arc_id = canvas.create_polygon(
                [x1, y1, x2, y2, x3, y3, x4, y4],
                fill=color, outline="#FFFFFF", width=2,
            )

            text_angle = angle + section_angle / 2
            text_x = cx + radius * 0.6 * math.cos(math.radians(text_angle))
            text_y = cy + radius * 0.6 * math.sin(math.radians(text_angle))
            canvas.create_text(
                text_x, text_y, text=str(points),
                font=tkfont.Font(family="Helvetica", size=16, weight="bold"),
                fill=TEXT_LIGHT,
            )

            self.wheel_sections.append((arc_id, points))
            angle = angle_end

        # Círculo central decorativo
        canvas.create_oval(cx - 20, cy - 20, cx + 20, cy + 20,
                           fill=BG_HEADER, outline=ACCENT_GOLD, width=3)
        canvas.create_text(cx, cy, text="🎯",
                           font=tkfont.Font(family="Helvetica", size=20))

    def spin_wheel(self):
        """Gira la ruleta y asigna puntos al estudiante seleccionado."""
        selection = self.student_listbox.curselection()
        if not selection:
            messagebox.showwarning("Advertencia", "Selecciona un estudiante primero.")
            return

        student = self.student_listbox.get(selection[0])
        self.btn_spin_wheel.config(state="disabled", bg="#ADB5BD")

        points = random.choice(WHEEL_SECTIONS)
        self._animate_wheel_spin(student, points, 15)

    def _animate_wheel_spin(self, student, points, frame):
        """Anima el giro de la ruleta (cuenta regresiva de frames)."""
        if frame > 0:
            random_pts = random.choice(WHEEL_SECTIONS)
            self.wheel_result_lbl.config(text=str(random_pts), fg=SLOT_TEXT)
            delay = int(20 + frame * 2)
            self.after(delay, self._animate_wheel_spin, student, points, frame - 1)
        else:
            self.wheel_result_lbl.config(text=str(points), fg=ACCENT_GOLD)
            self.db.add_points(student, points)
            self.wheel_canvas.delete("all")
            self._draw_wheel()
            self.after(1000, lambda: (
                self.btn_spin_wheel.config(state="normal", bg=BTN_REVEAL),
                self.show_wheel_screen(),
            ))
