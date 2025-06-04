import practicas.Cirugia as Cirugia
import practicas.Clinica as Clinica
import practicas.Emergencias as Emergencias
from evento.Evento import Evento
from box.Box import Box
from sanitario.Sanitario import Sanitario
from main import rng
import csv


def prioridad(practica):
    return 2 if practica.__class__.__name__ == "Emergencias" else 1


def iniciar_colas(
    tiempo: int = 0,
    iteraciones: int = 0,
    desde: int = 0,
    media_llegada_cirugia: float = 60,
    llegada_clinica_min: float = 600,
    llegada_clinica_max: float = 840,
    llegada_emergencia_min: float = 360,
    llegada_emergencia_max: float = 600,
    duracion_min: float = 60,
    duracion_max: float = 120,
    sanit_s_min: float = 1,
    sanit_s_max: float = 3,
    edo_const_1: float = 3,
    edo_const_2: float = 0.05,
    h: float = 0.1,
    max_espera: int = 1
):
    vector_estado = []
    t = 0
    box = Box()
    box.set_libre()

    cola_espera = []
    eventos_futuros = []

    suma_espera_cirugia = suma_espera_clinica = suma_espera_emergencia = 0
    cant_turnos_cirugia = cant_turnos_clinica = cant_turnos_emergencia = 0

    cirugia = Cirugia.Cirugia(media_llegada_cirugia, duracion_min, duracion_max)
    clinica = Clinica.Clinica(llegada_clinica_min, llegada_clinica_max, duracion_min, duracion_max)
    emergencia = Emergencias.Emergencias(llegada_emergencia_min, llegada_emergencia_max, duracion_min, duracion_max)

    eventos_futuros += [
        Evento(cirugia.llegada, "llegada_cirugia", cirugia),
        Evento(clinica.llegada, "llegada_clinica", clinica),
        Evento(emergencia.llegada, "llegada_emergencia", emergencia)
    ]
    eventos_futuros.sort()

    for i in range(iteraciones):
        if not eventos_futuros:
            break

        evento = eventos_futuros.pop(0)
        t = evento.tiempo
        esta = box.estado()
        if t > tiempo:
            break
        random_duracion = None
        duracion_en_box = None
        random_sanit = None
        sanit_s = None
        tiempo_sanit = None

        # inicializar campos por defecto
        c_rnd, c_dur, c_lleg = "", "", ""
        cl_rnd, cl_dur, cl_lleg = "", "", ""
        e_rnd, e_dur, e_lleg = "", "", ""

        if evento.tipo.startswith("llegada"):
            practica = evento.practica
            nombre = practica.__class__.__name__.lower()

            if box.libre:
                box.set_ocupado()
                practica.duracion()
                random_duracion = practica.random_num_duracion
                duracion_en_box = practica.duracion_var
                fin_tipo = f"fin_{nombre}"
                eventos_futuros.append(Evento(t + duracion_en_box, fin_tipo, practica))

                if isinstance(practica, Cirugia.Cirugia):
                    cant_turnos_cirugia += 1
                elif isinstance(practica, Clinica.Clinica):
                    cant_turnos_clinica += 1
                else:
                    cant_turnos_emergencia += 1
            else:
                if len(cola_espera) < max_espera:
                    cola_espera.append(practica)

            practica.frecuencia_llegada(t)
            eventos_futuros.append(Evento(practica.llegada, evento.tipo, practica))

            if nombre == "cirugia":
                c_rnd, c_dur, c_lleg = round(practica.random_num_frecuencia, 4), round(practica.duracion_var, 2), round(practica.llegada, 2)
            elif nombre == "clinica":
                cl_rnd, cl_dur, cl_lleg = round(practica.random_num_frecuencia, 4), round(practica.duracion_var, 2), round(practica.llegada, 2)
            elif nombre == "emergencias":
                e_rnd, e_dur, e_lleg = round(practica.random_num_frecuencia, 4), round(practica.duracion_var, 2), round(practica.llegada, 2)

        elif evento.tipo.startswith("fin_"):
            box.set_sanitizando()
            sanitario = Sanitario(sanit_s_min, sanit_s_max, edo_const_1, edo_const_2, h)
            random_sanit = rng.random()
            sanit_s = 1 + random_sanit * (sanit_s_max - sanit_s_min)
            tiempo_sanit = sanitario.runge_kutta(sanit_s)
            eventos_futuros.append(Evento(t + tiempo_sanit, "_fin_sanitizacion"))

        elif evento.tipo == "_fin_sanitizacion":
            if cola_espera:
                cola_espera.sort(key=lambda p: (prioridad(p), p.llegada))
                proxima = cola_espera.pop(0)
                box.set_ocupado()
                proxima.duracion()
                random_duracion = proxima.random_num_duracion
                duracion_en_box = proxima.duracion_var
                fin_tipo = f"fin_{proxima.__class__.__name__.lower()}"
                eventos_futuros.append(Evento(t + duracion_en_box, fin_tipo, proxima))

                espera = t - proxima.llegada
                if isinstance(proxima, Cirugia.Cirugia):
                    suma_espera_cirugia += espera
                    cant_turnos_cirugia += 1
                elif isinstance(proxima, Clinica.Clinica):
                    suma_espera_clinica += espera
                    cant_turnos_clinica += 1
                else:
                    suma_espera_emergencia += espera
                    cant_turnos_emergencia += 1
            else:
                box.set_libre()

        eventos_futuros.sort()
        if t >= desde:
            registro = {
            "tiempo": round(t, 2),
            "evento": evento.tipo,

            "cirugia_rnd_llegada": c_rnd,
            "cirugia_duracion": c_dur,
            "cirugia_llegada": c_lleg,

            "clinica_rnd_llegada": cl_rnd,
            "clinica_duracion": cl_dur,
            "clinica_llegada": cl_lleg,

            "emergencia_rnd_llegada": e_rnd,
            "emergencia_duracion": e_dur,
            "emergencia_llegada": e_lleg,

            "box_rnd_duracion": round(random_duracion, 4) if random_duracion is not None else "",
            "box_duracion": round(duracion_en_box, 2) if duracion_en_box else "",
            "box_fin": round(t + duracion_en_box, 2) if duracion_en_box else "",

            "sanit_rnd": round(random_sanit, 4) if random_sanit else "",
            "sanit_s": round(sanit_s, 2) if sanit_s else "",
            "sanit_duracion": round(tiempo_sanit, 2) if tiempo_sanit else "",
            "sanit_fin": round(t + tiempo_sanit, 2) if tiempo_sanit else "",

            "estado_box": esta,
            "cola_normal": len([p for p in cola_espera if prioridad(p) == 1]),
            "cola_prioritaria": len([p for p in cola_espera if prioridad(p) == 2]),

            "espera_cirugia": round(suma_espera_cirugia, 2),
            "espera_clinica": round(suma_espera_clinica, 2),
            "espera_emergencia": round(suma_espera_emergencia, 2),

            "turnos_cirugia": cant_turnos_cirugia,
            "turnos_clinica": cant_turnos_clinica,
            "turnos_emergencia": cant_turnos_emergencia,

            "eventos_futuros": ", ".join(f"{ev.tipo}@{round(ev.tiempo, 2)}" for ev in eventos_futuros)
            }

            vector_estado.append(registro)

    with open("vector_estado.csv", mode="w", newline="", encoding="utf-8") as archivo:
        writer = csv.DictWriter(archivo, fieldnames=vector_estado[0].keys(), delimiter=';')
        writer.writeheader()
        writer.writerows(vector_estado)


if __name__ == "__main__":
    iniciar_colas(tiempo=10000, iteraciones=100, desde=2000)
