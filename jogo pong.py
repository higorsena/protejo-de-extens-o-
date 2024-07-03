import pygame
import math

# Inicialização do Pygame
pygame.init()

# Configurações da tela
largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Pong com IA")

# Cores
preto = (0, 0, 0)
branco = (255, 255, 255)

# Raquetes
largura_raquete, altura_raquete = 10, 100
raquete1_x, raquete1_y = 10, altura // 2 - altura_raquete // 2
raquete2_x, raquete2_y = largura - 20, altura // 2 - altura_raquete // 2

# Bola
raio_bola = 10
bola_x, bola_y = largura // 2, altura // 2
velocidades_bola = {"fácil": 0.3, "médio": 0.5, "difícil": 0.7, "impossível": 0.8}
aumento_velocidade = 0.02  # Valor do aumento de velocidade a cada ponto

# Pontuação
pontuação1 = 0
pontuação2 = 0
fonte = pygame.font.Font(None, 36)
fonte_contagem = pygame.font.Font(None, 72)

# Dificuldade
dificuldade = None
velocidades_raquete = {"fácil": 0.3, "médio": 0.45, "difícil": 0.6, "impossível": 0.8}
velocidades_ia = {"fácil": 0.1, "médio": 0.2, "difícil": 0.4, "impossível": 0.8}
erro_ia = {"fácil": 30, "médio": 15, "difícil": 5, "impossível": 0}  # Erro da IA em pixels

