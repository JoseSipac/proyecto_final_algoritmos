# Proyecto Final – Algoritmos de Grafos y Codificacion de Huffman

## Portada

**Universidad:** Universidad Da Vinci de Guatemala  
**Facultad:** Ingenieria
**Curso:** Analisis de Algoritmo
**Proyecto:** Implementacion de algoritmos de Prim, Kruskal, Dijkstra, Huffman
**Estudiante:** Jose Geovany Sipac Pixtun 
**Carnet:** 202301480 
**Fecha:** 03-12-2025

---

## Objetivos

### Objetivo general

Implementar y analizar cuatro algoritmos fundamentales como Prim, Kruskal, Dijkstra y Huffman, utilizando Python, aplicandolos sobre datos de entrada definidos como CSV y TXT, generando salidas visuales en imagenes PNG y gestionando el proyecto mediante un flujo de trabajo Gitflow.

### Objetivos especificos

1. Implementar los algoritmos de Prim y Kruskal para obtener arboles de expansion minima  a partir de un grafo no dirigido y ponderado leido desde un archivo CSV.
2. Implementar el algoritmo de Dijkstra para calcular las rutas mas cortas desde un nodo origen hacia todos los demas nodos del grafo.
3. Implementar el algoritmo de Huffman para construir un arbol de codificacion optima a partir de un texto y generar los codigos binarios asociados a cada caracter.
4. Generar representaciones graficas  de los resultados de cada algoritmo para documentar el comportamiento y facilitar su interpretacion.
5. Aplicar un flujo de trabajo de versionamiento basado en Gitflow, utilizando ramas de `feature`, `develop`, `main`, `release` y `hotfix`, dejando evidencia mediante capturas de comandos y PRs.

---

## Explicacion teorica de los algoritmos

### 1. Algoritmo de Prim

El algoritmo de Prim se utiliza para encontrar un Arbol de Expansion Minima (MST) en un grafo conexo, no dirigido y ponderado.  
La idea principal es construir el MST de forma incremental, comenzando desde un nodo cualquiera y, en cada paso, agregando la arista de menor peso que conecta un nodo ya visitado con un nodo no visitado.

Pasos generales:

1. Elegir un nodo inicial y marcarlo como visitado.
2. Colocar en una estructura en este caso, un `heap`/cola de prioridad todas las aristas que salen desde los nodos visitados hacia nodos no visitados.
3. Seleccionar la arista de menor peso que conecte con un nodo no visitado.
4. Agregar esa arista al MST y marcar el nuevo nodo como visitado.
5. Repetir hasta haber visitado todos los nodos del grafo.

El resultado es un conjunto de aristas que conectan todos los nodos con el costo total minimo, sin formar ciclos.

---

### 2. Algoritmo de Kruskal

El algoritmo de Kruskal tambien se usa para encontrar el Arbol de Expansion Minima (MST), pero su enfoque es diferente:

1. Toma todas las aristas del grafo y las ordena de menor a mayor peso.
2. Recorre la lista de aristas ordenadas y va agregando cada arista al MST si no forma un ciclo.
3. Para detectar ciclos de forma eficiente se utiliza una estructura de Conjuntos Disjuntos.
4. El proceso termina cuando se han agregado exactamente `|V| - 1` aristas.

---

### 3. Algoritmo de Dijkstra

El algoritmo de Dijkstra resuelve el problema de rutas mas cortas desde un nodo origen hacia todos los demas nodos del grafo, siempre que los pesos de las aristas sean no negativos.

1. Inicializa la distancia al origen como 0 y al resto de nodos como infinito.
2. Utiliza una cola de prioridad heap para ir seleccionando repetidamente el nodo con menor distancia provisional.
3. Desde ese nodo, intenta relajar las aristas: si pasar por ese nodo reduce la distancia a un vecino, se actualiza la distancia y el predecesor.
4. El proceso continua hasta haber procesado todos los nodos alcanzables.

Ademas de las distancias, se guarda el nodo anterior en el camino, lo que permite reconstruir la ruta completa desde el origen hacia cualquier nodo destino.

---

### 4. Algoritmo de Huffman

El algoritmo de Huffman es una tecnica de compresion sin perdida que asigna codigos binarios de longitud variable a los caracteres de un texto, de tal forma que:

- Los caracteres mas frecuentes obtienen codigos mas cortos.
- Los caracteres menos frecuentes obtienen codigos mas largos.
- El codigo resultante es prefijo, es decir, ningun codigo es prefijo de otro.

1. Calcular la frecuencia de cada caracter del texto.
2. Crear un nodo por cada caracter y ponerlos en una cola de prioridad min-heap ordenados por frecuencia.
3. Extraer los dos nodos con menor frecuencia, combinarlos en un nuevo nodo cuyo peso es la suma de ambos, y volver a insertarlo en el heap.
4. Repetir el proceso hasta que quede un solo nodo: la raiz del arbol de Huffman.
5. Recorrer el arbol, asignando un `0` al ir a la izquierda y un `1` al ir a la derecha, para generar los codigos binarios.

