import csv
import matplotlib.pyplot as plt
import networkx as nx


class ConjuntoDisjunto:
    """
    Estructura de conjuntos disjuntos para usar en el algoritmo de Kruskal.
    """

    def __init__(self, elementos):
        # en el inicio cada elemento es su propio padre
        self.padre = {x: x for x in elementos}
        self.rango = {x: 0 for x in elementos}

    def encontrar(self, x):
        # se busca el representante de cada conjunto 
        if self.padre[x] != x:
            self.padre[x] = self.encontrar(self.padre[x])
        return self.padre[x]

    def unir(self, a, b):
        # se unen los conjuntos que tienen a y b
        raiz_a = self.encontrar(a)
        raiz_b = self.encontrar(b)

        if raiz_a == raiz_b:
            # si ya estaban en el mismo conjunto
            return False

        # se unen por rango
        if self.rango[raiz_a] < self.rango[raiz_b]:
            self.padre[raiz_a] = raiz_b
        elif self.rango[raiz_a] > self.rango[raiz_b]:
            self.padre[raiz_b] = raiz_a
        else:
            self.padre[raiz_b] = raiz_a
            self.rango[raiz_a] += 1

        return True


def cargar_nodos_y_aristas(ruta_csv):
    """
    Se lee archivo CSV y devuelvee nodos y aristas.
    Formato esperado para que funcione: origen,destino,peso
    """
    nodos = set()
    aristas = []

    with open(ruta_csv, "r", encoding="utf-8", newline="") as archivo:
        lector = csv.reader(archivo)
        next(lector, None)  # se salta el encabezado si existe 

        for fila in lector:
            if not fila or len(fila) < 3:
                continue

            origen, destino, peso_str = fila

            try:
                peso = float(peso_str)
            except:
                # esto es por si hay una fila que no sea numero
                continue

            nodos.add(origen)
            nodos.add(destino)
            aristas.append((origen, destino, peso))

    return list(nodos), aristas


def kruskal(nodos, aristas):
    """
    Implementacion del algoritmo de Kruskal devuelve aristas del MST y el costo total
    Complejidad:
        Tiempo: O(E log E) ≈ O(E log V) por el ordenamiento de aristas
        Espacio: O(V + E) por las estructuras de conjuntos disjuntos y la lista de aristas
    """
    if not nodos or not aristas:
        return [], 0.0

    ds = ConjuntoDisjunto(nodos)
    # se ordenan las aristas por el peso 
    aristas_ordenadas = sorted(aristas, key=lambda x: x[2])

    mst = []
    costo_total = 0.0

    for u, v, peso in aristas_ordenadas:
        if ds.unir(u, v):
            mst.append((u, v, peso))
            costo_total += peso

            # siempre hay una arista menos que la cantidad de nodos
            if len(mst) == len(nodos) - 1:
                break

    return mst, costo_total


def dibujar_mst(aristas, mst, ruta_imagen):
    """
    Dibuja el grafo completo y resalta el MST.
    """
    G = nx.Graph()

    # se agregan todas las aristaas del grafo
    for u, v, peso in aristas:
        G.add_edge(u, v, weight=peso)

    posiciones = nx.spring_layout(G, seed=24)

    plt.figure(figsize=(8, 6))
    nx.draw_networkx_nodes(G, posiciones)
    nx.draw_networkx_edges(G, posiciones, alpha=0.4)
    nx.draw_networkx_labels(G, posiciones)

    # se colocal en rojo las aristasn MST
    aristas_mst = [(u, v) for u, v, _ in mst]
    nx.draw_networkx_edges(
        G,
        posiciones,
        edgelist=aristas_mst,
        width=3,
        edge_color="red"
    )

    etiquetas = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, posiciones, edge_labels=etiquetas)

    plt.axis("off")
    plt.tight_layout()
    plt.savefig(ruta_imagen, dpi=200)
    plt.close()


def ejecutar_kruskal():
    print("\n[KRUSKAL] Ejecutando algoritmo de Kruskal...")

    ruta_csv = "data/grafos/grafos_ciudades.csv"
    nodos, aristas = cargar_nodos_y_aristas(ruta_csv)

    if not nodos or not aristas:
        print("No se pudieron cargar nodos o aristas desde el CSV.")
        return

    mst, costo_total = kruskal(nodos, aristas)

    print("\n[KRUSKAL] Arbol de expansion minima (MST):")
    for u, v, peso in mst:
        print(f"{u} -- {v} (peso: {peso})")

    print(f"Costo total del MST: {costo_total}\n")

    ruta_imagen = "docs/evidencias/kruskal_mst.png"
    dibujar_mst(aristas, mst, ruta_imagen)
    print(f"Imagen generada: {ruta_imagen}\n")


if __name__ == "__main__":
    ejecutar_kruskal()
