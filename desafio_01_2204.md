# 🧠 Desafío 1 — El Validador de Jerarquía

**Fecha:** 22 de Abril de 2026
**Tema:** Estructura de Datos (Pila / Stack)

---

## 📌 Instrucción

Crea un método que reciba una cadena de texto compuesta **solo** por llaves, corchetes y paréntesis: `{[()]}`.

El programa debe devolver:
- `True` si todos los símbolos están correctamente balanceados y cerrados en orden.
- `False` si no.

---

## ⚠️ El reto lógico

No basta con contar aperturas y cierres. Por ejemplo:

```
[(])  →  False  ❌  (el corchete se cerró antes que el paréntesis)
[()]  →  True   ✅
```

---

## 💻 Tu tarea

1. Crea el archivo `desafio_01.py`.
2. Implementa el método `validar_jerarquia(cadena)`.
3. Prueba con al menos **3 cadenas distintas**: una válida, una inválida y una vacía.

---

## 🔍 Pregunta de reflexión

> ¿Qué ocurre en la memoria cada vez que encuentras un símbolo de cierre? ¿Qué estructura de datos te permite rastrear el orden de apertura?

Prepárate para explicarlo en voz alta al final de la clase.

---

> _"Un problema well-defined es un problema medio resuelto."_ 🚀
