from menu import mostrar_menu
from fase1 import jogar_fase_1
from gameover import Game_over
 
def main():
    jogando = True 
    while jogando:
        mostrar_menu()
        jogar_fase_1()
        jogando = Game_over()

if __name__ == "__main__":
    main()
