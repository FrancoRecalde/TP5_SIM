import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pandas as pd
from iniciar import iniciar_colas
from sanitario.Sanitario import Sanitario


def validar_parametros() -> bool:
    try:
        tiempo = int(ent_tiempo.get())
        iteraciones = int(ent_iteraciones.get())
        desde = int(ent_desde.get())

        if tiempo <= 0 or iteraciones <= 0:
            raise ValueError("Tiempo e iteraciones deben ser mayores que 0")

        def validar_rango(min_val, max_val, nombre):
            if float(min_val.get()) < 0 or float(max_val.get()) < 0:
                raise ValueError(f"{nombre} no puede ser negativo")
            if float(min_val.get()) >= float(max_val.get()):
                raise ValueError(f"{nombre}: el mínimo debe ser menor que el máximo")

        validar_rango(ent_clinica_min, ent_clinica_max, "Llegada clínica")
        validar_rango(ent_emergencia_min, ent_emergencia_max, "Llegada emergencia")
        validar_rango(ent_duracion_min_cir, ent_duracion_max_cir, "Duración cirugía")
        validar_rango(ent_duracion_min_cli, ent_duracion_max_cli, "Duración clínica")
        validar_rango(ent_duracion_min_em, ent_duracion_max_em, "Duración emergencia")
        validar_rango(ent_sanit_s_min, ent_sanit_s_max, "S sanitización")

        if float(ent_const_1.get()) < 0 or float(ent_const_2.get()) < 0:
            raise ValueError("Las constantes de la EDO no pueden ser negativas")
        if float(ent_h.get()) <= 0:
            raise ValueError("El paso h debe ser mayor que 0")
        if int(ent_max_espera.get()) < 0:
            raise ValueError("La espera máxima no puede ser negativa")

        return True
    except ValueError as e:
        messagebox.showerror("Error de validación", str(e))
        return False


def ejecutar_simulacion():
    if not validar_parametros():
        return
    try:
        iniciar_colas(
            tiempo=int(ent_tiempo.get()),
            iteraciones=int(ent_iteraciones.get()),
            desde=int(ent_desde.get()),
            media_llegada_cirugia=float(ent_media_cirugia.get()),
            llegada_clinica_min=float(ent_clinica_min.get()),
            llegada_clinica_max=float(ent_clinica_max.get()),
            llegada_emergencia_min=float(ent_emergencia_min.get()),
            llegada_emergencia_max=float(ent_emergencia_max.get()),
            duracion_min_cir=float(ent_duracion_min_cir.get()),
            duracion_max_cir=float(ent_duracion_max_cir.get()),
            duracion_min_cli=float(ent_duracion_min_cli.get()),
            duracion_max_cli=float(ent_duracion_max_cli.get()),
            duracion_min_em=float(ent_duracion_min_em.get()),
            duracion_max_em=float(ent_duracion_max_em.get()),
            sanit_s_min=float(ent_sanit_s_min.get()),
            sanit_s_max=float(ent_sanit_s_max.get()),
            edo_const_1=float(ent_const_1.get()),
            edo_const_2=float(ent_const_2.get()),
            h=float(ent_h.get()),
            max_espera=int(ent_max_espera.get())
        )
        messagebox.showinfo("Éxito", "Simulación completada. Se generó el archivo CSV.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al ejecutar la simulación: {e}")


def visualizar_excel():
    try:
        df = pd.read_csv("vector_estado.csv", delimiter=';')
        ventana = tk.Toplevel(root)
        ventana.title("Vector de Estado")
        ventana.geometry("1400x700")

        container = ttk.Frame(ventana)
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(container)
        scrollbar_y = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollbar_x = ttk.Scrollbar(container, orient="horizontal", command=canvas.xview)

        scrollable_frame = ttk.Frame(canvas)
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))

        tree = ttk.Treeview(scrollable_frame, show="headings")
        tree.pack(expand=True, fill='both')

        tree["columns"] = list(df.columns)

        for col in df.columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor='center')

        for _, row in df.iterrows():
            tree.insert("", "end", values=list(row))

    except FileNotFoundError:
        messagebox.showerror("Error", "No se encontró el archivo vector_estado.csv")


