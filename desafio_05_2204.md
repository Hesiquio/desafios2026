# 🧠 Desafío 5 — Radar de Colisiones

**Fecha:** 22 de Abril de 2026
**Tema:** Lógica Booleana / Geometría 2D

---

## 📌 Instrucción

Imagina dos rectángulos en un plano 2D. Cada uno está definido por los siguientes parámetros:

| Parámetro | Descripción                                   |
|-----------|-----------------------------------------------|
| `x, y`    | Coordenada de la esquina superior izquierda   |
| `ancho`   | Anchura del rectángulo                        |
| `alto`    | Altura del rectángulo                         |

Crea un método que reciba dos objetos `Rectangulo` y devuelva:
- `True` si se están **tocando o encimando**.
- `False` si están totalmente separados.

---

## ⚠️ El reto lógico

Es un rompecabezas de comparaciones. Debes evaluar los límites de cada lado (izquierdo, derecho, superior e inferior) **simultáneamente**.

---

## 💻 Tu tarea

1. Crea el archivo `desafio_05.py`.
2. Implementa la clase `Rectangulo` y el método `detectar_colision(rect_a, rect_b)`.
3. Prueba con 3 casos: rectángulos encimados, rectángulos que se tocan en un borde y rectángulos totalmente separados.

---

## 🔍 Pregunta de reflexión

> ¿Es más sencillo determinar cuándo dos rectángulos **no** se tocan y luego negar la condición? ¿Cuándo un rectángulo quedaría completamente a la izquierda, derecha, arriba o abajo del otro?

Prepárate para explicarlo en voz alta al final de la clase.

---

> _"Un problema well-defined es un problema medio resuelto."_ 🚀
