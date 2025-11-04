from menu import mostrar_menu
from fase1 import jogar_fase_1
from fase2 import jogar_fase_2
from gameover import Game_over
 
def main():
    jogando = True 
    while jogando:
        mostrar_menu()
        jogar_fase_1()
        jogar_fase_2()
        jogando = Game_over()

if __name__ == "__main__":
    main()

#ORDEM DE FASES E ANIMAÇÕES
#Eidein chegando na frente da vila / fase 1 - Entrada da vila
#Alguem chamando ele para ir na guilda / fase 2 - Vila
#Ele recebendo a missão de ir ao templo / fase 3 - Floresta
#Subindo a montanha e entrando no templo / fase 4 - Templo
#Tudo desabando e conversa sobre Dr.G / fase 5 - Esconderijo secreto
#Trilha para o reino elfico / fase 6 - Trilha
#Chegada na ilha perdida / fase 7 - Ilha
#Voltando para o reino elfico e inicio d batalha contra o imperio / fase 8 - Reino draconato
#Chegada ao santuario / fase 9 - Santuario
#Final