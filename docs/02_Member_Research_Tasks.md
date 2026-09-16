# 02. PHÂN CÔNG NHIỆM VỤ & ĐỊNH HƯỚNG TỰ NGHIÊN CỨU

Tài liệu này định hướng cho từng thành viên trong nhóm biết rõ:
1. **Phạm vi mã nguồn** mình sở hữu và chịu trách nhiệm.
2. **Những kiến thức / câu hỏi cần tự nghiên cứu** để code và trả lời vấn đáp.
3. **Từ khóa tra cứu học thuật** (Sách giáo trình, bài báo, tài liệu).
4. **Tiêu chuẩn nghiệm thu** trước khi tạo Pull Request vào nhánh `develop`.

---

## Thành Viên 1: Không Gian Trạng Thái & Tìm Kiếm UCS

- **Nhánh Git:** `feature/member1-state-ucs`
- **Mã nguồn phụ trách:**
  - `source/core/parser.py`: Đọc file map định dạng chuẩn `.txt` thành đối tượng bản đồ.
  - `source/core/state.py`: Lớp `State` biểu diễn trạng thái của trò chơi.
  - `source/core/action.py`: Định nghĩa các hướng di chuyển (`North`, `South`, `East`, `West`).
  - `source/core/node.py`: Cấu trúc dữ liệu `SearchNode` (lưu state, parent, action, path_cost).
  - `source/search/ucs.py`: Thuật toán tìm kiếm Uniform-Cost Search.
  - `source/tests/test_state.py`: Unit test kiểm tra tính đúng đắn của logic di chuyển và đẩy hộp.

### ❓ Chủ Đề & Câu Hỏi Cần Tự Nghiên Cứu
1. **Mô hình hóa State:**
   - Trong Sokoban, thành phần nào là **tĩnh** (static) và thành phần nào là **động** (dynamic)? Tại sao không nên nhét danh sách tường (`walls`) và danh sách đích (`goals`) vào phép so sánh trạng thái bằng nhau (`__eq__`) và hàm băm (`__hash__`)?
   - Vị trí các hộp có thứ tự hay không có thứ tự? Nếu dùng `list` các tọa độ hộp thì hai trạng thái có cùng vị trí hộp nhưng khác thứ tự trong list có bị coi là khác nhau không? Cấu trúc dữ liệu nào trong Python giải quyết được vấn đề này (ví dụ: `frozenset` hoặc sorted `tuple`)?
2. **Hàm sinh trạng thái kế tiếp (`get_successors`):**
   - Khi nào người chơi thực hiện được hành động di chuyển thường (`Move`)?
   - Khi nào người chơi thực hiện được hành động đẩy hộp (`Push`)? Ô phía sau hộp phải thỏa mãn điều kiện gì?
   - Cần cập nhật tọa độ người chơi và tọa độ hộp mới ra sao?
3. **Thuật toán UCS (Uniform-Cost Search):**
   - Hàng đợi ưu tiên (Priority Queue) trong Python được cài đặt bằng thư viện nào (`heapq`)?
   - Nếu chi phí mỗi bước đi đều bằng 1 (step cost = 1), thuật toán UCS có điểm gì tương đồng và khác biệt so với BFS?
   - Cần quản lý tập đóng (`closed_set` / `explored`) thế nào để tránh duyệt lại các trạng thái đã đi qua gây lặp vô tận (infinite loop)?

### 🔍 Từ Khóa Tra Cứu
- *Russell & Norvig, "Artificial Intelligence: A Modern Approach" (AIMA) - Chapter 3: Solving Problems by Searching.*
- *Python `heapq` module documentation.*
- *State-space formulation for Sokoban puzzle.*
- *Hashable immutable objects in Python (`frozenset`, `namedtuple`).*

---

## Thành Viên 2: Thiết Kế Heuristic & Tìm Kiếm A* Search

- **Nhánh Git:** `feature/member2-astar-heuristic`
- **Mã nguồn phụ trách:**
  - `source/search/heuristic.py`: Hàm ước lượng chi phí $h(n)$.
  - `source/search/astar.py`: Thuật toán tìm kiếm A\* ($f(n) = g(n) + h(n)$).
  - `source/experiment/admissibility.py`: Kiểm chứng tính chất của hàm Heuristic qua thực nghiệm.

