# 🧠 Desafío 6 — El Algoritmo de Intercambio

**Fecha:** 22 de Abril de 2026
**Tema:** Ordenamiento Manual (Bubble Sort)

---

## 📌 Instrucción

Se te entrega un arreglo de 5 números desordenados. Crea un método que los ordene de **menor a mayor** sin usar ninguna función de ordenamiento del lenguaje (`sort`, `sorted`, etc.).

---

## 🔄 Algoritmo a implementar: Burbuja (Bubble Sort)

Sigue estos pasos:

1. Compara el elemento en la posición actual con el siguiente.
2. Si el primero es **mayor** que el segundo, intercámbialos (*swap*).
3. Avanza al siguiente par y repite.
4. Continúa pasando por el arreglo hasta que no haya más intercambios necesarios.

---

## 🚫 Restricción importante

Debes usar una **variable temporal** para realizar el intercambio. No uses atajos del lenguaje para hacer el swap.

```python
# Así se hace el intercambio:
temp = arreglo[i]
arreglo[i] = arreglo[i + 1]
arreglo[i + 1] = temp
```

---

## 💻 Tu tarea

1. Crea el archivo `desafio_06.py`.
2. Implementa el método `ordenar_burbuja(arreglo)`.
3. Prueba con el arreglo `[42, 7, 19, 3, 88]` y muestra el arreglo después de cada pasada completa.

---

## 🔍 Pregunta de reflexión

> ¿Por qué es necesaria la variable temporal para hacer el swap? ¿Qué pasaría si intentaras hacer `arreglo[i] = arreglo[i + 1]` directamente, sin guardar el valor anterior?

Prepárate para explicarlo en voz alta al final de la clase.

---

> _"Un problema well-defined es un problema medio resuelto."_ 🚀
