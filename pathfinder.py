import heapq

class PathFinder:
    def __init__(self, building_map):
        self.map = building_map

    def heuristic(self, a, b):
        # Khoảng cách Manhattan + chi phí đổi tầng
        (f1, x1, y1) = a
        (f2, x2, y2) = b
        return abs(x1 - x2) + abs(y1 - y2) + abs(f1 - f2) * 10

    def find_path(self, start, goal):
        """
        start/goal format: (floor, x, y)
        """
        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = {start: 0}

        while open_set:
            _, current = heapq.heappop(open_set)

            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                return path[::-1]

            f, x, y = current
            neighbors = []

            # Di chuyển 4 hướng trên cùng 1 tầng
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if self.map.is_valid_step(f, nx, ny):
                    neighbors.append((f, nx, ny))

            # Chuyển tầng qua thang máy
            ex, ey = self.map.elevator_pos
            if (x, y) == (ex, ey):
                other_floor = 2 if f == 1 else 1
                neighbors.append((other_floor, x, y))

            for neighbor in neighbors:
                # Chi phí đổi tầng = 5, di chuyển thường = 1
                cost = 5 if neighbor[0] != f else 1
                tentative_g = g_score[current] + cost

                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + self.heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score, neighbor))

        return None