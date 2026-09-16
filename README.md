# Sokoban AI Project (Course: 503043 – Introduction to AI)

Dự án môn học **503043 - Nhập môn Trí tuệ Nhân tạo (Introduction to Artificial Intelligence)**.
Triển khai giải thuật tìm kiếm không gian trạng thái (State-Space Search) cho trò chơi Sokoban (đơn người chơi và đối kháng hai người chơi).

---

## 📌 Phân công Toàn diện 4 Thành viên (Code + Soạn Slide + Thuyết trình)

| Thành viên | Nhiệm vụ Code độc quyền | Slide phụ trách | Thuyết trình (Thời lượng) | Nhánh Git |
| :--- | :--- | :---: | :---: | :--- |
| **Member 1** | 📁 `source/core/`<br>📄 `source/search/ucs.py`<br>📁 `source/tests/` | **Slide 1, 2, 3**<br>*(Formulation & UCS)* | **00:00 - 01:10**<br>*(70 giây)* | `feature/member1-state-ucs` |
| **Member 2** | 📄 `source/search/heuristic.py`<br>📄 `source/search/astar.py`<br>📄 `source/experiment/admissibility.py` | **Slide 4, 5, 6**<br>*(Heuristic, A*, Admissible)* | **01:10 - 02:40**<br>*(90 giây)* | `feature/member2-astar-heuristic` |
| **Member 3** | 📁 `source/competitive/`<br>📁 `source/agents/` | **Slide 7, 8**<br>*(Competitive & AI Agent)* | **02:40 - 03:40**<br>*(60 giây)* | `feature/member3-competitive` |
| **Member 4** | 📁 `source/gui/`<br>📄 `source/experiment/benchmark.py`<br>📄 `source/main.py` | **Slide 9, 10**<br>*(Pygame GUI & Benchmark)* | **03:40 - 04:40**<br>*(60 giây)* | `feature/member4-gui-integration` |
| **Cả nhóm** | Ôn tập câu hỏi vấn đáp (`docs/04_Slide_and_Video_Requirements.md`) | -- | **04:40 - 05:00 + Q&A** | |


---

## 📊 Thang điểm Rubric Chính thức (10.0 Điểm)

1. **Formulation (2.0 điểm):** Biểu diễn State, Actions, Start, Goal, Path cost.
2. **Uninformed Search (3.0 điểm):** Cài đặt UCS + Chạy thực thi + **Visualize kết quả**.
3. **Informed Search (3.0 điểm):** Cài đặt A* & Heuristic + Chạy thực thi + **Visualize kết quả**.
4. **Presentation (1.0 điểm):** Chuẩn bị tài liệu, slide 4:3, video demo <= 3 phút, trình bày lưu loát trong <= 5 phút.
5. **Q&A Vấn đáp (1.0 điểm):** Trả lời chính xác các câu hỏi của Giảng viên.

---

## 📖 Tài Liệu Hướng Dẫn & Nhiệm Vụ Nghiên Cứu (`docs/`)

Thư mục `docs/` được tinh gọn thành 4 tài liệu cốt lõi giúp các thành viên định hướng tự học, tự nghiên cứu và phối hợp hiệu quả:

| STT | File Tài liệu | Mục đích sử dụng & Nội dung chính | Đối tượng |
| :-: | :--- | :--- | :---: |
| **01** | [`01_Project_Overview_Rubric.md`](docs/01_Project_Overview_Rubric.md) | **Tổng quan đề tài & Bảng điểm Rubric 10.0đ** từ Giảng viên, quy định nộp bài và chống đạo văn / AI policy. | **Cả nhóm** (Bắt buộc đọc đầu tiên) |
| **02** | [`02_Member_Research_Tasks.md`](docs/02_Member_Research_Tasks.md) | **Phân công nhiệm vụ, câu hỏi tự nghiên cứu, từ khóa tra cứu học thuật** và tiêu chuẩn nghiệm thu cho từng thành viên. | **Từng thành viên** (Đọc kỹ phần của mình) |
| **03** | [`03_Interface_Contracts.md`](docs/03_Interface_Contracts.md) | **Quy ước kỹ thuật & Giao diện dùng chung:** Hệ tọa độ `(row, col)`, cấu trúc `State`, kiểu dữ liệu Input/Output của các hàm tìm kiếm để 4 bạn code độc lập không bị xung đột khi merge. | **Cả nhóm** (Bắt buộc tuân thủ khi code) |
| **04** | [`04_Slide_and_Video_Requirements.md`](docs/04_Slide_and_Video_Requirements.md) | **Quy định Slide 4:3, Video demo <= 3 phút** và các nhóm câu hỏi trọng tâm ôn tập vấn đáp bảo vệ (Q&A). | **Cả nhóm** (Dùng khi làm Slide & Ôn thi) |


