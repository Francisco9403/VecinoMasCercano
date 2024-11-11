import osmnx as ox
import networkx as nx

# Función para solicitar una ciudad válida
def obtener_ciudad():
    while True:
        lugar = input("Introduce la ciudad y el país (por ejemplo, 'Junín, Argentina'): ")
        try:
            grafo = ox.graph_from_place(lugar, network_type='drive')
            return grafo, lugar
        except ox._errors.InsufficientResponseError:
            print("No se pudo descargar la red de calles para la ciudad ingresada. Por favor, intenta de nuevo.")

# Función para obtener direcciones desde un archivo válido
def obtener_direcciones_desde_archivo():
    while True:
        ruta_archivo = input("Introduce la ruta del archivo de texto con las direcciones: ")
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as file:
                direcciones = [linea.strip() for linea in file.readlines()]
                if not direcciones:
                    raise ValueError("El archivo está vacío o mal formateado.")
            return direcciones
        except (FileNotFoundError, ValueError) as e:
            print(f"Ese ubicacion es erronea. Por favor, intenta de nuevo.")

# Función para solicitar un número válido de casas por segmento
def obtener_numero_segmentos():
    while True:
        try:
            limite_diarios = int(input("Introduce el número máximo de casas por segmento: "))
            if limite_diarios > 0:
                return limite_diarios
            else:
                print("El número debe ser mayor que 0. Inténtalo de nuevo.")
        except ValueError:
            print("Debes ingresar un número entero válido. Inténtalo de nuevo.")

# Descargar la red de calles de la ciudad especificada por el usuario
grafo, lugar = obtener_ciudad()
print("-" * 50)

# Obtener las direcciones desde el archivo proporcionado por el usuario
direcciones_usuario = obtener_direcciones_desde_archivo()

# Convertir las direcciones ingresadas en coordenadas geográficas (geocodificación)
ubicaciones = [ox.geocode(direccion) for direccion in direcciones_usuario]

# Obtener el nodo más cercano a cada ubicación (en la red de calles) usando las coordenadas (longitud, latitud)
nodos_casas = [ox.distance.nearest_nodes(grafo, latlong[1], latlong[0]) for latlong in ubicaciones]

# Calcular la matriz de distancias entre cada par de ubicaciones utilizando el grafo de calles
distancias = []
for i in range(len(nodos_casas)):
    fila = []
    for j in range(len(nodos_casas)):
        if i != j:
            distancia = nx.shortest_path_length(grafo, nodos_casas[i], nodos_casas[j], weight='length')
            fila.append(distancia)
        else:
            fila.append(0)
    distancias.append(fila)

# Función para resolver el Problema del Viajante (TSP) usando la heurística del vecino más cercano
def tsp_vecino_mas_cercano(distancias, limite):
    num_nodos = len(distancias)
    visitado = [False] * num_nodos
    recorridos = []
    distancia_total = 0
    inicio = 0

    while not all(visitado):
        tour = [inicio]
        visitado[inicio] = True
        distancia_segmento = 0
        contador = 0

        while contador < limite and not all(visitado):
            actual = tour[-1]
            siguiente = None
            distancia_minima = float('inf')

            for i in range(num_nodos):
                if not visitado[i] and distancias[actual][i] < distancia_minima:
                    siguiente = i
                    distancia_minima = distancias[actual][i]

            if siguiente is not None:
                tour.append(siguiente)
                visitado[siguiente] = True
                distancia_segmento += distancia_minima
                contador += 1

        distancia_segmento += distancias[tour[-1]][inicio]
        tour.append(inicio)

        recorridos.append((tour, distancia_segmento))
        distancia_total += distancia_segmento

    return recorridos, distancia_total

# Pedir al usuario que ingrese el número máximo de casas por segmento
print("-" * 50)
limite_diarios = obtener_numero_segmentos()

# Obtener los recorridos por segmentos y la distancia total recorrida
recorridos_segmentados, distancia_total = tsp_vecino_mas_cercano(distancias, limite_diarios)

print("-" * 50)
#print("\nMatriz de distancias entre ubicaciones:\n")
#for fila in distancias:
#    print(fila)
#print("\n" + "-" * 50)

