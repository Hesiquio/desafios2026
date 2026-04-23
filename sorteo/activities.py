# =============================================================================
#  sorteo/activities.py
#  Control de entregas y ranking de actividades
# =============================================================================

import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from .constants import (
    BG_MAIN, BG_CARD, BG_HEADER, BTN_PRIMARY, BTN_HOVER,
    TEXT_DARK, TEXT_LIGHT, TEXT_MUTED, ACCENT_GOLD
)

class ActivitiesMixin:
    """Mixin para la gestión de actividades y control de entregas."""

    def show_activities_menu(self):
        """Pantalla principal de gestión de actividades."""
        self._clear()

        hdr = tk.Frame(self.container, bg=BG_HEADER, pady=12)
        hdr.pack(fill="x")
        tk.Label(hdr, text="📋  CONTROL DE ACTIVIDADES",
                 font=self.f_header, bg=BG_HEADER, fg=TEXT_LIGHT).pack()

        body = tk.Frame(self.container, bg=BG_MAIN, padx=30, pady=20)
        body.pack(fill="both", expand=True)

        # Botón nueva actividad
        self._make_btn(body, "➕  Nueva Actividad", self._create_activity_dialog,
                       color="#06D6A0", px=20, py=10).pack(pady=(0, 20))

        tk.Label(body, text="Actividades Recientes:",
                 font=self.f_title, bg=BG_MAIN, fg=TEXT_DARK).pack(anchor="w")

        # Lista de actividades
        canvas = tk.Canvas(body, bg=BG_MAIN, highlightthickness=0)
        scrollbar = tk.Scrollbar(body, command=canvas.yview)
        sf = tk.Frame(canvas, bg=BG_MAIN)

        sf.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=sf, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        activities = self.db.get_activities()

        if not activities:
            tk.Label(sf, text="No hay actividades creadas.",
                     font=self.f_body, bg=BG_MAIN, fg=TEXT_MUTED).pack(pady=20)
        else:
            for aid, name, created in activities:
                card = tk.Frame(sf, bg=BG_CARD, highlightbackground="#DEE2E6",
                                highlightthickness=1, padx=15, pady=10)
                card.pack(fill="x", pady=5)

                info = tk.Frame(card, bg=BG_CARD)
                info.pack(side="left", fill="both", expand=True)
                tk.Label(info, text=name, font=self.f_name, bg=BG_CARD, fg=TEXT_DARK).pack(anchor="w")
                tk.Label(info, text=f"Iniciada: {created}", font=self.f_small, bg=BG_CARD, fg=TEXT_MUTED).pack(anchor="w")

                btn_frame = tk.Frame(card, bg=BG_CARD)
                btn_frame.pack(side="right")
                
                self._make_btn(btn_frame, "Registrar Entregas", lambda a=aid, n=name: self.show_submission_screen(a, n),
                               color=BTN_PRIMARY, px=10, py=5, font=self.f_small).pack(side="left", padx=2)
                
                self._make_btn(btn_frame, "Ver Ranking", lambda a=aid, n=name: self.show_activity_ranking(a, n),
                               color="#FF9F1C", px=10, py=5, font=self.f_small).pack(side="left", padx=2)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self._make_btn(body, "← Volver al Menú", self.show_main_menu,
                       color="#6C757D", hover="#495057", px=20, py=8, font=self.f_body).pack(pady=10)

    def _create_activity_dialog(self):
        name = simpledialog.askstring("Nueva Actividad", "¿Nombre de la tarea/actividad?")
        if name:
            aid = self.db.create_activity(name)
            self.show_activities_menu()

    def show_submission_screen(self, activity_id, activity_name):
        """Pantalla para marcar quién va entregando en tiempo real."""
        self._clear()

        hdr = tk.Frame(self.container, bg=BG_HEADER, pady=12)
        hdr.pack(fill="x")
        tk.Label(hdr, text=f"📥  REGISTRANDO: {activity_name}",
                 font=self.f_title, bg=BG_HEADER, fg=ACCENT_GOLD).pack()

        body = tk.Frame(self.container, bg=BG_MAIN, padx=30, pady=20)
        body.pack(fill="both", expand=True)

        tk.Label(body, text="Haz clic en el nombre del alumno para marcar la entrega:",
                 font=self.f_body, bg=BG_MAIN, fg=TEXT_DARK).pack(pady=(0, 15))

        # Usar la lista de alumnos actuales o cargar del leaderboard
        recent_students = self.students if self.students else [s[0] for s in self.db.get_leaderboard(100)]
        
        if not recent_students:
            tk.Label(body, text="No hay alumnos cargados. Inicia un sorteo primero.",
                     font=self.f_body, bg=BG_MAIN, fg="#EF233C").pack()
        else:
            # Grid de botones de alumnos
            grid_frame = tk.Frame(body, bg=BG_MAIN)
            grid_frame.pack(fill="both", expand=True)
            
            # Obtener ya entregados para deshabilitar
            already_submitted = [r[0] for r in self.db.get_activity_ranking(activity_id)]

            for i, student in enumerate(sorted(recent_students)):
                btn_color = "#6C757D" if student in already_submitted else BTN_PRIMARY
                btn_text = f"✅ {student}" if student in already_submitted else student
                
                btn = self._make_btn(grid_frame, btn_text, None, color=btn_color)
                btn.config(command=lambda b=btn, s=student: self._mark_submission(activity_id, s, b))
                
                if student in already_submitted:
                    btn.config(state="disabled")
                
                btn.grid(row=i // 3, column=i % 3, sticky="nsew", padx=5, pady=5)
            
            for j in range(3): grid_frame.columnconfigure(j, weight=1)

        self._make_btn(body, "Ver Ranking Actual", lambda: self.show_activity_ranking(activity_id, activity_name),
                       color="#FF9F1C", px=20, py=10).pack(pady=10)
        
        self._make_btn(body, "← Volver", self.show_activities_menu,
                       color="#6C757D", hover="#495057", px=20, py=8).pack()

    def _mark_submission(self, activity_id, student_name, button):
        pos = self.db.register_submission(activity_id, student_name)
        if pos:
            button.config(text=f"✅ #{pos} {student_name}", state="disabled", bg="#6C757D")
            # Opcional: Feedback visual de éxito
        else:
            messagebox.showinfo("Info", "Este alumno ya ha entregado.")

    def show_activity_ranking(self, activity_id, activity_name):
        """Muestra el orden de entrega de una actividad."""
        self._clear()

        hdr = tk.Frame(self.container, bg=BG_HEADER, pady=12)
        hdr.pack(fill="x")
        tk.Label(hdr, text=f"🏆  RANKING: {activity_name}",
                 font=self.f_title, bg=BG_HEADER, fg=ACCENT_GOLD).pack()

        body = tk.Frame(self.container, bg=BG_MAIN, padx=30, pady=20)
        body.pack(fill="both", expand=True)

        ranking = self.db.get_activity_ranking(activity_id)

        if not ranking:
            tk.Label(body, text="Aún no hay entregas registradas.",
                     font=self.f_body, bg=BG_MAIN, fg=TEXT_MUTED).pack(pady=20)
        else:
            # Tabla de ranking
            for student, pos, time in ranking:
                card = tk.Frame(body, bg=BG_CARD, highlightbackground=BTN_PRIMARY if pos <= 3 else "#DEE2E6",
                                highlightthickness=2 if pos <= 3 else 1, padx=15, pady=8)
                card.pack(fill="x", pady=4)
                
                medal = "🥇" if pos == 1 else "🥈" if pos == 2 else "🥉" if pos == 3 else f"#{pos}"
                tk.Label(card, text=f"{medal}  {student}", font=self.f_name, bg=BG_CARD, fg=TEXT_DARK).pack(side="left")
                tk.Label(card, text=f"Hora: {time.split(' ')[1]}", font=self.f_small, bg=BG_CARD, fg=TEXT_MUTED).pack(side="right")

        btn_frame = tk.Frame(body, bg=BG_MAIN, pady=15)
        btn_frame.pack()
        
        self._make_btn(btn_frame, "Continuar Registrando", lambda: self.show_submission_screen(activity_id, activity_name),
                       color=BTN_PRIMARY, px=20, py=10).pack(side="left", padx=5)
        
        self._make_btn(btn_frame, "← Volver", self.show_activities_menu,
                       color="#6C757D", px=20, py=10).pack(side="left", padx=5)
