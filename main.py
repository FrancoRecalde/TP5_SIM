from TP2_SIM.iniciar import *
import random




def main():
    tiempo = input("Ingrese el tiempo de simulación (en minutos): ")
    iteraciones = input("Ingrese el número de iteraciones a mostrar: ")
    desde = input("Ingrese el tiempo desde el cual se desea mostrar la simulación: ")
    
    iniciar_colas(tiempo, iteraciones, desde)
    print("This is the main function of the TP2_SIM module.")
    # Add your code logic here
    
    
if __name__ == "__main__":
    SEED = 12345
    rng = random.Random(SEED)
    main()