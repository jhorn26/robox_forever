def create_level(coord):
    corners_number = len(coord["corners_positions"])
    walls = []
    dimension = find_dimension(coord)
    coord["dimension"] = [dimension]
    #Encontra todos os pontos das arestas dos polígonos
    for i in range(corners_number):
        walls = find_all_walls(coord["corners_positions"][i], coord["corners_positions"][(i+1) % corners_number], walls)
    for k in coord["corners_positions"]:
        walls.append(k)
    coord["walk_positions"] = find_all_inside([find_one_inside(dimension[0], dimension[1], walls)], walls + coord["walls_positions"])
    coord["walls_positions"] += walls
    return coord
    
#Encontra todos os pontos entre dois cantos do poligono entre os quais há uma aresta
def find_all_walls(P, Q, walls):
    if P[0] == Q[0]:
        diff = Q[1]-P[1]
        for k in range(1, abs(diff)):
            walls.append((P[0], P[1] + int(abs(diff)/diff)*k))
    else: 
        diff = Q[0]-P[0]
        for k in range(1, abs(Q[0]-P[0])):
            walls.append((P[0] + int(abs(diff)/diff)*k, P[1]))
    return walls

#Encontra um ponto no interior do polígono
def find_one_inside(m, n, walls):
    for i in range(m):
        thickness = 0
        for j in range(n):
            if (j, i) in walls:
                thickness += 1
            if (j, i) in walls and (j + 1, i) not in walls and thickness == 1:
                return (j + 1, i)

#Encontra todos os pontos do polígono
def find_all_inside(inside_set, walls):
    #Inicialização
    to_visit_set = [inside_set[0]]
    while len(to_visit_set) > 0:
        #Escolhe um ponto do conjunto de pontos a serem visitados
        point = to_visit_set[0]
        #Se um vizinho do ponto escolhido não está na aresta do polígono, não foi visitado e não está na lista de pontos para visitar, adiciona ele 
        #no interior do poligono e na lista de pontos para visitar
        neighbors = [(point[0] + 1, point[1]), (point[0] - 1, point[1]), (point[0], point[1] + 1), (point[0], point[1] - 1)]
        for n in neighbors:
            if n not in inside_set and n not in to_visit_set and n not in walls:
                inside_set.append(n) 
                to_visit_set.append(n)      
        to_visit_set.remove(point)
    return inside_set

#Encontra a dimensão do polígono (lados do menor retangulo que o contem)
def find_dimension(coord):
    M = 0
    N = 0
    for k in coord["corners_positions"]:
        if k[0] > M:
            M = k[0]
        if k[1] > N:
            N = k[1]
    return (M, N)