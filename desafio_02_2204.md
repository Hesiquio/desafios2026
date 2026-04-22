# 🧠 Desafío 2 — El Puente de Comunicación

**Fecha:** 22 de Abril de 2026
**Tema:** Lógica de Continuidad / Arreglos Booleanos

---

## 📌 Instrucción

Imagina 5 servidores conectados en cadena: **A → B → C → D → E**.

Se te entregará un arreglo de 4 valores booleanos que representan si cada cable funciona (`True`) o está roto (`False`).

Crea un método que determine si un mensaje enviado desde **A** puede llegar a **E**. Si el camino se corta, debe indicar exactamente en qué servidor se detuvo el mensaje.

---

## 📊 Ejemplos de entrada y salida

| Arreglo de cables               | Resultado esperado                        |
|---------------------------------|-------------------------------------------|
| `[True, False, True, True]`     | `"El mensaje se quedó en el Servidor B"`  |
| `[True, True, True, True]`      | `"El mensaje llegó al Servidor E"`        |
| `[False, True, True, True]`     | `"El mensaje se quedó en el Servidor A"`  |

---

## 💻 Tu tarea

1. Crea el archivo `desafio_02.py`.
2. Implementa el método `verificar_conexion(cables)`.
3. Prueba con los 3 ejemplos de la tabla y agrega uno propio.

---

## 🔍 Pregunta de reflexión

> ¿Puedes relacionar el índice del cable roto con el nombre del servidor donde se detiene el mensaje? ¿Cuál es la relación matemática entre ambos?

Prepárate para explicarlo en voz alta al final de la clase.

---

> _"Un problema well-defined es un problema medio resuelto."_ 🚀