### ❓ Chủ Đề & Câu Hỏi Cần Tự Nghiên Cứu
1. **Lý thuyết về Heuristic:**
   - Heuristic chấp nhận được (**Admissible**) là gì? Tại sao tính chất $h(n) \le h^*(n)$ lại đảm bảo A\* tìm ra lời giải tối ưu (optimal)?
   - Heuristic nhất quán (**Consistent / Monotonic**) là gì? Mối quan hệ $h(n) \le c(n, a, n') + h(n')$ có ý nghĩa gì đối với việc không cần mở lại các node đã nằm trong tập đóng?
2. **Thiết kế Heuristic cho Sokoban:**
   - **Mức cơ bản (Manhattan Distance):** Nếu tính tổng khoảng cách Manhattan từ mỗi hộp đến đích gần nhất $\sum \min |r_b - r_g| + |c_b - c_g|$, hàm này có nhược điểm gì? (Ví dụ: nhiều hộp cùng chọn một đích duy nhất).
   - **Mức nâng cao (Minimum-Cost Bipartite Matching):** Làm thế nào để ghép cặp 1-1 giữa $k$ hộp và $k$ đích sao cho tổng chi phí là nhỏ nhất? Tìm hiểu thuật toán Hungarian (hoặc `scipy.optimize.linear_sum_assignment`).
   - **Khoảng cách thực tế (Maze Distance):** Khoảng cách Manhattan đi xuyên tường có phản ánh đúng số bước đẩy hộp trong mê cung không? Có thể dùng BFS từ trước trên bản đồ tĩnh để tính sẵn khoảng cách thực tế giữa mọi cặp ô sàn không?
   - **Phát hiện Deadlock (Bế tắc):** Khi một hộp bị đẩy vào góc tường (corner) mà ô đó không phải là đích, trạng thái đó có bao giờ giải được nữa không? Tỉa nhánh (pruning) các trạng thái deadlock này bằng cách trả về $h = \infty$ mang lại lợi ích gì cho tốc độ A\*?
3. **Thực nghiệm kiểm chứng tính chất:**
   - Làm thế nào để dùng thực nghiệm chứng minh hàm Heuristic của mình là Admissible? (Gợi ý: Dùng UCS tìm chi phí tối ưu $h^*(n)$ của một tập trạng thái mẫu, sau đó so sánh giá trị $h(n)$ với $h^*(n)$ xem $h(n) \le h^*(n)$ có luôn đúng không).

### 🔍 Từ Khóa Tra Cứu
- *AIMA Chapter 3.5 & 3.6: Informed (Heuristic) Search Strategies, Heuristic Functions.*
- *Bipartite Matching Heuristic for Sokoban.*
- *Hungarian Algorithm / Munkres Algorithm.*
- *Simple Deadlock Detection in Sokoban (Corner Deadlocks, Freeze Deadlocks).*

---

## Thành Viên 3: Đối Kháng 2 Agent (Competitive Solo) & Trọng Tài Game

- **Nhánh Git:** `feature/member3-competitive`
- **Mã nguồn phụ trách:**

  - `source/competitive/state.py`: Lớp trạng thái cho 2 người chơi (Agent A và Agent B).
  - `source/competitive/conflict.py`: Bộ quy tắc phân xử va chạm/xung đột khi 2 agent cùng di chuyển.
  - `source/competitive/engine.py`: Vòng lặp điều phối trận đấu giữa 2 agent với giới hạn thời gian mỗi bước $\le 1000$ms.
  - `source/agents/agent_a.py`: Thuật toán của Agent A (Chiến lược 1).
  - `source/agents/agent_b.py`: Thuật toán của Agent B (Chiến lược 2).

### ❓ Chủ Đề & Câu Hỏi Cần Tự Nghiên Cứu
1. **Luật thi đấu đối kháng (Competitive Mechanics):**
   - Hai agent cùng nằm trên một bản đồ có nhiều hộp và nhiều đích. Cả 2 cùng đưa ra quyết định di chuyển đồng thời (simultaneous move) trong vòng tối đa $1000$ms.
   - Các trường hợp xung đột (Conflict) có thể xảy ra:
     * **Vertex Conflict:** Cả 2 agent cùng muốn bước vào cùng một ô $(r, c)$. Phân xử thế nào? (Ví dụ: cả 2 cùng bị đứng yên, hoặc ưu tiên agent có khoảng cách gần hơn).
     * **Edge / Swap Conflict:** Agent A ở ô 1 muốn sang ô 2, trong khi Agent B ở ô 2 muốn sang ô 1.
     * **Box Contention:** Cả 2 agent cùng muốn đẩy cùng một chiếc hộp theo hai hướng khác nhau.
   - Khi một agent đã đẩy được một hộp vào đích thành công: Agent kia có được phép đẩy chiếc hộp đó ra khỏi đích để phá hoặc cướp điểm không?
