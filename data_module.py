
def get_adj_matrix(number):
    file = open(f"Taxicab_{number}.txt", "r")
    lines = file.readlines()
    file.close()
    n = int(lines[0].replace('n = ', ''))
    print("Кол-во вершин:", n)
    matrix = []
    for i in range(n):
        matrix.append([0] * n)
    points = []
    for i in range(1, len(lines)):
        elements = lines[i].split('\t')
        x, y = int(elements[0]), int(elements[1])
        points.append([x, y])

    for i in range(n):
        x, y = points[i]
        for j in range(i + 1, n):
            a, b = points[j]
            dest = abs(x - a) + abs(y - b)
            matrix[i][j] = dest
            matrix[j][i] = dest
    # print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in matrix]))
    return matrix


def write_solution(depot, max_route_cost, total_cost, n, routes):
    with open(rf"Agafonova_{n}_1.txt", "w", encoding='utf-8') as file:
        file.write(f"c Депо = {depot + 1}, самый длинный цикл = {max_route_cost}, суммарная длина = {total_cost},\n")
        list_edges = get_list_edges(routes, depot)
        file.write(f"p edge {n} {len(list_edges)}\n")
        for edge in list_edges:
            file.write(f"e {edge[0] + 1} {edge[1] + 1}\n")

def get_list_edges(routes, depot):
    list_edges = []
    for route in routes:
        if len(route) == 0:
            continue
        edge = sorted((depot, route[0]))
        if not list_edges.__contains__(edge):
            list_edges.append(edge)
        if len(route) <= 1:
            continue
        for i in range(1, len(route)):
            edge = sorted((route[i - 1], route[i]))
            if not list_edges.__contains__(edge):
                list_edges.append(edge)
        edge = sorted((depot, route[len(route)-1]))
        if not list_edges.__contains__(edge):
            list_edges.append(edge)
    return sorted(list_edges)