import tkinter as tk
from tkinter import messagebox
import random

# Definição das constantes
TAMANHO_TABULEIRO = 3
JOGADOR_X = 'X'
JOGADOR_O = 'O'
VAZIO = ' '

class JogoDaVelha:
    def __init__(self, root):
        self.root = root
        self.root.title("Jogo da Velha")
        self.tabuleiro = [[VAZIO for _ in range(TAMANHO_TABULEIRO)] for _ in range(TAMANHO_TABULEIRO)]
        self.jogador_atual = JOGADOR_X
        self.botoes = [[None for _ in range(TAMANHO_TABULEIRO)] for _ in range(TAMANHO_TABULEIRO)]
        self.nivel_dificuldade = tk.StringVar(value="Médio")  # Definindo nível de dificuldade padrão
        self.criar_interface()
        self.iniciar_jogo()

    def criar_interface(self):
        # Criação dos botões do tabuleiro
        for i in range(TAMANHO_TABULEIRO):
            for j in range(TAMANHO_TABULEIRO):
                self.botoes[i][j] = tk.Button(self.root, font=('normal', 40), width=5, height=2,
                                              command=lambda i=i, j=j: self.clicar_botao(i, j))
                self.botoes[i][j].grid(row=i, column=j)

        # Criação do menu para selecionar nível de dificuldade
        menu_dificuldade = tk.OptionMenu(self.root, self.nivel_dificuldade, "Fácil", "Médio", "Difícil")
        menu_dificuldade.grid(row=TAMANHO_TABULEIRO, column=0, columnspan=TAMANHO_TABULEIRO)

    def iniciar_jogo(self):
        for i in range(TAMANHO_TABULEIRO):
            for j in range(TAMANHO_TABULEIRO):
                self.botoes[i][j].config(text=VAZIO, state=tk.NORMAL)
        self.tabuleiro = [[VAZIO for _ in range(TAMANHO_TABULEIRO)] for _ in range(TAMANHO_TABULEIRO)]
        self.jogador_atual = JOGADOR_X

    def clicar_botao(self, i, j):
        if self.tabuleiro[i][j] == VAZIO:
            self.tabuleiro[i][j] = self.jogador_atual
            self.botoes[i][j].config(text=self.jogador_atual, state=tk.DISABLED)
            if self.verificar_vencedor(self.jogador_atual):
                messagebox.showinfo("Jogo da Velha", f"Jogador {self.jogador_atual} venceu!")
                self.iniciar_jogo()
            elif self.tabuleiro_cheio():
                messagebox.showinfo("Jogo da Velha", "Deu Velha!")
                self.iniciar_jogo()
            else:
                self.trocar_jogador()

    def trocar_jogador(self):
        self.jogador_atual = JOGADOR_O if self.jogador_atual == JOGADOR_X else JOGADOR_X
        if self.jogador_atual == JOGADOR_O:
            self.root.after(800, self.jogada_ia)

    def jogada_ia(self):
        if self.nivel_dificuldade.get() == "Fácil":
            self.jogada_aleatoria()
        elif self.nivel_dificuldade.get() == "Médio":
            i, j = self.encontrar_melhor_jogada(profundidade_max=2)
            self.clicar_botao(i, j)
        elif self.nivel_dificuldade.get() == "Difícil":
            i, j = self.encontrar_melhor_jogada()
            self.clicar_botao(i, j)

    def jogada_aleatoria(self):
        jogadas_disponiveis = [(i, j) for i in range(TAMANHO_TABULEIRO) for j in range(TAMANHO_TABULEIRO) if self.tabuleiro[i][j] == VAZIO]
        if jogadas_disponiveis:
            i, j = random.choice(jogadas_disponiveis)
            self.clicar_botao(i, j)

    def verificar_vencedor(self, jogador):
        for i in range(TAMANHO_TABULEIRO):
            if all(self.tabuleiro[i][j] == jogador for j in range(TAMANHO_TABULEIRO)):
                return True
            if all(self.tabuleiro[j][i] == jogador for j in range(TAMANHO_TABULEIRO)):
                return True
        if all(self.tabuleiro[i][i] == jogador for i in range(TAMANHO_TABULEIRO)) or \
           all(self.tabuleiro[i][TAMANHO_TABULEIRO - 1 - i] == jogador for i in range(TAMANHO_TABULEIRO)):
            return True
        return False

    def tabuleiro_cheio(self):
        return all(self.tabuleiro[i][j] != VAZIO for i in range(TAMANHO_TABULEIRO) for j in range(TAMANHO_TABULEIRO))

    def minimax(self, profundidade, e_maximizador, profundidade_max=None):
        if self.verificar_vencedor(JOGADOR_O):
            return 10 - profundidade
        if self.verificar_vencedor(JOGADOR_X):
            return profundidade - 10
        if self.tabuleiro_cheio():
            return 0
        if profundidade_max is not None and profundidade >= profundidade_max:
            return 0

        if e_maximizador:
            melhor_valor = -float('inf')
            for i in range(TAMANHO_TABULEIRO):
                for j in range(TAMANHO_TABULEIRO):
                    if self.tabuleiro[i][j] == VAZIO:
                        self.tabuleiro[i][j] = JOGADOR_O
                        valor = self.minimax(profundidade + 1, False, profundidade_max)
                        self.tabuleiro[i][j] = VAZIO
                        melhor_valor = max(melhor_valor, valor)
            return melhor_valor
        else:
            melhor_valor = float('inf')
            for i in range(TAMANHO_TABULEIRO):
                for j in range(TAMANHO_TABULEIRO):
                    if self.tabuleiro[i][j] == VAZIO:
                        self.tabuleiro[i][j] = JOGADOR_X
                        valor = self.minimax(profundidade + 1, True, profundidade_max)
                        self.tabuleiro[i][j] = VAZIO
                        melhor_valor = min(melhor_valor, valor)
            return melhor_valor

    def encontrar_melhor_jogada(self, profundidade_max=None):
        melhor_valor = -float('inf')
        melhor_jogada = (-1, -1)
        for i in range(TAMANHO_TABULEIRO):
            for j in range(TAMANHO_TABULEIRO):
                if self.tabuleiro[i][j] == VAZIO:
                    self.tabuleiro[i][j] = JOGADOR_O
                    valor = self.minimax(0, False, profundidade_max)
                    self.tabuleiro[i][j] = VAZIO
                    if valor > melhor_valor:
                        melhor_valor = valor
                        melhor_jogada = (i, j)
        return melhor_jogada

# Criação da janela principal
root = tk.Tk()
jogo = JogoDaVelha(root)
root.mainloop()
