from menu import mostrar_menu
from fase1 import jogar_fase_1
from fase2 import jogar_fase_2
from fase3 import jogar_fase_3
from fase4 import jogar_fase_4
from fase5 import jogar_fase_5
from fase6 import jogar_fase_6
from fase7 import jogar_fase_7
from fase8 import jogar_fase_8
from fase9 import jogar_fase_9
from faseBoss import faseBoss
from final import tela_final
from gameover import Game_over
import estado_jogo

def main():
    mostrar_menu()

    while True:
        if estado_jogo.fase_atual == 0:
            mostrar_menu()
        if estado_jogo.fase_atual == 1:
            jogar_fase_1()
        elif estado_jogo.fase_atual == 2:
            jogar_fase_2()
        elif estado_jogo.fase_atual == 3:
            jogar_fase_3()
        elif estado_jogo.fase_atual == 4:
            jogar_fase_4()
        elif estado_jogo.fase_atual == 5:
            jogar_fase_5()
        elif estado_jogo.fase_atual == 6:
            jogar_fase_6()
        elif estado_jogo.fase_atual == 7:
            jogar_fase_7()
        elif estado_jogo.fase_atual == 8:
            jogar_fase_8()
        elif estado_jogo.fase_atual == 9:
            jogar_fase_9()
        elif estado_jogo.fase_atual == 10:
            faseBoss()
        elif estado_jogo.fase_atual == 11:
            tela_final()

if __name__ == "__main__":
    main()

#ORDEM DE FASES E ANIMAÇÕES
#Eidein chegando na frente da vila / fase 1 - Entrada da vila (chave)
#Alguem chamando ele para ir na guilda / fase 2 - Vila
#Ele recebendo a missão de ir ao templo / fase 3 - Floresta (orbe)
#Subindo a montanha e entrando no templo / fase 4 - Templo (espada)
#Tudo desabando e conversa sobre Dr.G / fase 5 - Esconderijo secreto (escudo)
#Trilha para o reino elfico / fase 6 - Trilha (anel)
#Chegada na ilha perdida / fase 7 - Ilha (emblema)
#Voltando para o reino elfico e inicio d batalha contra o imperio / fase 8 - Reino draconato (sangue)
#Chegada ao santuario / fase 9 - Santuario
#Final