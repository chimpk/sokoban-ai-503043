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
        # TODO: Member 4 implement
        pass

    def step_backward(self) -> GameState:
        # TODO: Member 4 implement
        pass

    def toggle_pause(self) -> bool:
        # TODO: Member 4 implement
        pass

    def get_current_state(self) -> GameState:
        # TODO: Member 4 implement
        pass

    def get_action_count(self) -> tuple[int, int]:
        # TODO: Member 4 implement
        pass
