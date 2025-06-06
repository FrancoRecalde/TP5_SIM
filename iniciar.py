import practicas.Cirugia as Cirugia
import practicas.Clinica as Clinica
import practicas.Emergencias as Emergencias
from evento.Evento import Evento
from box.Box import Box
from sanitario.Sanitario import Sanitario
from RNG import rng
import csv


def prioridad(practica):
    return 2 if practica.__class__.__name__ == "Emergencias" else 1


def iniciar_colas(
    tiempo,
    iteraciones,
    desde,
    media_llegada_cirugia,
    llegada_clinica_min,
    llegada_clinica_max,
    llegada_emergencia_min,
    llegada_emergencia_max,
    duracion_min_cir,
    duracion_max_cir,
    duracion_min_cli,
    duracion_max_cli,
    duracion_min_em,
    duracion_max_em,
    sanit_s_min,
    sanit_s_max,
    edo_const_1,
    edo_const_2,
    h,
    max_espera
):
    vector_estado = []
    t = 0
    box = Box()
    box.set_libre()

    cola_espera = []
    eventos_futuros = []

    suma_espera_cirugia = suma_espera_clinica = suma_espera_emergencia = 0
    cant_turnos_cirugia = cant_turnos_clinica = cant_turnos_emergencia = 0

    tiempo_total_sanit = 0

    cirugia = Cirugia.Cirugia(media_llegada_cirugia, duracion_min_cir, duracion_max_cir)
    clinica = Clinica.Clinica(llegada_clinica_min, llegada_clinica_max, duracion_min_cli, duracion_max_cli)
    emergencia = Emergencias.Emergencias(llegada_emergencia_min, llegada_emergencia_max, duracion_min_em, duracion_max_em)

    eventos_futuros = [Evento(0, "inicio", None)]

    last_c_lleg = ""
    last_cl_lleg = ""
    last_e_lleg = ""

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

        c_rnd, c_dur, c_lleg = "", "", ""
        cl_rnd, cl_dur, cl_lleg = "", "", ""
        e_rnd, e_dur, e_lleg = "", "", ""

        rechazada = False

        if evento.tipo == "inicio":
            cirugia.frecuencia_llegada(0)
            cirugia.duracion()
            clinica.frecuencia_llegada(0)
            clinica.duracion()
            emergencia.frecuencia_llegada(0)
            emergencia.duracion()

            eventos_futuros += [
                Evento(cirugia.llegada, "llegada_cirugia", cirugia),
                Evento(clinica.llegada, "llegada_clinica", clinica),
                Evento(emergencia.llegada, "llegada_emergencia", emergencia)
            ]
            eventos_futuros.sort()

            c_rnd, c_dur, c_lleg = round(cirugia.random_num_frecuencia, 4), round(cirugia.llegada - t, 2), round(cirugia.llegada, 2)
            cl_rnd, cl_dur, cl_lleg = round(clinica.random_num_frecuencia, 4), round(clinica.llegada - t, 2), round(clinica.llegada, 2)
            e_rnd, e_dur, e_lleg = round(emergencia.random_num_frecuencia, 4), round(emergencia.llegada - t, 2), round(emergencia.llegada, 2)

            last_c_lleg = c_lleg
            last_cl_lleg = cl_lleg
            last_e_lleg = e_lleg

            if t >= desde:
                registro = {
                    "tiempo": 0,
                    "evento": "inicio",

                    "cirugia_rnd_llegada": c_rnd,
                    "cirugia_duracion": c_dur,
                    "cirugia_llegada": c_lleg,

                    "clinica_rnd_llegada": cl_rnd,
                    "clinica_duracion": cl_dur,
                    "clinica_llegada": cl_lleg,

                    "emergencia_rnd_llegada": e_rnd,
                    "emergencia_duracion": e_dur,
                    "emergencia_llegada": e_lleg,

                    "box_rnd_duracion": "",
                    "box_duracion": "",
                    "box_fin": "",

                    "sanit_rnd": "",
                    "sanit_s": "",
                    "sanit_duracion": "",
                    "sanit_fin": "",

                    "estado_box": box.estado(),
                    "cola_normal": 0,
                    "cola_prioritaria": 0,

                    "espera_cirugia": 0,
                    "espera_clinica": 0,
                    "espera_emergencia": 0,

                    "turnos_cirugia": 0,
                    "turnos_clinica": 0,
                    "turnos_emergencia": 0,

                    "prom_espera_cirugia": 0,
                    "prom_espera_clinica": 0,
                    "prom_espera_emergencia": 0,

                    "tasa_ocupacion_sanit": 0,

                    "rechazada": False,

                    "eventos_futuros": ", ".join(f"{ev.tipo}@{round(ev.tiempo, 2)}" for ev in eventos_futuros)
                }

                vector_estado.append(registro)
            continue
        
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
                    cola_espera.append((practica, t))
                else:
                    rechazada = True

            practica.frecuencia_llegada(t)
            eventos_futuros.append(Evento(practica.llegada, evento.tipo, practica))

            if nombre == "cirugia":
                c_rnd, c_dur, c_lleg = round(practica.random_num_frecuencia, 4), round(practica.llegada - t, 2), round(practica.llegada, 2)
                last_c_lleg = c_lleg
            elif nombre == "clinica":
                cl_rnd, cl_dur, cl_lleg = round(practica.random_num_frecuencia, 4), round(practica.llegada - t, 2), round(practica.llegada, 2)
                last_cl_lleg = cl_lleg
            elif nombre == "emergencias":
                e_rnd, e_dur, e_lleg = round(practica.random_num_frecuencia, 4), round(practica.llegada - t, 2), round(practica.llegada, 2)
                last_e_lleg = e_lleg

        elif evento.tipo.startswith("fin_"):
            box.set_sanitizando()
            sanitario = Sanitario(sanit_s_min, sanit_s_max, edo_const_1, edo_const_2, h)
            random_sanit = rng.random()
            sanit_s = 1 + random_sanit * (sanit_s_max - sanit_s_min)
            tiempo_sanit = sanitario.runge_kutta(sanit_s)
            tiempo_total_sanit += tiempo_sanit
            eventos_futuros.append(Evento(t + tiempo_sanit, "_fin_sanitizacion"))

        elif evento.tipo == "_fin_sanitizacion":
            if cola_espera:
                cola_espera.sort(key=lambda p: (prioridad(p[0]), p[1]))
                proxima, llegada_cola = cola_espera.pop(0)
                box.set_ocupado()
                proxima.duracion()
                random_duracion = proxima.random_num_duracion
                duracion_en_box = proxima.duracion_var
                fin_tipo = f"fin_{proxima.__class__.__name__.lower()}"
                eventos_futuros.append(Evento(t + duracion_en_box, fin_tipo, proxima))

                espera = t - llegada_cola
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
                "cirugia_llegada": last_c_lleg,

                "clinica_rnd_llegada": cl_rnd,
                "clinica_duracion": cl_dur,
                "clinica_llegada": last_cl_lleg,

                "emergencia_rnd_llegada": e_rnd,
                "emergencia_duracion": e_dur,
                "emergencia_llegada": last_e_lleg,

                "box_rnd_duracion": round(random_duracion, 4) if random_duracion is not None else "",
                "box_duracion": round(duracion_en_box, 2) if duracion_en_box else "",
                "box_fin": round(t + duracion_en_box, 2) if duracion_en_box else "",

                "sanit_rnd": round(random_sanit, 4) if random_sanit else "",
                "sanit_s": round(sanit_s, 2) if sanit_s else "",
                "sanit_duracion": round(tiempo_sanit, 2) if tiempo_sanit else "",
                "sanit_fin": round(t + tiempo_sanit, 2) if tiempo_sanit else "",

                "estado_box": box.estado(),
                "cola_normal": len([p for p in cola_espera if prioridad(p[0]) == 1]),
                "cola_prioritaria": len([p for p in cola_espera if prioridad(p[0]) == 2]),

                "espera_cirugia": round(suma_espera_cirugia, 2),
                "espera_clinica": round(suma_espera_clinica, 2),
                "espera_emergencia": round(suma_espera_emergencia, 2),

                "turnos_cirugia": cant_turnos_cirugia,
                "turnos_clinica": cant_turnos_clinica,
                "turnos_emergencia": cant_turnos_emergencia,

                "prom_espera_cirugia": round(suma_espera_cirugia / cant_turnos_cirugia, 2) if cant_turnos_cirugia else 0,
                "prom_espera_clinica": round(suma_espera_clinica / cant_turnos_clinica, 2) if cant_turnos_clinica else 0,
                "prom_espera_emergencia": round(suma_espera_emergencia / cant_turnos_emergencia, 2) if cant_turnos_emergencia else 0,

                "tasa_ocupacion_sanit": round((tiempo_total_sanit / t) * 100, 2) if t else 0,

                "rechazada": rechazada,

                "eventos_futuros": ", ".join(f"{ev.tipo}@{round(ev.tiempo, 2)}" for ev in eventos_futuros)
            }

            vector_estado.append(registro)

    with open("vector_estado.csv", mode="w", newline="", encoding="utf-8") as archivo:
        writer = csv.DictWriter(archivo, fieldnames=vector_estado[0].keys(), delimiter=';')
        writer.writeheader()
        writer.writerows(vector_estado)
