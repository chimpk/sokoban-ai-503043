# 01. TỔNG QUAN ĐỀ TÀI & QUY ĐỊNH CHẤM ĐIỂM (RUBRIC)

> **Học phần:** 503043 - Nhập môn Trí tuệ Nhân tạo (Introduction to Artificial Intelligence)  
> **Đề bài chính thức:** `rubric/2627-HK1-AI-GK.pdf`  
> **Thang điểm chính thức:** `rubric/RUBRIC_GK.docx`  

---

## 1. Mục Tiêu Dự Án
Bài tập lớn gồm 2 phần chính:
1. **Task 1: Giải bài toán Sokoban bằng Tìm kiếm không gian trạng thái (State-Space Search)**
   - Biểu diễn bài toán Sokoban dưới dạng không gian trạng thái chuẩn (State, Action, Transition, Goal Test, Path Cost).
   - Cài đặt thuật toán tìm kiếm mù: **Uniform-Cost Search (UCS)**.
   - Cài đặt thuật toán tìm kiếm có thông tin: **A\* Search** với ít nhất một hàm Heuristic tự thiết kế (phải phân tích tính Admissible và Consistent).
   - Xây dựng giao diện đồ họa trực quan hóa (GUI Visualization) bằng **Pygame** cho phép chạy từng bước giải, tua lại, tạm dừng.
   - So sánh, đánh giá thực nghiệm hiệu năng giữa UCS và A\* trên các bản đồ thử nghiệm.
   - Phần mở rộng: Chế độ thi đấu đối kháng giữa 2 Agent (Competitive Two-Agent) trên cùng một bản đồ.

2. **Task 2: Tài liệu báo cáo, Slide thuyết trình & Video demo**
   - Bộ Slide thuyết trình xuất ra định dạng `presentation.pdf`, tỷ lệ chuẩn **4:3**, thời lượng thuyết trình trên lớp **không quá 05 phút**.
   - Video demo hệ thống chạy thực tế thời lượng **không quá 03 phút**, gắn link vào `demo.txt`.
   - Vấn đáp bảo vệ (Q&A) trực tiếp với giảng viên.


---

## 2. Bảng Phân Bổ Điểm Chi Tiết (10.0 Điểm Rubric)

| Thành phần | Tiêu chí đánh giá | Điểm tối đa |
| :--- | :--- | :---: |
| **1. Biểu diễn bài toán** | Trình bày đầy đủ, chính xác: Không gian trạng thái, Không gian hành động, Hàm chuyển trạng thái, Điều kiện đích, Hàm chi phí đường đi. | **2.0 điểm** |
| **2. Tìm kiếm mù (Uninformed)** | Cài đặt đúng thuật toán Uniform-Cost Search (UCS); Trực quan hóa kết quả tìm kiếm trên giao diện đồ họa (Pygame). | **3.0 điểm** |
| **3. Tìm kiếm có thông tin (Informed)** | Thiết kế và cài đặt hàm Heuristic; Cài đặt đúng thuật toán A\* Search; Trực quan hóa kết quả trên Pygame; Đánh giá và kiểm chứng tính chất Heuristic (Admissible & Consistent). | **3.0 điểm** |
| **4. Tài liệu & Slide báo cáo** | Slide đúng tỉ lệ 4:3, cấu trúc mạch lạc, video demo $\le 3$ phút rõ ràng, tổ chức mã nguồn sạch sẽ, tuân thủ cấu trúc thư mục. | **1.0 điểm** |
| **5. Vấn đáp bảo vệ (Q&A)** | Từng thành viên trả lời rõ ràng, hiểu sâu mã nguồn mình viết, giải thích được cơ chế thuật toán và quyết định thiết kế. | **1.0 điểm** |
| **TỔNG CỘNG** | | **10.0 điểm** |

---

## 3. Quy Định Nộp Bài & Tổ Chức Thư Mục

- Toàn bộ mã nguồn chạy được của dự án nằm trọn vẹn trong thư mục `source/`.
- Task 2 là bài thuyết trình và video demo (được quy định chi tiết tại `docs/04_Slide_and_Video_Requirements.md`), xuất ra file `presentation.pdf` và `demo.txt`.
- Cấu trúc file nộp cuối cùng (file nén `AI_midterm_<groupID>_<studentID>.zip`):
  ```text
  AI_midterm_<groupID>_<studentID>.zip
  ├── source/
  │   ├── main.py
  │   ├── core/
  │   ├── search/
  │   ├── experiment/
  │   ├── competitive/
  │   ├── gui/
  │   ├── tests/
  │   ├── agents/
  │   └── maps/
  ├── presentation.pdf (Tỷ lệ 4:3, tối đa 10 slide)
  └── demo.txt (Chứa link video YouTube/Drive <= 3 phút)

  ```
- **Chính sách học thuật:** Nghiêm cấm sử dụng mã nguồn sinh tự động hoàn toàn từ AI mà không hiểu bản chất. Từng thành viên phải nắm vững từng dòng code trong phần việc được phân công để bảo vệ 1.0 điểm vấn đáp cá nhân.
