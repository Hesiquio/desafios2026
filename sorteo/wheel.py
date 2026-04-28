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

# Valores y colores de las secciones de la ruleta (Puntos)
WHEEL_POINTS   = [10, 20, 50, 100, 150, 200, 50, 10]
WHEEL_COLORS_P = ["#FFADAD", "#FFD6A5", "#FDFFB6", "#CAFFBF", "#9BF6FF", "#A0C4FF", "#BDB2FF", "#FFC6FF"]


class WheelMixin:
    """Mixin con la pantalla y la animación de la ruleta de puntos."""

    # =========================================================================
    #  PANTALLA 3 — RULETA DE PUNTOS
    # =========================================================================

    def show_wheel_screen(self, mode="student"):
        """
        Muestra la pantalla de la ruleta.
        modos: "student" (seleccionar quién) o "points" (cuánto gana)
        """
        if not hasattr(self, 'wheel_mode'):
            self.wheel_mode = mode
        else:
            self.wheel_mode = mode

        # Si no hay estudiantes cargados y estamos en modo student, intentar cargar el último grupo
        if not self.students and self.wheel_mode == "student":
            groups = self.db.get_groups()
            if groups:
                data = self.db.load_group(groups[0][0])
                self.students = data['students']
                self.current_group_name = data['name']
            else:
                messagebox.showinfo("Sin datos", "Por favor, crea o selecciona un grupo primero.")
                self.show_main_menu()
                return

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
        
        # Pre-seleccionar si ya tenemos un ganador del primer giro
        if hasattr(self, 'selected_student') and self.selected_student:
            try:
                idx = all_students.index(self.selected_student)
                self.student_listbox.select_set(idx)
                self.student_listbox.see(idx)
            except ValueError:
                if all_students: self.student_listbox.select_set(0)
        elif all_students:
            self.student_listbox.select_set(0)

        # ── Panel derecho: tómbola de texto ───────────────────────────────
        right_panel = tk.Frame(body, bg=BG_MAIN)
        right_panel.pack(side="right", fill="both", expand=True)

        title_text = "🎯 ¡Selecciona al Estudiante!" if self.wheel_mode == "student" else "💰 ¡Gira por los Puntos!"
        tk.Label(right_panel, text=title_text,
                 font=self.f_title, bg=BG_MAIN, fg=TEXT_DARK).pack(pady=(0, 15))

        # Marco para el "Slot" / Tómbola
        slot_frame = tk.Frame(right_panel, bg="#212529", padx=40, pady=60,
                              highlightbackground=ACCENT_GOLD, highlightthickness=3)
        slot_frame.pack(pady=20, fill="x")

        result_text = "—"
        if hasattr(self, 'selected_student') and self.selected_student:
            result_text = self.selected_student
        
        self.wheel_result_lbl = tk.Label(
            slot_frame, text=result_text,
            font=tkfont.Font(family="Helvetica", size=48, weight="bold"),
            bg="#212529", fg=ACCENT_GOLD,
            wraplength=500
        )
        self.wheel_result_lbl.pack()

        btn_frame = tk.Frame(right_panel, bg=BG_MAIN)
        btn_frame.pack(fill="x", pady=20)

        btn_text = "🎡   GIRAR PARA ELEGIR ALUMNO" if self.wheel_mode == "student" else "💰   GIRAR PARA GANAR PUNTOS"
        self.btn_spin_wheel = self._make_btn(
            btn_frame, btn_text,
            self.spin_wheel, color=BTN_REVEAL, hover=BTN_REVEAL_H,
            px=40, py=14, font=self.f_btn,
        )
        self.btn_spin_wheel.pack(fill="x")

        # ── Top rápido (Específico del grupo si hay uno cargado) ──────────
        tk.Label(body, text=f"🏆 Ranking: {getattr(self, 'current_group_name', 'Global')}",
                 font=self.f_name, bg=BG_MAIN, fg=TEXT_DARK).pack(pady=(20, 10))

        if self.students:
            lb_quick = self.db.get_group_leaderboard(self.students)[:10]
        else:
            lb_quick = self.db.get_leaderboard(10)
        if lb_quick:
            medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
            grid_lb = tk.Frame(body, bg=BG_MAIN)
            grid_lb.pack()
            
            for rank, (name, points, _) in enumerate(lb_quick, 1):
                row = (rank-1) // 5
                col = (rank-1) % 5
                medal = medals[rank-1] if rank <= 10 else f"#{rank}"
                tk.Label(grid_lb,
                         text=f"{medal} {name}\n{points} pts",
                         font=self.f_small, bg=BG_CARD, fg=TEXT_DARK,
                         padx=10, pady=5, width=15, relief="flat",
                         highlightbackground="#DEE2E6", highlightthickness=1
                         ).grid(row=row, column=col, padx=4, pady=4)

        tk.Frame(body, height=0, bg=BG_MAIN).pack(pady=10)
        footer_btns = tk.Frame(body, bg=BG_MAIN)
        footer_btns.pack()

        self._make_btn(footer_btns, "🔄 Cambiar Grupo",
                       self._pick_group_for_wheel,
                       color="#4361EE", px=20, py=8,
                       font=self.f_body).pack(side="left", padx=5)

        self._make_btn(footer_btns, "← Volver al Menú",
                       self.show_main_menu,
                       color="#6C757D", hover="#495057", px=20, py=8,
                       font=self.f_body).pack(side="left", padx=5)

    def _show_wheel_from_sorteo(self):
        """Navega a la ruleta desde la pantalla de fin de sorteo."""
        self.show_wheel_screen()

    # =========================================================================
    #  DIBUJO Y ANIMACIÓN
    # =========================================================================

    def _draw_wheel(self):
        """No se usa en este modo de tómbola de texto."""
        pass

    def spin_wheel(self):
        """Gira la tómbola según el modo actual."""
        if self.wheel_mode == "student":
            if not self.students:
                messagebox.showwarning("Error", "No hay estudiantes en el grupo.")
                return
            
            # Preparar datos de tómbola
            self.wheel_sections_data = self.students[:]
            
            self.btn_spin_wheel.config(state="disabled", bg="#ADB5BD")
            winner = random.choice(self.students)
            self._animate_wheel_spin(winner, 30)
        else:
            # Modo puntos
            selection = self.student_listbox.curselection()
            if not selection:
                messagebox.showwarning("Advertencia", "Selecciona un estudiante primero.")
                return

            self.wheel_sections_data = WHEEL_POINTS
            
            self.btn_spin_wheel.config(state="disabled", bg="#ADB5BD")
            points = random.choice(WHEEL_POINTS)
            self._animate_wheel_spin(points, 30)

    def _animate_wheel_spin(self, final_result, frame):
        """Anima el cambio de nombres/puntos tipo tómbola."""
        if frame > 0:
            # Mostrar valores aleatorios durante el giro
            random_val = random.choice(self.wheel_sections_data)
            self.wheel_result_lbl.config(text=str(random_val), fg=ACCENT_GOLD)
            
            # Frenado progresivo
            delay = int(20 + (30 - frame) ** 1.5)
            self.after(delay, self._animate_wheel_spin, final_result, frame - 1)
        else:
            # Resultado final con efecto de parpadeo
            self.wheel_result_lbl.config(text=str(final_result), fg="#00FF00") # Verde para el ganador
            
            if self.wheel_mode == "student":
                self.selected_student = final_result
                self.after(2000, lambda: self.show_wheel_screen(mode="points"))
            else:
                selection = self.student_listbox.curselection()
                student = self.student_listbox.get(selection[0])
                self.db.add_points(student, final_result)
                
                self.after(1000, lambda: (
                    messagebox.showinfo("¡Puntos!", f"¡{student} ha ganado {final_result} puntos!"),
                    setattr(self, 'selected_student', None),
                    self.show_wheel_screen(mode="student")
                ))
