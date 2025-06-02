import practicas.Cirugia as Cirugia
import practicas.Clinica as Clinica
import practicas.Emergencias as Emergencias
from evento.Evento import Evento
from box.Box import Box
from sanitario.Sanitario import Sanitario
from main import rng
import csv


def prioridad(practica):
    if practica.__class__.__name__ == "Emergencias":
        return 2
    return 1  # Cirugía o Clínica


def iniciar_colas(tiempo: int = 0, iteraciones: int = 0, desde: int = 0) -> None:
    vector_estado = []
    t = 0
    box = Box()
    box.set_libre()

    cola_espera = []
    eventos_futuros = []

    # Iniciar primeras prácticas
    cirugia = Cirugia.Cirugia()
    clinica = Clinica.Clinica()
    emergencia = Emergencias.Emergencias()

    eventos_futuros.append(Evento(tiempo=cirugia.llegada, tipo="llegada_cirugia", practica=cirugia))
    eventos_futuros.append(Evento(tiempo=clinica.llegada, tipo="llegada_clinica", practica=clinica))
    eventos_futuros.append(Evento(tiempo=emergencia.llegada, tipo="llegada_emergencia", practica=emergencia))
    eventos_futuros.sort()

    print("\n📅 INICIO DE LA SIMULACIÓN")
    for i in range(iteraciones):
        if not eventos_futuros:
            print("✅ No hay más eventos futuros. Fin de simulación.")
            break

        evento = eventos_futuros.pop(0)
        t = evento.tiempo

        print(f"\n================ Iteración {i + 1} ================")
        print(f"🕒 Tiempo actual: {t:.2f} minutos")
        print(f"📌 Evento procesado: {evento.tipo}")
        esta = box.estado()
        print(f"📦 Estado del box: {esta}")
        print(f"🎫 Cantidad en cola: {len(cola_espera)}")

        random_duracion = None  # por defecto no hay random para duración

        if evento.tipo.startswith("llegada"):
            practica = evento.practica
            nombre = practica.__class__.__name__

            print(f"🧍‍♂️ Llega una práctica de tipo: {nombre}")

            if box.libre:
                print(f"✅ Box libre → comienza la práctica de {nombre}")
                box.set_ocupado()
                #practica.duracion()
                random_duracion = round(practica.random_num_duracion, 4)
                print(f"   - Duración estimada: {practica.duracion_var:.2f} minutos")
                fin_tipo = f"fin_{nombre.lower()}"
                eventos_futuros.append(Evento(t + practica.duracion_var, tipo=fin_tipo, practica=practica))
            else:
                if len(cola_espera) < 5:
                    print(f"⏳ Box ocupado → se encola {nombre}")
                    cola_espera.append(practica)
                else:
                    print(f"❌ Se retira {nombre} por exceso de espera (cola llena)")

            # Reprogramar próxima llegada
            practica.frecuencia_llegada(t)
            eventos_futuros.append(Evento(practica.llegada, tipo=evento.tipo, practica=practica))
            print(f"   - Llegada futura programada: {practica.llegada:.2f} minutos")

        elif evento.tipo.startswith("fin_"):
            nombre = evento.practica.__class__.__name__
            print(f"🏁 Fin de práctica de {nombre}")
            print("🧼 Iniciando sanitización del box...")
            box.set_sanitizando()
            sanitario = Sanitario()
            tiempo_sanit = sanitario.calcular_tiempo()
            print(f"   - Tiempo estimado de sanitización: {tiempo_sanit:.2f} minutos")
            eventos_futuros.append(Evento(t + tiempo_sanit, tipo="_fin_sanitizacion"))

        elif evento.tipo == "_fin_sanitizacion":
            print(f"🧽 Fin de sanitización")
            if cola_espera:
                cola_espera.sort(key=lambda p: (prioridad(p), p.llegada))
                proxima = cola_espera.pop(0)
                nombre = proxima.__class__.__name__
                #proxima.duracion()
                random_duracion = round(proxima.random_num_duracion, 4)
                print(f"🎉 Ingresa {nombre} desde la cola al box, con duración {proxima.duracion_var:.2f}")
                box.set_ocupado()
                fin_tipo = f"fin_{nombre.lower()}"
                eventos_futuros.append(Evento(t + proxima.duracion_var, tipo=fin_tipo, practica=proxima))
            else:
                print("✅ No hay prácticas esperando → box queda libre")
                box.set_libre()

        eventos_futuros.sort()

        registro = {
            "iteracion": i + 1,
            "tiempo": round(t, 2),
            "evento": evento.tipo,
            "box_estado": esta,
            "cola_espera": len(cola_espera),
            "tipo_practica": evento.practica.__class__.__name__ if evento.practica else "—",
            "tiempo_duracion": round(evento.practica.duracion_var, 2) if evento.practica else None,
            "tiempo_llegada": round(evento.practica.llegada, 2) if evento.practica else None,
            "random_duracion": random_duracion,
            "random_llegada": round(evento.practica.random_num_frecuencia, 4) if evento.practica else None
        }

        vector_estado.append(registro)

    print("\n🏁 SIMULACIÓN FINALIZADA\n")
    with open("vector_estado.csv", mode="w", newline="", encoding="utf-8") as archivo:
        writer = csv.DictWriter(archivo, fieldnames=vector_estado[0].keys(), delimiter=';')
        writer.writeheader()
        writer.writerows(vector_estado)


if __name__ == "__main__":
    iniciar_colas(tiempo=100000, iteraciones=10, desde=0)
