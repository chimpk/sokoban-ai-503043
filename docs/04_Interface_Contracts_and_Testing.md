# 04. QUY ƯỚC GIAO DIỆN KỸ THUẬT & KẾ HOẠCH KIỂM THỬ TOÀN DIỆN
## (INTERFACE CONTRACTS, DATA TYPES & COMPREHENSIVE TEST SUITE)

> **Mục tiêu:** Cung cấp đặc tả giao diện bất biến (Immutable Contracts) giữa các module mã nguồn để các thành viên tích hợp không xảy ra xung đột, cùng kế hoạch kiểm thử đơn vị tự động (Unit Tests) và danh mục các trường hợp biên (Edge Cases).

---

## MỤC LỤC
1. [Hệ Tọa Độ & Hành Động Chuẩn Hóa](#1-hệ-tọa-độ--hành-động-chuẩn-hóa)
2. [Cấu Trúc Lớp Dữ Liệu Bất Biến (Dataclasses & State)](#2-cấu-trúc-lớp-dữ-liệu-bất-biến-dataclasses--state)
3. [Chữ Ký Hàm Tìm Kiếm & Lớp Heuristic](#3-chữ-ký-hàm-tìm-kiếm--lớp-heuristic)
4. [Giao Diện Chế Độ Đối Kháng 2 Agent](#4-giao-diện-chế-độ-đối-kháng-2-agent)
5. [Kế Hoạch Kiểm Thử Toàn Diện (Unit Test Suites)](#5-kế-hoạch-kiểm-thử-toàn-diện-unit-test-suites)
6. [Danh Mục Các Trường Hợp Biên (Edge Cases) Phòng Ngừa Lỗi](#6-danh-mục-các-trường-hợp-biên-edge-cases-phòng-ngừa-lỗi)

---

## 1. HỆ TỌA ĐỘ & HÀNH ĐỘNG CHUẨN HÓA

### 1.1. Quy ước tọa độ
- Toàn bộ hệ thống sử dụng quy ước tọa độ `(row, col)` 0-indexed:
  - `row`: Chỉ số dòng ($0 \le row < height$), tăng dần từ trên xuống dưới.
  - `col`: Chỉ số cột ($0 \le col < width$), tăng dần từ trái sang phải.
- ⚠️ Không sử dụng `(x, y)` trong logic bài toán để tránh nhầm lẫn đảo trục.

### 1.2. Danh sách hành động hợp lệ
```python
ACTIONS = ["North", "South", "West", "East"]
ACTION_DELTAS = {
    "North": (-1, 0),
    "South": (1, 0),
    "West":  (0, -1),
    "East":  (0, 1),
    "Wait":  (0, 0),   # Chỉ dùng trong chế độ đối kháng
}
```

---

## 2. CẤU TRÚC LỚP DỮ LIỆU BẤT BIẾN (DATACLASSES & STATE)

### 2.1. Lớp Dữ Liệu Tĩnh: `MapStaticData` (`source/core/state.py`)
```python
from dataclasses import dataclass

@dataclass(frozen=True)
class MapStaticData:
    width: int
    height: int
    walls: frozenset[tuple[int, int]]                 # Tập tọa độ tường '%'
    goals: frozenset[tuple[int, int]]                 # Tập tọa độ đích 'D' và 'C'
    initial_player_pos: tuple[int, int]               # Vị trí xuất phát của người chơi 'A'
    initial_box_positions: frozenset[tuple[int, int]] # Tập tọa độ ban đầu của các hộp
```

### 2.2. Lớp Trạng Thái Động: `GameState` (`source/core/state.py`)
```python
class GameState:
    __slots__ = ('player_pos', 'box_positions', '_hash')

    def __init__(self, player_pos: tuple[int, int], box_positions: frozenset[tuple[int, int]]):
        self.player_pos: tuple[int, int] = player_pos
        self.box_positions: frozenset[tuple[int, int]] = box_positions
        self._hash: int = hash((self.player_pos, self.box_positions))

    def is_goal(self, goals: frozenset[tuple[int, int]]) -> bool:
        return self.box_positions == goals

    def get_successors(self, static_data: MapStaticData) -> list[tuple[str, "GameState"]]:
        """Trả về: list các tuple (action_name, next_state)."""
        pass

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, GameState):
            return False
        return self.player_pos == other.player_pos and self.box_positions == other.box_positions

    def __hash__(self) -> int:
        return self._hash
```

---

## 3. CHỮ KÝ HÀM TÌM KIẾM & LỚP HEURISTIC

### 3.1. Chuẩn Kết Quả Tìm Kiếm (`SearchResult`)
```python
from typing import Optional

SearchResult = tuple[
    Optional[list[str]],  # actions: Danh sách hành động hoặc None nếu vô nghiệm
    int,                  # path_cost: Tổng chi phí lời giải (số bước đi)
    float,                # elapsed_time_ms: Thời gian chạy tính bằng milliseconds
    int,                  # nodes_expanded: Tổng số node lấy ra khỏi Frontier để mở rộng
    int                   # nodes_generated: Tổng số node con được tạo ra đưa vào Frontier
]

def uniform_cost_search(initial_state: GameState, static_data: MapStaticData) -> SearchResult:
    pass

def astar_search(initial_state: GameState, static_data: MapStaticData, heuristic_obj) -> SearchResult:
    pass
```

### 3.2. Lớp Heuristic (`source/search/heuristic.py`)
```python
class SokobanHeuristic:
    def __init__(self, static_data: MapStaticData):
        """Khởi tạo và precompute bảng khoảng cách tĩnh BFS từ các ô đích."""
        self.static_data = static_data
        self.dist_table = self._precompute_maze_distances()

    def evaluate(self, state: GameState) -> int:
        """Trả về float('inf') nếu là Deadlock, ngược lại trả về Hungarian Matching Cost."""
        pass
```

---

## 4. GIAO DIỆN CHẾ ĐỘ ĐỐI KHÁNG 2 AGENT

### 4.1. Lớp Trạng Thái Đối Kháng: `CompetitiveState` (`source/competitive/state.py`)
```python
@dataclass
class CompetitiveState:
    agent_a_pos: tuple[int, int]
    agent_b_pos: tuple[int, int]
    box_positions: frozenset[tuple[int, int]]
    box_owners: dict[tuple[int, int], Optional[str]] # Hộp -> 'A', 'B' hoặc None
    score_a: int
    score_b: int
    current_step: int
    max_steps: int
    static_data: MapStaticData
```

### 4.2. Giao diện cơ sở cho AI Agent: `BaseAgent` (`source/agents/base_agent.py`)
```python
class BaseAgent:
    def __init__(self, agent_id: str, name: str):
        self.agent_id: str = agent_id  # 'A' hoặc 'B'
        self.name: str = name

    def get_next_action(self, state: CompetitiveState, remaining_time_ms: float) -> str:
        """
        Trả về 1 hành động trong ['North', 'South', 'East', 'West', 'Wait'].
        Ràng buộc bắt buộc: Thời gian thực thi không được vượt quá remaining_time_ms (<= 1000ms).
        """
        raise NotImplementedError
```

---

## 5. KẾ HOẠCH KIỂM THỬ TOÀN DIỆN (UNIT TEST SUITES)

Đặt tại thư mục `source/tests/`, sử dụng thư viện chuẩn `unittest`:

### 5.1. Kiểm thử Parser (`test_parser.py`)
- `test_valid_parsing`: Đọc chuẩn xác các ký tự `%`, `A`, `B`, `D`, `C`, khoảng trắng từ `example_map.txt`.
- `test_unbalanced_boxes_goals`: Phát hiện lỗi khi số lượng hộp khác số lượng đích.
- `test_missing_player`: Báo lỗi khi thiếu vị trí người chơi `A`.

### 5.2. Kiểm thử Trạng thái & Chuyển tiếp (`test_state.py`)
- `test_valid_move`: Di chuyển vào ô sàn trống hợp lệ.
- `test_move_into_wall`: Di chuyển vào tường bị chặn đứng.
- `test_valid_push`: Đẩy hộp vào ô trống hợp lệ, cập nhật đúng vị trí người và hộp.
- `test_push_into_wall`: Đẩy hộp vào tường bị từ chối.
- `test_push_into_box`: Đẩy hộp vào một hộp khác bị từ chối.
- `test_state_hash_equality`: Hai trạng thái có cùng vị trí người chơi và hộp (bất kể thứ tự khởi tạo) đều có cùng giá trị băm và so sánh bằng `==` trả về `True`.

### 5.3. Kiểm thử Thuật toán Tìm kiếm (`test_search.py`)
- `test_ucs_optimality`: UCS tìm ra lời giải tối ưu trên bản đồ nhỏ.
- `test_astar_optimality`: A* tìm ra lời giải có cùng chi phí tối ưu với UCS.
- `test_unsolvable_map`: Bản đồ bế tắc trả về `None` an toàn, không bị treo chương trình.

### 5.4. Kiểm thử Heuristic & Deadlock (`test_heuristic.py`)
- `test_admissibility`: $h(s) \le h^*(s)$ trên toàn bộ tập trạng thái mẫu.
- `test_consistency`: $h(s) - h(s') \le 1$ trên toàn bộ các bước chuyển hợp lệ.
- `test_corner_deadlock`: Hộp ở góc tường không phải đích trả về $h = \infty$.

### 5.5. Kiểm thử Chế độ Đối kháng (`test_competitive.py`)
- `test_vertex_collision`: Hai Agent cùng đi vào 1 ô $\implies$ Cả hai đứng yên.
- `test_swap_collision`: Hai Agent đi xuyên qua nhau $\implies$ Cả hai đứng yên.
- `test_box_stealing`: Agent B đẩy hộp của Agent A ra khỏi đích $\implies$ Điểm của Agent A bị trừ 1.
- `test_timeout_guard`: Agent chạy quá 1,000 ms bị ngắt an toàn và trả về `"Wait"`.

---

## 6. DANH MỤC CÁC TRƯỜNG HỢP BIÊN (EDGE CASES) PHÒNG NGỪA LỖI

| # | Tình huống biên (Edge Case) | Hậu quả nếu không xử lý | Giải pháp đã cài đặt trong hệ thống |
| :-: | :--- | :--- | :--- |
| **1** | Hộp nằm sẵn trên đích lúc bắt đầu (ký hiệu `C`). | Bị bỏ sót hộp hoặc không tính vào tập đích. | Parser tự động thêm `C` vào cả tập Hộp ban đầu và tập Đích ban đầu. |
| **2** | Trùng chi phí $f(n)$ hoặc $g(n)$ trong Priority Queue. | Python báo lỗi `TypeError: '<' not supported between SearchNode`. | Thêm biến đếm số thứ tự sinh ra `counter`: `(f, h, counter, node)`. |
| **3** | Bản đồ không có lời giải (Unsolvable Map). | Chương trình lặp vô tận gây treo màn hình. | Thuật toán kiểm tra `while frontier:`, trả về `None` khi hàng đợi rỗng, GUI hiển thị thông báo "No Solution". |
| **4** | Agent chạy quá thời gian 1,000 ms trong đối kháng. | Bị trừ 1.0 điểm Requirement 7. | Lớp `TimeoutGuard` giới hạn ngắt an toàn tại $950$ ms. |
| **5** | Bản đồ lớn gây tràn RAM khi chạy UCS. | Sập chương trình (Out-of-memory). | Module benchmark đặt giới hạn bộ nhớ đỉnh điểm (500 MB) để ngắt an toàn và ghi nhận số liệu. |

---

## 7. LỆNH CHẠY TOÀN BỘ KIỂM THỬ TỰ ĐỘNG
```bash
python -m unittest discover -s source/tests -p "test_*.py" -v
```
Toàn bộ các test case bắt buộc phải hiển thị **`OK`** trước khi tiến hành nộp bài.
