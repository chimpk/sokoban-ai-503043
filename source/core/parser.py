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
    # TODO: Member 1 implement map parser
    pass
