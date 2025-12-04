import csv
import heapq

import matplotlib.pyplot as plt
import networkx as nx


def cargar_grafo_desde_csv(ruta_csv):
    """
    se carga el grafo en formato CVS no dirigido para que funcione el
    Formato esperado es el sigueinte: origen,destino,peso
    """
    grafo = {}
    aristas = []

    with open(ruta_csv, "r", encoding="utf-8", newline="") as archivo:
        lector = csv.reader(archivo)
        next(lector, None)  # si hay encabezado se lo salta

        for fila in lector:
            if not fila or len(fila) < 3:
                continue

            origen, destino, peso_str = fila

            try:
                peso = float(peso_str)
            except:
                # por si el peso contiene algo que no sea acorde a lo esperado
                continue

            if origen not in grafo:
                grafo[origen] = []
            if destino not in grafo:
                grafo[destino] = []

            # como se estan utilizando grafos no dirijidos se agragan en los dos sentidos
            grafo[origen].append((destino, peso))
            grafo[destino].append((origen, peso))

            aristas.append((origen, destino, peso))

    return grafo, aristas


def dijkstra(grafo, origen):
    """
    Implementación del algoritmo de Dijkstra para devolver las distancias minimas
    Complejidad:
        Tiempo: O((V + E) log V) usando cola de prioridad (heap)
        Espacio: O(V + E) por el grafo, distancias y predecesores
    """
    distancias = {}
    anterior = {}

    # se inician las distancias en infinito
    for nodo in grafo:
        distancias[nodo] = float("inf")
        anterior[nodo] = None

    distancias[origen] = 0.0

    # esta es la cola de prioridad
    cola = [(0.0, origen)]

    while cola:
        dist_actual, nodo_actual = heapq.heappop(cola)

        # si se tiene la mejor distanacia minima se ignora y se pasa a la sigueinte para validar
        if dist_actual > distancias[nodo_actual]:
            continue

        for vecino, peso in grafo[nodo_actual]:
            nueva_dist = dist_actual + peso
            if nueva_dist < distancias[vecino]:
                distancias[vecino] = nueva_dist
                anterior[vecino] = nodo_actual
                heapq.heappush(cola, (nueva_dist, vecino))

    return distancias, anterior


def reconstruir_camino(anterior, destino):
    """
    Recostruye el camino utilizando el diccionario anterior
    """
    camino = []
    actual = destino

    while actual is not None:
        camino.append(actual)
        actual = anterior[actual]

    camino.reverse()
    return camino


def dibujar_caminos_dijkstra(aristas, aristas_arbol, ruta_imagen):
    """
    Se dibuja el grafo siempre tomando el camino mas corto obtenido
    """
    G = nx.Graph()

    for u, v, peso in aristas:
        G.add_edge(u, v, weight=peso)

    posiciones = nx.spring_layout(G, seed=99)

    plt.figure(figsize=(8, 6))

    # grafo completo 
    nx.draw_networkx_nodes(G, posiciones)
    nx.draw_networkx_edges(G, posiciones, alpha=0.3)
    nx.draw_networkx_labels(G, posiciones)

    # aristas del árbol de caminos mas corto
    nx.draw_networkx_edges(
        G,
        posiciones,
        edgelist=aristas_arbol,
        width=3,
        edge_color="blue"
    )

    etiquetas = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, posiciones, edge_labels=etiquetas)

    plt.axis("off")
    plt.tight_layout()
    plt.savefig(ruta_imagen, dpi=200)
    plt.close()


def ejecutar_dijkstra():
    print("\n[DIJKSTRA] Ejecutando algoritmo de Dijkstra...")

    ruta_csv = "data/grafos/grafos_ciudades.csv"
    grafo, aristas = cargar_grafo_desde_csv(ruta_csv)

    if not grafo:
        print("El grafo no se pudo cargar o está vacio.")
        return

    print("Nodos disponibles:", ", ".join(str(n) for n in grafo.keys()))
    origen = input("Ingrese el nodo origen: ").strip()

    if origen not in grafo:
        print(f"El nodo origen '{origen}' no existe en el grafo.")
        return

    distancias, anterior = dijkstra(grafo, origen)

    print(f"\n[DIJKSTRA] Rutas mss cortas desde el nodo origen: {origen}\n")
    for nodo in grafo.keys():
        d = distancias[nodo]
        if d == float("inf"):
            print(f"{origen} -> {nodo}: NO ALCANZABLE")
        else:
            camino = reconstruir_camino(anterior, nodo)
            camino_str = " -> ".join(str(x) for x in camino)
            print(f"{origen} -> {nodo} (dist = {d}): {camino_str}")

    # se contruye e camino mas corto
    aristas_arbol = []
    for nodo, ant in anterior.items():
        if ant is not None:
            aristas_arbol.append((ant, nodo))

    # esta es la ruta de salida
    ruta_imagen = "docs/evidencias/dijkstra_paths.png"
    dibujar_caminos_dijkstra(aristas, aristas_arbol, ruta_imagen)
    print(f"\nImagen generada: {ruta_imagen}\n")


if __name__ == "__main__":
    ejecutar_dijkstra()
