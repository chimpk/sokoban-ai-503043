# 01. TỔNG QUAN ĐỀ TÀI & BẢNG QUY ĐỊNH CHẤM ĐIỂM (RUBRIC MAPPING)

> **Học phần:** 503043 - Nhập môn Trí tuệ Nhân tạo (Introduction to Artificial Intelligence)  
> **Đơn vị đào tạo:** Khoa Công nghệ Thông tin - Trường Đại học Tôn Đức Thắng (TDTU)  
> **Giảng viên phụ trách:** Thầy Trịnh Hùng Cường  
> **Tài liệu gốc đối chiếu:**  
> - Đề bài chính thức: `rubric/2627-HK1-AI-GK.pdf` (Task 1: 8.0 điểm, Task 2: 2.0 điểm, 8 Yêu cầu kỹ thuật)  
> - Phiếu chấm điểm chính thức: `rubric/RUBRIC_GK.docx` (Thang điểm Rubric 10.0, 5 tiêu chí chuẩn hóa)

---

## 1. Mục Tiêu Dự Án & Tầm Nhìn Kỹ Thuật

Dự án yêu cầu xây dựng một hệ thống hoàn chỉnh giải bài toán **Sokoban** cổ điển bằng các phương pháp Tìm kiếm không gian trạng thái (State-Space Search) kinh điển của Trí tuệ Nhân tạo, đồng thời mở rộng sang mô hình **Đối kháng 2 Agent (Competitive Two-Agent Problem)**.

Mục tiêu chất lượng: **Đạt điểm tối đa (10.0/10.0)** ở tất cả các hạng mục đánh giá bằng cách giải quyết triệt để mọi yêu cầu, có lập luận toán học chặt chẽ, cài đặt mã nguồn chuẩn mực OOP, giao diện trực quan thân thiện và chuẩn bị bài thuyết trình, vấn đáp sắc bén.

---

## 2. Ma Trận Đối Chiếu Chi Tiết: Đề Bài (PDF) vs Phiếu Chấm Điểm (Word Rubric)

Bảng dưới đây ánh xạ 1-1 giữa 5 tiêu chí của `RUBRIC_GK.docx` và 8 yêu cầu kỹ thuật cùng Task 2 trong `2627-HK1-AI-GK.pdf`:

