
from src.prim import ejecutar_prim
from src.kruskal import ejecutar_kruskal
from src.dijkstral import ejecutar_dijkstra
from src.huffman import ejecutar_huffman

def mostrar_menu(opciones):
    print('Seleccione una opción:')
    for clave in sorted(opciones):
        print(f' {clave}) {opciones[clave][0]}')


def leer_opcion(opciones):
    while (a := input('Opción: ')) not in opciones:
        print('Opción incorrecta, vuelva a intentarlo.')
    return a


def ejecutar_opcion(opcion, opciones):
    opciones[opcion][1]()


def generar_menu(opciones, opcion_salida):
    opcion = None
    while opcion != opcion_salida:
        mostrar_menu(opciones)
        opcion = leer_opcion(opciones)
        ejecutar_opcion(opcion, opciones)
        print()


def menu_principal():
    opciones = {
        '0': ('Salir', salir),
        '1': ('Ejecutar PRIM', accion1),
        '2': ('Ejecutar KRUSKAL', accion2),
        '3': ('Ejecutar DIJKSTRA', accion3),
        '4': ('Ejecutar HUFFMAN', accion4),          
    }

    generar_menu(opciones, '0')


def accion1():
    print('\n[PRIM] Ejecutando algoritmo de Prim...')

    ejecutar_prim()

def accion2():
    print('\n[KRUSKAL] Ejecutando algoritmo de Kruskal...')
    ejecutar_kruskal()

def accion3():
    print('\n Ejecutando algoritmo de Dijkstra...')
    ejecutar_dijkstra()

def accion4():
    print('\n Ejecutando algoritmo de Huffman...')
    ejecutar_huffman()

def salir():
    print('Saliendo')


if __name__ == '__main__':
    menu_principal()