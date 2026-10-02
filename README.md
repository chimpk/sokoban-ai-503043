# Sokoban AI Project (Course: 503043 – Introduction to AI)

> **Học phần:** 503043 - Nhập môn Trí tuệ Nhân tạo (Introduction to Artificial Intelligence)  
> **Khoa:** Công nghệ Thông tin - Trường Đại học Tôn Đức Thắng (TDTU)  
> **Giảng viên phụ trách:** Thầy Nguyễn Thành An (`nguyenthanhan@tdtu.edu.vn`)  
> **Đề bài & Phiếu chấm điểm chính thức:** Đặt tại thư mục `rubric/` ([2627-HK1-AI-GK.pdf](rubric/2627-HK1-AI-GK.pdf) và [RUBRIC_GK.docx](rubric/RUBRIC_GK.docx))

---

## 📌 Phân Công Toàn Diện 4 Thành Viên (Code + Báo Cáo + Soạn Slide + Thuyết Trình)

| Thành viên | Nhiệm vụ Code độc quyền | Slide phụ trách | Thuyết trình (Thời lượng) | Nhánh Git |
| :--- | :--- | :---: | :---: | :--- |
| **Member 1** | 📁 `source/core/`<br>📄 `source/search/ucs.py`<br>📁 `source/tests/` | **Slide 1, 2, 3**<br>*(Formulation & UCS)* | **00:00 - 01:10**<br>*(70 giây)* | `feature/member1-state-ucs` |
| **Member 2** | 📄 `source/search/heuristic.py`<br>📄 `source/search/astar.py`<br>📄 `source/experiment/admissibility.py` | **Slide 4, 5, 6**<br>*(Heuristic, A*, Admissible)* | **01:10 - 02:40**<br>*(90 giây)* | `feature/member2-astar-heuristic` |
| **Member 3** | 📁 `source/competitive/`<br>📁 `source/agents/` | **Slide 7, 8**<br>*(Competitive & AI Agent)* | **02:40 - 03:40**<br>*(60 giây)* | `feature/member3-competitive` |
| **Member 4** | 📁 `source/gui/`<br>📄 `source/experiment/benchmark.py`<br>📄 `source/main.py` | **Slide 9, 10**<br>*(Pygame GUI & Benchmark)* | **03:40 - 04:40**<br>*(60 giây)* | `feature/member4-gui-integration` |
| **Cả nhóm** | Ôn tập câu hỏi vấn đáp bảo vệ (`docs/09_Presentation_Script_and_Oral_QA_Preparation.md`) | -- | **04:40 - 05:00 + Q&A** | `develop` / `main` |

---

## 📊 Thang Điểm Rubric Chính Thức (10.0 Điểm)

1. **Formulation (2.0 điểm):** Biểu diễn State-Space, Actions, Start, Goal, Path Cost, Deadlock concept.
2. **Uninformed Search (3.0 điểm):** Cài đặt UCS + Chạy thực thi + **Visualize kết quả trên Pygame GUI**.
3. **Informed Search (3.0 điểm):** Cài đặt A* & Heuristic (CẤM Euclidean, CẤM Manhattan) + Chạy thực thi + **Visualize kết quả** + Chứng minh & Thực nghiệm Admissible & Consistent.
4. **Presentation (1.0 điểm):** Chuẩn bị tài liệu kỹ lưỡng, slide 4:3 nền sáng in đen trắng đọc rõ, video demo $\le 3$ phút, thuyết trình lưu loát $\le 5$ phút.
5. **Q&A Vấn Đáp (1.0 điểm):** Trả lời chính xác, thuyết phục các câu hỏi vấn đáp trực tiếp từ Giảng viên.

---

## 📖 Hệ Thống Tài Liệu Kỹ Thuật Toàn Diện (`docs/`)

Bộ 10 tài liệu hoàn chỉnh, không để ngỏ bất kỳ câu hỏi nào, cung cấp 100% giải pháp, công thức toán học, thuật toán và kịch bản thuyết trình/vấn đáp:

