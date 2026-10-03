# 02. KIẾN TRÚC HỆ THỐNG, TỪ ĐIỂN BIẾN & LỜI GIẢI KỸ THUẬT TOÀN DIỆN
## (TECHNICAL ARCHITECTURE, DATA DICTIONARY & COMPLETE SOLUTIONS)

> **Mục tiêu:** Cung cấp tài liệu kỹ thuật thống nhất toàn dự án: kiến trúc module, quy tắc sở hữu code không xung đột (Zero-conflict Git), từ điển biến và thuộc tính chuẩn hóa, cùng toàn bộ lời giải chi tiết 100% cho 4 mảng nhiệm vụ của 4 thành viên.

---

## MỤC LỤC
1. [Kiến Trúc Tổng Thể & Quy Tắc Sở Hữu Code (Zero-Conflict)](#1-kiến-trúc-tổng-thể--quy-tắc-sở-hữu-code-zero-conflict)
2. [Từ Điển Biến & Thuộc Tính Dùng Chung Toàn Hệ Thống](#2-từ-điển-biến--thuộc-tính-dùng-chung-toàn-hệ-thống)
3. [Thành Viên 1: Không Gian Trạng Thái, Parser & Thuật Toán UCS](#3-thành-viên-1-không-gian-trạng-thái-parser--thuật-toán-ucs)
4. [Thành Viên 2: Thiết Kế Heuristic Hungarian, A* Search & Deadlock Pruning](#4-thành-viên-2-thiết-kế-heuristic-hungarian-a-search--deadlock-pruning)
5. [Thành Viên 3: Trò Chơi Đối Kháng 2 Agent, Xử Lý Xung Đột & AI Agent $\le 1000$ ms](#5-thành-viên-3-trò-chơi-đối-kháng-2-agent-xử-lý-xung-đột--ai-agent-le-1000-ms)
6. [Thành Viên 4: Pygame GUI OOP, Playback Controller & Tương Thích macOS Ventura Intel](#6-thành-viên-4-pygame-gui-oop-playback-controller--tương-thích-macos-ventura-intel)

---

## 1. KIẾN TRÚC TỔNG THỂ & QUY TẮC SỞ HỮU CODE (ZERO-CONFLICT)

### 1.1. Nguyên tắc thiết kế phần mềm
- **Zero-Conflict Ownership:** Mỗi thành viên sở hữu trọn vẹn một nhóm file độc quyền trên nhánh Git của mình, không chỉnh sửa file của thành viên khác để tránh xung đột mã nguồn khi gộp nhánh (Merge).
- **Phân tách trách nhiệm (Separation of Concerns):** Thuật toán tìm kiếm lõi (Search Core) hoàn toàn độc lập với Giao diện đồ họa (Pygame GUI) và Động cơ đối kháng (Competitive Engine).
- **Lập trình Hướng đối tượng (OOP):** Theo yêu cầu nghiêm ngặt của Requirement 5.

### 1.2. Sơ đồ cây thư mục & Phân quyền file mã nguồn
```text
source/
├── core/                   --> [Member 1 phụ trách] Nền tảng State-Space & Parser
│   ├── action.py           (Hằng số hành động: North, South, West, East, Wait)
│   ├── state.py            (GameState, MapStaticData, Transition, Goal check)
│   ├── parser.py           (Đọc file map text sang GameState và MapStaticData)
│   └── node.py             (SearchNode: state, parent, action, g, h, f)
│
├── search/                 --> [Member 1 & Member 2 phụ trách]
│   ├── ucs.py              --> [Member 1] Uniform Cost Search
│   ├── heuristic.py        --> [Member 2] Heuristic Hungarian Bipartite Matching
│   └── astar.py            --> [Member 2] A* Search Algorithm
│
├── experiment/             --> [Member 2 & Member 4 phụ trách]
│   ├── admissibility.py    --> [Member 2] Kiểm thử thực nghiệm Admissible & Consistent
│   └── benchmark.py        --> [Member 4] Đo đạc Time, Memory, Nodes, Cost & Vẽ biểu đồ
│
├── competitive/            --> [Member 3 phụ trách] Chế độ Đối kháng 2 Agent
│   ├── state.py            (CompetitiveState: agent pos, boxes, score, max steps)
│   ├── conflict.py         (ConflictResolver: phân xử va chạm đồng thời)
│   └── engine.py           (CompetitiveEngine: vòng lặp n bước, TimeoutGuard)
│
├── gui/                    --> [Member 4 phụ trách] Giao diện Pygame OOP
│   ├── game.py             (Vòng lặp sự kiện Pygame chính)
│   ├── renderer.py         (Vẽ map, nhân vật, box, wall, goal, chia tỷ lệ)
│   ├── button.py           (Nút bấm UI có hiệu ứng hover)
│   └── playback.py         (Bộ điều khiển phát lại: Play, Pause, Next, Prev)
│
├── tests/                  --> [Member 1 phụ trách điều phối & Toàn nhóm]
│   ├── test_parser.py      --> [Member 1] Kiểm thử Parser: đọc %, A, B, D, C, khoảng trắng
│   ├── test_state.py       --> [Member 1] Kiểm thử trạng thái: walk, push, wall, collision, hash O(1)
│   ├── test_search.py      --> [Member 1 & 2] Kiểm thử UCS & A*: tính tối ưu & vô nghiệm
│   ├── test_heuristic.py   --> [Member 2] Kiểm thử Heuristic: Admissible, Consistent, Deadlock
│   └── test_competitive.py --> [Member 3] Kiểm thử Đối kháng: xung đột ô, cướp hộp, timeout
│
├── agents/                 --> [Member 3 phụ trách] File độc lập cho từng Agent (Req 8)
│   ├── base_agent.py       (Interface chuẩn BaseAgent)
│   ├── agent_a.py          (Thuật toán AI cho Agent A <= 1000ms)
│   └── agent_b.py          (Thuật toán AI cho Agent B <= 1000ms)
│
├── maps/                   --> Thư mục chứa các map thử nghiệm
│   ├── example_map.txt     (Bản đồ chính thức từ đề thi: 7 hộp, 7 đích)
│   ├── map_01.txt          (Bản sao bản đồ chính thức)
│   ├── map_02.txt          (Bản đồ mê cung 2 hộp)
│   └── competitive_map.txt (Bản đồ đối kháng đối xứng 14x14)
│
└── main.py                 --> [Member 4 phụ trách] Điểm kích hoạt chạy ứng dụng (CLI)
```

---

## 2. TỪ ĐIỂN BIẾN & THUỘC TÍNH DÙNG CHUNG TOÀN HỆ THỐNG

Để đảm bảo code tích hợp trơn tru, toàn bộ 4 thành viên tuân thủ nghiêm ngặt từ điển thuộc tính dưới đây:

### 2.1. Hệ tọa độ chuẩn
- **Quy ước duy nhất:** Tọa độ luôn là tuple 2 số nguyên 0-indexed: `(row, col)`.
  - `row`: Chỉ số dòng (từ trên xuống dưới: $0 \le row < height$).
  - `col`: Chỉ số cột (từ trái sang phải: $0 \le col < width$).
- ⚠️ **Tuyệt đối không đảo thứ tự thành `(x, y)` hay `(col, row)`** trong logic lõi. Khi vẽ lên Pygame, Renderer tự chuyển đổi: `pixel_x = col * tile_size` và `pixel_y = row * tile_size`.

### 2.2. Hành động và Vector di chuyển
```python
ACTIONS = ["North", "South", "West", "East"]
ACTION_DELTAS = {
    "North": (-1, 0),  # Dòng giảm 1 (Lên trên)
    "South": (1, 0),   # Dòng tăng 1 (Xuống dưới)
    "West":  (0, -1),  # Cột giảm 1 (Sang trái)
    "East":  (0, 1),   # Cột tăng 1 (Sang phải)
    "Wait":  (0, 0),   # Đứng yên (chế độ đối kháng)
}
```

### 2.3. Bảng thuộc tính các Class cốt lõi
| Tên Class | Thuộc tính (Attribute) | Kiểu dữ liệu | Ý nghĩa |
| :--- | :--- | :--- | :--- |
| **`MapStaticData`** | `width`<br>`height`<br>`walls`<br>`goals`<br>`initial_player_pos`<br>`initial_box_positions` | `int`<br>`int`<br>`frozenset[tuple[int, int]]`<br>`frozenset[tuple[int, int]]`<br>`tuple[int, int]`<br>`frozenset[tuple[int, int]]` | Chiều rộng bản đồ.<br>Chiều cao bản đồ.<br>Tập tọa độ các bức tường (`%`).<br>Tập tọa độ các ô đích (`D` và `C`).<br>Vị trí người chơi lúc bắt đầu.<br>Vị trí các hộp lúc bắt đầu. |
| **`GameState`** | `player_pos`<br>`box_positions`<br>`_hash` | `tuple[int, int]`<br>`frozenset[tuple[int, int]]`<br>`int` | Tọa độ người chơi hiện tại.<br>Tập hợp tọa độ các chiếc hộp hiện tại.<br>Giá trị băm `hash((player_pos, box_positions))`. |
| **`SearchNode`** | `state`<br>`parent`<br>`action`<br>`g`<br>`h`<br>`f` | `GameState`<br>`Optional[SearchNode]`<br>`Optional[str]`<br>`int`<br>`int`<br>`int` | Trạng thái của node.<br>Con trỏ node cha để lần ngược đường đi.<br>Hành động dẫn từ parent tới node.<br>Chi phí đường đi từ gốc đến node.<br>Ước lượng chi phí từ node đến đích.<br>Tổng chi phí đánh giá: $f = g + h$. |
| **`CompetitiveState`** | `agent_a_pos`<br>`agent_b_pos`<br>`box_positions`<br>`box_owners`<br>`score_a`<br>`score_b`<br>`current_step`<br>`max_steps` | `tuple[int, int]`<br>`tuple[int, int]`<br>`frozenset[tuple[int, int]]`<br>`dict[tuple[int, int], Optional[str]]`<br>`int`<br>`int`<br>`int`<br>`int` | Tọa độ hiện tại của Agent A.<br>Tọa độ hiện tại của Agent B.<br>Tập tọa độ các hộp.<br>Ánh xạ hộp -> Chủ sở hữu (`'A'`, `'B'`, `None`).<br>Điểm số hiện tại của Agent A.<br>Điểm số hiện tại của Agent B.<br>Bước đếm thời gian hiện tại.<br>Số bước tối đa của ván đấu $n$. |

---

## 3. THÀNH VIÊN 1: KHÔNG GIAN TRẠNG THÁI, PARSER & THUẬT TOÁN UCS

### 3.1. Phân Tách Tĩnh - Động (Static vs Dynamic Optimization)
- Tường (`walls`) và Đích (`goals`) không bao giờ đổi trong quá trình tìm kiếm.
- Lưu trữ `walls` và `goals` trong `MapStaticData` (duy nhất 1 phiên bản trong RAM).
- `GameState` chỉ lưu `(player_pos, box_positions)` với `__slots__` $\implies$ giảm kích thước RAM mỗi node xuống dưới 80 Bytes, tăng tốc độ băm $O(1)$.

### 3.2. Hàm Sinh Trạng Thái Kế Tiếp (`get_successors`)
1. Với mỗi hành động $a \in \{\text{North}, \text{South}, \text{West}, \text{East}\}$ có độ dời $\Delta$:
2. Vị trí dự kiến: $P' = P + \Delta$. Nếu $P' \in \text{walls} \implies$ Bỏ qua.
3. Nếu $P' \notin \text{boxes} \implies$ Bước đi thường (Walk), $S' = \text{GameState}(P', \text{boxes})$.
4. Nếu $P' \in \text{boxes}$ (Đẩy hộp):
   - Vị trí sau khi đẩy của hộp: $B' = P' + \Delta$.
   - Nếu $B' \in \text{walls}$ hoặc $B' \in \text{boxes} \implies$ Bị chặn, bỏ qua.
   - Ngược lại $\implies$ $B_{\text{new}} = (\text{boxes} \setminus \{P'\}) \cup \{B'\}$, $S' = \text{GameState}(P', B_{\text{new}})$.
5. Mỗi bước đi hợp lệ có chi phí $c = 1$.

### 3.3. Thuật toán Uniform-Cost Search (UCS)
- Sử dụng Priority Queue `heapq` với tuple `(g, counter, node)` để tránh lỗi so sánh Node khi trùng chi phí $g$.
- Quản lý tập đóng bằng `cost_so_far: dict[GameState, int]`.
- Goal test thực hiện khi node được lấy ra (`heappop`) khỏi hàng đợi.

---

## 4. THÀNH VIÊN 2: THIẾT KẾ HEURISTIC HUNGARIAN, A* SEARCH & DEADLOCK PRUNING

### 4.1. Tại Sao Cấm Manhattan & Euclidean?
Đề bài quy định rõ: *"Note that Euclidean and Manhattan distances are not allowed."*
Manhattan và Euclidean giả định không gian phẳng không vật cản. Trong Sokoban, các bức tường tạo nên hành lang ngoằn ngoèo; khoảng cách Manhattan bỏ qua tường sẽ đánh giá quá lỏng, gây nổ trạng thái.

### 4.2. Kiến Trúc Heuristic Đề Xuất
$$h(s) = \begin{cases} \infty & \text{nếu } \text{IsDeadlock}(s) \\ h_{\text{matching}}(s) & \text{ngược lại} \end{cases}$$
1. **Static Maze Distance:** Chạy BFS ngược từ từng ô đích $g \in G$ trên lưới sàn không tường, lưu vào bảng `dist_table[goal][(r, c)]`. Tính trước 1 lần duy nhất khi nạp bản đồ ($< 2$ ms).
2. **Minimum-Cost Bipartite Matching:** Xây dựng ma trận chi phí $C_{i, j} = \text{dist\_table}[g_j][b_i]$. Giải bài toán gán 1-1 bằng thuật toán Hungarian (Kuhn-Munkres) để tìm cận dưới nhỏ nhất của tổng số bước đẩy hộp.
3. **Deadlock Detection Engine:**
   - *Corner Deadlock:* Hộp ở ô có 2 tường vuông góc kề nhau mà không phải đích $\implies$ Deadlock.
   - *Line Deadlock:* Hộp sát tường mà suốt chiều dài tường không có đích $\implies$ Deadlock.
   - *2x2 Freeze Deadlock:* Khối $2 \times 2$ gồm hộp và tường (ít nhất 1 hộp không ở đích) $\implies$ Deadlock.
   Khi phát hiện Deadlock, gán ngay $h(s) = \infty$, tỉa bỏ nhánh tìm kiếm.

### 4.3. Thuật Toán A* Search Với Tie-Breaking Trên $h$
- Hàng đợi ưu tiên lưu tuple `(f, h, counter, node)` với $f = g + h$.
- Khi hai node trùng $f$, ưu tiên node có $h$ nhỏ hơn (gần đích hơn) $\implies$ A* đâm thẳng về đích với tốc độ mở rộng node nhanh hơn gấp 10 lần.

---

## 5. THÀNH VIÊN 3: TRÒ CHƠI ĐỐI KHÁNG 2 AGENT, XỬ LÝ XUNG ĐỘT & AI AGENT $\le 1000$ MS

### 5.1. Mô Hình Đối Kháng & Hành Động Đồng Thời
- Hai Agent cùng hoạt động trên một bản đồ, đưa ra hành động cùng lúc trong từng bước thời gian.
- Trò chơi kết thúc khi hết $n$ bước (do người dùng nhập) hoặc toàn bộ hộp đã vào đích.
- Bên nào sở hữu nhiều hộp trên đích hơn khi kết thúc sẽ thắng cuộc.

### 5.2. Ma Trận Xử Lý Xung Đột (Conflict Resolver)
- **Vertex Collision:** Cùng đi vào 1 ô trống $\implies$ Cả 2 đứng yên ở vị trí cũ.
- **Swap Collision:** Cố đi xuyên qua nhau $\implies$ Cả 2 bị chặn đứng.
- **Box Contention:** Cùng đẩy 1 hộp $\implies$ Hộp đứng yên, 2 Agent đứng yên.
- **Push Into Opponent:** Đẩy hộp vào ô đối thủ đang đứng $\implies$ Nếu đối thủ không rời ô đó trong lượt này thì cú đẩy bị hủy.

### 5.3. Luật Cướp Hộp (Box Stealing)
Agent đối thủ có quyền đẩy một hộp đang nằm trên đích của đối phương ra ngoài ô thường:
- Điểm của đối thủ bị trừ 1, hộp chuyển về trạng thái trung lập.
- Sau đó Agent có thể đẩy lại hộp này vào một đích khác để ghi điểm cho mình.

### 5.4. Chiến Lược AI & Timeout Guard $\le 1000$ ms
- **Agent A (Real-Time Hungarian A*):** Tìm kiếm mục tiêu tối ưu, coi Agent B là vật cản tạm thời.
- **Agent B (Greedy Best-First with Disruption):** Ưu tiên cướp hộp đối thủ hoặc cản đường đi của Agent A.
- **Timeout Guard:** Ngưỡng an toàn $900$ ms. Nếu thuật toán tìm kiếm chưa hoàn thành trong 900ms, lập tức ngắt vòng lặp an toàn và trả về bước đi tốt nhất hiện có.

---

## 6. THÀNH VIÊN 4: PYGAME GUI OOP, PLAYBACK CONTROLLER & TƯƠNG THÍCH MAC OS VENTURA INTEL

### 6.1. Kiến Trúc GUI Hướng Đối Tượng (OOP)
- Phân chia module: `SokobanApp`, `BoardRenderer`, `PlaybackController`, `UIButton`.
- Tính kích thước ô vuông tự động theo kích thước cửa sổ:
  $$\text{tile\_size} = \min(\lfloor W_{\text{board}} / cols \rfloor, \lfloor H_{\text{board}} / rows \rfloor)$$
- Thứ tự vẽ lớp (Layered Rendering): Background $\to$ Floor $\to$ Walls $\to$ Goals $\to$ Boxes (đổi màu theo Agent A/B) $\to$ Players $\to$ HUD Dashboard.

### 6.2. Bộ Điều Khiển Phát Lại (Playback Controller)
- Phím `Space`: Tạm dừng / Tiếp tục (`is_paused`).
- Phím `→` (Mũi tên phải): Tiến 1 bước trên lịch sử `history`.
- Phím `←` (Mũi tên trái): Lùi 1 bước (Undo tức thì).
- Action Counter trên HUD: Hiển thị tiến độ `Current / Total actions`.

### 6.3. Checklist Tương Thích Hoàn Hảo macOS 13.7.8 (Ventura) Intel Core i5
- Thư viện: `pygame>=2.5.0` (khắc phục triệt để lỗi crash OpenGL và lỗi treo event loop trên Ventura Intel).
- Đường dẫn: 100% sử dụng `pathlib.Path` hoặc `os.path.join`, không dùng dấu gạch chéo Windows `\`.
- Phông chữ: Sử dụng phông hệ thống cross-platform `Helvetica` hoặc `pygame.font.Font(None, size)`.
- Màn hình Retina: Sử dụng cờ `pygame.SCALED` để hiển thị sắc nét và chuẩn xác tọa độ chuột.
