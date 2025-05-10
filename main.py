import copy
import math
import random
from data_module import get_adj_matrix, write_solution

def recalculate_routes(new_depot, old_depot, routes):
    other_nodes = [node for route in routes for node in route]
    other_nodes.remove(new_depot)
    other_nodes.append(old_depot)
    random.shuffle(other_nodes)
    new_routes = [[] for _ in range(m)]
    for i, node in enumerate(other_nodes):
        new_routes[i % m].append(node)
    return new_routes

def simulated_annealing(adj_matrix, m, initial_temp=1000, cooling_rate=0.995, stop_temp=1e-3, max_iter=1000):
    n = len(adj_matrix)
    vertices = list(range(n))

    # Начальное случайное решение
    def initial_solution():
        depot = random.choice(vertices)
        other_nodes = [v for v in vertices if v != depot]
        random.shuffle(other_nodes)
        routes = [[] for _ in range(m)]
        for i, node in enumerate(other_nodes):
            routes[i % m].append(node)
        return depot, routes

    def route_cost(route, depot):
        path = [depot] + route + [depot]
        return sum(adj_matrix[path[i]][path[i + 1]] for i in range(len(path) - 1))

    def total_cost(routes, depot):
        route_costs = [route_cost(r, depot) for r in routes]
        return max(route_costs), sum(route_costs)

    # Получение соседнего решения
    def neighbor(depot, routes):
        new_routes = copy.deepcopy(routes)
        operation = random.choice(['move_vertex', 'swap_vertices', 'change_depot'])
        # Перенести вершину в другой маршрут
        if operation == 'move_vertex':
            from_idx = random.randint(0, m - 1)
            if new_routes[from_idx]:
                node = random.choice(new_routes[from_idx])
                new_routes[from_idx].remove(node)
                to_idx = random.randint(0, m - 1)
                new_routes[to_idx].append(node)
        # Поменять местами две вершины маршрута
        elif operation == 'swap_vertices':
            r_idx = random.randint(0, m - 1)
            if len(new_routes[r_idx]) >= 2:
                i, j = random.sample(range(len(new_routes[r_idx])), 2)
                new_routes[r_idx][i], new_routes[r_idx][j] = new_routes[r_idx][j], new_routes[r_idx][i]
        # Изменить депо
        elif operation == 'change_depot':
            new_depot = random.choice([v for v in vertices if v != depot])
            new_routes = recalculate_routes(new_depot, depot, new_routes)
            return new_depot, new_routes
        return depot, new_routes

    # Имитация отжига
    current_depot, current_routes = initial_solution()
    current_max_cost, current_total_cost = total_cost(current_routes, current_depot)
    best_solution = (current_depot, current_routes)
    best_cost = (current_max_cost, current_total_cost)

    temp = initial_temp
    while temp > stop_temp:
        for _ in range(max_iter):
            new_depot, new_routes = neighbor(current_depot, current_routes)
            new_max_cost, new_total_cost = total_cost(new_routes, new_depot)

            delta = new_max_cost - current_max_cost
            if delta < 0 or (delta == 0 and new_total_cost < current_total_cost) or random.random() < math.exp(
                    -delta / temp):
                current_depot, current_routes = new_depot, new_routes
                current_max_cost, current_total_cost = new_max_cost, new_total_cost
                if (current_max_cost < best_cost[0]) or (
                        current_max_cost == best_cost[0] and current_total_cost < best_cost[1]):
                    best_solution = (current_depot, copy.deepcopy(current_routes))
                    best_cost = (current_max_cost, current_total_cost)
                    print(current_depot, best_cost)
        temp *= cooling_rate

    return best_solution, best_cost

n = 64
adj_matrix = get_adj_matrix(n)
m = int(math.log2(n))
solution, cost = simulated_annealing(adj_matrix, m, initial_temp=5000, cooling_rate=0.995, stop_temp=1e-3,
                                     max_iter=1000)
print("Депо:", solution[0])
print("Маршруты:", solution[1])
print("Максимальная стоимость:", cost[0])
print("Общая стоимость:", cost[1])
write_solution(solution[0], cost[0], cost[1], n, solution[1])
