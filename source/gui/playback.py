from ..core.state import GameState, MapStaticData

class PlaybackController:
    """
    Quản lý việc phát lại (playback) solution (R5):
      - Space: pause / resume
      - Arrow Right (->): step forward
      - Arrow Left (<-): step backward
      - action count tracking
    """
    def __init__(self, initial_state: GameState, actions: list[str], static_data: MapStaticData):
        # TODO: Member 4 implement playback controller
        pass

    def step_forward(self) -> GameState:
        """Tiến 1 bước theo action tiếp theo."""
        # TODO: Member 4 implement
        pass

    def step_backward(self) -> GameState:
        """Lùi lại 1 bước trước đó."""
        # TODO: Member 4 implement
        pass

    def toggle_pause(self) -> bool:
        """Đổi trạng thái pause/play."""
        # TODO: Member 4 implement
        pass

    def get_current_state(self) -> GameState:
        """Lấy trạng thái hiện tại trên bàn cờ."""
        # TODO: Member 4 implement
        pass

    def get_action_count(self) -> tuple[int, int]:
        """Trả về tuple: (bước hiện tại, tổng số bước)."""
        # TODO: Member 4 implement
        pass
