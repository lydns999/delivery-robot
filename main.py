import pygame
import sys
from delivery_map import BuildingMap
from pathfinder import PathFinder

# Khởi tạo Pygame
pygame.init()

CELL_SIZE = 45
WIDTH, HEIGHT = 10, 10
PANEL_HEIGHT = 100 # Cửa sổ điều khiển phía dưới
SCREEN_WIDTH = WIDTH * CELL_SIZE * 2 + 100
SCREEN_HEIGHT = HEIGHT * CELL_SIZE + 80 + PANEL_HEIGHT

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mo Phong Xe Giao Hang Da Tang")

# Màu sắc
WHITE = (255, 255, 255)
GRAY = (220, 220, 220)
DARK_GRAY = (180, 180, 180)
BLACK = (30, 30, 30)
RED = (230, 57, 70)       # Chướng ngại vật
BLUE = (69, 123, 157)     # Thang máy
GREEN = (42, 157, 143)    # Xe giao hàng
YELLOW = (233, 196, 106)  # Điểm đích
ORANGE = (244, 162, 97)   # Đường đi
BTN_COLOR = (200, 210, 225)
BTN_HOVER = (170, 190, 215)

bm = BuildingMap()
pf = PathFinder(bm)

start_pos = (1, 0, 0)
target_pos = (2, 8, 8)

path = []
path_index = 0
is_running = False

# Lịch sử vật cản để Undo
obstacle_history = []

def save_history():
    # Lưu bản sao cấu trúc vật cản hiện tại
    history_item = {
        1: [row[:] for row in bm.floors[1]],
        2: [row[:] for row in bm.floors[2]]
    }
    obstacle_history.append(history_item)

# Font chữ chuẩn không bị lỗi mã hóa
font_title = pygame.font.SysFont("Arial", 22, bold=True)
font_ui = pygame.font.SysFont("Arial", 16)

