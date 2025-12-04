import heapq
from collections import Counter

import matplotlib.pyplot as plt
import networkx as nx


class NodoHuffman:
    """
    Nodo para el arbol de Huffman
    freq: frecuencia del caracter
    char: caracter 
    izquierda o derecha: hijos
    """

    def __init__(self, freq, char=None, izquierda=None, derecha=None):
        self.freq = freq
        self.char = char
        self.izquierda = izquierda
        self.derecha = derecha

    # esto es para que heapq pueda hacer la comparacion de nodos
    def __lt__(self, otro):
        return self.freq < otro.freq


def cargar_texto_desde_txt(ruta_txt):
    """se lee el archivo de texto utilizado para la prueba completo y lo devuelve como string"""
    with open(ruta_txt, "r", encoding="utf-8") as archivo:
        return archivo.read()


def construir_arbol_huffman(texto):
    """ se construye el arbol de Huffman a partir del texto
      Complejidad:
        Tiempo: O(k log k), donde k es la cantidad de simbolos distintos
        Espacio: O(k) para guardar los nodos del arbol
    """
    if not texto:
        return None

    frecuencias = Counter(texto)

    # se crea un nodo por cada caracter
    monticulo = []
    for ch, f in frecuencias.items():
        monticulo.append(NodoHuffman(f, ch))

    heapq.heapify(monticulo)

    # este caso es si solo hay un carcter distinto 
    if len(monticulo) == 1:
        unico = monticulo[0]
        return NodoHuffman(unico.freq, None, unico, None)

    # se combinas los nodos de menor frecuencia hasta que quede solo uno
    while len(monticulo) > 1:
        n1 = heapq.heappop(monticulo)
        n2 = heapq.heappop(monticulo)
        nuevo = NodoHuffman(n1.freq + n2.freq, None, n1, n2)
        heapq.heappush(monticulo, nuevo)

    return monticulo[0]


def generar_codigos(nodo, prefijo="", codigos=None):
    """se crea el codigo binario para cada caracter del arbol de Huffman"""
    if codigos is None:
        codigos = {}

    if nodo is None:
        return codigos

    # si es hoja
    if nodo.char is not None:
        # si solo hay un caracter se le da 0
        codigos[nodo.char] = prefijo or "0"
    else:
        # izquierda es 0, derecha es 1
        generar_codigos(nodo.izquierda, prefijo + "0", codigos)
        generar_codigos(nodo.derecha, prefijo + "1", codigos)

    return codigos


def arbol_huffman_a_texto(nodo, nivel=0):
    """se devuelve la representacion en texto del arbol de Huffman."""
    if nodo is None:
        return ""

    sangria = "  " * nivel

    if nodo.char is not None:
        ch = nodo.char
        if ch == "\n":
            ch_mostrar = "\\n"
        elif ch == " ":
            ch_mostrar = "␣"
        else:
            ch_mostrar = ch

        linea = f"{sangria}Hoja: '{ch_mostrar}' (freq={nodo.freq})\n"
    else:
        linea = f"{sangria}Nodo interno (freq={nodo.freq})\n"
        linea += arbol_huffman_a_texto(nodo.izquierda, nivel + 1)
        linea += arbol_huffman_a_texto(nodo.derecha, nivel + 1)

    return linea


def agregar_nodos_y_aristas(grafo, nodo, nombre):
    """
    se carga el arbon en DiGraph de networkx para que se pueda dibujar.
    """
    if nodo.char is not None:
        if nodo.char == "\n":
            ch_mostrar = "\\n"
        elif nodo.char == " ":
            ch_mostrar = "␣"
        else:
            ch_mostrar = nodo.char
        etiqueta = f"{ch_mostrar}\n{nodo.freq}"
    else:
        etiqueta = f"*\n{nodo.freq}"

    grafo.add_node(nombre, label=etiqueta)

    if nodo.izquierda:
        nombre_izq = f"{nombre}0"
        grafo.add_edge(nombre, nombre_izq, bit="0")
        agregar_nodos_y_aristas(grafo, nodo.izquierda, nombre_izq)

    if nodo.derecha:
        nombre_der = f"{nombre}1"
        grafo.add_edge(nombre, nombre_der, bit="1")
        agregar_nodos_y_aristas(grafo, nodo.derecha, nombre_der)


