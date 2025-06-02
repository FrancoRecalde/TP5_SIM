import tkinter as tk
from tkinter import ttk
import csv

def cargar_csv(ruta):
    with open(ruta, newline='', encoding='utf-8') as archivo:
        reader = csv.DictReader(archivo, delimiter=';')
        campos = reader.fieldnames
        filas = [fila for fila in reader]
    return campos, filas

def mostrar_tabla():
    campos, filas = cargar_csv("vector_estado.csv")

    ventana = tk.Tk()
    ventana.title("Vector de Estado - Simulación TP5")

    tree = ttk.Treeview(ventana, columns=campos, show="headings")
    tree.pack(expand=True, fill="both")

    # Configurar encabezados
    for col in campos:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=100)

    # Insertar filas
    for fila in filas:
        valores = [fila[c] for c in campos]
        tree.insert("", "end", values=valores)

    # Scroll vertical
    scrollbar = ttk.Scrollbar(ventana, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    ventana.mainloop()

if __name__ == "__main__":
    mostrar_tabla()