| STT | File Tài liệu | Mục đích sử dụng & Nội dung cốt lõi | Đối tượng sử dụng |
| :-: | :--- | :--- | :---: |
| **01** | [`01_Project_Overview_Rubric.md`](docs/01_Project_Overview_Rubric.md) | **Tổng quan đề tài & Ma trận Rubric 10.0đ**, ánh xạ chi tiết 8 Yêu cầu kỹ thuật, quy định nộp bài và kỷ luật học thuật. | **Cả nhóm** (Bắt buộc đọc trước) |
| **02** | [`02_Technical_Architecture_and_Member_Solutions.md`](docs/02_Technical_Architecture_and_Member_Solutions.md) | **Kiến trúc hệ thống, từ điển biến & lời giải kỹ thuật toàn diện** cho cả 4 thành viên (không còn câu hỏi tự nghiên cứu). | **Từng thành viên** (Đọc kỹ phần việc của mình) |
| **03** | [`03_State_Space_and_Search_Algorithms.md`](docs/03_State_Space_and_Search_Algorithms.md) | **Mô hình hóa không gian trạng thái toán học AIMA** $\langle \mathcal{S}, s_0, \mathcal{A}, \mathcal{T}, \mathcal{G}, c \rangle$, Canonical state băm $O(1)$, và thuật toán UCS & A* Search chi tiết. | **Member 1, 2** (Formulation & Search) |
| **04** | [`04_Interface_Contracts_and_Testing.md`](docs/04_Interface_Contracts_and_Testing.md) | **Quy ước giao diện bất biến & Kế hoạch kiểm thử toàn diện**, đặc tả dataclasses, 5 bộ Unit Test và danh mục các trường hợp biên (Edge Cases). | **Cả nhóm** (Bắt buộc tuân thủ khi code) |
| **05** | [`05_Heuristic_Proof_and_Experimental_Benchmark.md`](docs/05_Heuristic_Proof_and_Experimental_Benchmark.md) | **Chứng minh toán học Admissible & Consistent**, Heuristic Hungarian Bipartite Matching + Deadlock Pruning, Báo cáo thực nghiệm 0% vi phạm và Benchmark UCS vs A*. | **Member 2, 4** (Trích nội dung vào Slide & Báo cáo) |
| **06** | [`06_Competitive_Game_Theory_and_AI_Design.md`](docs/06_Competitive_Game_Theory_and_AI_Design.md) | **Lý thuyết trò chơi đối kháng 2 Agent**, ma trận phân xử xung đột đồng thời, luật cướp hộp, AI Agent $\le 1000$ ms, bản đồ đối xứng $14 \times 14$ và kiến trúc cắm ghép file thi đấu. | **Member 3, 4** (Chế độ thi đấu đối kháng) |
| **07** | [`07_Pygame_GUI_and_MacOS_Compatibility.md`](docs/07_Pygame_GUI_and_MacOS_Compatibility.md) | **Thiết kế giao diện Pygame OOP**, co giãn tỷ lệ động, bộ điều khiển Playback (Space, $\to$, $\gets$), và checklist tương thích tuyệt đối **macOS 13.7.8 Ventura Intel i5**. | **Member 4** (Giao diện đồ họa) |
| **08** | [`08_Slide_and_Video_Production_Guide.md`](docs/08_Slide_and_Video_Production_Guide.md) | **Hướng dẫn sản xuất Slide 4:3 nền sáng** in đen trắng đọc rõ, cấu trúc 10 slide chuẩn, kịch bản Video Demo $\le 3$ phút và quy cách đóng gói zip tránh mất 50% điểm. | **Cả nhóm** (Làm Slide & Video) |
| **09** | [`09_Presentation_Script_and_Oral_QA_Preparation.md`](docs/09_Presentation_Script_and_Oral_QA_Preparation.md) | **Kịch bản thuyết trình chi tiết từng giây** cho 4 thành viên ($\le 5$ phút) và **Bộ 25 câu hỏi vấn đáp kèm câu trả lời mẫu xuất sắc** bảo vệ 1.0 điểm cá nhân trước Giảng viên. | **Cả nhóm** (Luyện tập thuyết trình & Vấn đáp) |
| **10** | [`10_Admin_and_Pull_Request_Workflow.md`](docs/10_Admin_and_Pull_Request_Workflow.md) | **Quy trình Trưởng nhóm (Admin)** thiết lập quyền bảo vệ nhánh (Branch Protection) và **Pull Request Workflow** để quản lý quá trình ghép code, review code trước khi merge, tránh rủi ro hỏng code gốc. | **Cả nhóm & Admin** (Quản lý merge code) |

---

## 📁 Cấu Trúc Mã Nguồn Chuẩn Nộp Bài

```text
.
├── .gitignore
├── README.md
├── requirements.txt
├── demo.txt
│
├── rubric/                                 # Đề thi & Rubric chính thức của Giảng viên
│   ├── 2627-HK1-AI-GK.pdf
│   └── RUBRIC_GK.docx
│
├── docs/                                   # Bộ 9 tài liệu kỹ thuật & giải pháp lý thuyết hoàn chỉnh
│   ├── 01_Project_Overview_Rubric.md
│   ├── 02_Technical_Architecture_and_Member_Solutions.md
│   ├── 03_State_Space_and_Search_Algorithms.md
│   ├── 04_Interface_Contracts_and_Testing.md
│   ├── 05_Heuristic_Proof_and_Experimental_Benchmark.md
│   ├── 06_Competitive_Game_Theory_and_AI_Design.md
│   ├── 07_Pygame_GUI_and_MacOS_Compatibility.md
│   ├── 08_Slide_and_Video_Production_Guide.md
│   ├── 09_Presentation_Script_and_Oral_QA_Preparation.md
│   └── 10_Admin_and_Pull_Request_Workflow.md
│
└── source/                                 # Toàn bộ mã nguồn chạy được của dự án
    ├── main.py                             # Điểm khởi chạy chương trình (CLI entry point)
    ├── core/                               # Không gian trạng thái & mô hình chuyển tiếp
    ├── search/                             # UCS, A* Search và Heuristic Hungarian
    ├── competitive/                        # Trọng tài đối kháng & Conflict Resolver
    ├── agents/                             # Agent A và Agent B độc lập
    ├── gui/                                # Giao diện Pygame OOP & Playback Controller
    ├── experiment/                         # Script Benchmark & Kiểm chứng Admissibility
    ├── maps/                               # Bộ bản đồ chuẩn thử nghiệm
    └── tests/                              # Unit tests tự động
```

