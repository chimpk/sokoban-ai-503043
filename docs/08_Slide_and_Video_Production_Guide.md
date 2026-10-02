# 08. HƯỚNG DẪN SẢN XUẤT SLIDE THUYẾT TRÌNH & VIDEO DEMO
## (SLIDE & VIDEO DEMO PRODUCTION GUIDE)

> **Tài liệu phục vụ cho:**  
> - **Task 2: Presentation & Submission (2.0 điểm)** trong đề bài chính thức.  
> - **Tiêu chí 4: Presentation - Materials & Fluency (1.0 điểm Rubric)**.

---

## MỤC LỤC
1. [Quy Định Bắt Buộc Về Slide Thuyết Trình (`presentation.pdf`)](#1-quy-định-bắt-buộc-về-slide-thuyết-trình-presentationpdf)
2. [Cấu Trúc Khung 10 Slide Chuẩn 4:3 Ăn Trọn Điểm Rubric](#2-cấu-trúc-khung-10-slide-chuẩn-43-ăn-trọn-điểm-rubric)
3. [Quy Định & Kịch Bản Quay Video Demo $\le 3$ Phút (`demo.txt`)](#3-quy-định--kịch-bản-quay-video-demo-le-3-phút-demotxt)
4. [Quy Cách Đóng Gói Hồ Sơ Nộp Bài Tránh Bị Trừ 50% Điểm](#4-quy-cách-đóng-gói-hồ-sơ-nộp-bài-tránh-bị-trừ-50-điểm)

---

## 1. QUY ĐỊNH BẮT BUỘC VỀ SLIDE THUYẾT TRÌNH (`presentation.pdf`)

Căn cứ theo đề bài chính thức `rubric/2627-HK1-AI-GK.pdf`:

1. **Tỷ lệ khung hình bắt buộc:** **4:3** (`Use a 4:3 slide aspect ratio`). Tuyệt đối không dùng 16:9.
2. **Quy định màu sắc & máy chiếu:**
   - **TRÁNH:** Phông nền tối (dark background) và các hình khối màu mè phức tạp vì máy chiếu giảng đường rất mờ.
   - **BẮT BUỘC:** Thiết kế phông nền sáng (trắng hoặc xám rất nhạt `#F8F9FA`), văn bản màu đen/xanh đậm độ tương phản cao, đảm bảo **in ra đen trắng (grayscale) trên giấy A4 vẫn đọc rõ ràng 100%**.
3. **Quy định về mã nguồn:**
   - **TUYỆT ĐỐI KHÔNG DÁN CODE THÔ** (`Avoid embedding raw source code in the presentation`).
   - Sử dụng **sơ đồ khối (diagrams), bảng số liệu và mã giả ngắn gọn (pseudocode)** để minh họa thuật toán.
4. **Nội dung bắt buộc phải có:**
   - Danh sách thành viên: MSSV, Họ tên, Email, Nhiệm vụ được giao, Tỷ lệ hoàn thành (%).
   - Tóm tắt cách tiếp cận giải quyết bài toán.
   - Phân tích Ưu điểm và Nhược điểm của các giải pháp đề xuất.
   - Bảng tổng kết tỷ lệ hoàn thành từng Task.
5. **Thời lượng thuyết trình:** **TỐI ĐA 05 PHÚT** (300 giây). Quá thời gian sẽ bị dừng bài và trừ điểm.

---

## 2. CẤU TRÚC KHUNG 10 SLIDE CHUẨN 4:3 ĂN TRỌN ĐIỂM RUBRIC

```text
┌─────────────────────────────────────────────────────────────┐
│ Slide 1: Giới thiệu nhóm & Bảng phân công thành viên        │
│ Slide 2: Formulation - Không gian trạng thái Sokoban        │
│ Slide 3: Uninformed Search - Thuật toán UCS                 │
│ Slide 4: Informed Search - Thiết kế Heuristic Hungarian     │
│ Slide 5: Informed Search - Thuật toán A* Search             │
│ Slide 6: Chứng minh & Kiểm chứng Admissible & Consistent    │
│ Slide 7: Chế độ Đối kháng 2 Agent & Xử lý Xung đột          │
│ Slide 8: Thuật toán AI cho Agent Đối kháng (<= 1000ms)      │
│ Slide 9: Kết quả Thực nghiệm So sánh UCS vs A* (Biểu đồ)    │
│ Slide 10: Ưu / Nhược điểm, Bảng hoàn thành Task & Q&A       │
└─────────────────────────────────────────────────────────────┘
```

### Chi tiết nội dung từng Slide:
* **Slide 1 (Member 1):** Tên đề tài, Giảng viên hướng dẫn, Bảng danh sách thành viên (MSSV, Họ tên, Email, nhiệm vụ chính, tỷ lệ đóng góp 100%).
* **Slide 2 (Member 1 - Ăn 2.0đ Formulation):** Mô hình hóa bộ 6 thành phần: State $s = (p, B)$, Actions 4 hướng, Transition Model (Walk vs Push), Goal Test, Path Cost $c=1$.
* **Slide 3 (Member 1 - Ăn 3.0đ Uninformed):** Thuật toán UCS, Priority Queue theo $g(n)$, sơ đồ khối hoặc pseudocode, ảnh chụp GUI kết quả chạy UCS trên bản đồ mẫu.
* **Slide 4 (Member 2 - Ăn điểm Heuristic):** Lý do cấm Manhattan/Euclidean, giải pháp Static Maze Distance BFS + Hungarian Bipartite Matching + Deadlock Pruning.
* **Slide 5 (Member 2 - Ăn 3.0đ Informed):** Thuật toán A*, hàm đánh giá $f(n) = g(n) + h(n)$, tie-breaking trên $h(n)$, ảnh chụp GUI kết quả chạy A*.
* **Slide 6 (Member 2 - Ăn điểm Req 4):** Lập luận toán học tính Admissible & Consistent, bảng báo cáo thực nghiệm 100 trạng thái và 2,000 bước chuyển với 0% vi phạm.
* **Slide 7 (Member 3 - Ăn điểm Req 6):** Mô hình 2-Agent đối kháng, luật $n$ bước, cơ chế cướp hộp, ma trận phân xử xung đột đồng thời (Vertex, Swap, Push contention).
* **Slide 8 (Member 3 - Ăn điểm Req 7):** Thuật toán AI cho 2 Agent (Real-Time Hungarian A* vs Greedy Best-First Disruption), cơ chế bảo vệ Timeout Guard $\le 1000$ ms.
* **Slide 9 (Member 4 - Ăn điểm Req 3 & 5):** Kiến trúc GUI Pygame OOP, bộ điều khiển Playback (Space/Left/Right), biểu đồ cột Matplotlib so sánh Time & Space giữa UCS và A*.
* **Slide 10 (Member 4 - Tổng kết):** Phân tích Ưu điểm & Nhược điểm của từng phương pháp, Bảng tỷ lệ hoàn thành 8 Requirements (đều đạt 100%), lời cảm ơn và chuyển sang phần Q&A.

---

## 3. QUY ĐỊNH & KỊCH BẢN QUAY VIDEO DEMO $\le 3$ PHÚT (`demo.txt`)

### 3.1. Quy định chính thức
- **Thời lượng:** **Tối đa 03 phút** (180 giây). Quá thời lượng sẽ bị trừ điểm nặng.
- **Định dạng nộp:** File `demo.txt` đặt tại thư mục gốc của đồ án, chứa duy nhất 1 đường link xem trực tiếp (YouTube Unlisted hoặc Google Drive quyền công khai).
- **Âm thanh & Hình ảnh:** Độ phân giải tối thiểu 1080p, có giọng thuyết minh (voice-over) rõ ràng hoặc phụ đề chú thích từng thao tác.

### 3.2. Kịch bản phân cảnh video demo (Timeline chi tiết)
- **00:00 - 00:20 (20 giây): Giới thiệu mở đầu**
  - Mở file `main.py`, giới thiệu tên nhóm, thành viên và cấu trúc dự án.
- **00:20 - 00:55 (35 giây): Demo Thuật toán UCS**
  - Chạy lệnh: `python source/main.py --map source/maps/example_map.txt --algorithm ucs`
  - Chỉ ra số node mở rộng, thời gian chạy và tổng chi phí lời giải trên HUD.
- **00:55 - 01:40 (45 giây): Demo Thuật toán A* & Playback Controls**
  - Chạy lệnh: `python source/main.py --map source/maps/example_map.txt --algorithm astar`
  - Nhấn mạnh sự chênh lệch vượt trội: A* mở rộng ít node hơn gấp hàng chục lần và chạy nhanh hơn rõ rệt.
  - Thao tác trực tiếp các phím:
    * Bấm `Space` $\to$ Trò chơi tạm dừng (`Status: PAUSED`).
    * Bấm `Mũi tên phải (→)` $\to$ Nhân vật tiến 1 bước, Action Counter tăng lên.
    * Bấm `Mũi tên trái (←)` $\to$ Nhân vật lùi lại 1 bước (Undo mượt mà).
    * Bấm `Space` $\to$ Trò chơi tiếp tục chạy tự động về đích.
- **01:40 - 02:40 (60 giây): Demo Chế độ Đối kháng 2 Agent**
  - Chạy lệnh: `python source/main.py --mode competitive --steps 100 --map source/maps/competitive_map.txt`
  - Nhập số bước $n = 100$.
  - Quay cận cảnh:
    * Agent A (Avatar xanh) và Agent B (Avatar đỏ) di chuyển cùng lúc.
    * Hộp do Agent A đẩy vào đích đổi sang **Màu Xanh Dương**.
    * Hộp do Agent B đẩy vào đích đổi sang **Màu Đỏ**.
    * Agent B chạy lại đẩy hộp của Agent A ra khỏi đích (cướp hộp, trừ điểm đối thủ trực tiếp trên bảng tỉ số).
    * Tình huống 2 Agent chạm trán cản đường nhau (Conflict Resolver xử lý an toàn).
- **02:40 - 03:00 (20 giây): Kết thúc & Lời chào**
  - Hiển thị kết quả ván đấu (Winner), tóm tắt kết quả đạt được.

---

## 4. QUY CÁCH ĐÓNG GÓI HỒ SƠ NỘP BÀI TRÁNH BỊ TRỪ 50% ĐIỂM

Đề bài cảnh báo:
> *"Missing any required materials from the submission will result in a deduction of at least 50% of the presentation score."*

Tên file nộp:
```text
AI_midterm_<project group ID>_<your student ID>.zip
```

Cấu trúc bên trong file nén (bắt buộc đúng 100%):
```text
AI_midterm_<groupID>_<studentID>/
├── source/                      # Thư mục mã nguồn chạy được
│   ├── main.py                  # Điểm khởi chạy chương trình
│   ├── core/
│   ├── search/
│   ├── gui/
│   ├── competitive/
│   ├── agents/
│   ├── experiment/
│   ├── maps/
│   └── tests/
├── presentation.pdf             # Slide tỷ lệ 4:3 (nền sáng, in đen trắng rõ ràng)
└── demo.txt                     # File text chứa URL video demo <= 3 phút
```
