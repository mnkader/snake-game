import queue
import time

class Algorithms:
    def __init__(self, grid_x, grid_y, grid):
        self.grid = grid
        self.X = grid_x
        self.Y = grid_y


    def get_neighbors(self, position, obstacles : list):
        in_grid_neighbors = []
        neighbors = [[position[0] + 10, position[1]],
                    [position[0] - 10, position[1]],
                    [position[0], position[1] + 10],
                    [position[0], position[1] - 10]]
        
        for pos in neighbors:
            if self.is_valid_pos(pos, obstacles):
                in_grid_neighbors.append(pos)
        return in_grid_neighbors
    
    def is_valid_pos(self, pos : tuple, obstacles : list):
        for obstacle in obstacles:
            if pos in obstacle:
                return False
        if pos[0] < 0 or pos[0] >= self.X or pos[1] < 0 or pos[1] >= self.Y:
            return False
        return True

    def breath_first_search(self, start : tuple, end : tuple, obstacles : list):
        q = [start]
        visited = {tuple(pos): False for pos in self.grid}
        visited[start] = True

        prev = {tuple(pos): None for pos in self.grid}
        start_timer = time.perf_counter()
        while q:
            node = q.pop(0)
            neighbors = self.get_neighbors(node, obstacles)
            for next_node in neighbors:
                if not visited[tuple(next_node)] :#and is position free:
                    q.append(tuple(next_node))
                    visited[tuple(next_node)] = True
                    prev[tuple(next_node)] = node
            end_timer = time.perf_counter()
            if (end_timer - start_timer) > 1:
                print(f'Stuck in a loop at breath_first_search')

        
        path = list()
        prev_node = end
        start_node_found = False
        while not start_node_found:
            if prev[prev_node] is None:
                return []
            prev_node = prev[prev_node]
            if prev_node == start:
                path.append(end)
                return path
            path.insert(0, prev_node)
        
        return []

    def distance(self, food, n):
        # Manhattan distance
        return abs(food[0]-n[0]) + abs(food[1]-n[1])

    def get_least_costly_node(self, neighbors, end : tuple):
        least_costly_node = neighbors[0]
        least_costly = self.distance(end, least_costly_node)
        for next_node in neighbors:
            cost_of_travel = self.distance(end, next_node)
            if least_costly > cost_of_travel:
                least_costly = cost_of_travel
                least_costly_node = next_node
        return least_costly_node  

    def a_star(self, start : tuple, end : tuple, obstacle_list : list):
        obstacles = obstacle_list.copy()
        q = queue.PriorityQueue()
        q.put((0, start))
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0
        count = 0
        starttime = time.perf_counter()
        endtime = 0
        while q: 
            node = q.get()[1]

            neighbors = self.get_neighbors(node, obstacles)
            if neighbors is None or len(neighbors) == 0:
                break

            for next_node in neighbors:
                next_node = tuple(next_node)
                new_cost = cost_so_far[node] + 10   

                if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                    cost_so_far[next_node] = new_cost
                    cost_of_travel = new_cost + self.distance(end, next_node)
                    q.put((cost_of_travel, tuple(next_node)))
                    came_from[tuple(next_node)] = node
            if node == end:
                break
            else:
                count +=1
                if node == (490, 490) and  node != end:
                    return []
            endtime = time.perf_counter()
            if (endtime-starttime) > 1:
                return []
        current = end
        path = [current]
        for _ in range(len(came_from)):
            current = came_from[current]
            path.append(current)
            if current == start:
                break

        return path