---

## 🗓 Lộ Trình Thực Hiện Dự Án (Roadmap 2 Tuần)

Dự án có thời hạn 3 tuần, do đó lộ trình 2 tuần sẽ giúp nhóm có dư 1 tuần cuối để luyện tập thuyết trình, sửa lỗi và dự phòng rủi ro.

### Tuần 1: Xây Dựng Nền Tảng & Giải Thuật Cốt Lõi
- **Ngày 1-2 (Thiết lập & Core):** 
  - **Member 1:** Hoàn thiện mô hình hoá trạng thái (State, Action) và unit tests cho `core/`.
  - **Member 4:** Dựng khung Pygame, load được map (`example_map.txt`) và hiển thị tĩnh.
- **Ngày 3-5 (Giải thuật & Đấu trí cơ bản):**
  - **Member 1:** Cài đặt xong UCS.
  - **Member 2:** Phác thảo hàm Heuristic và khung A*.
  - **Member 3:** Thiết kế xong luật chơi đối kháng và môi trường cho 2 Agent.
- **Ngày 6-7 (Tích hợp & Báo cáo tiến độ):**
  - **Member 2:** Hoàn thiện A* (không dùng Manhattan/Euclidean).
  - **Member 4:** Nối UCS/A* vào Pygame để agent tự di chuyển (Playback).
  - **Cả nhóm:** Cập nhật tiến độ lần 1.

### Tuần 2: Mở Rộng, Thực Nghiệm & Đóng Gói
- **Ngày 8-9 (Thực nghiệm & Trí tuệ nhân tạo):**
  - **Member 2:** Chạy thực nghiệm chứng minh Heuristic là Admissible và Consistent.
  - **Member 3:** Code xong thuật toán điều khiển cho 2 AI Agent thi đấu (đảm bảo thời gian quyết định < 1000ms).
  - **Member 4:** Xây dựng script Benchmark so sánh UCS và A*.
- **Ngày 10-11 (Ghép Code & Tối Ưu):**
  - **Cả nhóm:** Merge tất cả các nhánh (`feature/...`) vào `develop`. Khắc phục xung đột (Conflict) nếu có. Tối ưu code và fix bug diện rộng.
- **Ngày 12-13 (Tài Liệu & Báo Cáo):**
  - **Cả nhóm:** Soạn Slide (áp dụng tỷ lệ 4:3) theo phần được phân công. Quay Video Demo (< 3 phút).
- **Ngày 14 (Tổng duyệt & Nộp bài):**
  - **Cả nhóm:** Chạy thử Q&A vấn đáp, đóng gói mã nguồn thành file zip theo đúng chuẩn `AI_midterm_<ID Nhóm>_<ID SV>` và nộp bài.

---

## 🚀 Hướng Dẫn Cài Đặt & Chạy Ứng Dụng

### 1. Cài đặt môi trường
Khuyến nghị sử dụng Python 3.10 hoặc 3.11:
```bash
pip install -r requirements.txt
```

### 2. Chạy giải thuật đơn người chơi với giao diện Pygame (Single-Agent Mode)
```bash
# Chạy với thuật toán A* Search (Mặc định)
python source/main.py --map source/maps/example_map.txt --algorithm astar

# Chạy với thuật toán UCS
python source/main.py --map source/maps/example_map.txt --algorithm ucs
```
*Điều khiển trên GUI:*
- `Phím Space`: Tạm dừng / Tiếp tục chạy.
- `Phím Mũi tên phải (→)`: Tiến 1 bước.
- `Phím Mũi tên trái (←)`: Lùi 1 bước.

### 3. Chạy chế độ thi đấu đối kháng 2 Agent (Competitive Two-Agent Mode)
```bash
python source/main.py --mode competitive --steps 100 --map source/maps/competitive_map.txt
```

### 4. Chạy bộ kiểm thử tự động (Unit Tests)
```bash
python -m unittest discover -s source/tests -p "test_*.py" -v
```

### 5. Chạy đo lường thực nghiệm Benchmark (So sánh UCS vs A*)
```bash
python -m source.experiment.benchmark
```
