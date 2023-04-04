# importing libraries
import cv2
from multiprocessing import Semaphore

import datos
from datos import tracking_general, TTL_MAX
from functions import get_iou, coincide_rostro_en_tracking, coincide_cuerpo_en_tracking

semaforo = Semaphore(1)


def seguimiento_cuerpo(cuerpos, nombre_camara):
    for cuerpo in cuerpos:
        # verifico si no se ha incluido en el tracking para insertarla
        if not coincide_cuerpo_en_tracking(cuerpo, tracking_general):
            cuerpo["ttl"] = TTL_MAX

            semaforo.acquire()
            tracking_general.append(cuerpo)
            semaforo.release()

        for persona_seguida in tracking_general:
            # si se detecta procedente de un local sin camara, asignarle la camara actual
            if cuerpo["nombre"] == persona_seguida["nombre"] and persona_seguida["nombre_camara"] == "NINGUNO":
                semaforo.acquire()
                persona_seguida["nombre_camara"] = nombre_camara
                semaforo.release()

            # print("IOU (Seguimiento cuerpo)", get_iou(cuerpo["coordenadas_cuerpo"], persona_seguida["coordenadas_cuerpo"]))
            if get_iou(cuerpo["coordenadas_cuerpo"], persona_seguida["coordenadas_cuerpo"]) > 0.1:

                semaforo.acquire()
                persona_seguida["coordenadas_cuerpo"] = cuerpo["coordenadas_cuerpo"]
                semaforo.release()

                if cuerpo["confianza_cuerpo"] > persona_seguida["confianza_cuerpo"]:

                    semaforo.acquire()

                    persona_seguida["confianza_cuerpo"] = cuerpo["confianza_cuerpo"]
                    persona_seguida["nombre"] = cuerpo["nombre"]

                    semaforo.release()

                semaforo.acquire()
                persona_seguida["ttl"] = TTL_MAX
                semaforo.release()


def seguimiento_rostro(rostros, nombre_camara):
    for rostro in rostros:
        # verifico si no se ha incluido en el tracking para insertarla
        if not coincide_rostro_en_tracking(rostro, tracking_general):
            rostro["ttl"] = TTL_MAX

            semaforo.acquire()
            tracking_general.append(rostro)
            semaforo.release()

        for persona_seguida in tracking_general:
            # si se detecta procedente de un local sin camara, asignarle la camara actual
            if rostro["nombre"] == persona_seguida["nombre"] and persona_seguida["nombre_camara"] == "NINGUNO":
                semaforo.acquire()
                persona_seguida["nombre_camara"] = nombre_camara
                semaforo.release()

            # print("IOU (Seguimiento rostro)", get_iou(rostro["coordenadas_rostro"], persona_seguida["coordenadas_rostro"]))
            if get_iou(rostro["coordenadas_rostro"], persona_seguida["coordenadas_rostro"]) > 0.1:

                semaforo.acquire()
                persona_seguida["coordenadas_rostro"] = rostro["coordenadas_rostro"]
                semaforo.release()

                if rostro["distancia_rostro"] < persona_seguida["distancia_rostro"]:

                    semaforo.acquire()

                    persona_seguida["distancia_rostro"] = rostro["distancia_rostro"]
                    persona_seguida["nombre"] = rostro["nombre"]

                    semaforo.release()

                semaforo.acquire()
                persona_seguida["ttl"] = TTL_MAX
                semaforo.release()

            # historial(persona_seguida["nombre"])


def seguimiento(rostros, cuerpos, nombre_camara):
    seguimiento_cuerpo(cuerpos, nombre_camara)
    seguimiento_rostro(rostros, nombre_camara)

