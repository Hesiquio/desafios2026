# 🧠 Desafío 4 — El Cajero Automático "Manual"

**Fecha:** 22 de Abril de 2026
**Tema:** Descomposición Numérica / Algoritmos Greedy

---

## 📌 Instrucción

Crea un método que reciba una cantidad entera de dinero y determine la **cantidad mínima de billetes** necesarios para entregar esa suma.

**Denominaciones disponibles:** `$500`, `$200`, `$100`, `$50`

---

## 🚫 Restricción importante

**No puedes usar el operador de módulo `%`.**

Debes resolver el problema usando únicamente **restas sucesivas** o **divisiones enteras** para agotar cada denominación antes de pasar a la siguiente.

---

## 📊 Ejemplo de salida esperada

Para una entrada de `$1,850`:

```
Monto: $1850
Billetes de $500: 3
Billetes de $200: 1
Billetes de $100: 1
Billetes de $50:  1
Total de billetes: 6
```

---

## 💻 Tu tarea

1. Crea el archivo `desafio_04.py`.
2. Implementa el método `calcular_billetes(monto)`.
3. Prueba con los montos: `$1,850`, `$700` y `$50`.

---

## 🔍 Pregunta de reflexión

> ¿Por qué conviene empezar siempre por el billete de mayor denominación? ¿Qué pasaría si empezaras por el de `$50`?

Prepárate para explicarlo en voz alta al final de la clase.

---

> _"Un problema well-defined es un problema medio resuelto."_ 🚀
