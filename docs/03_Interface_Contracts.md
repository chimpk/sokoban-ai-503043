# 03. QUY ƯỚC KỸ THUẬT & GIAO DIỆN CHUNG (INTERFACE CONTRACTS)

> **MỤC ĐÍCH QUAN TRỌNG:**  
> Để 4 thành viên code độc lập trên 4 nhánh Git khác nhau mà **khi gộp lại (merge) chạy trơn tru 100% không bị xung đột hay lỗi sai kiểu dữ liệu**, toàn bộ các định nghĩa trong tài liệu này là **BẤT BIẾN (IMMUTABLE)**. Mọi thành viên bắt buộc tuân thủ đúng tên gọi và kiểu dữ liệu dưới đây.

---

## 1. Hệ Tọa Độ & Hành Động

### 1.1. Quy ước tọa độ
- Mọi tọa độ trên lưới đều là một tuple 2 số nguyên 0-indexed: `(row, col)`.
  - `row`: Chỉ số dòng (từ `0` đến `height - 1`, tăng dần từ trên xuống dưới).
  - `col`: Chỉ số cột (từ `0` đến `width - 1`, tăng dần từ trái sang phải).
- **Tuyệt đối không đảo thứ tự** thành `(x, y)` hay `(col, row)` trong cấu trúc dữ liệu lõi. Khi vẽ lên Pygame, Thành viên 4 sẽ tự chuyển đổi `x = col * tile_size` và `y = row * tile_size`.

### 1.2. Danh sách hành động hợp lệ
- Tên hành động là chuỗi ký tự (String) viết hoa chữ cái đầu:
  ```python
  ACTIONS = ["North", "South", "West", "East"]
  ```
- Vector dịch chuyển tương ứng trên lưới:
  - `"North"`: `(-1, 0)` (lên trên)
  - `"South"`: `(1, 0)` (xuống dưới)
  - `"West"`: `(0, -1)` (sang trái)
  - `"East"`: `(0, 1)` (sang phải)

---

## 2. Cấu Trúc Đối Tượng `State` (`core/state.py`)

Lớp `State` là đối tượng trung tâm được chia sẻ giữa toàn bộ các module.

```python
class State:
    def __init__(
        self,
        player_pos: tuple[int, int],
        box_positions: frozenset[tuple[int, int]],
        walls: frozenset[tuple[int, int]],
        goals: frozenset[tuple[int, int]],
        height: int,
        width: int
    ):
        self.player_pos = player_pos
        self.box_positions = box_positions
        self.walls = walls
        self.goals = goals
        self.height = height
        self.width = width

    def is_goal(self) -> bool:
        """Trả về True nếu tất cả các hộp đều nằm trên các ô đích."""
        pass

    def get_successors(self) -> list[tuple["State", str, int]]:
        """
        Sinh danh sách các trạng thái kế tiếp hợp lệ.
        Mỗi phần tử trong danh sách trả về là: (next_state, action_name, step_cost).
        Trong bài toán này, step_cost mặc định = 1.
        """
        pass

    def __eq__(self, other) -> bool:
        """
        So sánh 2 trạng thái bằng nhau.
        CHÚ Ý: Chỉ so sánh player_pos và box_positions (vì walls và goals là tĩnh).
        """
        pass

    def __hash__(self) -> int:
        """
        Băm trạng thái để lưu được vào Set / Dict (Closed Set).
        CHÚ Ý: hash((self.player_pos, self.box_positions)).
        """
        pass
```

---

## 3. Giao Diện Hàm Tìm Kiếm (`search/ucs.py` & `search/astar.py`)

Cả 2 thuật toán tìm kiếm đều phải tuân thủ đúng signature (chữ ký hàm) và kiểu dữ liệu trả về để module Benchmark và GUI có thể gọi thay thế cho nhau dễ dàng:

```python
def uniform_cost_search(initial_state: State) -> tuple[Optional[list[str]], int, float, int]:
    """
    Tìm kiếm bằng thuật toán Uniform-Cost Search.
    
    Returns:
        tuple gồm:
        - actions: Danh sách hành động đi đến đích, ví dụ ['North', 'East', ...] (hoặc None nếu vô nghiệm).
        - path_cost: Tổng chi phí của lời giải (int).
        - elapsed_time_ms: Thời gian chạy thuật toán tính bằng mili-giây (float).
        - nodes_expanded: Tổng số node đã được lấy ra khỏi Frontier để mở rộng (int).
    """
    pass

def astar_search(initial_state: State, heuristic_func) -> tuple[Optional[list[str]], int, float, int]:
    """
    Tìm kiếm bằng thuật toán A* Search.
    
    Args:
        initial_state: Trạng thái xuất phát.
        heuristic_func: Hàm nhận vào (state: State) -> float (ước lượng chi phí).
        
    Returns:
        tuple tương tự như ucs: (actions, path_cost, elapsed_time_ms, nodes_expanded).
    """
    pass
```

---

## 4. Giao Diện Agent Thi Đấu Đối Kháng (`agents/`)

Mỗi Agent trong chế độ 2 người chơi phải kế thừa một giao diện chung:

```python
class BaseAgent:
    def __init__(self, agent_id: str, name: str):
        self.agent_id = agent_id  # 'A' hoặc 'B'
        self.name = name

    def get_next_action(self, competitive_state, remaining_time_ms: float) -> str:
        """
        Nhận vào trạng thái trận đấu hiện tại và thời gian còn lại (ms).
        Trả về 1 hành động trong ['North', 'South', 'East', 'West', 'Wait'].
        BẮT BUỘC: Thời gian tính toán không được vượt quá 1000ms.
        """
        raise NotImplementedError
```