def seguimiento_cuerpo_2(cuerpos, nombre_camara):
    for cuerpo in cuerpos:
        # verifico si no se ha incluido en el tracking para insertarla
        if not coincide_cuerpo_en_tracking(cuerpo, tracking_general):
            cuerpo["ttl"] = TTL_MAX

            semaforo.acquire()
            tracking_general.append(cuerpo)
            semaforo.release()

        for persona_seguida in tracking_general:
            # si se detecta procedente de un local sin camara, asignarle la camara actual
            if cuerpo["nombre"] == persona_seguida["nombre"] and persona_seguida["nombre_camara"] == "NINGUNO":
                semaforo.acquire()
                persona_seguida["nombre_camara"] = nombre_camara
                semaforo.release()

            # print("IOU (Seguimiento cuerpo)", get_iou(cuerpo["coordenadas_cuerpo"], persona_seguida["coordenadas_cuerpo"]))
            if get_iou(cuerpo["coordenadas_cuerpo"], persona_seguida["coordenadas_cuerpo"]) > 0.1:

                semaforo.acquire()
                persona_seguida["coordenadas_cuerpo"] = cuerpo["coordenadas_cuerpo"]
                semaforo.release()

                if cuerpo["confianza_cuerpo"] > persona_seguida["confianza_cuerpo"]:

                    semaforo.acquire()

                    persona_seguida["confianza_cuerpo"] = cuerpo["confianza_cuerpo"]
                    persona_seguida["nombre"] = cuerpo["nombre"]

                    semaforo.release()

                semaforo.acquire()
                persona_seguida["ttl"] = TTL_MAX
                semaforo.release()
            
            if cuerpo["coordenadas_rostro"] != (0,0,0,0):
                if get_iou(cuerpo["coordenadas_rostro"], persona_seguida["coordenadas_rostro"]) > 0.1:

                    semaforo.acquire()
                    persona_seguida["coordenadas_rostro"] = cuerpo["coordenadas_rostro"]
                    semaforo.release()

                    if cuerpo["distancia_rostro"] < persona_seguida["distancia_rostro"]:

                        semaforo.acquire()

                        persona_seguida["distancia_rostro"] = cuerpo["distancia_rostro"]
                        persona_seguida["nombre"] = cuerpo["nombre"]

                        semaforo.release()

                    semaforo.acquire()
                    persona_seguida["ttl"] = TTL_MAX
                    semaforo.release()

def rectangulo_nombre_rostros(coordenadas_local, nombre_camara, frame, camara):
    for persona in tracking_general:
        # Si se encuentra en el local actual y la camara actual
        if persona["coordenadas_local"] == coordenadas_local and persona["nombre_camara"] == nombre_camara:
            if persona["coordenadas_cuerpo"] != (0, 0, 0, 0):
                cv2.rectangle(frame,
                              (persona["coordenadas_cuerpo"][0],
                               persona["coordenadas_cuerpo"][1]),
                              (persona["coordenadas_cuerpo"][2],
                               persona["coordenadas_cuerpo"][3]),
                              datos.VERDE, 2)

                cv2.rectangle(frame,
                              (persona["coordenadas_cuerpo"][0],
                               persona["coordenadas_cuerpo"][3] - 35),
                              (persona["coordenadas_cuerpo"][2],
                               persona["coordenadas_cuerpo"][3]),
                              datos.VERDE, cv2.FILLED)
                cv2.putText(frame, persona["nombre"], (persona["coordenadas_cuerpo"][0] + 6, persona["coordenadas_cuerpo"][3] - 6),
                            datos.font, 1.0, datos.BLANCO, 1)

                if persona["ttl"] == 0:
                    i = 0
                    for (top, right, bottom, left) in camara["rectangulos"]:
                        # print("IOU (Rectangulo nombre rostros)", get_iou(persona["coordenadas_cuerpo"], (top, right, bottom, left)))
                        if get_iou(persona["coordenadas_cuerpo"], (top, right, bottom, left)) > 0.1:
                            semaforo.acquire()
                            # persona["coordenadas_rostro"] = camara["rectangulos_relacionados"][i]
                            persona["coordenadas_local"] = camara["locales_relacionados"][i]
                            persona["nombre_camara"] = camara["camaras_relacionadas"][i]
                            persona["ttl"] = datos.TTL_MAX
                            semaforo.release()
                        i = i + 1


def rectangulos_entrada_salida(camara, frame):
    for (left, top, right, bottom) in camara["rectangulos"]:
        cv2.rectangle(frame, (left, top), (right, bottom), datos.MARRON, 2)
