class Alumno:
    def __init__(self, nombre, calificacion):
        self.nombre = nombre
        self.calificacion = calificacion

class Grupo:
    def __init__(self, nombre_grupo):
        self.nombre_grupo = nombre_grupo
        self.estudiantes = []
        self.promedio_grupal = 0

    def inscribir_alumno(self, alumno):
        self.estudiantes.append(alumno)
        
        total = sum(est.calificacion for est in self.estudiantes)
        self.promedio_grupal = total / len(self.estudiantes)

    def mostrar_reporte(self):
        print(f"Grupo: {self.nombre_grupo} | Promedio Actual: {self.promedio_grupal}")

# --- Ejecución ---
# 1. Creamos al alumno y al grupo
estudiante_1 = Alumno("GADIEL", 70)
mi_grupo = Grupo("ISC-201")

# 2. Lo inscribimos
mi_grupo.inscribir_alumno(estudiante_1)
mi_grupo.mostrar_reporte()

# 3. El alumno mejora su calificación (Cambio de estado)
print("--- Actualizando calificación del alumno ---")
estudiante_1.calificacion = 100

mi_grupo.mostrar_reporte()