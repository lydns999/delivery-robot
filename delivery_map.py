class BuildingMap:
    def __init__(self, width=10, height=10):
        self.width = width
        self.height = height
        # Ma trận cho tầng 1 và tầng 2 (0: Trống, 1: Chướng ngại vật, 2: Thang máy)
        self.floors = {
            1: [[0 for _ in range(width)] for _ in range(height)],
            2: [[0 for _ in range(width)] for _ in range(height)]
        }
        # Tọa độ cố định của thang máy ở cả 2 tầng
        self.elevator_pos = (4, 4)
        self._setup_map()

    def _setup_map(self):
        # Thiết lập thang máy
        ex, ey = self.elevator_pos
        self.floors[1][ey][ex] = 2
        self.floors[2][ey][ex] = 2

        # Đặt chướng ngại vật Tầng 1
        obstacles_f1 = [(1, 2), (2, 2), (3, 2), (4, 2), (6, 5), (6, 6)]
        for x, y in obstacles_f1:
            self.floors[1][y][x] = 1

        # Đặt chướng ngại vật Tầng 2
        obstacles_f2 = [(2, 4), (2, 5), (2, 6), (7, 1), (7, 2)]
        for x, y in obstacles_f2:
            self.floors[2][y][x] = 1

    def is_valid_step(self, floor, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.floors[floor][y][x] != 1 # Không va vào chướng ngại vật
        return False