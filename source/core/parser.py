from .state import GameState, MapStaticData

def parse_map_file(file_path: str) -> tuple[GameState, MapStaticData]:
    """
    Đọc file layout bản đồ (input path theo yêu cầu của đề).
    Ký hiệu:
      % : obstacle / wall
      A : vị trí ban đầu của agent
      B : box
      D : designated position / goal
      C : box đang nằm trên designated position
      space : blank cell

    Trả về: (initial_game_state, map_static_data)
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()
    
    walls = set()
    goals = set()
    player_pos = (-1, -1)
    box_positions = set()
    
    height = len(lines)
    width = max((len(line) for line in lines), default=0)
    
    for r, line in enumerate(lines):
        for c, char in enumerate(line):
            if char == '%':
                walls.add((r, c))
            elif char == 'A':
                player_pos = (r, c)
            elif char == 'B':
                box_positions.add((r, c))
            elif char == 'D':
                goals.add((r, c))
            elif char == 'C':
                box_positions.add((r, c))
                goals.add((r, c))
                
    static_data = MapStaticData(walls, goals, height, width)
    initial_state = GameState(player_pos, box_positions)
    return initial_state, static_data