| Tiêu chí Rubric (RUBRIC_GK.docx) | Trọng số Rubric | Yêu cầu tương ứng trong Đề bài (2627-HK1-AI-GK.pdf) | Tiêu chuẩn đạt mức tối đa (> 80% Hoàn thành) | Thành viên phụ trách chính |
| :--- | :---: | :--- | :--- | :--- |
| **1. Formulation** (Biểu diễn bài toán) | **2.0 điểm** | **Requirement 1 (1.0đ):** Biểu diễn bài toán Sokoban dưới dạng state-space search.<br>**Requirement 6 (1.0đ):** Tái biểu diễn thành bài toán đối kháng 2 Agent. | • Trình bày tường minh: State space, Action space, Transition model, Goal test, Path cost, Start state.<br>• Phân tách rõ thành phần Động (Dynamic: player, boxes) và Tĩnh (Static: walls, goals) để tối ưu bộ nhớ.<br>• Mô hình hóa đầy đủ cơ chế đối kháng: Hành động đồng thời (Simultaneous), luật $n$ bước, cướp hộp, xử lý xung đột (Conflict resolution). | **Member 1 (Req 1)**<br>+<br>**Member 3 (Req 6)** |
| **2. Uninformed Search** (Tìm kiếm mù) | **3.0 điểm** | **Requirement 2 (0.5đ):** Cài đặt UCS.<br>**Requirement 3 (0.5đ):** Thực nghiệm UCS vs A* (Time & Space).<br>**Requirement 5 (1.0đ):** Giao diện Pygame hiển thị kết quả UCS.<br>**Requirement 7 (1.0đ):** Thuật toán điều khiển Agent (UCS/BFS/DFS/IDS). | • Cài đặt thuật toán Uniform-Cost Search (UCS) chuẩn xác với Priority Queue (`heapq`).<br>• Quản lý tập đóng (`explored_set`) ngăn ngừa vòng lặp vô tận.<br>• Thực thi trên các bản đồ thử nghiệm, ghi nhận đầy đủ Time, Nodes Expanded, Nodes Generated, Peak Memory.<br>• Trực quan hóa đường đi giải được từng bước trên Pygame GUI có nút Play/Pause/Step. | **Member 1 (Code UCS)**<br>+<br>**Member 4 (GUI & Benchmark)**<br>+<br>**Member 3 (Agent AI)** |
| **3. Informed Search** (Tìm kiếm có thông tin) | **3.0 điểm** | **Requirement 2 (0.5đ):** Cài đặt A* và đề xuất Heuristic (CẤM Euclidean, CẤM Manhattan).<br>**Requirement 4 (1.0đ):** Phân tích và kiểm chứng Admissible & Consistent.<br>**Requirement 5 (0.5đ):** Giao diện Pygame hiển thị kết quả A*.<br>**Requirement 8 (1.0đ):** Reimplement GUI đối kháng, hộp màu riêng, mã nguồn Agent tách rời. | • Đề xuất hàm Heuristic sáng tạo, hiệu quả: **Minimum-Cost Bipartite Matching trên khoảng cách đường đi thực tế men theo tường (Static Maze Distance)** kết hợp **Deadlock Detection**.<br>• Chứng minh lý thuyết tính Admissible ($h(n) \le h^*(n)$) và Consistent ($h(n) \le c + h(n')$).<br>• Thiết kế và chạy thực nghiệm kiểm chứng 2 tính chất trên tập dữ liệu mẫu, báo cáo tỷ lệ vi phạm = 0%.<br>• Trực quan hóa A* trên GUI Pygame.<br>• GUI đối kháng phân biệt màu hộp của từng Agent, tải động file agent độc lập. | **Member 2 (Heuristic & A*, Proof)**<br>+<br>**Member 4 (GUI & Experiments)**<br>+<br>**Member 3 (Competitive GUI)** |
| **4. Presentation: Materials & Fluency** | **1.0 điểm** | **Task 2:** Bộ tài liệu báo cáo, Slide 4:3, Video Demo $\le 3$ phút, thuyết trình lưu loát $\le 5$ phút. | • Slide đúng tỉ lệ 4:3, nền sáng (light background), in đen trắng vẫn đọc rõ.<br>• Trình bày bằng sơ đồ/mã giả (pseudocode), tuyệt đối KHÔNG dán code thô lên slide.<br>• Đầy đủ danh sách thành viên, tỷ lệ đóng góp, ưu nhược điểm giải pháp.<br>• Thuyết trình mạch lạc, kiểm soát thời gian chặt chẽ $\le 5$ phút.<br>• Video demo $\le 3$ phút đầy đủ tính năng, dẫn link tại `demo.txt`. | **Cả 4 thành viên**<br>(Mỗi người 60 - 75 giây) |
| **5. Presentation: Q&A** | **1.0 điểm** | **Task 2:** Trả lời chính xác, thuyết phục các câu hỏi vấn đáp trực tiếp từ Giảng viên. | • Từng thành viên nắm vững phần việc của mình, hiểu sâu mã nguồn và lý thuyết toán học nền tảng.<br>• Giải thích mạch lạc cơ chế thuật toán, nguyên nhân chọn thiết kế, các trường hợp biên (edge cases). | **Cả 4 thành viên** |
| **TỔNG CỘNG** | **10.0 điểm** | | **Cam kết chuẩn đầu ra: Đạt điểm tối đa 10.0** | |

---

## 3. Chi Tiết 8 Yêu Cầu Kỹ Thuật (Task 1: 8.0 Điểm)

### Requirement 1 (1.0 điểm): Mô hình hóa State-Space Search
- **Đầu vào:** File text bản đồ (ví dụ: `example_map.txt`).
- **Ký hiệu bản đồ:**
  - `%`: Tường / Vật cản (Obstacles / Walls)
  - `A`: Vị trí xuất phát của người chơi (The Agent / The Man)
  - `B`: Hộp (Boxes)
  - `D`: Vị trí đích cần đưa hộp vào (Designated positions - Red points)
  - `C`: Hộp đang nằm sẵn trên vị trí đích (Dark brown boxes)
  - ` ` (khoảng trắng): Ô sàn trống (Blank walkable cells)
- **Đầu ra:** Danh sách hành động (`North`, `East`, `West`, `South`) và tổng chi phí (`total cost`).
- **Biểu diễn toán học chuẩn:**
  - Trạng thái $S = (p, B)$ với $p = (r, c)$ là tọa độ người chơi, $B = \{(r_{b1}, c_{b1}), \dots\}$ là tập tọa độ các hộp.
  - Tường $W$ và Đích $G$ là bất biến (static environment).

### Requirement 2 (1.0 điểm): Cài đặt UCS, A* và Thiết kế Heuristic
- **Cài đặt UCS:** Mở rộng node theo thứ tự chi phí $g(n)$ tăng dần.
- **Cài đặt A\*:** Mở rộng node theo hàm đánh giá $f(n) = g(n) + h(n)$.
- **QUY ĐỊNH BẮT BUỘC TỪ ĐỀ BÀI:**
  > *"Note that Euclidean and Manhattan distances are not allowed."*  
  > (Lưu ý: Tuyệt đối KHÔNG ĐƯỢC PHÉP sử dụng khoảng cách Euclidean và Manhattan).
- **Giải pháp đề xuất chuẩn mực:**
  - **Static Maze Distance:** Tính khoảng cách ngắn nhất trên lưới sàn men theo tường bằng BFS tĩnh xuất phát từ các ô đích (bỏ qua các hộp khác và người chơi).
  - **Minimum-Cost Bipartite Matching:** Ghép cặp tối ưu 1-1 giữa tập hộp và tập đích bằng thuật toán Hungarian (Kuhn-Munkres) hoặc Linear Sum Assignment để tìm cận dưới tổng khoảng cách di chuyển nhỏ nhất.
  - **Deadlock Pruning:** Nhận diện các trạng thái bế tắc (hộp kẹt góc tường, hộp dạt vào tường biên không có đích, hộp dính chùm 2x2) để gán $h(s) = \infty$, lập tức loại bỏ khỏi không gian tìm kiếm.

### Requirement 3 (1.0 điểm): Thực nghiệm So sánh UCS vs A* (Time & Space)
- Phương pháp thực nghiệm: Chạy tự động hai thuật toán trên bộ dữ liệu kiểm thử chuẩn (từ bản đồ dễ 1-2 hộp đến bản đồ chuẩn `example_map.txt` 7 hộp).
- Chỉ số định lượng bắt buộc:
  1. Thời gian chạy (Execution Time tính bằng milliseconds / seconds).
  2. Số node đã lấy ra khỏi Frontier để mở rộng (Nodes Expanded).
  3. Số node con được sinh ra (Nodes Generated).
  4. Dung lượng bộ nhớ đỉnh điểm (Peak Memory dùng `tracemalloc`).
  5. Độ dài lời giải / Chi phí đường đi (Solution Cost / Path Length).
  6. Hệ số phân nhánh hiệu dụng (Effective Branching Factor $b^*$).
- Xuất dữ liệu bảng biểu và biểu đồ so sánh để đưa vào Slide.

### Requirement 4 (1.0 điểm): Phân tích & Thực nghiệm Tính Admissible và Consistent
- **Lý thuyết:**
  - Chứng minh $h(n) \le h^*(n)$ (Admissibility) với mọi $n$.
  - Chứng minh $h(n) \le c(n, a, n') + h(n')$ (Consistency / Monotonicity) với mọi bước chuyển.
- **Thực nghiệm:**
  - Lấy mẫu $K$ trạng thái hợp lệ trên không gian tìm kiếm.
  - Sử dụng UCS để tính chi phí tối ưu chính xác tuyệt đối $h^*(s)$.
  - Đo độ lệch $h(s) \le h^*(s)$ trên toàn bộ mẫu (Số vi phạm = 0).
  - Kiểm tra bất đẳng thức tam giác trên hàng ngàn bước chuyển $(s, a, s')$ (Số vi phạm = 0).

### Requirement 5 (1.0 điểm): Giao diện Pygame Thân Thiện, Hướng Đối Tượng & Tương Thích macOS
- **Tính năng bắt buộc:**
  - Tùy chọn 2 thuật toán: `UCS` và `A*`.
  - Hiển thị số lượng hành động trên màn hình (Action counter: `Current / Total`).
  - Phím điều khiển phát lại (Playback controls):
    - `Space`: Tạm dừng / Tiếp tục (Pause / Resume).
    - `→` (Mũi tên phải): Tiến 1 bước (Step forward).
    - `←` (Mũi tên trái): Lùi 1 bước (Step backward).
- **Tiêu chuẩn lập trình:**
  - Tổ chức theo mô hình Hướng đối tượng (OOP) chặt chẽ: `Game`, `Renderer`, `PlaybackController`, `Button`.
  - Mã nguồn tinh gọn, cấu trúc rõ ràng.
- **YÊU CẦU TƯƠNG THÍCH ĐẶC BIỆT:**
  > *"Ensure that the project can be executed on macOS 13.7.8 (Ventura) with an Intel Core i5 processor. Carefully verify the versions of all relevant Python libraries."*  
  > (Bắt buộc chạy được trơn tru trên macOS Ventura 13.7.8 chip Intel i5: Dùng `pygame>=2.5.0`, sử dụng `os.path.join` chuẩn hóa đường dẫn, không hardcode font Windows, xử lý màn hình Retina).

### Requirement 6 (1.0 điểm): Tái biểu diễn Bài toán Đối kháng 2 Agent (Competitive Two-Agent)
- Hai Agent (`Agent A` và `Agent B`) cùng thi đấu đẩy hộp về đích trên cùng bản đồ.
- Người dùng nhập số bước tối đa $n$. Sau $n$ bước, Agent nào đưa được nhiều hộp vào đích hơn sẽ thắng cuộc.
- Luật cướp hộp: Cho phép một agent đẩy một hộp mà đối thủ đã đặt vào đích ra khỏi đích để ghi điểm lại.
- **Hành động đồng thời (Simultaneous Moves):** Cả 2 agent đưa ra quyết định cùng lúc tại mỗi bước thời gian.
- **Vật lý không gian:** Hai agent không được đi xuyên qua nhau.
- Bản đồ đối kháng: Thiết kế bản đồ đối xứng, rộng hơn để tạo môi trường cạnh tranh công bằng.

### Requirement 7 (1.0 điểm): Thiết kế Thuật toán AI cho Agent Đối Kháng (≤ 1,000 ms)
- Ứng dụng các thuật toán đã học: BFS, UCS, DFS, DLS, IDS, GBFS, hoặc A*.
- **RÀNG BUỘC THỜI GIAN NGHIÊM NGẶT:**
  > *"The time limit for each decision-making step is 1,000 ms."*  
  > (Giới hạn thời gian cho mỗi quyết định là 1.0 giây).
- Thiết kế cơ chế Timeout Guard: Nếu thuật toán tìm kiếm chưa hoàn tất trong 950ms, hệ thống tự động trả về hành động an toàn tốt nhất hiện có (Fallback Greedy Action).

### Requirement 8 (1.0 điểm): Giao diện Đối Kháng & Kiến Trúc Mã Nguồn Độc Lập
- Nâng cấp giao diện Pygame cho chế độ đối kháng:
  - Hiển thị 2 Agent với avatar/màu sắc trực quan khác biệt.
  - Các hộp do các Agent khác nhau chiếm giữ / đưa vào đích được tô **MÀU SẮC KHÁC NHAU**.
  - Hiển thị bảng tỉ số thời gian thực (Scoreboard) và số bước còn lại ($n - \text{current}$).
- **Kiến trúc mã nguồn độc lập (Pluggable Agent Architecture):**
  - Thuật toán của 2 Agent nằm ở 2 file riêng biệt: `source/agents/agent_a.py` và `source/agents/agent_b.py`.
  - Có thể dễ dàng thay thế file của nhóm khác vào để thi đấu đối kháng trực tiếp.

---

## 4. Chi Tiết Task 2: Thuyết Trình, Video Demo & Quy Định Nộp Bài (2.0 Điểm)

### 4.1. Quy Định Slide Thuyết Trình (presentation.pdf)
1. **Tỷ lệ khung hình:** Bắt buộc **4:3** (Không dùng 16:9).
2. **Màu sắc & Phông nền:**
   - **TRÁNH:** Phông nền tối (dark background) và các hình khối màu mè phức tạp vì máy chiếu giảng đường rất mờ.
   - **BẮT BUỘC:** Thiết kế phông nền sáng, độ tương phản cao, đảm bảo **in ra đen trắng (grayscale) vẫn đọc rõ ràng 100%**.
3. **Nội dung slide:**
   - Slide 1: Bảng thành viên (MSSV, Họ tên, Email, Nhiệm vụ được phân công, Tỷ lệ hoàn thành %).
   - Trình bày giải pháp bằng **sơ đồ khối (diagrams) và mã giả (pseudocode)**. Tuyệt đối KHÔNG dán code thô vào slide.
   - Phân tích rõ Ưu điểm (Advantages) và Nhược điểm (Disadvantages) của từng giải pháp tiếp cận.
   - Bảng tổng kết tỷ lệ hoàn thành từng Task.
4. **Thời lượng thuyết trình:** **Tối đa 05 phút** (Quá thời gian sẽ bị dừng bài và trừ điểm).

### 4.2. Quy Định Video Demo (demo.txt)
- Thời lượng video: **Tối đa 03 phút**.
- File nộp: `demo.txt` chứa duy nhất đường link truy cập video (YouTube không công khai hoặc Google Drive mở quyền truy cập).
- Nội dung video cần quay đủ:
  1. Chạy thuật toán UCS và A* giải bản đồ mẫu trên Pygame GUI.
  2. Thao tác các phím Space (Pause), Mũi tên phải (Next step), Mũi tên trái (Prev step).
  3. Chạy chế độ thi đấu đối kháng 2 Agent với $n$ bước người dùng nhập, minh họa hộp đổi màu và xử lý va chạm.

### 4.3. Cấu Trúc Gói Nộp Bài & Tên File Bắt Buộc
- Tên thư mục gốc và file nén zip:
  `AI_midterm_<project group ID>_<your student ID>.zip`
- Cấu trúc bên trong file nén:
  ```text
  AI_midterm_<groupID>_<studentID>/
  ├── source/                      # Thư mục mã nguồn chạy được
  │   ├── main.py                  # File chạy chính
  │   ├── core/                    # State, Action, Parser, Node
  │   ├── search/                  # UCS, A*, Heuristic
  │   ├── gui/                     # Pygame Renderer, Controls, Playback
  │   ├── competitive/             # Engine, Conflict Resolver, State
  │   ├── agents/                  # agent_a.py, agent_b.py
  │   ├── experiment/              # Benchmark, Admissibility checker
  │   ├── maps/                    # example_map.txt, map_02.txt,...
  │   └── tests/                   # Unit tests
  ├── presentation.pdf             # Slide thuyết trình tỷ lệ 4:3
  └── demo.txt                     # File text chứa URL video demo <= 3 phút
  ```

---

## 5. Chính Sách Kỷ Luật Học Thuật & Phòng Tránh Rủi Ro Điểm 0

1. **Nộp trễ hạn:** Bất kỳ nhóm nào nộp trễ hạn đều nhận điểm **0.0** cho toàn bộ thành viên.
2. **Thiếu tài liệu nộp:** Thiếu bất kỳ tài liệu bắt buộc nào (`source/`, `presentation.pdf`, `demo.txt`) sẽ bị trừ **tối thiểu 50% tổng điểm phần thuyết trình**.
3. **Sao chép mã nguồn:** Sao chép code trên Internet hoặc sao chép giữa các nhóm sẽ nhận điểm **0.0** ngay lập tức và chuyển lên Hội đồng kỷ luật.
4. **Quy định về AI:**
   > *"The use of AI tools is prohibited in this project. If any AI-generated symbols or other identifiable AI-generated content are found in the source code files, the group will receive a score of 0.0 for the corresponding task."*  
   - Mã nguồn phải được viết bằng tay, sạch sẽ, chuẩn PEP 8.
   - Không chứa bất kỳ comment, ký hiệu, hay watermark đặc trưng của các công cụ sinh mã AI.
   - Từng thành viên phải nắm rõ từng dòng lệnh do mình phụ trách để trả lời câu hỏi vấn đáp cá nhân (1.0 điểm).
