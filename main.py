from delivery_map import BuildingMap
from pathfinder import PathFinder

def render_path(building_map, path):
    for f in [1, 2]:
        print(f"\n--- BẢN ĐỒ TẦNG {f} ---")
        floor_path = [pos for pos in path if pos[0] == f]
        path_coords = [(p[1], p[2]) for p in floor_path]

        for y in range(building_map.height):
            row = ""
            for x in range(building_map.width):
                val = building_map.floors[f][y][x]
                if (x, y) == building_map.elevator_pos:
                    row += "[E]" if (x, y) in path_coords else " E "
                elif (x, y) in path_coords:
                    row += " * "
                elif val == 1:
                    row += " # " # Chướng ngại vật
                else:
                    row += " . "
            print(row)

if __name__ == "__main__":
    bm = BuildingMap()
    pf = PathFinder(bm)

    start_pos = (1, 0, 0) # Tầng 1, vị trí (0,0)
    target_pos = (2, 8, 8) # Tầng 2, vị trí (8,8)

    print(f"Xe xuất phát tại: Tầng {start_pos[0]}, Tọa độ {start_pos[1:]}")
    print(f"Điểm cần giao tại: Tầng {target_pos[0]}, Tọa độ {target_pos[1:]}")

    path = pf.find_path(start_pos, target_pos)

    if path:
        print("\n=> ĐÃ TÌM THẤY LỘ TRÌNH GIAO HÀNG:")
        for step in path:
            if step[1:] == bm.elevator_pos and step != path[-1]:
                print(f"-> Tầng {step[0]} tại Thang máy {step[1:]}")
            else:
                print(f"-> Tầng {step[0]} vị trí {step[1:]}")
        render_path(bm, path)
    else:
        print("Không tìm được đường đi!")