from abc import ABC, abstractmethod
from typing import Any

class BaseAgent(ABC):
    """
    Lớp cơ sở trừu tượng cho AI Agent trong chế độ đối kháng (Requirement 7 & 8).
    Đặc tả tại: docs/04_Interface_Contracts_and_Testing.md (Mục 4.2)
    """
    def __init__(self, agent_id: str, name: str):
        self.agent_id: str = agent_id  # 'A' hoặc 'B'
        self.name: str = name

    @abstractmethod
    def get_next_action(self, state: Any, remaining_time_ms: float) -> str:
        """
        Trả về 1 hành động trong ['North', 'South', 'East', 'West', 'Wait'].
        Ràng buộc: Thời gian thực thi không vượt quá remaining_time_ms (<= 1000ms).
        """
        raise NotImplementedError
