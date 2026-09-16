# 04. QUY ĐỊNH SLIDE, VIDEO DEMO & ĐỊNH HƯỚNG BẢO VỆ (Q&A)

> Căn cứ theo quy định tại đề bài `rubric/2627-HK1-AI-GK.pdf` và thang điểm `rubric/RUBRIC_GK.docx`.

---

## 1. Quy Định Về Slide Báo Cáo & Thuyết Trình (`presentation.pdf`)

Căn cứ Mục `II. Tasks - b) Task 2: Presentation` trong đề bài:
- **Thời lượng thuyết trình:** **TỐI ĐA 05 PHÚT** (`The presentation must not exceed 05 minutes`).
- **Định dạng & Vị trí:** Bắt buộc xuất ra file `presentation.pdf` đặt ngay tại thư mục gốc của đồ án (bên cạnh thư mục `source/`).
- **Tỷ lệ khung hình:** Bắt buộc là **4:3** (`Use a 4:3 slide aspect ratio`).
- **Quy định hình thức:**
  - **Tránh nền tối và màu sắc lòe loẹt** do hạn chế của máy chiếu (`Avoid dark backgrounds and colorful shapes due to projector limitations`).
  - **In trắng đen vẫn đọc rõ ràng** (`Ensure that all content is sufficiently clear and readable when the presentation is printed in grayscale`).
  - **Tuyệt đối không chèn mã nguồn thô** (`Avoid embedding raw source code in the presentation`), thay vào đó phải sử dụng **mã giả (pseudocode)** và/hoặc **sơ đồ (diagrams)**.
- **Nội dung bắt buộc phải có:**
  1. Danh sách sinh viên: MSSV, Họ tên, Email, Nhiệm vụ được giao, % Hoàn thành.
  2. Trình bày tóm tắt cách tiếp cận giải quyết các yêu cầu (dùng mã giả / sơ đồ).
  3. Ưu điểm và nhược điểm của các phương pháp đã đề xuất.
  4. Bảng tổng kết % hoàn thành của từng nhiệm vụ.


### Gợi ý cấu trúc 10 Slide theo chuẩn Rubric:
1. **Slide 1: Tiêu đề & Giới thiệu nhóm** (Tên đề tài, Giảng viên hướng dẫn, Danh sách thành viên kèm MSSV và % đóng góp).
2. **Slide 2: Bài toán Sokoban & Không gian trạng thái** (State, Action, Transition, Goal Test, Path Cost).
3. **Slide 3: Thuật toán Uninformed Search (UCS)** (Nguyên lý hàng đợi ưu tiên, cách xử lý trạng thái lặp với Closed Set).
4. **Slide 4: Thiết kế hàm Heuristic** (Ý tưởng thiết kế, công thức toán học, cơ chế ghép cặp hoặc phát hiện bế tắc Deadlock).
5. **Slide 5: Phân tích & Kiểm chứng tính Admissible và Consistent** (Chứng minh lý thuyết và số liệu thực nghiệm).
6. **Slide 6: Thuật toán Informed Search (A\*)** (Hàm đánh giá $f(n) = g(n) + h(n)$, so sánh lý thuyết với UCS).
7. **Slide 7: Kết quả thực nghiệm & Đánh giá hiệu năng** (Bảng số liệu và biểu đồ so sánh: Thời gian (ms), Bộ nhớ (KB), Số node mở rộng trên các map).
8. **Slide 8: Phần mở rộng: Chế độ 2 Agent đối kháng** (Cơ chế phân xử xung đột, chiến lược của 2 Agent, luật tính điểm).
9. **Slide 9: Kiến trúc hệ thống & Giao diện Pygame** (Sơ đồ kiến trúc module, các tính năng Play/Pause/Undo của GUI).
10. **Slide 10: Kết luận & Bài học kinh nghiệm** (Tổng kết kết quả đạt được, hướng phát triển tiếp theo).

---

## 2. Quy Định Về Video Demo (`demo.txt`)

- **Thời lượng:** Tối đa **3 phút** (quá 3 phút sẽ bị trừ điểm theo quy định của môn học).
- **Cách nộp:** Tải video lên YouTube (chế độ Unlisted/Không công khai) hoặc Google Drive (bật quyền "Bất kỳ ai có link đều xem được"). Dán đường link trực tiếp vào file `demo.txt` ở thư mục gốc.
- **Nội dung cần thể hiện trong video:**
  1. Giới thiệu ngắn gọn thành viên và phân công công việc (~20 giây).
  2. Demo thuật toán UCS chạy trên bản đồ mẫu, trực quan hóa trên Pygame (~40 giây).
  3. Demo thuật toán A\* chạy trên cùng bản đồ, nhấn mạnh sự chênh lệch về số bước và số node mở rộng (~50 giây).
  4. Demo tính năng điều khiển GUI (Pause, Next step, Previous step) (~30 giây).
  5. Demo chế độ 2 Agent đối kháng solo cùng lúc (~40 giây).

---

## 3. Định Hướng Ôn Tập Vấn Đáp Bảo Vệ (Q&A Preparation)

Giảng viên sẽ hỏi xoay từng thành viên ngẫu nhiên để chấm **1.0 điểm vấn đáp cá nhân**. Dưới đây là các chủ đề trọng tâm từng thành viên bắt buộc phải tự tìm hiểu kỹ:

### Nhóm câu hỏi lý thuyết thuật toán:
- **Thành viên 1:**
  - *"Tại sao trong hàm `__eq__` và `__hash__` của State, em không đưa tọa độ của các bức tường vào so sánh?"*
  - *"UCS khác gì với Dijkstra? Nếu bài toán có cạnh mang trọng số âm thì UCS có chạy được không?"*
  - *"Em quản lý Closed Set bằng cấu trúc dữ liệu nào trong Python và độ phức tạp truy vấn là bao nhiêu?"*

### Nhóm câu hỏi Heuristic & A\*:
- **Thành viên 2:**
  - *"Thế nào là một Heuristic Admissible? Nếu hàm Heuristic đánh giá vượt quá chi phí thực tế ($h > h^*$) thì A\* có tìm ra lời giải tối ưu không? Vì sao?"*
  - *"Tại sao hàm Heuristic của em lại thỏa mãn tính Consistent? Em chứng minh bằng toán học hoặc thực nghiệm như thế nào?"*
  - *"Khi gặp trạng thái Deadlock (hộp ở góc tường không phải đích), hàm Heuristic của em xử lý thế nào?"*

### Nhóm câu hỏi Đối kháng (Competitive Multi-agent):
- **Thành viên 3:**
  - *"Nếu hai Agent cùng muốn di chuyển vào một ô trong cùng một lượt, hệ thống xử lý ra sao để không bị lỗi trạng thái?"*
  - *"Thuật toán của Agent B thông minh hơn Agent A ở điểm nào? Nó có dự đoán được nước đi của đối thủ không?"*
  - *"Cơ chế giới hạn thời gian 1000ms mỗi lượt được cài đặt như thế nào trong Python?"*

### Nhóm câu hỏi GUI & Thực nghiệm:
- **Thành viên 4:**
  - *"Trên các bản đồ lớn và phức tạp, thuật toán nào tiết kiệm bộ nhớ và mở rộng ít node hơn? Tỷ lệ chênh lệch là bao nhiêu?"*
  - *"Cơ chế tua lại bước đi (Undo / Previous step) trên giao diện Pygame được lưu trữ dữ liệu như thế nào?"*
  - *"Khi đo bộ nhớ tiêu thụ của thuật toán, em sử dụng thư viện nào và đo ở thời điểm nào của chương trình?"*