2. **Chiến thuật Agent:**
   - **Agent A (Chiến lược Tham lam - Greedy):** Luôn tìm kiếm hộp tự do gần mình nhất và đẩy vào đích tự do gần nhất. Dễ cài đặt, phản ứng nhanh.
   - **Agent B (Chiến lược Nâng cao):** Dự đoán hướng đi của Agent A, ưu tiên chiếm giữ các hộp ở vị trí cạnh tranh cao, hoặc tìm cách phong tỏa đường đi của đối phương.
3. **Cách tính điểm (Scoring):**
   - Trận đấu dừng lại sau $n$ lượt bước (turns) hoặc khi tất cả các hộp đã vào đích.
   - Điểm số được tính dựa trên: Số hộp do agent đưa vào đích thành công, số bước di chuyển hiệu quả, hình phạt nếu chạy quá thời gian (timeout > 1000ms).

### 🔍 Từ Khóa Tra Cứu
- *Multi-Agent Path Finding (MAPF) with conflict resolution.*
- *Simultaneous Move Games in AI.*
- *Greedy vs Strategic heuristic search agents.*

---

## Thành Viên 4: Giao Diện Pygame, Playback & Đánh Giá Thực Nghiệm

- **Nhánh Git:** `feature/member4-gui-integration`
- **Mã nguồn phụ trách:**
  - `source/gui/renderer.py`: Vẽ bản đồ, tường, sàn, hộp, người chơi, đích lên cửa sổ Pygame.
  - `source/gui/playback.py`: Bộ điều khiển phát lại chuỗi hành động (Play, Pause, Step Next, Step Prev).
  - `source/gui/game.py`: Vòng lặp chính của ứng dụng GUI Pygame.
  - `source/experiment/benchmark.py`: Kịch bản chạy tự động đo lường hiệu năng UCS vs A\*.
  - `source/main.py`: Điểm khởi chạy chương trình từ dòng lệnh.

### ❓ Chủ Đề & Câu Hỏi Cần Tự Nghiên Cứu
1. **Trực quan hóa đồ họa (Pygame GUI):**
   - Làm thế nào để tính toán kích thước ô vuông (`tile_size`) phù hợp với kích thước cửa sổ màn hình, bất kể bản đồ to hay nhỏ?
   - Cần vẽ các lớp hình ảnh (layers) theo thứ tự nào để không bị đè hình? (Thứ tự chuẩn: Nền sàn -> Tường -> Ô đích -> Hộp / Hộp trên đích -> Người chơi).
   - Cơ chế Playback: Làm thế nào để tua ngược (Undo/Previous step)? Cần lưu trữ lịch sử trạng thái (`state_history`) như thế nào khi người dùng ấn phím Mũi tên trái ($\leftarrow$)?
2. **Đo lường & So sánh thực nghiệm:**
   - Đề bài và Rubric yêu cầu so sánh những chỉ số nào giữa UCS và A\*?
     * **Thời gian thực thi (Execution Time):** Đo bằng `time.perf_counter()` (đơn vị: ms).
     * **Bộ nhớ tiêu thụ (Peak Memory):** Đo bằng module `tracemalloc` (đơn vị: KB hoặc MB).
     * **Số bước giải (Solution Length / Steps):** Tổng số hành động trong lời giải.
     * **Chi phí lời giải (Path Cost):** Tổng chi phí thực tế.
     * **Số node đã mở rộng (Nodes Expanded):** Số trạng thái được lấy ra khỏi hàng đợi ưu tiên.
     * **Số node đã sinh ra (Nodes Generated):** Tổng số node con được tạo ra trong quá trình tìm kiếm.
   - Cách xuất kết quả ra bảng và dùng `matplotlib` vẽ biểu đồ trực quan (biểu đồ cột so sánh thời gian và số node mở rộng) để chèn vào Slide thuyết trình.

### 🔍 Từ Khóa Tra Cứu
- *Pygame grid-based game rendering tutorial.*
- *State pattern and history tracking for Undo/Redo in games.*
- *Python `time.perf_counter` and `tracemalloc` benchmarking.*
- *Matplotlib grouped bar chart for algorithm comparison.*
