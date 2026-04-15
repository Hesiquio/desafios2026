# 🐍 Desafíos 2026 — Programación Orientada a Objetos en Python

Bienvenido/a a este repositorio de desafíos de programación. Aquí encontrarás una serie de ejercicios prácticos diseñados para aprender y reforzar los conceptos fundamentales de la **Programación Orientada a Objetos (POO)** usando Python.

---

## 📚 ¿Qué aprenderás?

Cada desafío aplica uno o varios conceptos clave de POO:

| Concepto | Descripción |
|---|---|
| **Clase** | Plantilla o molde para crear objetos |
| **Objeto** | Instancia concreta de una clase |
| **Atributos** | Variables que pertenecen a un objeto |
| **Métodos** | Funciones que pertenecen a una clase |
| **Estado** | Los valores actuales de los atributos de un objeto |

---

## 🗂️ Estructura del repositorio

```
desafios2026/
├── desafio1.py   # Clase Producto — Control de inventario
├── desafio2.py   # Clase Cajero  — Simulación de cajero automático
├── desafio3.py   # Clases Alumno y Grupo — Sistema escolar
└── README.md
```

---

## 🚀 Desafíos

### Desafío 1 — Control de Inventario (`desafio1.py`)

**Contexto:** Modelas un producto de una tienda con su stock disponible.

**Clase:** `Producto`

| Atributo | Descripción |
|---|---|
| `nombre` | Nombre del producto |
| `stock` | Unidades disponibles |

| Método | Descripción |
|---|---|
| `agregar_stock(cantidad)` | Incrementa el stock |
| `vender(cantidad)` | Reduce el stock; valida que no quede negativo |

**Lo que practica:**
- Crear una clase con `__init__`
- Modificar el estado de un objeto desde sus métodos
- Validar condiciones antes de cambiar el estado

**Ejecución esperada:**
```
Error: No hay suficiente stock.
Stock final de Laptop: 0
```

---

### Desafío 2 — Cajero Automático (`desafio2.py`)

**Contexto:** Simulas el comportamiento básico de un cajero bancario con límites de retiro.

**Clase:** `Cajero`

| Atributo | Descripción |
|---|---|
| `usuario` | Nombre del titular de la cuenta |
| `saldo` | Saldo disponible en cuenta |
| `limite_retiro` | Monto máximo permitido por operación |

| Método | Descripción |
|---|---|
| `retirar_efectivo(monto)` | Valida el límite, verifica saldo y realiza el retiro |

**Lo que practica:**
- Condiciones anidadas dentro de un método
- Separación entre estado interno (`self.saldo`) y estado mostrado al usuario
- Protección de datos mediante reglas de negocio

> ⚠️ **Observa:** Aunque el retiro es exitoso, `self.saldo` en el objeto **no se actualiza**. ¿Qué línea deberías agregar para corregirlo?

**Ejecución esperada:**
```
Retiro exitoso de: $3000
Su nuevo saldo es: $5000
Saldo real en cuenta tras el retiro: $8000
```

---

### Desafío 3 — Sistema Escolar (`desafio3.py`)

**Contexto:** Modelas dos entidades que interactúan: un alumno y su grupo escolar.

**Clases:** `Alumno` y `Grupo`

**Clase `Alumno`:**

| Atributo | Descripción |
|---|---|
| `nombre` | Nombre del estudiante |
| `calificacion` | Calificación actual |

**Clase `Grupo`:**

| Atributo | Descripción |
|---|---|
| `nombre_grupo` | Identificador del grupo (ej. `ISC-201`) |
| `estudiantes` | Lista de objetos `Alumno` inscritos |
| `promedio_grupal` | Promedio calculado automáticamente |

| Método | Descripción |
|---|---|
| `inscribir_alumno(alumno)` | Agrega un alumno y recalcula el promedio |
| `mostrar_reporte()` | Imprime el estado actual del grupo |

**Lo que practica:**
- Relación entre clases (composición)
- Listas de objetos
- Cálculo dinámico de atributos derivados

> 🔍 **Punto de reflexión:** Al actualizar `estudiante_1.calificacion = 100`, el promedio del grupo **no cambia**. ¿Por qué? ¿Cómo lo resolverías?

**Ejecución esperada:**
```
Grupo: ISC-201 | Promedio Actual: 70.0
--- Actualizando calificación del alumno ---
Grupo: ISC-201 | Promedio Actual: 70.0
```

---

## ▶️ Cómo ejecutar los desafíos

Asegúrate de tener **Python 3** instalado. Desde la terminal, dentro de la carpeta del proyecto:

```bash
# Ejecutar un desafío específico
python desafio1.py
python desafio2.py
python desafio3.py
```

---

## 💡 Consejos para estudiantes

1. **Lee el código antes de ejecutarlo.** Intenta predecir la salida en papel.
2. **Modifica los valores** de prueba (stock, saldo, calificación) y observa cómo cambia el comportamiento.
3. **Responde las preguntas de reflexión** (marcadas con 🔍 y ⚠️) — son la parte más importante del aprendizaje.
4. **No copies y pegues.** Escribe el código tú mismo/a para que el aprendizaje sea real.

---

## 🧑‍💻 Requisitos

- Python 3.8 o superior
- Sin dependencias externas (solo la librería estándar de Python)

---

> _"El código que no entiendes no te pertenece."_ — Aprende cada línea. 🚀
