import numpy as np
from tqdm import tqdm
import pickle


# cuadrícula
class Board:
    def __init__(self):
        self.state = np.zeros((3, 3))

    def valid_moves(self):
        return [(i, j) for j in range(3) for i in range(3) if self.state[i, j] == 0]

    def update(self, symbol, row, col):
        if self.state[row, col] == 0:
            self.state[row, col] = symbol
        else:
            raise ValueError("movimiento ilegal !")

    def is_game_over(self):
        # comprobar filas y columnas
        if (self.state.sum(axis=0) == 3).sum() >= 1 or (
            self.state.sum(axis=1) == 3
        ).sum() >= 1:
            return 1
        if (self.state.sum(axis=0) == -3).sum() >= 1 or (
            self.state.sum(axis=1) == -3
        ).sum() >= 1:
            return -1
        # comprobar diagonales
        diag_sums = [
            sum([self.state[i, i] for i in range(3)]),
            sum([self.state[i, 3 - i - 1] for i in range(3)]),
        ]
        if diag_sums[0] == 3 or diag_sums[1] == 3:
            return 1
        if diag_sums[0] == -3 or diag_sums[1] == -3:
            return -1
        # empate
        if len(self.valid_moves()) == 0:
            return 0
        # seguir jugando
        return None

    def reset(self):
        self.state = np.zeros((3, 3))


# juego
class Game:
    def __init__(self, player1, player2):
        player1.symbol = 1
        player2.symbol = -1
        self.players = [player1, player2]
        self.board = Board()

    def selfplay(self, rounds=100):
        wins = [0, 0]
        for i in tqdm(range(1, rounds + 1)):
            self.board.reset()
            for player in self.players:
                player.reset()
            game_over = False
            while not game_over:
                for player in self.players:
                    action = player.move(self.board)
                    self.board.update(player.symbol, action[0], action[1])
                    for player in self.players:
                        player.update(self.board)
                    if self.board.is_game_over() is not None:
                        game_over = True
                        break
            self.reward()
            for ix, player in enumerate(self.players):
                if self.board.is_game_over() == player.symbol:
                    wins[ix] += 1
        return wins

    def reward(self):
        winner = self.board.is_game_over()
        if winner == 0:  # empate
            for player in self.players:
                player.reward(0.5)
        else:  # le damos 1 recompensa al jugador que gana
            for player in self.players:
                if winner == player.symbol:
                    player.reward(1)
                else:
                    player.reward(0)


# agente
class Agent:
    def __init__(self, alpha=0.5, prob_exp=0.5):
        self.value_function = {}  # tabla con pares estado -> valor
        self.alpha = alpha  # learning rate
        self.positions = []  # guardamos todas las posiciones de la partida
        self.prob_exp = prob_exp  # probabilidad de explorar

    def reset(self):
        self.positions = []

    def move(self, board, explore=True):
        valid_moves = board.valid_moves()
        # exploracion
        if explore and np.random.uniform(0, 1) < self.prob_exp:
            # vamos a una posición aleatoria
            ix = np.random.choice(len(valid_moves))
            return valid_moves[ix]
        # explotacion
        # vamos a la posición con más valor
        max_value = -1000
        for row, col in valid_moves:
            next_board = board.state.copy()
            next_board[row, col] = self.symbol
            next_state = str(next_board.reshape(3 * 3))
            value = (
                0
                if self.value_function.get(next_state) is None
                else self.value_function.get(next_state)
            )
            if value >= max_value:
                max_value = value
                best_row, best_col = row, col
        return best_row, best_col

    def update(self, board):
        self.positions.append(str(board.state.reshape(3 * 3)))

    def reward(self, reward):
        # al final de la partida (cuando recibimos la recompensa)
        # iteramos por tods los estados actualizando su valor en la tabla
        for p in reversed(self.positions):
            if self.value_function.get(p) is None:
                self.value_function[p] = 0
            self.value_function[p] += self.alpha * (reward - self.value_function[p])
            reward = self.value_function[p]


agent1 = Agent(prob_exp=1)
agent2 = Agent()

game = Game(agent1, agent2)

game.selfplay(300000)

import pandas as pd

funcion_de_valor = sorted(
    agent1.value_function.items(), key=lambda kv: kv[1], reverse=True
)
tabla = pd.DataFrame(
    {
        "estado": [x[0] for x in funcion_de_valor],
        "valor": [x[1] for x in funcion_de_valor],
    }
)

print(tabla)


with open("agente.pickle", "wb") as handle:
    pickle.dump(agent1.value_function, handle, protocol=pickle.HIGHEST_PROTOCOL)