def posicion_jerarquica(grafo, raiz, ancho=1.0, gap_vertical=0.2, nivel_vertical=0, x_centro=0.5, pos=None):
    """
    se calculan las posiciones para dibujar el arbol de forma ordenada
    """
    if pos is None:
        pos = {raiz: (x_centro, nivel_vertical)}
    else:
        pos[raiz] = (x_centro, nivel_vertical)

    hijos = list(grafo.successors(raiz))
    if not hijos:
        return pos

    dx = ancho / len(hijos)
    siguiente_x = x_centro - ancho / 2 - dx / 2

    for hijo in hijos:
        siguiente_x += dx
        pos = posicion_jerarquica(
            grafo,
            hijo,
            ancho=dx,
            gap_vertical=gap_vertical,
            nivel_vertical=nivel_vertical - gap_vertical,
            x_centro=siguiente_x,
            pos=pos
        )

    return pos


def dibujar_arbol_huffman(nodo, ruta_imagen):
    """se dibuja el arbon y se guarda como png"""
    if nodo is None:
        return

    grafo = nx.DiGraph()
    agregar_nodos_y_aristas(grafo, nodo, "root")

    posiciones = posicion_jerarquica(grafo, "root")

    plt.figure(figsize=(12, 6))
    nx.draw(grafo, posiciones, with_labels=False, arrows=True)

    etiquetas_nodos = nx.get_node_attributes(grafo, "label")
    nx.draw_networkx_labels(grafo, posiciones, labels=etiquetas_nodos, font_size=8)

    etiquetas_aristas = nx.get_edge_attributes(grafo, "bit")
    nx.draw_networkx_edge_labels(grafo, posiciones, edge_labels=etiquetas_aristas)

    plt.axis("off")
    plt.tight_layout()
    plt.savefig(ruta_imagen, dpi=200)
    plt.close()


def dibujar_frecuencias(texto, ruta_imagen):
    """se dibuja una grafica con las frecuencias"""
    if not texto:
        return

    frecuencias = Counter(texto)

    caracteres = []
    valores = []
    for ch, f in frecuencias.items():
        if ch == "\n":
            etiqueta = "\\n"
        elif ch == " ":
            etiqueta = "␣"
        else:
            etiqueta = ch
        caracteres.append(etiqueta)
        valores.append(f)

    plt.figure(figsize=(10, 4))
    plt.bar(caracteres, valores)
    plt.xlabel("Caracter")
    plt.ylabel("Frecuencia")
    plt.title("Frecuencias de caracteres (Huffman)")
    plt.tight_layout()
    plt.savefig(ruta_imagen, dpi=200)
    plt.close()


def ejecutar_huffman():
    print("\n[HUFFMAN] Ejecutando algoritmo de Huffman...")

    ruta_txt = "data/textos/mensaje_huffman.txt"
    texto = cargar_texto_desde_txt(ruta_txt)

    if not texto:
        print("El archivo de texto esta vacio.")
        return

    raiz = construir_arbol_huffman(texto)
    codigos = generar_codigos(raiz)
    texto_arbol = arbol_huffman_a_texto(raiz)

    print("\n[HUFFMAN] Tabla de codigos (caracter -> codigo):\n")
    for ch, codigo in codigos.items():
        if ch == "\n":
            ch_mostrar = "\\n"
        elif ch == " ":
            ch_mostrar = "␣"
        else:
            ch_mostrar = ch
        print(f"'{ch_mostrar}': {codigo}")

    print("\n[HUFFMAN] Arbol de Huffman (forma textual):\n")
    print(texto_arbol)

    ruta_arbol = "docs/evidencias/huffman_tree.png"
    ruta_freq = "docs/evidencias/huffman_freq.png"

    dibujar_arbol_huffman(raiz, ruta_arbol)
    dibujar_frecuencias(texto, ruta_freq)

    print(f"\nImagenes generadas: {ruta_arbol}, {ruta_freq}\n")


if __name__ == "__main__":
    ejecutar_huffman()
