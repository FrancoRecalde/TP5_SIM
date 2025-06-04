import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pandas as pd
from iniciar import iniciar_colas
from sanitario.Sanitario import Sanitario



def abrir_interfaz():
    def ejecutar_simulacion():
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
                duracion_min=float(ent_duracion_min.get()),
                duracion_max=float(ent_duracion_max.get()),
                sanit_s_min=float(ent_sanit_s_min.get()),
                sanit_s_max=float(ent_sanit_s_max.get()),
                edo_const_1=float(ent_const_1.get()),
                edo_const_2=float(ent_const_2.get()),
                h=float(ent_h.get()),
                max_espera=int(ent_max_espera.get())
            )
            messagebox.showinfo("Éxito", "Simulación completada. Se generó el archivo CSV.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")


    def visualizar_excel():
        try:
            df = pd.read_csv("vector_estado.csv", delimiter=';')
            ventana = tk.Toplevel(root)
            ventana.title("Vector de Estado")

            container = ttk.Frame(ventana)
            container.pack(fill="both", expand=True)

            canvas = tk.Canvas(container)
            scrollbar_y = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
            scrollbar_x = ttk.Scrollbar(container, orient="horizontal", command=canvas.xview)

            scrollable_frame = ttk.Frame(canvas)
            scrollable_frame.bind(
                "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

            canvas.pack(side="left", fill="both", expand=True)
            scrollbar_y.pack(side="right", fill="y")
            scrollbar_x.pack(side="bottom", fill="x")

            tree = ttk.Treeview(scrollable_frame)
            tree.pack(expand=True, fill='both')

            tree["columns"] = list(df.columns)
            tree["show"] = "headings"

            for col in df.columns:
                tree.heading(col, text=col)
                tree.column(col, width=100)

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
            s_obj = s_max  # Se usa el máximo como objetivo explícitamente

            t = 0
            s = 0

            pasos = []
            while s < s_obj:
                k1 = h * (a * t + b * s ** 2)
                k2 = h * (a * (t + h / 2) + b * (s + k1 / 2) ** 2)
                k3 = h * (a * (t + h / 2) + b * (s + k2 / 2) ** 2)
                k4 = h * (a * (t + h) + b * (s + k3) ** 2)
                delta_s = (k1 + 2 * k2 + 2 * k3 + k4) / 6
                pasos.append((round(t, 4), round(s, 4), round(k1, 4), round(k2, 4), round(k3, 4), round(k4, 4), round(delta_s, 4)))
                s += delta_s
                t += h

            ventana = tk.Toplevel(root)
            ventana.title("Runge-Kutta para cálculo de S")

            text = tk.Text(ventana, wrap="none", height=30, width=100)
            text.pack(expand=True, fill="both")

            text.insert("end", f"S objetivo: {round(s_obj, 4)}\n\n")
            text.insert("end", "Paso\tS(t)\tk1\tk2\tk3\tk4\tΔS\n")
            text.insert("end", "-------------------------------------------------------------\n")
            for t_step, s_step, k1, k2, k3, k4, delta in pasos:
                text.insert("end", f"{t_step}\t{s_step}\t{k1}\t{k2}\t{k3}\t{k4}\t{delta}\n")
            text.insert("end", f"\nTiempo estimado total: {round(t * 10, 4)} min")

        except Exception as e:
            messagebox.showerror("Error", str(e))


    root = tk.Tk()
    root.title("Simulación Centro Médico")

    frame = ttk.Frame(root, padding=10)
    frame.pack(expand=True, fill="both")

    campos = [
        ("Tiempo límite", "10000"),
        ("Iteraciones", "100"),
        ("Desde (mostrar)", "0"),
        ("Media llegada cirugía", "600"),
        ("Llegada clínica min", "600"),
        ("Llegada clínica max", "840"),
        ("Llegada emergencia min", "360"),
        ("Llegada emergencia max", "600"),
        ("Duración min", "60"),
        ("Duración max", "120"),
        ("Sanit S min", "1"),
        ("Sanit S max", "3"),
        ("Constante 1 EDO (a)", "3"),
        ("Constante 2 EDO (b)", "0.05"),
        ("Paso h", "0.1"),
        ("Máx espera en cola", "5")
    ]

    entradas = []

    for i, (label, default) in enumerate(campos):
        ttk.Label(frame, text=label).grid(row=i, column=0, sticky='w')
        entrada = ttk.Entry(frame)
        entrada.insert(0, default)
        entrada.grid(row=i, column=1)
        entradas.append(entrada)

    (
        ent_tiempo,
        ent_iteraciones,
        ent_desde,
        ent_media_cirugia,
        ent_clinica_min,
        ent_clinica_max,
        ent_emergencia_min,
        ent_emergencia_max,
        ent_duracion_min,
        ent_duracion_max,
        ent_sanit_s_min,
        ent_sanit_s_max,
        ent_const_1,
        ent_const_2,
        ent_h,
        ent_max_espera
    ) = entradas

    btn_frame = ttk.Frame(root, padding=10)
    btn_frame.pack()

    btn_simular = ttk.Button(btn_frame, text="Ejecutar Simulación", command=ejecutar_simulacion)
    btn_simular.grid(row=0, column=0, padx=5)

    btn_ver = ttk.Button(btn_frame, text="Visualizar Excel", command=visualizar_excel)
    btn_ver.grid(row=0, column=1, padx=5)

    btn_sanit = ttk.Button(btn_frame, text="Mostrar cálculo de S", command=mostrar_calculo_s)
    btn_sanit.grid(row=0, column=2, padx=5)

    root.mainloop()



abrir_interfaz()