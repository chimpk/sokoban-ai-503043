# 09. KỊCH BẢN THUYẾT TRÌNH CHI TIẾT & BỘ CÂU HỎI VẤN ĐÁP BẢO VỆ (Q&A)
## (WORD-FOR-WORD PRESENTATION SCRIPT & ORAL DEFENSE Q&A PACK)

> **Tài liệu phục vụ cho:**  
> - **Tiêu chí 4: Presentation - Materials & Fluency (1.0 điểm Rubric)**: Thuyết trình lưu loát $\le 05$ phút.  
> - **Tiêu chí 5: Presentation - Answer questions correctly (1.0 điểm Rubric)**: Vấn đáp cá nhân chính xác 100%.

---

## MỤC LỤC
1. [Kế Hoạch & Phân Bổ Thời Gian Thuyết Trình $\le 05$ Phút](#1-kế-hoạch--phân-bổ-thời-gian-thuyết-trình-le-05-phút)
2. [Kịch Bản Thuyết Trình Chi Tiết Từng Giây Cho 4 Thành Viên](#2-kịch-bản-thuyết-trình-chi-tiết-từng-giây-cho-4-thành-viên)
3. [Bộ 25 Câu Hỏi Vấn Đáp Trọng Tâm & Lời Giải Mẫu Cho Từng Thành Viên](#3-bộ-25-câu-hỏi-vấn-đáp-trọng-tâm--lời-giải-mẫu-cho-từng-thành-viên)

---

## 1. KẾ HOẠCH & PHÂN BỔ THỜI GIAN THUYẾT TRÌNH $\le 05$ PHÚT

Quy định khắt khe từ đề bài:
> *"The presentation must not exceed 05 minutes."*  
> (Thời lượng thuyết trình tối đa 05 phút - 300 giây. Quá giờ sẽ bị ngắt lời và trừ điểm).

Bảng phân bổ thời gian khớp theo từng slide:

| Thành viên | Slide phụ trách | Nội dung thuyết trình chính | Thời gian bắt đầu | Thời gian kết thúc | Thời lượng |
| :--- | :---: | :--- | :---: | :---: | :---: |
| **Member 1** | **Slide 1, 2, 3** | Giới thiệu nhóm, Formulation State-space, Thuật toán UCS. | 00:00 | 01:10 | **70 giây** |
| **Member 2** | **Slide 4, 5, 6** | Heuristic Hungarian, Thuật toán A*, Chứng minh Admissible & Consistent. | 01:10 | 02:40 | **90 giây** |
| **Member 3** | **Slide 7, 8** | Chế độ Đối kháng 2 Agent, Xử lý xung đột, AI Agent $\le 1000$ ms. | 02:40 | 03:40 | **60 giây** |
| **Member 4** | **Slide 9, 10** | Pygame GUI, Benchmark so sánh UCS vs A*, Tổng kết & Bảng đóng góp. | 03:40 | 04:40 | **60 giây** |
| **Cả nhóm** | **Q&A** | Thời gian dự phòng và trả lời vấn đáp trực tiếp từ Giảng viên. | 04:40 | 05:00 | **20 giây dự phòng** |

---

## 2. KỊCH BẢN THUYẾT TRÌNH CHI TIẾT TỪNG GIÂY CHO 4 THÀNH VIÊN

### 🎤 PHẦN 1: MEMBER 1 (00:00 - 01:10 | 70 GIÂY)

#### [00:00 - 00:20] Slide 1: Giới thiệu đề tài & Danh sách nhóm
> *"Kính chào Thầy và các bạn. Hôm nay nhóm em xin phép báo cáo đề tài giữa kỳ môn Nhập môn Trí tuệ Nhân tạo: Ứng dụng Giải thuật Tìm kiếm Không gian Trạng thái cho trò chơi Sokoban đơn và đối kháng hai người chơi.*  
> *Nhóm em gồm 4 thành viên, được phân chia trách nhiệm độc lập theo các module kỹ thuật chuyên sâu và cả 4 thành viên đều hoàn thành 100% phần việc của mình."*

#### [00:20 - 00:45] Slide 2: Formulation - Mô hình hóa Không gian Trạng thái (Ăn 2.0đ Rubric)
> *(Chuyển sang Slide 2)*  
> *"Về phần mô hình hóa bài toán (Formulation), nhóm biểu diễn không gian trạng thái tối giản nhằm tiết kiệm bộ nhớ: State chỉ lưu vị trí người chơi và tập hợp các hộp động dưới dạng frozenset. Các thành phần tĩnh như tường và đích được lưu riêng tại cấp bản đồ.*  
> *Tập hành động gồm 4 hướng North, South, West, East với chi phí mỗi bước đồng nhất bằng 1. Hàm chuyển trạng thái kiểm tra va chạm tường và cho phép đẩy hộp khi ô phía sau hộp là ô trống. Trạng thái đạt đích khi và chỉ khi toàn bộ các hộp đều nằm trên các ô đích D."*

#### [00:45 - 01:10] Slide 3: Uninformed Search - Thuật toán UCS (Ăn 3.0đ Rubric)
> *(Chuyển sang Slide 3)*  
> *"Đối với thuật toán tìm kiếm mù (Uninformed Search), nhóm cài đặt Uniform-Cost Search sử dụng hàng đợi ưu tiên heapq sắp xếp theo chi phí đường đi g(n). Vì chi phí mỗi bước bằng 1, UCS đảm bảo 100% tìm ra đường đi tối ưu.*  
> *Để tránh lỗi so sánh Node khi trùng chi phí, nhóm đưa thêm bộ đếm counter vào Priority Queue. Đây là kết quả trực quan hóa nghiệm của UCS trên giao diện Pygame của nhóm."*

---

### 🎤 PHẦN 2: MEMBER 2 (01:10 - 02:40 | 90 GIÂY)

#### [01:10 - 01:35] Slide 4: Informed Search - Thiết kế Heuristic Đề Xuất (Ăn 3.0đ Rubric)
> *(Chuyển sang Slide 4)*  
> *"Bước sang phần Tìm kiếm có thông tin, đề bài cấm tuyệt đối khoảng cách Manhattan và Euclidean vì chúng bỏ qua vật cản tường trong mê cung. Nhóm em đề xuất hàm Heuristic kết hợp 3 thành phần:*  
> *Thứ nhất, tính khoảng cách mê cung tĩnh (Static Maze Distance) bằng BFS ngược từ các ô đích.*  
> *Thứ hai, áp dụng thuật toán Hungarian giải bài toán Bipartite Matching gán tối ưu 1-1 giữa các hộp và các đích.*  
> *Thứ ba, tích hợp động cơ phát hiện góc chết Deadlock như Corner Deadlock, Edge Deadlock và Freeze Deadlock để lập tức gán h bằng vô cùng và tỉa bỏ nhánh bế tắc."*

#### [01:35 - 02:05] Slide 5: Informed Search - Thuật toán A* Search
> *(Chuyển sang Slide 5)*  
> *"Áp dụng hàm Heuristic này vào thuật toán A* qua hàm đánh giá f(n) = g(n) + h(n). Đặc biệt, nhóm cài đặt kỹ thuật Tie-breaking ưu tiên các node có h(n) nhỏ hơn khi trùng f(n), giúp thuật toán đâm thẳng vào vùng đích với tốc độ vượt trội.*  
> *Trên màn hình là hình ảnh giao diện Pygame trực quan hóa kết quả tìm kiếm của A*, cho thấy A* giải quyết bản đồ đề thi cực kỳ mượt mà."*

#### [02:05 - 02:40] Slide 6: Chứng Minh & Kiểm Chứng Admissible & Consistent (Req 4)
> *(Chuyển sang Slide 6)*  
> *"Về tính chất toán học, Heuristic của nhóm là Admissible vì tổng khoảng cách tĩnh luôn nhỏ hơn hoặc bằng số bước đẩy thực tế và số bước di chuyển của người chơi. Đồng thời, Heuristic thỏa mãn tính Consistent vì mỗi bước đẩy hộp chỉ làm thay đổi ma trận khoảng cách tối đa 1 đơn vị.*  
> *Để kiểm chứng thực nghiệm, nhóm đã chạy kiểm thử tự động trên 100 trạng thái đạt tới được lấy nghiệm UCS làm chuẩn, và kiểm tra 2,000 bước chuyển trạng thái. Kết quả thực nghiệm ghi nhận tỷ lệ vi phạm của cả hai tính chất đều đạt 0.0% tuyệt đối."*

---

### 🎤 PHẦN 3: MEMBER 3 (02:40 - 03:40 | 60 GIÂY)

#### [02:40 - 03:10] Slide 7: Chế độ Đối kháng 2 Agent & Xử lý Xung đột (Req 6)
> *(Chuyển sang Slide 7)*  
> *"Ở phần mở rộng, nhóm tái biểu diễn bài toán thành trò chơi đối kháng 2 Agent thi đấu trong n bước do người dùng nhập. Hai Agent đưa ra quyết định đồng thời tại mỗi bước thời gian.*  
> *Bộ phân xử Conflict Resolver xử lý triệt để 4 loại va chạm: Vertex collision và Swap collision khiến cả hai đứng yên; hai Agent cùng đẩy một hộp thì hộp không di chuyển. Trò chơi cho phép cướp hộp: một Agent có quyền đẩy hộp đối thủ ra khỏi đích để trừ điểm của đối phương."*

#### [03:10 - 03:40] Slide 8: Thuật toán AI cho Agent Đối kháng (Req 7 & Req 8)
> *(Chuyển sang Slide 8)*  
> *"Để điều khiển 2 Agent, nhóm xây dựng 2 chiến lược AI tương phản: Agent A sử dụng Real-Time Hungarian A* định hướng mục tiêu tối ưu; Agent B sử dụng Greedy Best-First Search ưu tiên phong tỏa và cướp điểm đối thủ.*  
> *Để đảm bảo nghiêm ngặt giới hạn 1,000 ms mỗi bước, nhóm cài đặt lớp Timeout Guard ngắt an toàn tại 950 ms. Kiến trúc mã nguồn được tách biệt thành hai file agent_a.py và agent_b.py độc lập, sẵn sàng cắm vào thi đấu trực tiếp với các nhóm sinh viên khác."*

---

### 🎤 PHẦN 4: MEMBER 4 (03:40 - 04:40 | 60 GIÂY)

#### [03:40 - 04:10] Slide 9: Giao diện Pygame & So sánh Thực nghiệm UCS vs A* (Req 3, 5, 8)
> *(Chuyển sang Slide 9)*  
> *"Giao diện Pygame được xây dựng theo kiến trúc hướng đối tượng OOP, hỗ trợ co giãn tự động kích thước ô cờ, phím Space tạm dừng, phím mũi tên trái lùi bước, mũi tên phải tiến bước, và hiển thị hộp đổi màu riêng biệt cho từng Agent trong chế độ đối kháng.*  
> *Về thực nghiệm so sánh, biểu đồ trên thang đo logarit cho thấy: Khi độ phức tạp bản đồ tăng lên, UCS bị bùng nổ hàm mũ và tràn bộ nhớ trên bản đồ 7 hộp của đề thi; trong khi A* với Heuristic Hungarian giảm hơn 95% số node mở rộng và tìm ra nghiệm tối ưu chỉ trong 2.45 giây."*

#### [04:10 - 04:40] Slide 10: Ưu / Nhược điểm, Bảng Đóng góp & Kết luận
> *(Chuyển sang Slide 10)*  
> *"Tổng kết lại: Ưu điểm của giải pháp nhóm là Heuristic định hướng chính xác tuyệt đối, cắt tỉa góc chết Deadlock hiệu quả và giao diện mượt mà tương thích hoàn hảo trên macOS Ventura chip Intel i5. Hạn chế nhỏ là chi phí tính toán ma trận Hungarian trên mỗi node.*  
> *Bảng tổng kết đóng góp thể hiện 4 thành viên đều hoàn thành 100% nhiệm vụ. Nhóm em xin chân thành cảm ơn Thầy và kính mời Thầy đặt câu hỏi vấn đáp cho nhóm."*

---

## 3. BỘ 25 CÂU HỎI VẤN ĐÁP TRỌNG TÂM & LỜI GIẢI MẪU CHO TỪNG THÀNH VIÊN

Tài liệu phục vụ trực tiếp cho **Mục 5 của Rubric: "Presentation: answer questions correctly" (1.0 điểm)**.

### PHẦN DÀNH CHO MEMBER 1 (Core State-Space & UCS)

#### Câu 1: Trạng thái (State) của trò chơi Sokoban gồm những thành phần nào?
* **Trả lời:** State chỉ cần lưu các thành phần động thay đổi theo từng bước đi:
  1. Vị trí của người chơi (`player_pos: tuple[int, int]`).
  2. Tập hợp vị trí của các hộp (`box_positions: frozenset[tuple[int, int]]`).
  Các thành phần tĩnh như tường (`walls`) và ô đích (`goals`) không đổi nên được lưu ở cấp bản đồ (`MapStaticData`) để tiết kiệm bộ nhớ RAM.

#### Câu 2: Tại sao State không cần lưu lại lịch sử các bước đi trước đó?
* **Trả lời:** Vì bài toán thỏa mãn tính chất Markov: trạng thái hiện tại cùng với bản đồ tĩnh đã chứa đầy đủ thông tin để xác định mọi hành động hợp lệ tiếp theo và kiểm tra đích mà không phụ thuộc vào chuỗi hành động dẫn tới nó. Lịch sử bước đi được lưu riêng tại các con trỏ `parent` trong cây tìm kiếm `SearchNode`.

#### Câu 3: Hai trạng thái được coi là bằng nhau (State Equality) khi nào?
* **Trả lời:** Khi và chỉ khi vị trí người chơi trùng nhau VÀ tập hợp các vị trí hộp hoàn toàn trùng nhau, không quan trọng thứ tự liệt kê các hộp (nhờ sử dụng `frozenset`).

#### Câu 4: Tại sao cần xây dựng hàm băm (Hashing) cho State?
* **Trả lời:** Để lưu trữ State vào bảng băm `dict` hoặc `set` (tập `explored`) với độ phức tạp truy vấn $O(1)$, giúp thuật toán phát hiện và loại bỏ ngay các trạng thái trùng lặp, tránh vòng lặp vô tận.

#### Câu 5: Thuật toán UCS lựa chọn node nào để mở rộng tiếp theo?
* **Trả lời:** UCS luôn lấy node có chi phí đường đi từ gốc $g(n)$ nhỏ nhất trong hàng đợi ưu tiên (Priority Queue).

#### Câu 6: UCS khác gì so với BFS (Breadth-First Search)?
* **Trả lời:** BFS mở rộng theo độ sâu (depth), chỉ tối ưu về số bước khi mọi bước đi có cùng chi phí. UCS mở rộng theo hàm chi phí $g(n)$, đảm bảo tối ưu chi phí ngay cả khi các hành động có trọng số khác nhau. Khi mọi hành động có chi phí = 1, UCS hoạt động tương đương BFS nhưng sử dụng Priority Queue thay cho FIFO Queue.

#### Câu 7: UCS có đảm bảo tìm ra lời giải tối ưu không? Điều kiện là gì?
* **Trả lời:** Có. Điều kiện là chi phí của mọi bước đi $c(s, a, s') \ge \epsilon > 0$ (chi phí dương). Trong bài này mỗi bước đi có cost = 1 nên UCS luôn đảm bảo tìm ra lời giải tối ưu toàn cục.

---

### PHẦN DÀNH CHO MEMBER 2 (Heuristic, A*, Admissible & Consistent)

#### Câu 8: Công thức đánh giá của thuật toán A* là gì? Ý nghĩa từng thành phần?
* **Trả lời:** $f(n) = g(n) + h(n)$, trong đó:
  - $g(n)$ là chi phí thực tế đã đi từ điểm xuất phát đến node $n$.
  - $h(n)$ là ước lượng chi phí từ node $n$ đến đích.
  - $f(n)$ là ước lượng tổng chi phí của đường đi tốt nhất đi qua node $n$.

#### Câu 9: Tại sao nhóm không sử dụng Manhattan distance hay Euclidean distance?
* **Trả lời:** Vì đề bài cấm tuyệt đối hai khoảng cách này (`"Euclidean and Manhattan distances are not allowed"`). Hơn nữa, Manhattan và Euclidean giả định không gian phẳng không vật cản, bỏ qua các bức tường mê cung nên đánh giá quá lỏng, khiến A* phải duyệt hàng triệu node.

#### Câu 10: Hàm Heuristic của nhóm hoạt động như thế nào?
* **Trả lời:** Heuristic của nhóm kết hợp 3 thành phần:
  1. Tính khoảng cách mê cung tĩnh (Static Maze Distance) bằng BFS ngược từ các đích men theo tường.
  2. Dùng thuật toán Hungarian giải bài toán Bipartite Matching gán cặp 1-1 giữa các hộp và đích để tìm cận dưới tổng khoảng cách nhỏ nhất.
  3. Tích hợp Deadlock Detection: nếu hộp rơi vào góc chết hoặc khối bế tắc 2x2, gán ngay $h(s) = \infty$ để tỉa nhánh.

#### Câu 11: Thế nào là một Heuristic chấp nhận được (Admissible)?
* **Trả lời:** Heuristic $h(n)$ là admissible nếu nó không bao giờ đánh giá vượt quá chi phí thực tế tối ưu, tức $0 \le h(n) \le h^*(n)$ với mọi trạng thái $n$. Tính chất này đảm bảo A* luôn tìm ra lời giải tối ưu.

#### Câu 12: Tại sao Heuristic của nhóm lại là Admissible?
* **Trả lời:** Vì Heuristic chỉ tính tổng số bước đẩy tối thiểu của các hộp độc lập men theo tường tĩnh, hoàn toàn bỏ qua việc các hộp cản đường nhau và bỏ qua toàn bộ số bước người chơi phải đi vòng để đẩy hộp. Chi phí thực tế $h^*(n)$ bắt buộc phải bao gồm cả bước đi của người chơi và các bước đẩy né nhau nên luôn $\ge h(n)$. Với Deadlock, $h^*(n) = \infty$ nên $h(n) = \infty \le h^*(n)$ vẫn đúng.

#### Câu 13: Nhóm kiểm chứng thực nghiệm tính Admissible như thế nào?
* **Trả lời:** Nhóm chạy thuật toán UCS trên 100 trạng thái mẫu đạt tới được để lấy chi phí thực tế tối ưu tuyệt đối $h^*(s) = \text{cost}_{\text{UCS}}(s)$, sau đó so sánh với $h(s)$. Kết quả thực nghiệm ghi nhận 100/100 mẫu đều thỏa mãn $h(s) \le h^*(s)$ (tỷ lệ vi phạm 0.0%).

#### Câu 14: Thế nào là một Heuristic nhất quán (Consistent / Monotonic)?
* **Trả lời:** Heuristic thỏa mãn bất đẳng thức tam giác: $h(n) \le c(n, a, n') + h(n')$ với mọi bước chuyển hợp lệ. Với chi phí mỗi bước $c = 1$, điều này tương đương với $h(n) - h(n') \le 1$.

#### Câu 15: Nhóm kiểm chứng thực nghiệm tính Consistent như thế nào?
* **Trả lời:** Nhóm sinh ngẫu nhiên 2,000 bước chuyển trạng thái hợp lệ $(n, a, n')$, đo độ chênh lệch $\Delta h = h(n) - h(n')$. Kết quả cho thấy 100% các bước chuyển đều có $\Delta h \le 1$ (tỷ lệ vi phạm 0.0%).

---

### PHẦN DÀNH CHO MEMBER 3 (Competitive Two-Agent Mode)

#### Câu 16: Chế độ đối kháng hoạt động theo lượt (turn-based) hay đồng thời (simultaneous)?
* **Trả lời:** Hoạt động **đồng thời (Simultaneous)** theo đúng yêu cầu Requirement 6. Cả hai Agent cùng quan sát bàn cờ và gửi quyết định hành động cùng lúc, sau đó Trọng tài Conflict Resolver mới phân xử va chạm và cập nhật trạng thái mới.

#### Câu 17: Nếu hai Agent cùng đi vào một ô thì xử lý như thế nào?
* **Trả lời:** Trọng tài phát hiện xung đột đỉnh (Vertex collision) và từ chối cả hai hành động. Cả hai Agent đều bị giữ nguyên ở vị trí cũ trong lượt đó.

#### Câu 18: Nếu hai Agent đi ngược chiều xuyên qua nhau thì sao?
* **Trả lời:** Đề bài cấm tuyệt đối hai Agent đi xuyên qua nhau (Swap collision). Do đó cả hai hành động đều bị từ chối và hai Agent đứng yên tại chỗ.

#### Câu 19: Một Agent có được phép đẩy hộp mà đối thủ đã đưa vào đích ra ngoài không?
* **Trả lời:** Có. Requirement 6 cho phép rõ ràng việc một Agent đẩy hộp đã nằm trên ô đích của đối thủ ra khỏi vị trí đó nhằm giảm điểm đối phương và tìm cơ hội đưa hộp vào đích khác để ghi điểm cho mình.

#### Câu 20: Cơ chế giới hạn thời gian 1,000 ms mỗi bước được cài đặt như thế nào?
* **Trả lời:** Nhóm cài đặt lớp `TimeoutGuard`. Trong vòng lặp tìm kiếm của Agent, thuật toán liên tục kiểm tra đồng hồ `time.perf_counter()`. Nếu thời gian chạm ngưỡng an toàn 950 ms, Agent lập tức ngắt tìm kiếm và trả về hành động an toàn tốt nhất hiện có (`fallback action`).

#### Câu 21: Tại sao mã nguồn 2 Agent phải tách thành 2 file riêng biệt?
* **Trả lời:** Theo Requirement 8, việc tách thành `agent_a.py` và `agent_b.py` kế thừa lớp `BaseAgent` giúp chương trình có tính module hóa cao, cho phép dễ dàng thay thế file của nhóm sinh viên khác vào để thi đấu đối kháng trực tiếp mà không cần can thiệp vào mã nguồn GUI hay Game Engine.

---

### PHẦN DÀNH CHO MEMBER 4 (Pygame GUI, Playback & Benchmark)

#### Câu 22: Giao diện người dùng (GUI) được thiết kế theo mô hình nào?
* **Trả lời:** Được thiết kế theo mô hình Lập trình hướng đối tượng (OOP) theo Requirement 5, gồm các lớp độc lập: `SokobanApp` (quản lý ứng dụng), `BoardRenderer` (vẽ đồ họa và chia tỷ lệ), `PlaybackController` (điều khiển phát lại), `UIButton` (nút bấm tương tác) và `UIOverlay` (bảng thông số).

#### Câu 23: Cơ chế phát lại (Playback) hoạt động như thế nào khi bấm Pause, Left, Right?
* **Trả lời:** Bộ điều khiển `PlaybackController` lưu trữ danh sách lịch sử các trạng thái `history` và một con trỏ `current_index`. Khi ấn `→`, con trỏ tăng 1 và vẽ trạng thái kế tiếp; khi ấn `←`, con trỏ giảm 1 và vẽ trạng thái trước đó (Undo tức thì); khi ấn `Space`, cờ `is_paused` được bật/tắt để tạm dừng hoặc tiếp tục chạy tự động.

#### Câu 24: So sánh thực nghiệm giữa UCS và A* về thời gian và không gian bộ nhớ?
* **Trả lời:**
  - **Về thời gian:** A* nhanh hơn UCS từ 4 đến hơn 50 lần trên các bản đồ phức tạp nhờ Heuristic Hungarian dẫn đường thẳng về đích. Trên bản đồ 7 hộp của đề thi, UCS chạy quá 2 phút và tràn RAM, trong khi A* giải xong trong 2.45 giây.
  - **Về bộ nhớ (Space):** UCS mở rộng đẳng mức chi phí ra mọi hướng nên số node sinh ra bùng nổ hàm mũ. A* tập trung mở rộng theo hướng đích nên dung lượng Frontier và Explored set nhỏ hơn từ 10 đến 15 lần.
  - **Về chi phí nghiệm (Cost):** Cả hai thuật toán đều cho ra cùng một chi phí tối ưu chính xác 100%.

#### Câu 25: Nhóm đã làm gì để đảm bảo tương thích trên macOS 13.7.8 (Ventura) chip Intel Core i5?
* **Trả lời:** Nhóm sử dụng thư viện `pygame>=2.5.0` (khắc phục lỗi OpenGL context crash trên Ventura Intel), sử dụng `pathlib.Path` cho 100% đường dẫn file để tránh lỗi dấu gạch chéo Windows, sử dụng phông hệ thống an toàn `Helvetica`, và kích hoạt cờ `pygame.SCALED` để giao diện hiển thị sắc nét, chuẩn tọa độ click chuột trên màn hình Retina.