# Funções para desenhar o menu e a tela de jogo
def desenhar_menu():
    tela.fill(preto)
    texto_título = fonte.render("Selecione a dificuldade:", True, branco)
    retângulo_título = texto_título.get_rect(center=(largura // 2, altura // 2 - 50))
    tela.blit(texto_título, retângulo_título)

    for i, diff in enumerate(["fácil", "médio", "difícil", "impossível"]):
        texto_diff = fonte.render(diff.capitalize(), True, branco)
        retângulo_diff = texto_diff.get_rect(center=(largura // 2, altura // 2 + i * 50))
        tela.blit(texto_diff, retângulo_diff)

    pygame.display.flip()

def desenhar_jogo():
    tela.fill(preto)
    pygame.draw.rect(tela, branco, (raquete1_x, raquete1_y, largura_raquete, altura_raquete))
    pygame.draw.rect(tela, branco, (raquete2_x, raquete2_y, largura_raquete, altura_raquete))
    pygame.draw.circle(tela, branco, (bola_x, bola_y), raio_bola)

    # Exibir a pontuação
    texto_pontuação1 = fonte.render(str(pontuação1), True, branco)
    texto_pontuação2 = fonte.render(str(pontuação2), True, branco)
    tela.blit(texto_pontuação1, (largura // 4, 10))
    tela.blit(texto_pontuação2, (3 * largura // 4, 10))

    pygame.display.flip()

def mover_raquetes():
    global raquete1_y, raquete2_y
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_w] and raquete1_y > 0:
        raquete1_y -= velocidades_raquete[dificuldade]
    if teclas[pygame.K_s] and raquete1_y < altura - altura_raquete:
        raquete1_y += velocidades_raquete[dificuldade]

    if bola_x > largura // 2:  # Mover a IA apenas se a bola estiver indo em sua direção
        alvo_y = bola_y - altura_raquete // 2

        # Adicionar erro à IA nos níveis mais fáceis e médios
        if dificuldade == "fácil":
            alvo_y += erro_ia[dificuldade] * (0.5 - math.sin(math.radians(raquete2_y)))
        elif dificuldade == "médio":
            alvo_y += erro_ia[dificuldade] * (0.5 - math.sin(math.radians(raquete2_y)))

        if raquete2_y < alvo_y:
            raquete2_y += velocidades_ia[dificuldade]
        elif raquete2_y > alvo_y:
            raquete2_y -= velocidades_ia[dificuldade]

def mover_bola():
    global bola_x, bola_y, velocidade_bola_x, velocidade_bola_y, pontuação1, pontuação2
    if velocidade_bola_x != 0 and velocidade_bola_y != 0:
        bola_x += velocidade_bola_x
        bola_y += velocidade_bola_y

    if bola_y <= 0 or bola_y >= altura - raio_bola:
        velocidade_bola_y *= -1

    if bola_x <= 0 or bola_x >= largura - raio_bola:
        if bola_x <= 0:
            pontuação2 += 1
        else:
            pontuação1 += 1

        velocidade_bola_x = abs(velocidade_bola_x) + aumento_velocidade
        if velocidade_bola_y > 0:
            velocidade_bola_y += aumento_velocidade
        else:
            velocidade_bola_y -= aumento_velocidade

        bola_x, bola_y = largura // 2, altura // 2
        velocidade_bola_x, velocidade_bola_y = 0, 0
        tempo_inicial = pygame.time.get_ticks()

        while pygame.time.get_ticks() - tempo_inicial < 3000:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            tela.fill(preto)
            pygame.draw.rect(tela, branco, (raquete1_x, raquete1_y, largura_raquete, altura_raquete))
            pygame.draw.rect(tela, branco, (raquete2_x, raquete2_y, largura_raquete, altura_raquete))
            pygame.draw.circle(tela, branco, (bola_x, bola_y), raio_bola)

            tempo_restante = 3 - (pygame.time.get_ticks() - tempo_inicial) // 1000
            texto_contagem = fonte_contagem.render(str(tempo_restante), True, branco)
            retângulo_contagem = texto_contagem.get_rect(center=(largura // 2, altura // 2 - 100))
            tela.blit(texto_contagem, retângulo_contagem)

            pygame.display.flip()

        velocidade_bola_x, velocidade_bola_y = velocidades_bola[dificuldade], velocidades_bola[dificuldade]

# Tela de seleção de dificuldade
desenhar_menu()
while dificuldade is None:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            exit()
        if evento.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for i, diff in enumerate(["fácil", "médio", "difícil", "impossível"]):
                retângulo_diff = fonte.render(diff.capitalize(), True, branco).get_rect(center=(largura // 2, altura // 2 + i * 50))
                if retângulo_diff.collidepoint(mouse_x, mouse_y):
                    dificuldade = diff
                    break

velocidade_raquete = velocidades_raquete[dificuldade]
velocidade_ia = velocidades_ia[dificuldade]
velocidade_bola_x, velocidade_bola_y = velocidades_bola[dificuldade], velocidades_bola[dificuldade]

# Loop principal do jogo
executando = True
while executando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            executando = False

    mover_raquetes()
    mover_bola()

    if bola_x - raio_bola <= raquete1_x + largura_raquete and raquete1_y <= bola_y <= raquete1_y + altura_raquete:
        centro_y_bola = bola_y + raio_bola
        intersect_y_relativo = (raquete1_y + (altura_raquete / 2)) - centro_y_bola
        intersect_y_normalizado = (intersect_y_relativo / (altura_raquete / 2))
        ângulo_rebote = intersect_y_normalizado * (math.pi / 4)
        velocidade_bola_x = velocidades_bola[dificuldade] * math.cos(ângulo_rebote)
        velocidade_bola_y = velocidades_bola[dificuldade] * -math.sin(ângulo_rebote)
        
    elif bola_x + raio_bola >= raquete2_x and raquete2_y <= bola_y <= raquete2_y + altura_raquete:
        centro_y_bola = bola_y + raio_bola
        intersect_y_relativo = (raquete2_y + (altura_raquete / 2)) - centro_y_bola
        intersect_y_normalizado = (intersect_y_relativo / (altura_raquete / 2))
        ângulo_rebote = intersect_y_normalizado * (math.pi / 4)
        velocidade_bola_x = -velocidades_bola[dificuldade] * math.cos(ângulo_rebote)
        velocidade_bola_y = velocidades_bola[dificuldade] * -math.sin(ângulo_rebote)

    desenhar_jogo()

pygame.quit()
