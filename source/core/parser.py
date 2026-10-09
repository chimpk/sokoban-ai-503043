from .state import GameState, MapStaticData

VALID_CHARS = {'%', 'A', 'B', 'D', 'C', ' '}


class MapFormatError(ValueError):
    """
    Lỗi định dạng file bản đồ (thiếu người chơi, số hộp khác số đích, ký tự lạ...).
    """
    pass


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
    Raise MapFormatError nếu bản đồ không hợp lệ.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return parse_map_string(f.read())


def parse_map_string(content: str) -> tuple[GameState, MapStaticData]:
    """
    Phân tích nội dung bản đồ dạng chuỗi (dùng chung cho parse_map_file và unit test).
    """
    lines = content.splitlines()
    # Bỏ các dòng trống ở cuối file
    while lines and not lines[-1].strip():
        lines.pop()

    walls = set()
    goals = set()
    player_positions = []
    box_positions = set()

    height = len(lines)
    width = max((len(line) for line in lines), default=0)

    for r, line in enumerate(lines):
        for c, char in enumerate(line):
            if char not in VALID_CHARS:
                raise MapFormatError(f"Ký tự không hợp lệ {char!r} tại (row={r}, col={c})")
            if char == '%':
                walls.add((r, c))
            elif char == 'A':
                player_positions.append((r, c))
            elif char == 'B':
                box_positions.add((r, c))
            elif char == 'D':
                goals.add((r, c))
            elif char == 'C':
                box_positions.add((r, c))
                goals.add((r, c))

    if not player_positions:
        raise MapFormatError("Bản đồ thiếu vị trí người chơi 'A'")
    if len(player_positions) > 1:
        raise MapFormatError(f"Bản đồ có {len(player_positions)} người chơi 'A', chỉ được phép có 1")
    if len(box_positions) != len(goals):
        raise MapFormatError(
            f"Số hộp ({len(box_positions)}) khác số đích ({len(goals)})"
        )

    player_pos = player_positions[0]
    static_data = MapStaticData(walls, goals, height, width, player_pos, box_positions)
    initial_state = GameState(player_pos, box_positions)
    return initial_state, static_data
