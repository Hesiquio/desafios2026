# =============================================================================
#  sorteo/database.py
#  Gestor de base de datos SQLite para historial, grupos y leaderboard
# =============================================================================

import sqlite3
import json


class DatabaseManager:
    """Gestiona la persistencia de datos en SQLite."""

    def __init__(self, db_path="desafio_data.db"):
        self.db_path = db_path
        self._create_tables()

    def _create_tables(self):
        """Crea las tablas necesarias si no existen."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        # Tabla de grupos (sorteos guardados)
        c.execute('''
            CREATE TABLE IF NOT EXISTS groups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                students TEXT NOT NULL,
                num_teams INTEGER NOT NULL,
                teams TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                notes TEXT
            )
        ''')

        # Tabla de historial de sorteos
        c.execute('''
            CREATE TABLE IF NOT EXISTS draw_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                group_id INTEGER,
                group_name TEXT NOT NULL,
                teams TEXT NOT NULL,
                drawn_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                notes TEXT,
                FOREIGN KEY(group_id) REFERENCES groups(id)
            )
        ''')

        # Tabla de puntos/leaderboard
        c.execute('''
            CREATE TABLE IF NOT EXISTS leaderboard (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_name TEXT NOT NULL,
                points INTEGER DEFAULT 0,
                wheel_spins INTEGER DEFAULT 0,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Tabla de actividades
        c.execute('''
            CREATE TABLE IF NOT EXISTS activities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                group_id INTEGER,
                name TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(group_id) REFERENCES groups(id)
            )
        ''')

        # Migración: Añadir group_id si la tabla ya existía sin él
        try:
            c.execute('ALTER TABLE activities ADD COLUMN group_id INTEGER')
        except sqlite3.OperationalError:
            pass # Ya existe o la tabla es nueva y ya lo tiene

        # Tabla de entregas (registra el orden)
        c.execute('''
            CREATE TABLE IF NOT EXISTS activity_submissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                activity_id INTEGER,
                student_name TEXT NOT NULL,
                position INTEGER,
                submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(activity_id) REFERENCES activities(id)
            )
        ''')

        conn.commit()
        conn.close()

    # ── Grupos ────────────────────────────────────────────────────────────────

    def save_group(self, name, students, num_teams, teams, notes=""):
        """Guarda un grupo en la BD."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        students_json = json.dumps(students)
        teams_json = json.dumps(teams)

        c.execute('''
            INSERT INTO groups (name, students, num_teams, teams, notes)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, students_json, num_teams, teams_json, notes))

        conn.commit()
        group_id = c.lastrowid
        conn.close()
        return group_id

    def get_groups(self):
        """Retorna todos los grupos guardados."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('SELECT id, name, created_at FROM groups ORDER BY created_at DESC')
        groups = c.fetchall()
        conn.close()
        return groups

    def load_group(self, group_id):
        """Carga un grupo por ID."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute(
            'SELECT name, students, num_teams, teams, notes FROM groups WHERE id = ?',
            (group_id,)
        )
        row = c.fetchone()
        conn.close()

        if row:
            name, students_json, num_teams, teams_json, notes = row
            return {
                'name': name,
                'students': json.loads(students_json),
                'num_teams': num_teams,
                'teams': json.loads(teams_json),
                'notes': notes,
            }
        return None

    def delete_group(self, group_id):
        """Elimina un grupo."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('DELETE FROM groups WHERE id = ?', (group_id,))
        conn.commit()
        conn.close()

    # ── Historial ─────────────────────────────────────────────────────────────

    def save_draw_history(self, group_name, teams, notes="", group_id=None):
        """Guarda un sorteo en el historial."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        teams_json = json.dumps(teams)

        c.execute('''
            INSERT INTO draw_history (group_id, group_name, teams, notes)
            VALUES (?, ?, ?, ?)
        ''', (group_id, group_name, teams_json, notes))

        conn.commit()
        conn.close()

    def get_draw_history(self, limit=50):
        """Retorna el historial de sorteos."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            SELECT id, group_name, drawn_at, notes FROM draw_history
            ORDER BY drawn_at DESC LIMIT ?
        ''', (limit,))
        history = c.fetchall()
        conn.close()
        return history

    # ── Leaderboard ───────────────────────────────────────────────────────────

    def add_points(self, student_name, points):
        """Agrega puntos a un estudiante."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        c.execute('SELECT id FROM leaderboard WHERE student_name = ?', (student_name,))
        result = c.fetchone()

        if result:
            c.execute('''
                UPDATE leaderboard
                SET points = points + ?, wheel_spins = wheel_spins + 1,
                    last_updated = CURRENT_TIMESTAMP
                WHERE student_name = ?
            ''', (points, student_name))
        else:
            c.execute('''
                INSERT INTO leaderboard (student_name, points, wheel_spins)
                VALUES (?, ?, 1)
            ''', (student_name, points))

        conn.commit()
        conn.close()

    def get_leaderboard(self, limit=20):
        """Retorna el leaderboard ordenado por puntos."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            SELECT student_name, points, wheel_spins FROM leaderboard
            ORDER BY points DESC LIMIT ?
        ''', (limit,))
        leaderboard = c.fetchall()
        conn.close()
        return leaderboard

    def reset_leaderboard(self):
        """Limpia el leaderboard."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('DELETE FROM leaderboard')
        conn.commit()
        conn.close()

    # ── Actividades ───────────────────────────────────────────────────────────

    def create_activity(self, name, group_id):
        """Crea una nueva actividad ligada a un grupo."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('INSERT INTO activities (name, group_id) VALUES (?, ?)', (name, group_id))
        conn.commit()
        activity_id = c.lastrowid
        conn.close()
        return activity_id

    def get_activities(self):
        """Retorna todas las actividades con información de su grupo."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            SELECT a.id, a.name, a.created_at, g.name, a.group_id
            FROM activities a
            JOIN groups g ON a.group_id = g.id
            ORDER BY a.created_at DESC
        ''')
        rows = c.fetchall()
        conn.close()
        return rows

    def register_submission(self, activity_id, student_name):
        """Registra la entrega de un alumno y le asigna la siguiente posición disponible."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Verificar si ya entregó
        c.execute('''
            SELECT id FROM activity_submissions 
            WHERE activity_id = ? AND student_name = ?
        ''', (activity_id, student_name))
        if c.fetchone():
            conn.close()
            return False # Ya entregó

        # Obtener la siguiente posición
        c.execute('''
            SELECT COUNT(*) FROM activity_submissions WHERE activity_id = ?
        ''', (activity_id,))
        count = c.fetchone()[0]
        position = count + 1

        c.execute('''
            INSERT INTO activity_submissions (activity_id, student_name, position)
            VALUES (?, ?, ?)
        ''', (activity_id, student_name, position))
        
        conn.commit()
        conn.close()
        return position

    def get_activity_ranking(self, activity_id):
        """Obtiene el ranking de una actividad específica."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            SELECT student_name, position, submitted_at 
            FROM activity_submissions 
            WHERE activity_id = ? 
            ORDER BY position ASC
        ''', (activity_id,))
        rows = c.fetchall()
        conn.close()
        return rows