---

## 🌳 Quy trình làm việc Git (Git Workflow)

```text
main (Production / Stable Release)
  └── develop (Integration branch)
        ├── feature/member1-state-ucs
        ├── feature/member2-astar-heuristic
        ├── feature/member3-competitive
        └── feature/member4-gui-integration

```

### Hướng dẫn cho từng thành viên:
1. **Chuyển sang nhánh của mình:**
   ```bash
   git checkout feature/member<X>-<tên_nhánh>
   ```
2. **Cập nhật code mới nhất từ `develop` trước khi code:**
   ```bash
   git pull origin develop
   ```
3. **Commit công việc thường xuyên:**
   ```bash
   git add .
   git commit -m "feat: mô tả công việc vừa hoàn thành"
   git push origin feature/member<X>-<tên_nhánh>
   ```
4. **Hợp nhất (Merge):**
   - Khi hoàn thành tính năng, tạo **Pull Request (PR)** từ `feature/member<X>...` vào `develop`.
   - Cả nhóm review, sau đó merge vào `develop`.
   - Cuối kỳ, sau khi toàn bộ hệ thống chạy ổn định, merge `develop` vào `main`.

---

## 📁 Cấu trúc thư mục dự án chuẩn theo quy chế nộp bài

```text
.
├── .gitignore
├── README.md
├── requirements.txt
├── demo.txt
│
├── rubric/                                 # Tài liệu đề bài & phiếu chấm điểm từ Thầy/Cô
│   ├── 2627-HK1-AI-GK.pdf                  (Đề thi giữa kỳ chính thức)
│   └── RUBRIC_GK.docx                      (Phiếu chấm điểm Rubric chính thức)
│
├── docs/                                   # Bộ tài liệu yêu cầu, nhiệm vụ & quy ước kỹ thuật
│   ├── 01_Project_Overview_Rubric.md
│   ├── 02_Member_Research_Tasks.md
│   ├── 03_Interface_Contracts.md
│   └── 04_Slide_and_Video_Requirements.md
│
└── source/                                 # Thư mục chứa toàn bộ mã nguồn của dự án
    ├── main.py                             # [Member 4] Entry point khởi chạy
    ├── core/                               # [Member 1] Mô hình hóa State-space
    ├── search/                             # [Member 1 & 2] UCS, A*, Heuristic
    ├── experiment/                         # [Member 2 & 4] Admissibility, Benchmark
    ├── competitive/                        # [Member 3] Chế độ đối kháng 2 Agent
    ├── gui/                                # [Member 4] Giao diện Pygame
    ├── tests/                              # [Member 1] Unit tests
    ├── agents/                             # [Member 3] 2 Agent thi đấu độc lập
    │   ├── agent_a.py
    │   └── agent_b.py
    └── maps/                               # 2 bản đồ demo
        ├── map_01.txt                      (Bản đồ demo 1 - từ đề thi chính thức)
        └── map_02.txt                      (Bản đồ demo 2 - mê cung 2 hộp)
```

---

## 🚀 Hướng dẫn cài đặt & Chạy chương trình

### 1. Cài đặt thư viện:
```bash
pip install -r requirements.txt
```

### 2. Chạy chương trình chính (Sokoban GUI):
```bash
python source/main.py
```

### 3. Phím điều khiển giao diện:
- `Space`: Tạm dừng / Tiếp tục phát lại (Pause / Play).
- `→` (Mũi tên phải): Tiến 1 bước (Step forward).
- `←` (Mũi tên trái): Lùi 1 bước (Step backward).