class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self, surface):
        pos = pygame.mouse.get_pos()
        color = BTN_HOVER if self.rect.collidepoint(pos) else BTN_COLOR
        pygame.draw.rect(surface, color, self.rect, border_radius=5)
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=5)
        
        txt_surface = font_ui.render(self.text, True, BLACK)
        txt_rect = txt_surface.get_rect(center=self.rect.center)
        surface.blit(txt_surface, txt_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Các nút bấm điều khiển
btn_run = Button(30, SCREEN_HEIGHT - 80, 100, 40, "Chay")
btn_reset = Button(140, SCREEN_HEIGHT - 80, 100, 40, "Chay Lai")
btn_clear_obs = Button(250, SCREEN_HEIGHT - 80, 120, 40, "Xoa Het Can")
btn_undo = Button(380, SCREEN_HEIGHT - 80, 100, 40, "Hoan Tac")

clock = pygame.time.Clock()
running = True

while running:
    screen.fill(WHITE)
    
    # 1. Bắt sự kiện chuột và phím
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            m_pos = event.pos
            
            # Xử lý khi nhấn nút điều khiển
            if btn_run.is_clicked(m_pos):
                path = pf.find_path(start_pos, target_pos) or []
                path_index = 0
                is_running = True
                
            elif btn_reset.is_clicked(m_pos):
                path_index = 0
                is_running = False
                
            elif btn_clear_obs.is_clicked(m_pos):
                save_history()
                for f in [1, 2]:
                    for y in range(HEIGHT):
                        for x in range(WIDTH):
                            if (x, y) != bm.elevator_pos:
                                bm.floors[f][y][x] = 0
                path = []
                is_running = False
                
            elif btn_undo.is_clicked(m_pos):
                if obstacle_history:
                    last_state = obstacle_history.pop()
                    bm.floors[1] = [row[:] for row in last_state[1]]
                    bm.floors[2] = [row[:] for row in last_state[2]]
                    path = []
                    is_running = False

            # Xử lý khi nhấp vào ô trên bản đồ
            else:
                for f in [1, 2]:
                    offset_x = 30 if f == 1 else WIDTH * CELL_SIZE + 70
                    offset_y = 50
                    
                    grid_rect = pygame.Rect(offset_x, offset_y, WIDTH * CELL_SIZE, HEIGHT * CELL_SIZE)
                    if grid_rect.collidepoint(m_pos):
                        gx = (m_pos[0] - offset_x) // CELL_SIZE
                        gy = (m_pos[1] - offset_y) // CELL_SIZE
                        
                        # Không thao tác trên ô thang máy
                        if (gx, gy) == bm.elevator_pos:
                            continue
                            
                        # Nhấn giữ phím SHIFT hoặc click vào ô trống/đang có vật cản để bật/tắt vật cản
                        keys = pygame.key.get_pressed()
                        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                            save_history()
                            bm.floors[f][gy][gx] = 1 if bm.floors[f][gy][gx] == 0 else 0
                            path = []
                            is_running = False
                        else:
                            # Chọn điểm đích mới
                            if bm.floors[f][gy][gx] != 1:
                                target_pos = (f, gx, gy)
                                path = []
                                is_running = False

    # 2. Vẽ Bản đồ 2 tầng
    for f in [1, 2]:
        offset_x = 30 if f == 1 else WIDTH * CELL_SIZE + 70
        offset_y = 50

        # Tiêu đề tầng
        title = font_title.render(f"TANG {f}", True, BLACK)
        screen.blit(title, (offset_x, 15))

        for y in range(HEIGHT):
            for x in range(WIDTH):
                rect = pygame.Rect(offset_x + x * CELL_SIZE, offset_y + y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                
                # Tô màu ô
                if bm.floors[f][y][x] == 1:
                    pygame.draw.rect(screen, RED, rect) # Vật cản
                elif (x, y) == bm.elevator_pos:
                    pygame.draw.rect(screen, BLUE, rect) # Thang máy
                else:
                    pygame.draw.rect(screen, WHITE, rect)
                
                # Điểm xuất phát & Điểm đích
                if (f, x, y) == start_pos:
                    pygame.draw.rect(screen, GREEN, rect, 3)
                elif (f, x, y) == target_pos:
                    pygame.draw.rect(screen, YELLOW, rect)
                    
                pygame.draw.rect(screen, GRAY, rect, 1)

    # 3. Vẽ đường đi tìm kiếm được
    for p in path:
        pf_floor, px, py = p
        offset_x = 30 if pf_floor == 1 else WIDTH * CELL_SIZE + 70
        rect = pygame.Rect(offset_x + px * CELL_SIZE + 15, 50 + py * CELL_SIZE + 15, 15, 15)
        pygame.draw.ellipse(screen, ORANGE, rect)

    # 4. Xe di chuyển
    if is_running and path and path_index < len(path):
        cf, cx, cy = path[path_index]
        offset_x = 30 if cf == 1 else WIDTH * CELL_SIZE + 70
        robot_rect = pygame.Rect(offset_x + cx * CELL_SIZE + 8, 50 + cy * CELL_SIZE + 8, 28, 28)
        pygame.draw.rect(screen, GREEN, robot_rect, border_radius=4)
        
        path_index += 1
        pygame.time.delay(250) # Tốc độ chạy

    # 5. Bảng nút bấm & Hướng dẫn sử dụng
    pygame.draw.rect(screen, DARK_GRAY, (0, SCREEN_HEIGHT - PANEL_HEIGHT, SCREEN_WIDTH, PANEL_HEIGHT))
    
    btn_run.draw(screen)
    btn_reset.draw(screen)
    btn_clear_obs.draw(screen)
    btn_undo.draw(screen)

    # Dòng hướng dẫn thao tác
    guide_txt1 = font_ui.render("* Click chuot vao o trong de chon DIEM DICH (Mau vang).", True, BLACK)
    guide_txt2 = font_ui.render("* Giu phim SHIFT + Click chuot de Them/Xoa VAT CAN (Mau do).", True, BLACK)
    screen.blit(guide_txt1, (500, SCREEN_HEIGHT - 85))
    screen.blit(guide_txt2, (500, SCREEN_HEIGHT - 55))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()