print(f"\nRecorridos por segmentos (máximo de {limite_diarios} casas por segmento):\n")
for idx, (tour, distancia_segmento) in enumerate(recorridos_segmentados):
    print(f"Segmento {idx + 1} (Distancia: {distancia_segmento / 1000:.2f} km):")
    for i in tour:
        print(f"[Casa {i}, ({direcciones_usuario[i]})]")
    print("-" * 50)

print(f"\nDistancia total recorrida: {distancia_total / 1000:.2f} Kilómetros")
print("-" * 50)

#ox.plot_graph(grafo)





r"""
Convertir direcciones (si las tienes) a coordenadas (geocodificación)
ubicaciones = [

    error(502 mentros)  6600 metros(Distancia real)   6098 metros(Estimarcion del programa)  
    ox.geocode("418 Siria, Junin, Buenos Aires"),   #Deposito
    ox.geocode("27 Newbery, Junin, Buenos Aires"), 
    ox.geocode("1500 Belgrano, Junin, Buenos Aires"),

    error(960 metros)  9500 metros (Distancia real)  8540 metros(Estimarcion del programa)  
    ox.geocode("76, Doctor Calp, Eusebio Marcilla, Junín, Partido de Junín, Buenos Aires, B6000, Argentina"),   #Deposito
    ox.geocode("1022, Presidente Quintana, Libertad, Junín, Partido de Junín, Buenos Aires, B6000, Argentina"),
    ox.geocode("77, Dorrego, El Picaflor, Junín, Partido de Junín, Buenos Aires, 6000, Argentina"), 
]
"""

r"""
PS C:\Users\usuario\Desktop> python "Alternativa.py"
Introduce la ciudad y el país (por ejemplo, 'Junín, Argentina'): Junín, Argentina
Introduce una dirección (o escribe 'fin' para terminar): 418 Siria, Junin, Buenos Aires
Introduce una dirección (o escribe 'fin' para terminar): 1500 Belgrano, Junin, Buenos Aires
Introduce una dirección (o escribe 'fin' para terminar): 27 Newbery, Junin, Buenos Aires
Introduce una dirección (o escribe 'fin' para terminar): 1386, Italia, Uocra, Junín, Partido de Junín, Buenos Aires, B6000, Argentina
Introduce una dirección (o escribe 'fin' para terminar): 77, Dorrego, El Picaflor, Junín, Partido de Junín, Buenos Aires, 6000, Argentina
Introduce una dirección (o escribe 'fin' para terminar): fin
--------------------------------------------------

Matriz de distancias entre ubicaciones:

[0, 2202.2509999999993, 1690.5590000000002, 1216.7439999999997, 2314.91]
[2199.132, 0, 2233.627, 987.3159999999999, 3760.936000000001]
[1864.275, 2209.22, 0, 2456.767999999999, 1558.053]
[1216.736, 987.8219999999999, 2489.029, 0, 3531.6459999999997]
[2318.3830000000003, 3737.682, 1909.6050000000002, 3533.986, 0]

--------------------------------------------------
Introduce el número máximo de casas por segmento: 2

Recorridos por segmentos (máximo de 2 casas por segmento):

Segmento 1 (Distancia: 4.40 km):
[Casa 0, (418 Siria, Junin, Buenos Aires)]
[Casa 3, (1386, Italia, Uocra, Junín, Partido de Junín, Buenos Aires, B6000, Argentina)]
[Casa 1, (1500 Belgrano, Junin, Buenos Aires)]
[Casa 0, (418 Siria, Junin, Buenos Aires)]
--------------------------------------------------
Segmento 2 (Distancia: 5.57 km):
[Casa 0, (418 Siria, Junin, Buenos Aires)]
[Casa 2, (27 Newbery, Junin, Buenos Aires)]
[Casa 4, (77, Dorrego, El Picaflor, Junín, Partido de Junín, Buenos Aires, 6000, Argentina)]
[Casa 0, (418 Siria, Junin, Buenos Aires)]
--------------------------------------------------

Distancia total recorrida: 9.97 Kilómetros
--------------------------------------------------
PS C:\Users\usuario\Desktop> 
"""