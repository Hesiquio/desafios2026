# 🎲 Sorteo de Equipos + Ruleta de Puntos
## Guía de Nuevas Funcionalidades

---

## 📋 Resumen de Cambios

Se ha actualizado **sorteo_equipos.py** con las siguientes mejoras:

### 1️⃣ **SQLite Database (desafio_data.db)**
- 📁 Guardar grupos de estudiantes
- 📊 Historial completo de sorteos
- 🏆 Leaderboard con puntos de estudiantes

### 2️⃣ **Menú Principal Mejorado**
- Opción para nuevo sorteo
- Cargar grupos guardados anteriormente
- Acceder a la ruleta de puntos
- Ver historial de sorteos
- Ver leaderboard (ranking)

### 3️⃣ **Ruleta de Puntos (NUEVO)**
- 🎡 Ruleta visual interactiva
- 🎯 6 secciones con puntos: 10, 25, 50, 100, 200
- Seleccionar estudiante y girar
- Animación de giro realista
- Puntos se guardan automáticamente en la BD

### 4️⃣ **Gestión de Grupos**
- Guardar grupos con nombre personalizado
- Cargar y reutilizar grupos previos
- Eliminar grupos antiguos
- Ver fecha de creación

---

## 🚀 Cómo Usar

### **Pantalla Inicial**
```
⚽ GESTOR DE SORTEOS
├── 🎲 Nuevo Sorteo
├── 📁 Cargar Grupo Guardado
├── 🎡 Ruleta de Puntos
├── 📊 Ver Historial
├── 🏆 Ver Leaderboard
└── ❌ Salir
```

### **Nuevo Sorteo**
1. Ingresa los nombres de estudiantes (uno por línea)
2. Define el número de equipos (2-8)
3. Dale un nombre al grupo (opcional)
4. Presiona "Iniciar Sorteo"
5. Haz clic en "Revelar Siguiente Integrante" para cada alumno
6. Al terminar, puedes:
   - 🎡 Ir a la Ruleta de Puntos
   - 🔄 Hacer un nuevo sorteo
   - 🏠 Volver al menú

### **Cargar Grupo Guardado**
1. Ver lista de grupos previos
2. Seleccionar uno
3. Presionar "Cargar"
4. El sorteo se inicia con ese grupo
5. Los cambios se guardan automáticamente

### **Ruleta de Puntos**
1. Selecciona un estudiante de la lista
2. Presiona "🎪 Girar Ruleta"
3. La ruleta gira y muestra un número de puntos
4. Los puntos se asignan automáticamente
5. El leaderboard se actualiza en tiempo real
6. Puedes ver el Top 5 en la esquina derecha

### **Ver Historial**
- Lista cronológica de todos los sorteos realizados
- Muestra grupo, fecha y notas
- Útil para auditoría y seguimiento

### **Ver Leaderboard**
- Ranking de estudiantes por puntos
- Medallas: 🥇 🥈 🥉
- Muestra número de giros realizados
- Opción para limpiar el leaderboard

---

## 💾 Base de Datos

La aplicación crea automáticamente **desafio_data.db** con 3 tablas:

### **Tabla: groups**
```
id (PK) | name | students (JSON) | num_teams | teams (JSON) | created_at | notes
```

### **Tabla: draw_history**
```
id (PK) | group_id (FK) | group_name | teams (JSON) | drawn_at | notes
```

### **Tabla: leaderboard**
```
id (PK) | student_name | points | wheel_spins | last_updated
```

---

## 🎯 Características Técnicas

✅ **Sin dependencias externas** (solo tkinter nativo)
✅ **Interfaz moderna** con colores planos (Flat Design)
✅ **Animaciones suaves** para sorteo y ruleta
✅ **Persistencia** de datos en SQLite
✅ **Validación** de entrada de datos
✅ **Responsive** y adaptable a diferentes tamaños

---

## 🔧 Métodos Nuevos

```python
# Instancia de gestor de BD
self.db = DatabaseManager()

# Guardar grupo
self.db.save_group(name, students, num_teams, teams)

# Cargar grupo
self.db.load_group(group_id)

# Guardar en historial
self.db.save_draw_history(group_name, teams)

# Agregar puntos
self.db.add_points(student_name, points)

# Ver leaderboard
self.db.get_leaderboard(limit=20)

# Ver historial
self.db.get_draw_history(limit=50)
```

---

## 📸 Pantallas

### 1. Menú Principal
- Botones grandes y coloridos
- Acceso rápido a todas las funciones

### 2. Configuración de Sorteo
- Entrada de nombres
- Selector de equipos
- Nombre del grupo personalizado

### 3. Ruleta de Sorteo
- Animación de tómbola
- Nombres girando
- Parpadeo dorado del ganador

### 4. Ruleta de Puntos
- Canvas visual con 6 secciones
- Lista de estudiantes
- Resultado de puntos grande
- Top 5 leaderboard

### 5. Historial/Leaderboard
- Scroll con lista completa
- Información detallada
- Opciones de limpia

---

## 🎨 Colores y Estilos

```python
BG_MAIN    = "#F0F4F8"   # Fondo general
BG_CARD    = "#FFFFFF"   # Tarjetas
BG_HEADER  = "#1A1A2E"   # Header
BTN_PRIMARY= "#4361EE"   # Botón azul
BTN_REVEAL = "#F72585"   # Botón magenta
ACCENT_GOLD= "#FFD60A"   # Dorado
```

---

## 💡 Tips de Uso

1. **Grupos Reutilizables**: Guarda grupos de clases frecuentes
2. **Múltiples Competencias**: Crea leaderboards por tema/semana
3. **Historial Completo**: Todos los sorteos quedan registrados
4. **Puntos Progresivos**: Los puntos se acumulan entre sesiones
5. **Reset Opcional**: Puedes limpiar el leaderboard cuando sea necesario

---

## 🐛 Solución de Problemas

**P: ¿Dónde se guardan los datos?**
R: En `desafio_data.db` en la misma carpeta que el script

**P: ¿Puedo eliminar grupos?**
R: Sí, desde la pantalla "Cargar Grupo Guardado"

**P: ¿Se pierden los puntos si cierro la app?**
R: No, están en SQLite. Se guardan automáticamente

**P: ¿Cómo reseteo todo?**
R: Borra `desafio_data.db` y se crea una BD vacía

---

## 📝 Versión
**v2.0** - Ahora con SQLite y Ruleta de Puntos
Actualizado: 2026-04-22

---

¡Disfruta del nuevo sistema de sorteos y ruleta de puntos! 🎉