Este algoritmo es muy utilizado en esquemas de compresion como archivos, imagenes, etc.

---

## Complejidad teorica (O grande)

### Prim

- Implementacion con cola de prioridad `heapq`.
- Sea `V` el numero de nodos y `E` el numero de aristas.

**Complejidad de tiempo:**  
\[
O(E \log V)
\]

**Complejidad de espacio:**  
\[
O(V + E)
\]
por el grafo, el conjunto de visitados y la cola de prioridad.

---

### Kruskal

- Requiere ordenar las aristas y utilizar Union-Find.

**Complejidad de tiempo:**  
Ordenar aristas: \( O(E \log E) \approx O(E \log V) \)  
Operaciones de Union-Find: practicamente \( O(E) \) amortizado.

En total:
\[
O(E \log E) \approx O(E \log V)
\]

**Complejidad de espacio:**  
\[
O(V + E)
\]
por la lista de aristas y las estructuras de conjuntos disjuntos.

---

### Dijkstra

- Implementacion usando cola de prioridad `heapq` y listas de adyacencia.

**Complejidad de tiempo:**  
\[
O((V + E) \log V)
\]

**Complejidad de espacio:**  
\[
O(V + E)
\]
por el grafo, el diccionario de distancias y el diccionario de predecesores.

---

### Huffman

- Sea `k` el numero de simbolos distintos en el texto.

**Complejidad de tiempo:**

- Construccion del arbol: `O(k log k)` (por el uso del heap).
- Generacion de codigos: `O(k)`.

En total:
\[
O(k \log k)
\]

**Complejidad de espacio:**  
\[
O(k)
\]
por almacenar el arbol y la tabla de codigos.

---

## Formato de entrada

El proyecto utiliza dos tipos de archivos de entrada, ubicados en la carpeta `data/`:
Grafos para prim, kruskal y dijkstra
data/grafos/grafos_ciudades.csv
Textos para huffman
data/textos/mensaje_huffman.txt


## Ejecucion del programa

Python 3.x instalado.
Librerias adicionales: matplotlib y networkx

El archivo Princiapal es:
main.py

Teniendo un menu donde podemos elegir que algoritmo necesitamos ejecutar.

1 → Ejecutar Prim

2 → Ejecutar Kruskal

3 → Ejecutar Dijkstra

4 → Ejecutar Huffman

0 → Salir

Desde la Raiz podemos ejecutarlo asi:
python main.py

## Imagenes PNG generadas

Arbol de Expansion Minima – Prim
![Prim MST](docs/evidencias/prim_mst.png)

Arbol de Expansion Minima – Kruskal
![Kruskal MST](docs/evidencias/kruskal_mst.png)

Rutas mas cortas – Dijkstra
![Dijkstra Paths](docs/evidencias/dijkstra_paths.png)

Arbol de Huffman
![Huffman Tree](docs/evidencias/huffman_tree.png)

Frecuencias de Huffman
![Huffman Frequencies](docs/evidencias/huffman_freq.png)

## Flujo Gitflow aplicado

Para el versionamiento del proyecto se utilizo un flujo basado en Gitflow, con las siguientes ramas:

main: rama principal, contiene las versiones estables del proyecto.
develop: rama de desarrollo, donde se integran las funcionalidades antes de pasar a main.
feature/prim: implementacion y pruebas del algoritmo de Prim.
feature/kruskal: implementacion y pruebas del algoritmo de Kruskal.
feature/dijkstra: implementacion y pruebas del algoritmo de Dijkstra.
feature/huffman: implementacion y pruebas del algoritmo de Huffman.
release/v1.0.0: rama de preparacion para la version 1.0.0.
hotfix/...: rama utilizada para corregir un detalle puntual (por ejemplo, cambio de nombre en el README).

## Conclusiones finales

La implementacion de Prim y Kruskal permitio entender como diferentes enfoques pueden producir el mismo resultado: un arbol de expansion minima.

El algoritmo de Dijkstra mostro la importancia de las estructuras de datos eficientes, como las colas de prioridad, para resolver problemas de rutas mas cortas en grafos con pesos positivos.

El algoritmo de Huffman permitio relacionar estructuras de datos con aplicaciones reales de compresion de informacion, donde las frecuencias de los caracteres influyen directamente en la longitud de los codigos.

El uso de Gitflow ayudo a organizar el trabajo en ramas claras, facilitando el control de versiones y la integracion de cambios.

Combinar teoria, implementacion en codigo, generacion de imagenes y un flujo de versionamiento ordenado dio como resultado un proyecto mas completo, documentado y facil de explicar academicamente.