def mostrar_calculo_s():
    try:
        s_min = float(ent_sanit_s_min.get())
        s_max = float(ent_sanit_s_max.get())
        a = float(ent_const_1.get())
        b = float(ent_const_2.get())
        h = float(ent_h.get())

        sanitario = Sanitario(s_min, s_max, a, b, h)
        s_obj = s_max

        t = 0
        s = 0

        pasos = []
        while True:
            k1 = h * (a * t + b * s ** 2)
            k2 = h * (a * (t + h / 2) + b * (s + k1 / 2) ** 2)
            k3 = h * (a * (t + h / 2) + b * (s + k2 / 2) ** 2)
            k4 = h * (a * (t + h) + b * (s + k3) ** 2)
            delta_s = (k1 + 2 * k2 + 2 * k3 + k4) / 6
            pasos.append((round(t, 4), round(s, 4), round(k1, 4), round(k2, 4), round(k3, 4), round(k4, 4), round(delta_s, 4)))
            if s >= s_obj:
                break
            s += delta_s
            t += h


        ventana = tk.Toplevel(root)
        ventana.title("Runge-Kutta para cálculo de S")

        text = tk.Text(ventana, wrap="none", height=30, width=120, font=("Courier New", 10))
        text.pack(expand=True, fill="both")

        text.insert("end", f"S objetivo: {round(s_obj, 4)}\n\n")
        text.insert("end", "Paso\tS(t)\tk1\tk2\tk3\tk4\tΔS\n")
        text.insert("end", "-" * 90 + "\n")
        for fila in pasos:
            text.insert("end", "\t".join(map(str, fila)) + "\n")
        text.insert("end", f"\nTiempo estimado total: {round(t * 10, 4)} min")

    except Exception as e:
        messagebox.showerror("Error", str(e))


root = tk.Tk()
root.title("Simulación Centro Médico")
root.geometry("500x650")

frame = ttk.LabelFrame(root, text="Parámetros de Simulación", padding=15)
frame.pack(expand=True, fill="both", padx=10, pady=10)

campos = [
    ("Tiempo límite", "10000"),
    ("Iteraciones", "100"),
    ("Desde (mostrar)", "0"),
    ("Media llegada cirugía", "600"),
    ("Llegada clínica min", "600"),
    ("Llegada clínica max", "840"),
    ("Llegada emergencia min", "360"),
    ("Llegada emergencia max", "600"),
    ("Duración min cirugía", "60"),
    ("Duración max cirugía", "120"),
    ("Duración min clínica", "60"),
    ("Duración max clínica", "120"),
    ("Duración min emergencia", "70"),
    ("Duración max emergencia", "130"),
    ("Sanit S min", "1"),
    ("Sanit S max", "3"),
    ("Constante 1 (a)", "3"),
    ("Constante 2 (b)", "0.05"),
    ("Paso h", "0.1"),
    ("Máx espera en cola", "5")
]

entradas = []

for i, (label, default) in enumerate(campos):
    ttk.Label(frame, text=label + ":").grid(row=i, column=0, sticky='w', pady=2)
    entrada = ttk.Entry(frame)
    entrada.insert(0, default)
    entrada.grid(row=i, column=1, pady=2, padx=5)
    entradas.append(entrada)

(
    ent_tiempo, ent_iteraciones, ent_desde,
    ent_media_cirugia, ent_clinica_min, ent_clinica_max,
    ent_emergencia_min, ent_emergencia_max,
    ent_duracion_min_cir, ent_duracion_max_cir,
    ent_duracion_min_cli, ent_duracion_max_cli,
    ent_duracion_min_em, ent_duracion_max_em,
    ent_sanit_s_min, ent_sanit_s_max,
    ent_const_1, ent_const_2, ent_h, ent_max_espera
) = entradas

btn_frame = ttk.Frame(root, padding=10)
btn_frame.pack()

style = ttk.Style()
style.configure("TButton", padding=6, font=("Helvetica", 10, "bold"))

ttk.Button(btn_frame, text="Ejecutar Simulación", command=ejecutar_simulacion).grid(row=0, column=0, padx=10)
ttk.Button(btn_frame, text="Visualizar Excel", command=visualizar_excel).grid(row=0, column=1, padx=10)
ttk.Button(btn_frame, text="Mostrar cálculo de S", command=mostrar_calculo_s).grid(row=0, column=2, padx=10)

root.mainloop()
