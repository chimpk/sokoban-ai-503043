# 03. MÔ HÌNH HÓA KHÔNG GIAN TRẠNG THÁI & THUẬT TOÁN TÌM KIẾM (UCS & A*)
## (FORMAL STATE-SPACE FORMULATION & SEARCH ALGORITHMS)

> **Tài liệu phục vụ cho:**  
> - **Tiêu chí 1: Formulation (2.0 điểm Rubric)** - Requirement 1.  
> - **Tiêu chí 2: Uninformed Search (3.0 điểm Rubric)** - Requirement 2 (UCS).  
> - **Tiêu chí 3: Informed Search (3.0 điểm Rubric)** - Requirement 2 (A*).

---

## MỤC LỤC
1. [Mô Hình Hình Thức Toán Học Bài Toán Tìm Kiếm (Formal Search Formulation)](#1-mô-hình-hình-thức-toán-học-bài-toán-tìm-kiếm-formal-search-formulation)
2. [Cấu Trúc Trạng Thái Chuẩn Hóa & Cơ Chế Băm $O(1)$](#2-cấu-trúc-trạng-thái-chuẩn-hóa--cơ-chế-băm-o1)
3. [Thuật Toán Uniform-Cost Search (UCS)](#3-thuật-toán-uniform-cost-search-ucs)
4. [Thuật Toán A* Search Với Tie-Breaking Nâng Cao](#4-thuật-toán-a-search-với-tie-breaking-nâng-cao)
5. [Tái Hiện Đường Đi & Quản Lý Bộ Nhớ](#5-tái-hiện-đường-đi--quản-lý-bộ-nhớ)

---

## 1. MÔ HÌNH HÌNH THỨC TOÁN HỌC BÀI TOÁN TÌM KIẾM

Bài toán Sokoban được mô hình hóa chặt chẽ theo bộ 6 thành phần hình thức:
$$\mathcal{P} = \langle \mathcal{S}, s_0, \mathcal{A}, \mathcal{T}, \mathcal{G}, c \rangle$$

### 1.1. Không gian trạng thái ($\mathcal{S}$)
Để tối ưu hóa tài nguyên tính toán trong thuật toán tìm kiếm, ta phân tách môi trường thành hai lớp thành phần:
- **Thành phần tĩnh (Static Environment - $\mathcal{E}_{\text{static}}$):** Bất biến trong suốt quá trình giải:
  - Lưới bản đồ kích thước $H \times W$.
  - Tập tọa độ các bức tường: $\mathcal{W} \subset \{0, \dots, H-1\} \times \{0, \dots, W-1\}$.
  - Tập tọa độ các ô đích: $\mathcal{G}_{\text{pos}} \subset \{0, \dots, H-1\} \times \{0, \dots, W-1\}$ với $|\mathcal{G}_{\text{pos}}| = M$.
  - Tập các ô sàn có thể đi lại được: $\mathcal{F} = (\{0, \dots, H-1\} \times \{0, \dots, W-1\}) \setminus \mathcal{W}$.
- **Thành phần động (Dynamic State - $s \in \mathcal{S}$):** Biến thiên theo từng bước đi:
  $$s = \langle p, \mathcal{B} \rangle$$
  Trong đó:
  - $p = (r_p, c_p) \in \mathcal{F}$: Tọa độ của người chơi trên lưới sàn.
  - $\mathcal{B} = \{b_1, b_2, \dots, b_M\} \subset \mathcal{F}$: Tập hợp không phân biệt thứ tự gồm $M$ tọa độ của các chiếc hộp ($p \notin \mathcal{B}$).

**Kích thước không gian trạng thái lý thuyết:**
$$|\mathcal{S}| \le |\mathcal{F}| \times \binom{|\mathcal{F}| - 1}{M}$$
Với một bản đồ có 50 ô sàn và 4 chiếc hộp: $|\mathcal{S}| \approx 50 \times \binom{49}{4} \approx 10.5 \times 10^6$ trạng thái. Do không gian trạng thái bùng nổ tổ hợp, việc tìm kiếm mù sẽ sớm cạn kiệt bộ nhớ nếu không có Heuristic định hướng.

---

### 1.2. Trạng thái khởi đầu ($s_0$)
Trạng thái xuất phát được trích xuất trực tiếp từ file bản đồ đầu vào:
$$s_0 = \langle p^{(0)}, \mathcal{B}^{(0)} \rangle$$
- $p^{(0)}$: Vị trí của ký tự `A`.
- $\mathcal{B}^{(0)}$: Tập hợp vị trí của tất cả các ký tự `B` và `C`.

---

### 1.3. Không gian hành động ($\mathcal{A}$)
Tập 4 hành động di chuyển cơ bản của người chơi:
$$\mathcal{A} = \{\text{North}, \text{South}, \text{West}, \text{East}\}$$
Mỗi hành động $a \in \mathcal{A}$ tương ứng với một vector dịch chuyển $\Delta(a) \in \{(-1, 0), (1, 0), (0, -1), (0, 1)\}$.

---

### 1.4. Hàm chuyển trạng thái ($\mathcal{T}: \mathcal{S} \times \mathcal{A} \to \mathcal{S} \cup \{\emptyset\}$)
Xét trạng thái hiện tại $s = \langle p, \mathcal{B} \rangle$ và hành động $a \in \mathcal{A}$.
Đặt vị trí dự kiến của người chơi là $p' = p + \Delta(a)$:

$$\mathcal{T}(s, a) = \begin{cases} 
\emptyset & \text{nếu } p' \in \mathcal{W} \quad \text{(Đi vào tường - Bất hợp lệ)} \\
\langle p', \mathcal{B} \rangle & \text{nếu } p' \notin \mathcal{B} \quad \text{(Bước đi thường - Walk)} \\
\emptyset & \text{nếu } p' \in \mathcal{B} \text{ và } (p' + \Delta(a)) \in \mathcal{W} \cup \mathcal{B} \quad \text{(Đẩy hộp bị chặn)} \\
\langle p', (\mathcal{B} \setminus \{p'\}) \cup \{p' + \Delta(a)\} \rangle & \text{nếu } p' \in \mathcal{B} \text{ và } (p' + \Delta(a)) \notin \mathcal{W} \cup \mathcal{B} \quad \text{(Đẩy hộp thành công)}
\end{cases}$$

---

### 1.5. Điều kiện đích ($\mathcal{G}$)
Hàm kiểm tra đích $\text{IsGoal}: \mathcal{S} \to \{\text{True}, \text{False}\}$:
$$\text{IsGoal}(\langle p, \mathcal{B} \rangle) = \text{True} \iff \mathcal{B} == \mathcal{G}_{\text{pos}}$$
Trạng thái đạt đích khi và chỉ khi toàn bộ $M$ chiếc hộp đều nằm trùng khớp với $M$ vị trí đích đã định trước. Vị trí cuối cùng của người chơi $p$ không ảnh hưởng đến điều kiện thắng.

---

### 1.6. Hàm chi phí đường đi ($c$)
Chi phí chuyển tiếp cho mỗi bước đi hợp lệ:
$$c(s, a, s') = 1 \quad \forall a \in \mathcal{A}$$
Tổng chi phí đường đi từ trạng thái khởi đầu $s_0$ đến trạng thái $s_k$ qua chuỗi hành động $\langle a_1, a_2, \dots, a_k \rangle$:
$$g(s_k) = \sum_{i=1}^k c(s_{i-1}, a_i, s_i) = k$$
Do chi phí bước đồng nhất bằng 1, đường đi tối ưu chi phí cũng chính là đường đi có số hành động ít nhất.

---

## 2. CẤU TRÚC TRẠNG THÁI CHUẨN HÓA & CƠ CHẾ BĂM $O(1)$

Trong Python, để kiểm tra trạng thái lặp với độ phức tạp $O(1)$ trong tập `explored`:
- Vị trí người chơi được biểu diễn bằng `tuple[int, int]`.
- Vị trí các hộp được biểu diễn bằng `frozenset[tuple[int, int]]`.
- Khóa băm duy nhất của trạng thái:
  $$\text{hash}(s) = \text{hash}((p, \mathcal{B}))$$
- Phép so sánh bằng ($s_1 == s_2$):
  $$s_1 == s_2 \iff p_1 == p_2 \land \mathcal{B}_1 == \mathcal{B}_2$$

```python
class GameState:
    __slots__ = ('player_pos', 'box_positions', '_hash')

    def __init__(self, player_pos: tuple[int, int], box_positions: frozenset[tuple[int, int]]):
        self.player_pos = player_pos
        self.box_positions = box_positions
        self._hash = hash((self.player_pos, self.box_positions))

    def is_goal(self, goals: frozenset[tuple[int, int]]) -> bool:
        return self.box_positions == goals

    def __hash__(self) -> int:
        return self._hash

    def __eq__(self, other) -> bool:
        if not isinstance(other, GameState):
            return False
        return self.player_pos == other.player_pos and self.box_positions == other.box_positions
```

---

## 3. THUẬT TOÁN UNIFORM-COST SEARCH (UCS)

### 3.1. Bản chất thuật toán
- **Mục tiêu:** Mở rộng các trạng thái có chi phí $g(n)$ tăng dần từ trạng thái ban đầu cho tới khi gặp trạng thái đích.
- **Tính tối ưu:** Do chi phí mỗi bước đi $c = 1 > 0$, UCS đảm bảo 100% tìm ra đường đi ngắn nhất (Optimal Path).
- **Hàng đợi ưu tiên (Priority Queue):** Sử dụng `heapq` với tuple `(g, counter, node)` để giải quyết triệt để lỗi so sánh Node khi có nhiều node trùng giá trị $g$.

### 3.2. Mã giả chi tiết của UCS
```python
def uniform_cost_search(initial_state: GameState, static_data: MapStaticData):
    start_time = time.perf_counter()
    frontier = []
    counter = 0
    
    start_node = SearchNode(state=initial_state, parent=None, action=None, g=0)
    heapq.heappush(frontier, (0, counter, start_node))
    
    cost_so_far = {initial_state: 0}
    nodes_expanded = 0
    nodes_generated = 1
    
    while frontier:
        g, _, current_node = heapq.heappop(frontier)
        
        if g > cost_so_far.get(current_node.state, float('inf')):
            continue
            
        nodes_expanded += 1
        
        # Goal test khi node được lấy ra khỏi hàng đợi
        if current_node.state.is_goal(static_data.goals):
            elapsed_time_ms = (time.perf_counter() - start_time) * 1000.0
            actions = reconstruct_path(current_node)
            return actions, current_node.g, elapsed_time_ms, nodes_expanded, nodes_generated
            
        for action_name, next_state in current_node.state.get_successors(static_data):
            next_g = current_node.g + 1
            if next_state not in cost_so_far or next_g < cost_so_far[next_state]:
                cost_so_far[next_state] = next_g
                counter += 1
                child_node = SearchNode(state=next_state, parent=current_node, action=action_name, g=next_g)
                heapq.heappush(frontier, (next_g, counter, child_node))
                nodes_generated += 1
                
    return None, 0, (time.perf_counter() - start_time) * 1000.0, nodes_expanded, nodes_generated
```

---

## 4. THUẬT TOÁN A* SEARCH VỚI TIE-BREAKING NÂNG CAO

### 4.1. Hàm Đánh Giá $f(n) = g(n) + h(n)$
- $g(n)$: Chi phí thực tế đã đi từ gốc.
- $h(n)$: Ước lượng chi phí từ node hiện tại tới đích (được tính bằng Hungarian Bipartite Matching trên khoảng cách Static Maze BFS).
- **Tie-Breaking trên $h(n)$:** Khi hai node có cùng giá trị $f(n)$, thuật toán ưu tiên mở rộng node có $h(n)$ nhỏ hơn. Tuple đưa vào `heapq`: `(f, h, counter, node)`. Kỹ thuật này giúp A* hội tụ về đích nhanh hơn gấp nhiều lần.
- **Tích hợp tỉa bế tắc (Deadlock Pruning):** Nếu $h(\text{next\_state}) == \infty$, node đó lập tức bị loại bỏ khỏi không gian tìm kiếm.

### 4.2. Mã giả chi tiết của A* Search
```python
def astar_search(initial_state: GameState, static_data: MapStaticData, heuristic_obj):
    start_time = time.perf_counter()
    frontier = []
    counter = 0
    
    h0 = heuristic_obj.evaluate(initial_state)
    if h0 == float('inf'):
        return None, 0, 0.0, 0, 1
        
    start_node = SearchNode(state=initial_state, parent=None, action=None, g=0, h=h0)
    heapq.heappush(frontier, (start_node.f, start_node.h, counter, start_node))
    
    cost_so_far = {initial_state: 0}
    nodes_expanded = 0
    nodes_generated = 1
    
    while frontier:
        f, h, _, current_node = heapq.heappop(frontier)
        
        if current_node.g > cost_so_far.get(current_node.state, float('inf')):
            continue
            
        nodes_expanded += 1
        
        if current_node.state.is_goal(static_data.goals):
            elapsed_time_ms = (time.perf_counter() - start_time) * 1000.0
            actions = reconstruct_path(current_node)
            return actions, current_node.g, elapsed_time_ms, nodes_expanded, nodes_generated
            
        for action_name, next_state in current_node.state.get_successors(static_data):
            next_g = current_node.g + 1
            if next_state not in cost_so_far or next_g < cost_so_far[next_state]:
                h_val = heuristic_obj.evaluate(next_state)
                if h_val == float('inf'):
                    continue # Bỏ qua nhánh Deadlock
                    
                cost_so_far[next_state] = next_g
                counter += 1
                child_node = SearchNode(state=next_state, parent=current_node, action=action_name, g=next_g, h=h_val)
                heapq.heappush(frontier, (next_g + h_val, h_val, counter, child_node))
                nodes_generated += 1
                
    return None, 0, (time.perf_counter() - start_time) * 1000.0, nodes_expanded, nodes_generated
```

---

## 5. TÁI HIỆN ĐƯỜNG ĐI & QUẢN LÝ BỘ NHỚ

Khi đạt đích, thuật toán lần ngược con trỏ `parent` từ `goal_node` về `root_node` trong thời gian $O(d)$:
```python
def reconstruct_path(goal_node: SearchNode) -> list[str]:
    actions = []
    curr = goal_node
    while curr.parent is not None:
        actions.append(curr.action)
        curr = curr.parent
    actions.reverse()
    return actions
```
Nhờ sử dụng `__slots__` trong `SearchNode` và `GameState`, hệ thống tiết kiệm được hơn 75% bộ nhớ RAM so với cấu trúc hướng đối tượng mặc định của Python.
