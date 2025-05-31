import random

seed = 12345

random.seed(seed)


def generar_numero_aleatorio(n):
    for i in range(n):
        numero = random.uniform(0, 1)
        print(f"Número aleatorio {i + 1}: {numero:.2f}")




if __name__ == "__main__":
    # Generar un número aleatorio y mostrarlo
    n = 100
    generar_numero_aleatorio(n)
    print("Generación de números aleatorios completada.")