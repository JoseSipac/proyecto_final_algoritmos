import heapq
import csv

import matplotlib.pyplot as plt
import networkx as nx


def cargar_grafo_desde_csv(ruta_csv):
    """
    Carga el grafo desde un archivo CSV que creamos para las pruebas.
    Esperando el siguiente formato: origen,destino,peso
    """
    grafo = {}
    aristas = []

    with open(ruta_csv, "r", encoding="utf-8", newline="") as archivo:
        lector = csv.reader(archivo)
        next(lector, None)  # saltamos el encabezado si lo hay

        for fila in lector:
            if not fila or len(fila) < 3:
                continue

            origen, destino, peso_str = fila

            try:
                peso = float(peso_str)
            except:
                # por si existe un texto que no es en alguna fila
                continue

            # si el nodo no existe se inicializa
            if origen not in grafo:
                grafo[origen] = []
            if destino not in grafo:
                grafo[destino] = []

            # el grafo no es dirijisdo se agrada en los dos sentidos
            grafo[origen].append((destino, peso))
            grafo[destino].append((origen, peso))

            # se guarda para posteriormente dibujarlo
            aristas.append((origen, destino, peso))

    return grafo, aristas


def prim(grafo):
    """
    Se implemneta la lista la devolucion de la lista de atistas del MST y el costo total
    Complejidad:
        Tiempo: O(E log V), usando cola de prioridad (heap)
        Espacio: O(V + E) por el grafo y las estructuras auxiliares
    """
    if not grafo:
        return [], 0.0

    # se inica con cualqueir nodo
    nodo_inicio = next(iter(grafo.keys()))
    visitados = set([nodo_inicio])

    # cola de prioridad
    cola = []
    for vecino, peso in grafo[nodo_inicio]:
        heapq.heappush(cola, (peso, nodo_inicio, vecino))

    mst = []
    costo_total = 0.0

    # esto se realiza mientras haya aristas y falten nodos por visitar
    while cola and len(visitados) < len(grafo):
        peso, u, v = heapq.heappop(cola)

        # si ya se ha visitado el nodo es ignorado
        if v in visitados:
            continue

        visitados.add(v)
        mst.append((u, v, peso))
        costo_total += peso

        # agregamos las nuevas aristas del nodo v
        for siguiente, peso2 in grafo[v]:
            if siguiente not in visitados:
                heapq.heappush(cola, (peso2, v, siguiente))

    return mst, costo_total


def dibujar_mst(aristas, mst, ruta_imagen):
    """
    Se dibuja el grafo y se resalta
    """
    G = nx.Graph()

    # se agregan todas la aristas
    for u, v, peso in aristas:
        G.add_edge(u, v, weight=peso)

    # se calculan las posiciones de los nodos
    posiciones = nx.spring_layout(G, seed=42)

    plt.figure(figsize=(8, 6))

    # se dibujar los nodos y aristas
    nx.draw_networkx_nodes(G, posiciones)
    nx.draw_networkx_edges(G, posiciones, alpha=0.4)
    nx.draw_networkx_labels(G, posiciones)

    # aristas del MST con otro color
    aristas_mst = [(u, v) for u, v, _ in mst]
    nx.draw_networkx_edges(
        G,
        posiciones,
        edgelist=aristas_mst,
        width=3,
        edge_color="red"
    )

    # se muestran los pesos
    etiquetas = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, posiciones, edge_labels=etiquetas)

    plt.axis("off")
    plt.tight_layout()
    plt.savefig(ruta_imagen, dpi=200)
    plt.close()


def ejecutar_prim():
    print("\n[PRIM] Ejecutando algoritmo de Prim...")

    # esta es la ruta del archivo de entrada
    ruta_csv = "data/grafos/grafos_ciudades.csv"

    grafo, aristas = cargar_grafo_desde_csv(ruta_csv)

    if not grafo:
        print("El grafo no se pudo cargar o está vacio.")
        return

    mst, costo_total = prim(grafo)

    print("\n[PRIM] Arbol de expansion minima (MST):")
    for u, v, peso in mst:
        print(f"{u} -- {v} (peso: {peso})")

    print(f"Costo total del MST: {costo_total}")
     
    # esta es la ruta para nuestra evidencia
    ruta_imagen = "docs/evidencias/prim_mst.png"
    dibujar_mst(aristas, mst, ruta_imagen)
    print(f"Imagen generada: {ruta_imagen}\n")


if __name__ == "__main__":
    ejecutar_prim()
