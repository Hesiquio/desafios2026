# 🧠 Desafío 3 — Compresor de ADN

**Fecha:** 22 de Abril de 2026
**Tema:** Manejo de Estados / Cadenas de Texto

---

## 📌 Instrucción

Crea una clase `Genetica` con un método que reciba una secuencia de ADN como cadena de texto y devuelva su versión **comprimida**.

**Ejemplo:**

```
Entrada:  AAAAAATTTCCCCG
Salida:   A6T3C4G1
```

---

## ⚠️ El reto lógico

Debes detectar el **momento exacto** en que la letra cambia para:

1. Registrar la letra anterior junto con su contador.
2. Reiniciar el conteo para la siguiente letra.

Todo sin saltarte ninguna letra ni desbordar el arreglo.

---

## 💻 Tu tarea

1. Crea el archivo `desafio_03.py`.
2. Implementa la clase `Genetica` con el método `comprimir(secuencia)`.
3. Prueba con al menos 3 secuencias distintas, incluyendo una con una sola letra repetida y otra con todas las letras diferentes.

---

## 🔍 Pregunta de reflexión

> ¿Qué pasa con el **último grupo** de letras al recorrer la cadena? ¿Cómo te aseguras de no perderlo?

Prepárate para explicarlo en voz alta al final de la clase.

---

> _"Un problema well-defined es un problema medio resuelto."_ 🚀
