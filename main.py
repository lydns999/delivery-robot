import pygame
import sys
from delivery_map import BuildingMap
from pathfinder import PathFinder

# Khởi tạo Pygame
pygame.init()

CELL_SIZE = 50
WIDTH, HEIGHT = 10, 10
SCREEN_WIDTH = WIDTH * CELL_SIZE * 2 + 100 # Hiển thị 2 tầng song song
SCREEN_HEIGHT = HEIGHT * CELL_SIZE + 100

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mô Phỏng Xe Giao Hàng Đa Tầng")

# Màu sắc
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (30, 30, 30)
RED = (230, 57, 70)     # Chướng ngại vật
BLUE = (69, 123, 157)   # Thang máy
GREEN = (42, 157, 143)  # Xe giao hàng
YELLOW = (233, 196, 106)# Điểm đích
ORANGE = (244, 162, 97) # Đường đi

bm = BuildingMap()
pf = PathFinder(bm)
start_pos = (1, 0, 0)
target_pos = (2, 8, 8)
path = pf.find_path(start_pos, target_pos) or []

path_index = 0
clock = pygame.time.Clock()

running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Vẽ Tầng 1 và Tầng 2
    for f in [1, 2]:
        offset_x = 30 if f == 1 else WIDTH * CELL_SIZE + 70
        offset_y = 50

        # Tiêu đề tầng
        font = pygame.font.SysFont(None, 28)
        text = font.render(f"TẦNG {f}", True, BLACK)
        screen.blit(text, (offset_x, 15))

        # Vẽ lưới bản đồ
        for y in range(HEIGHT):
            for x in range(WIDTH):
                rect = pygame.Rect(offset_x + x * CELL_SIZE, offset_y + y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                
                if bm.floors[f][y][x] == 1:
                    pygame.draw.rect(screen, RED, rect) # Chướng ngại vật
                elif (x, y) == bm.elevator_pos:
                    pygame.draw.rect(screen, BLUE, rect) # Thang máy
                else:
                    pygame.draw.rect(screen, WHITE, rect)
                
                pygame.draw.rect(screen, GRAY, rect, 1)

    # Vẽ đường đi đã tìm được
    for p in path:
        f, x, y = p
        offset_x = 30 if f == 1 else WIDTH * CELL_SIZE + 70
        rect = pygame.Rect(offset_x + x * CELL_SIZE + 15, 50 + y * CELL_SIZE + 15, 20, 20)
        pygame.draw.ellipse(screen, ORANGE, rect)

    # Vẽ xe chuyển động
    if path and path_index < len(path):
        cf, cx, cy = path[path_index]
        offset_x = 30 if cf == 1 else WIDTH * CELL_SIZE + 70
        robot_rect = pygame.Rect(offset_x + cx * CELL_SIZE + 10, 50 + cy * CELL_SIZE + 10, 30, 30)
        pygame.draw.rect(screen, GREEN, robot_rect)
        
        path_index += 1
        pygame.time.delay(300) # Tốc độ di chuyển của xe

    pygame.display.flip()
    clock.tick(10)

pygame.quit()
sys.exit()