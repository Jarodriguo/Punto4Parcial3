TAM_PAGINA = 32
SEGFAULT_ADDR = 0x1FF

def procesar(segmentos, reqs, marcos_libres):
    tabla_paginas = {}          # (segmento, página) -> marco
    cola_paginas = []
    resultados = []
    marcos_disponibles = list(marcos_libres)

    for req in reqs:
        # Buscar a qué segmento pertenece la dirección
        segmento = None
        base = None
        for nombre, inicio, tam in segmentos:
            if inicio <= req < inicio + tam:
                segmento = nombre
                base = inicio
                break

        # Si no pertenece a ningún segmento → Segmentation Fault
        if segmento is None:
            resultados.append((req, SEGFAULT_ADDR, "Segmentation Fault"))
            continue

        desplazamiento = req - base
        pagina = desplazamiento // TAM_PAGINA
        offset = desplazamiento % TAM_PAGINA
        clave = (segmento, pagina)

        if clave in tabla_paginas:
            marco = tabla_paginas[clave]
            direccion_fisica = (marco * TAM_PAGINA) + offset
            resultados.append((req, direccion_fisica, "Marco ya estaba asignado"))
        else:
            if marcos_disponibles:
                marco = marcos_disponibles.pop(0)
                accion = "Marco libre asignado"
            else:
                clave_retirada = cola_paginas.pop(0)
                marco = tabla_paginas.pop(clave_retirada)
                accion = "Marco asignado"

            tabla_paginas[clave] = marco
            cola_paginas.append(clave)
            direccion_fisica = (marco * TAM_PAGINA) + offset
            resultados.append((req, direccion_fisica, accion))

    return resultados


def print_results(results):
    for result in results:
        print(f"Req: {result[0]:#04x} Direccion Fisica: {result[1]:#04x} Acción: {result[2]}")


if __name__ == '__main__':
    marcos_libres = [0x0, 0x1, 0x2]
    reqs = [0x00, 0x12, 0x64, 0x65, 0x8D, 0x8F, 0x19, 0x18, 0xF1, 0x0B, 0xDF, 0x0A]
    segmentos = [
        ('.text', 0x00, 0x1A),
        ('.data', 0x40, 0x28),
        ('.heap', 0x80, 0x1F),
        ('.stack', 0xC0, 0x22),
    ]

    resultados = procesar(segmentos, reqs, marcos_libres)
    print_results(resultados)
