# =============================================================================
#  sorteo_equipos.py
#  Herramienta visual de sorteo de equipos — Estilo Champions League
#  Autor  : Desarrollador Senior Python/GUI
#  Librerías: SOLO librería estándar (tkinter, random, math)
# =============================================================================

import tkinter as tk
from tkinter import font as tkfont
import random
import math

# ─────────────────────────────────────────────────────────────────────────────
#  PALETA DE COLORES  (Flat Design Moderno)
# ─────────────────────────────────────────────────────────────────────────────
BG_MAIN      = "#F0F4F8"   # Fondo general (gris azulado muy claro)
BG_CARD      = "#FFFFFF"   # Fondo de tarjetas
BG_HEADER    = "#1A1A2E"   # Header oscuro premium (azul medianoche)
BTN_PRIMARY  = "#4361EE"   # Botón principal (azul vibrante)
BTN_HOVER    = "#3A0CA3"   # Hover del botón principal
BTN_REVEAL   = "#F72585"   # Botón revelar (magenta impactante)
BTN_REVEAL_H = "#B5179E"   # Hover revelar
TEXT_DARK    = "#2B2D42"   # Texto principal
TEXT_LIGHT   = "#FFFFFF"   # Texto sobre fondos oscuros
TEXT_MUTED   = "#8D99AE"   # Texto secundario / placeholder
ACCENT_GOLD  = "#FFD60A"   # Dorado para el momento del clímax
SLOT_BG      = "#16213E"   # Fondo del área de tómbola (azul muy oscuro)
SLOT_TEXT    = "#4CC9F0"   # Color del nombre durante la animación (cian)

# Colores temáticos para cada equipo (hasta 8 equipos)
TEAM_COLORS = [
    "#4361EE",  # Azul Champions
    "#F72585",  # Magenta
    "#06D6A0",  # Verde esmeralda
    "#FF9F1C",  # Naranja
    "#7B2FBE",  # Púrpura
    "#EF233C",  # Rojo
    "#3A86FF",  # Azul cielo
    "#FB5607",  # Naranja rojo
]

TEAM_EMOJIS = ["⚽", "🏆", "🔥", "⭐", "💎", "🚀", "🎯", "👑"]


