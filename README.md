# Aprendizaje por Refuerzo en Tic-Tac-Toe (Juego del Gato)

Este proyecto implementa un agente de **aprendizaje por refuerzo** que aprende a jugar *Tic-Tac-Toe* mediante **self-play**.  
El modelo utiliza una tabla de valores (*value function*) donde asigna un valor a cada estado del tablero y se actualiza al finalizar cada partida.

---

## 🚀 ¿Qué hace este proyecto?

- Simula miles de partidas entre dos agentes.
- Los agentes aprenden mediante **exploración y explotación**.
- Guarda la **función de valor aprendida** en un archivo `agente.pickle`.
- Muestra en un DataFrame los estados mejor valorados por el agente.

---

## 🧠 Conceptos aprendidos

### 🔹 1. Representación del Tablero
El tablero se maneja con una matriz `3x3` de NumPy, donde:
- `1` → Jugador 1  
- `-1` → Jugador 2  
- `0` → Celda vacía  

Se implementan funciones para:
- Obtener movimientos válidos
- Actualizar el tablero
- Detectar victoria, empate o si el juego continúa

---

### 🔹 2. Self-play
El agente juega contra otro agente (uno más explorador, uno más explotador).  
Usa múltiples rondas para aprender estrategias ganadoras.

Cada ronda:
1. Ambos agentes juegan hasta terminar la partida.
2. Se les asignan recompensas:
   - Victoria → `1`
   - Empate → `0.5`
   - Derrota → `0`

---

### 🔹 3. Política de Acción
El agente decide entre:
- **Explorar**: moverse aleatoriamente con probabilidad `prob_exp`.
- **Explotar**: elegir el movimiento con mayor valor estimado en la función de valor.

---

### 🔹 4. Actualización de la Función de Valor
Al final de cada partida, el agente actualiza sus valores con:


🧩 Requisitos

Antes de ejecutar el script, instala las dependencias:

pip install -r requirements.txt

🧑‍💻 Autor

Desarrollado por Gus como parte de su aprendizaje en Python e IA.