# =============================================================================
#  CLASE PRINCIPAL
# =============================================================================
class SorteoApp(tk.Tk):
    """
    Ventana raíz de la aplicación. Gestiona el estado global y la navegación
    entre la pantalla de configuración y la pantalla de sorteo.
    """

    def __init__(self):
        super().__init__()
        self.title("⚽ Sorteo de Equipos — Champions Style")
        self.geometry("1050x720")
        self.minsize(850, 620)
        self.configure(bg=BG_MAIN)
        self.resizable(True, True)

        # ── Definir fuentes una sola vez ──────────────────────────────────
        self.f_header = tkfont.Font(family="Helvetica", size=22, weight="bold")
        self.f_title  = tkfont.Font(family="Helvetica", size=14, weight="bold")
        self.f_body   = tkfont.Font(family="Helvetica", size=11)
        self.f_slot   = tkfont.Font(family="Helvetica", size=34, weight="bold")
        self.f_name   = tkfont.Font(family="Helvetica", size=12, weight="bold")
        self.f_btn    = tkfont.Font(family="Helvetica", size=13, weight="bold")
        self.f_small  = tkfont.Font(family="Helvetica", size=9)

        # ── Estado de la aplicación ───────────────────────────────────────
        self.students      = []   # Lista mezclada de alumnos
        self.teams         = []   # Lista de listas [equipo1[], equipo2[], ...]
        self.num_teams     = 0    # Número de equipos configurados
        self.student_index = 0   # Puntero al próximo alumno por asignar
        self.assign_index  = 0   # Puntero al próximo equipo que recibirá un alumno
        self.is_animating  = False  # Bandera que evita doble clic durante animación

        # ── Contenedor maestro (pantallas se montan aquí) ─────────────────
        self.container = tk.Frame(self, bg=BG_MAIN)
        self.container.pack(fill="both", expand=True)

        self.show_config_screen()

    # =========================================================================
    #  UTILIDADES GENERALES
    # =========================================================================

    def _clear(self):
        """Destruye todos los widgets del contenedor para cambiar de pantalla."""
        for w in self.container.winfo_children():
            w.destroy()

    def _make_btn(self, parent, text, cmd, color=BTN_PRIMARY, hover=BTN_HOVER,
                  px=24, py=12, font=None, width=None):
        """
        Crea un botón flat con efecto hover.
        El hover se implementa con bind <Enter>/<Leave> porque tk.Button
        no soporta :hover nativo.
        """
        f = font or self.f_btn
        b = tk.Button(
            parent, text=text, command=cmd,
            bg=color, fg=TEXT_LIGHT, font=f,
            relief="flat", bd=0,
            activebackground=hover, activeforeground=TEXT_LIGHT,
            cursor="hand2", padx=px, pady=py
        )
        if width:
            b.config(width=width)
        b.bind("<Enter>", lambda e: b.config(bg=hover))
        b.bind("<Leave>", lambda e: b.config(bg=color))
        return b

    def _labeled_section(self, parent, text, row, col, colspan=1, pady=(0, 8)):
        """Crea un Label de sección con estilo uniforme."""
        lbl = tk.Label(parent, text=text, font=self.f_title,
                       bg=BG_MAIN, fg=TEXT_DARK, anchor="w")
        lbl.grid(row=row, column=col, columnspan=colspan,
                 sticky="w", pady=pady)
        return lbl

    # =========================================================================
    #  PANTALLA 1 — CONFIGURACIÓN
    # =========================================================================

    def show_config_screen(self):
        """Construye y muestra la pantalla de configuración inicial."""
        self._clear()

        # ── Header ───────────────────────────────────────────────────────
        hdr = tk.Frame(self.container, bg=BG_HEADER, pady=18)
        hdr.pack(fill="x")
        tk.Label(hdr, text="⚽  Sorteo de Equipos",
                 font=self.f_header, bg=BG_HEADER, fg=TEXT_LIGHT).pack()
        tk.Label(hdr, text="Al estilo Champions League — ¡Que empiece el drama!",
                 font=self.f_small, bg=BG_HEADER, fg=TEXT_MUTED).pack(pady=(3, 0))

        # ── Cuerpo ───────────────────────────────────────────────────────
        body = tk.Frame(self.container, bg=BG_MAIN, padx=40, pady=28)
        body.pack(fill="both", expand=True)
        body.columnconfigure(0, weight=3)
        body.columnconfigure(1, weight=1)
        body.rowconfigure(1, weight=1)

        # ── Panel izquierdo: área de texto ────────────────────────────────
        self._labeled_section(body, "📋  Lista de Alumnos   (uno por línea):", 0, 0)

        txt_wrap = tk.Frame(body, bg=BG_CARD,
                            highlightbackground="#CED4DA", highlightthickness=1)
        txt_wrap.grid(row=1, column=0, sticky="nsew", padx=(0, 18))

        sb = tk.Scrollbar(txt_wrap)
        sb.pack(side="right", fill="y")

        self.txt_students = tk.Text(
            txt_wrap, yscrollcommand=sb.set,
            font=self.f_body, bg=BG_CARD, fg=TEXT_MUTED,
            relief="flat", bd=10, wrap="word",
            insertbackground=BTN_PRIMARY
        )
        self.txt_students.pack(fill="both", expand=True)
        sb.config(command=self.txt_students.yview)

        # Placeholder de ejemplo
        _PH = (
            "Escribe o pega los nombres aquí…\n\n"
            "Ejemplo:\nAna García\nCarlos López\nMaría Pérez\n…"
        )
        self.txt_students.insert("1.0", _PH)

        def _focus_in(e):
            if self.txt_students.get("1.0", "end-1c") == _PH:
                self.txt_students.delete("1.0", "end")
                self.txt_students.config(fg=TEXT_DARK)

        self.txt_students.bind("<FocusIn>", _focus_in)
        self.txt_students.bind("<KeyRelease>", self._refresh_info)

        # ── Panel derecho: configuración ──────────────────────────────────
        right = tk.Frame(body, bg=BG_MAIN)
        right.grid(row=0, column=1, rowspan=2, sticky="nsew")

        card = tk.Frame(right, bg=BG_CARD, padx=22, pady=22,
                        highlightbackground="#DEE2E6", highlightthickness=1)
        card.pack(fill="x", pady=(30, 0))

        tk.Label(card, text="⚙️  Configuración",
                 font=self.f_title, bg=BG_CARD, fg=TEXT_DARK).pack(anchor="w")
        tk.Frame(card, height=1, bg="#DEE2E6").pack(fill="x", pady=10)

        tk.Label(card, text="Número de Equipos:",
                 font=self.f_body, bg=BG_CARD, fg=TEXT_DARK).pack(anchor="w", pady=(8, 4))

        vcmd = (self.register(lambda s: s.isdigit() or s == ""), "%P")
        e_wrap = tk.Frame(card, bg=BG_CARD,
                          highlightbackground=BTN_PRIMARY, highlightthickness=2)
        e_wrap.pack(fill="x", pady=(0, 14))
        self.entry_teams = tk.Entry(
            e_wrap, font=self.f_title, bg=BG_CARD, fg=TEXT_DARK,
            relief="flat", bd=8, justify="center",
            insertbackground=BTN_PRIMARY, validate="key", validatecommand=vcmd
        )
        self.entry_teams.insert(0, "2")
        self.entry_teams.pack(fill="x")
        self.entry_teams.bind("<KeyRelease>", self._refresh_info)

        tk.Frame(card, height=1, bg="#DEE2E6").pack(fill="x", pady=4)

        self.lbl_info = tk.Label(
            card, text="Ingresa los alumnos →",
            font=self.f_small, bg=BG_CARD, fg=TEXT_MUTED,
            wraplength=160, justify="center"
        )
        self.lbl_info.pack(pady=12)

        # ── Botón iniciar ─────────────────────────────────────────────────
        btn_row = tk.Frame(body, bg=BG_MAIN)
        btn_row.grid(row=2, column=0, columnspan=2, pady=(22, 0))
        self._make_btn(btn_row, "🎲   INICIAR SORTEO", self._start_sorteo,
                       px=44, py=16).pack()

        self.lbl_error = tk.Label(body, text="", font=self.f_small,
                                  bg=BG_MAIN, fg="#EF233C")
        self.lbl_error.grid(row=3, column=0, columnspan=2, pady=(8, 0))

    # ── Helpers de la pantalla de configuración ───────────────────────────

    def _refresh_info(self, _=None):
        """Actualiza en tiempo real el resumen de alumnos/equipos."""
        names = self._parse_names()
        try:
            nt = int(self.entry_teams.get())
        except ValueError:
            nt = 0

        if names and nt >= 2:
            lo = len(names) // nt
            hi = math.ceil(len(names) / nt)
            self.lbl_info.config(
                text=f"✅  {len(names)} alumnos → {nt} equipos\n"
                     f"(~{lo}–{hi} integrantes c/u)",
                fg="#06D6A0"
            )
        else:
            self.lbl_info.config(text="Ingresa los alumnos →", fg=TEXT_MUTED)

    def _parse_names(self):
        """Extrae la lista limpia de nombres del widget Text."""
        raw = self.txt_students.get("1.0", "end-1c").strip()
        bad = {
            "Escribe o pega los nombres aquí…",
            "Ejemplo:", "Ana García", "Carlos López", "María Pérez", "…"
        }
        return [l.strip() for l in raw.splitlines()
                if l.strip() and l.strip() not in bad]

    def _start_sorteo(self):
        """Valida la entrada y, si pasa, arranca la pantalla de sorteo."""
        names = self._parse_names()

        try:
            nt = int(self.entry_teams.get())
        except ValueError:
            self.lbl_error.config(text="⚠  Ingresa un número válido de equipos.")
            return

        if not names:
            self.lbl_error.config(text="⚠  La lista de alumnos está vacía.")
            return
        if nt < 2:
            self.lbl_error.config(text="⚠  Deben ser al menos 2 equipos.")
            return
        if nt > len(names):
            self.lbl_error.config(text="⚠  Hay más equipos que alumnos.")
            return
        if nt > 8:
            self.lbl_error.config(text="⚠  El máximo es 8 equipos.")
            return

        # ── Preparar estado global ────────────────────────────────────────
        self.students      = names[:]
        random.shuffle(self.students)          # "El bombo" interno
        self.num_teams     = nt
        self.teams         = [[] for _ in range(nt)]
        self.student_index = 0
        self.assign_index  = 0
        self.is_animating  = False

        self.show_sorteo_screen()

    # =========================================================================
    #  PANTALLA 2 — SORTEO CON ANIMACIÓN
    # =========================================================================

    def show_sorteo_screen(self):
        """Construye la pantalla principal del sorteo."""
        self._clear()

        # ── Header ───────────────────────────────────────────────────────
        hdr = tk.Frame(self.container, bg=BG_HEADER, pady=12)
        hdr.pack(fill="x")
        inner = tk.Frame(hdr, bg=BG_HEADER)
        inner.pack()
        tk.Label(inner, text="🎰  ¡EL SORTEO HA COMENZADO!",
                 font=self.f_header, bg=BG_HEADER, fg=ACCENT_GOLD).pack(side="left", padx=10)
        self.lbl_progress = tk.Label(
            inner, text=f"0 / {len(self.students)} asignados",
            font=self.f_body, bg=BG_HEADER, fg=TEXT_MUTED
        )
        self.lbl_progress.pack(side="left", padx=24)

        # ── Zona de la "tómbola" ──────────────────────────────────────────
        slot_zone = tk.Frame(self.container, bg=SLOT_BG, pady=18)
        slot_zone.pack(fill="x")

        self.slot_lbl = tk.Label(
            slot_zone, text="¿ Quién será el siguiente ?",
            font=self.f_slot, bg=SLOT_BG, fg=SLOT_TEXT, pady=8
        )
        self.slot_lbl.pack()

        self.slot_sub = tk.Label(
            slot_zone, text="Presiona el botón para revelar",
            font=self.f_body, bg=SLOT_BG, fg=TEXT_MUTED
        )
        self.slot_sub.pack()

        # ── Botón revelar ─────────────────────────────────────────────────
        btn_zone = tk.Frame(self.container, bg=BG_MAIN, pady=12)
        btn_zone.pack(fill="x")

        self.btn_reveal = self._make_btn(
            btn_zone, "🔮   REVELAR SIGUIENTE INTEGRANTE",
            self.reveal_next, color=BTN_REVEAL, hover=BTN_REVEAL_H, px=36, py=14
        )
        self.btn_reveal.pack()

        # ── Grid de tarjetas de equipo ────────────────────────────────────
        grid_frame = tk.Frame(self.container, bg=BG_MAIN)
        grid_frame.pack(fill="both", expand=True, padx=18, pady=8)

        cols = min(self.num_teams, 4)
        rows_needed = math.ceil(self.num_teams / cols)
        for c in range(cols):
            grid_frame.columnconfigure(c, weight=1)
        for r in range(rows_needed):
            grid_frame.rowconfigure(r, weight=1)

        self.team_cards       = []   # Frame exterior de cada equipo
        self.team_name_frames = []   # Frame interior donde se añaden los nombres

        for i in range(self.num_teams):
            row = i // cols
            col = i % cols
            color = TEAM_COLORS[i % len(TEAM_COLORS)]
            emoji = TEAM_EMOJIS[i % len(TEAM_EMOJIS)]

            # Tarjeta
            card = tk.Frame(grid_frame, bg=BG_CARD,
                            highlightbackground=color, highlightthickness=2,
                            padx=8, pady=6)
            card.grid(row=row, column=col, padx=6, pady=6, sticky="nsew")

            # Cabecera coloreada del equipo
            team_hdr = tk.Frame(card, bg=color, pady=5)
            team_hdr.pack(fill="x")
            tk.Label(team_hdr, text=f"{emoji}  Equipo {i + 1}",
                     font=self.f_name, bg=color, fg=TEXT_LIGHT).pack()

            # Zona de nombres
            nf = tk.Frame(card, bg=BG_CARD, pady=4)
            nf.pack(fill="both", expand=True)
            tk.Label(nf, text="— vacío —",
                     font=self.f_small, bg=BG_CARD, fg=TEXT_MUTED).pack(pady=6)

            self.team_cards.append(card)
            self.team_name_frames.append(nf)

        # ── Botón "Nuevo Sorteo" (oculto hasta el final) ──────────────────
        self.btn_restart = self._make_btn(
            self.container, "🔄   Nuevo Sorteo",
            self.show_config_screen,
            color="#6C757D", hover="#495057",
            px=20, py=8, font=self.f_body
        )
        # No se empaqueta todavía; aparecerá al terminar el sorteo.

    # =========================================================================
    #  LÓGICA DE ANIMACIÓN
    #
    #  Tkinter es single-thread: NO podemos usar time.sleep() ni loops
    #  bloqueantes. En cambio, usamos after(ms, callback) para programar
    #  llamadas futuras sin bloquear el event-loop de la GUI.
    #
    #  Flujo:
    #    reveal_next()           → valida y arranca
    #      └─ _run_slot_anim()  → loop de tómbola (frame 0..total)
    #           └─ _show_climax() → nombre real en dorado
    #                 └─ _blink() → parpadeo de clímax
    #                       └─ _assign_to_team() → nombre entra al equipo
    # =========================================================================

    def reveal_next(self):
        """Punto de entrada: deshabilita el botón e inicia la animación."""
        if self.is_animating or self.student_index >= len(self.students):
            return

        self.is_animating = True
        self.btn_reveal.config(state="disabled", bg="#ADB5BD")

        # Parámetros de la animación:
        #   total_frames : cuántos "saltos" de nombre se muestran (~2.5 s)
        #   init_delay   : intervalo inicial en ms (muy rápido = suspenso)
        self._run_slot_anim(frame=0, total=34, init_delay=42)

    def _run_slot_anim(self, frame, total, init_delay):
        """
        Bucle principal de la tómbola.

        Cada llamada:
          1. Elige un nombre aleatorio de la lista y lo muestra.
          2. Calcula el retardo del SIGUIENTE frame con una curva de frenado.
          3. Agenda la siguiente llamada con after(delay, ...).

        La curva de frenado: los primeros frames son rápidos (delay inicial),
        los últimos son lentos (delay * 4.5) para crear tensión creciente.
        Al llegar a total, llama a _show_climax() con el alumno real.
        """
        if frame >= total:
            # ── Fin de animación: mostrar el alumno real ──
            chosen = self.students[self.student_index]
            self._show_climax(chosen)
            return

        # Mostrar nombre aleatorio (efecto tómbola)
        self.slot_lbl.config(text=random.choice(self.students), fg=SLOT_TEXT)

        # Cálculo del siguiente retardo (frenado gradual)
        #   progress: 0.0 al inicio → 1.0 al final
        #   El multiplicador sube de 1× a ~4.5× en curva cuadrática
        progress = frame / total
        next_delay = int(init_delay * (1 + progress ** 1.6 * 4.5))
        next_delay = min(next_delay, 320)  # Cap máximo para el suspenso final

        # Programar el siguiente frame SIN bloquear la GUI
        self.after(next_delay, self._run_slot_anim, frame + 1, total, init_delay)

    def _show_climax(self, name):
        """Muestra el nombre real en dorado e inicia el parpadeo de clímax."""
        self.slot_lbl.config(text=name, fg=ACCENT_GOLD)
        self.slot_sub.config(
            text=f"➤  ¡Se une al  Equipo {self.assign_index + 1}!",
            fg=ACCENT_GOLD
        )
        # Iniciar parpadeo: 6 half-cycles (3 full blinks)
        self._blink(name, half_cycles=6, is_visible=False)

    def _blink(self, name, half_cycles, is_visible):
        """
        Efecto de parpadeo del nombre en el slot.
        Alterna la visibilidad del texto (dorado ↔ invisible) cada 160 ms.
        Al agotar los ciclos, llama a _assign_to_team().
        """
        if half_cycles <= 0:
            self.slot_lbl.config(text=name, fg=ACCENT_GOLD)
            self.after(350, self._assign_to_team, name)
            return

        color = ACCENT_GOLD if is_visible else SLOT_BG
        self.slot_lbl.config(fg=color)
        self.after(160, self._blink, name, half_cycles - 1, not is_visible)

    def _assign_to_team(self, name):
        """
        Asigna el alumno al equipo actual (round-robin balanceado)
        y actualiza visualmente la tarjeta correspondiente.
        """
        idx = self.assign_index
        team_color = TEAM_COLORS[idx % len(TEAM_COLORS)]

        self.teams[idx].append(name)

        # Limpiar el placeholder "— vacío —" la primera vez
        nf = self.team_name_frames[idx]
        if len(self.teams[idx]) == 1:
            for w in nf.winfo_children():
                w.destroy()

        # Añadir el nombre a la tarjeta con su color de equipo
        lbl = tk.Label(
            nf, text=f"  ✦  {name}",
            font=self.f_body, bg=BG_CARD, fg=team_color, anchor="w"
        )
        lbl.pack(fill="x", padx=6, pady=2)

        # Flash dorado en el borde de la tarjeta por 600 ms
        self.team_cards[idx].config(highlightbackground=ACCENT_GOLD,
                                     highlightthickness=3)
        self.after(600, lambda: self.team_cards[idx].config(
            highlightbackground=team_color, highlightthickness=2
        ))

        # ── Avanzar contadores ────────────────────────────────────────────
        self.student_index += 1
        # Round-robin: el próximo equipo en la rotación circular
        self.assign_index = (self.assign_index + 1) % self.num_teams

        self.lbl_progress.config(
            text=f"{self.student_index} / {len(self.students)} asignados"
        )

        # ── ¿Terminamos? ──────────────────────────────────────────────────
        if self.student_index >= len(self.students):
            self._finish()
        else:
            # Resetear slot y rehabilitar botón
            self.slot_lbl.config(text="¿ Quién será el siguiente ?",
                                  fg=SLOT_TEXT)
            self.slot_sub.config(text="Presiona el botón para revelar",
                                  fg=TEXT_MUTED)
            self.is_animating = False
            self.btn_reveal.config(state="normal", bg=BTN_REVEAL)
            # Restaurar bind del hover
            self.btn_reveal.bind("<Enter>", lambda e: self.btn_reveal.config(bg=BTN_REVEAL_H))
            self.btn_reveal.bind("<Leave>", lambda e: self.btn_reveal.config(bg=BTN_REVEAL))

    def _finish(self):
        """Pantalla final cuando todos los alumnos han sido asignados."""
        self.is_animating = False
        self.slot_lbl.config(text="🏆  ¡SORTEO COMPLETADO!  🏆", fg=ACCENT_GOLD)
        self.slot_sub.config(text="¡Que gane el mejor equipo! 🎉", fg=ACCENT_GOLD)
        self.btn_reveal.config(
            state="disabled",
            text="✅   ¡Todos asignados!",
            bg="#06D6A0"
        )
        # Mostrar el botón de reinicio que estaba oculto
        self.btn_restart.pack(pady=(0, 14))


# =============================================================================
#  PUNTO DE ENTRADA
# =============================================================================
if __name__ == "__main__":
    app = SorteoApp()
    app.mainloop()
