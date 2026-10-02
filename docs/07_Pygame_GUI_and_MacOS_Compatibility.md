# 07. THIẾT KẾ GIAO DIỆN PYGAME OOP & TƯƠNG THÍCH MACOS VENTURA INTEL
## (PYGAME GUI ARCHITECTURE, PLAYBACK CONTROLLER & MACOS VENTURA COMPATIBILITY)

> **Tài liệu phục vụ cho:**  
> - **Requirement 5 (1.0 điểm):** Xây dựng giao diện Pygame thân thiện người dùng, hỗ trợ UCS và A*, hiển thị số lượng hành động, các phím điều khiển Space, Left, Right, chuẩn OOP, tương thích macOS 13.7.8 Ventura Intel i5.  
> - **Requirement 8 (1.0 điểm):** Hỗ trợ hiển thị chế độ đối kháng 2 Agent, đổi màu hộp theo từng Agent.

---

## MỤC LỤC
1. [Yêu Cầu Đề Bài & Kiến Trúc Hướng Đối Tượng (OOP)](#1-yêu-cầu-đề-bài--kiến-trúc-hướng-đối-tượng-oop)
2. [Bố Cục Giao Diện & Kỹ Thuật Chia Tỷ Lệ Động (Dynamic Tile Sizing)](#2-bố-cục-giao-diện--kỹ-thuật-chia-tỷ-lệ-động-dynamic-tile-sizing)
3. [Đường Ống Vẽ Lớp Hình Ảnh (Layered Rendering Pipeline)](#3-đường-ống-vẽ-lớp-hình-ảnh-layered-rendering-pipeline)
4. [Bộ Điều Khiển Phát Lại (Playback Controller State Machine)](#4-bộ-điều-khiển-phát-lại-playback-controller-state-machine)
5. [Hiển Thị Chế Độ Đối Kháng 2 Agent & Phân Biệt Màu Hộp](#5-hiển-thị-chế-độ-đối-kháng-2-agent--phân-biệt-màu-hộp)
6. [Checklist Tương Thích Tuyệt Đối Trên macOS 13.7.8 (Ventura) Intel Core i5](#6-checklist-tương-thích-tuyệt-đối-trên-macos-1378-ventura-intel-core-i5)

---

## 1. YÊU CẦU ĐỀ BÀI & KIẾN TRÚC HƯỚNG ĐỐI TƯỢNG (OOP)

### 1.1. Yêu cầu chính thức từ đề bài
- Cài đặt giao diện trò chơi bằng thư viện **Pygame**.
- Đánh giá độ thân thiện UI/UX theo tiêu chuẩn của Giảng viên.
- Cung cấp 2 tùy chọn thuật toán: `UCS` và `A*`.
- Hiển thị số lượng hành động trên màn hình (Action count).
- Phím điều khiển phát lại:
  - `Space`: Tạm dừng / Tiếp tục chạy (Pause / Resume).
  - `→` (Mũi tên phải): Tiến 1 bước (Step forward).
  - `←` (Mũi tên trái): Lùi 1 bước (Step backward).
- Tổ chức theo mô hình **Hướng đối tượng (OOP)**, code gọn gàng, có cấu trúc.
- **Bắt buộc chạy được trên macOS 13.7.8 (Ventura) chip Intel Core i5**.

### 1.2. Kiến trúc các lớp (OOP Classes)
- `SokobanApp`: Lớp điều phối cấp cao quản lý vòng đời ứng dụng, khởi tạo Pygame và vòng lặp sự kiện chính.
- `BoardRenderer`: Lớp chuyên trách vẽ bản đồ, tính toán tọa độ pixel, hiển thị các sprite/texture và căn giữa bàn cờ.
- `PlaybackController`: Máy trạng thái quản lý chuỗi lịch sử các bước đi `history`, con trỏ `current_index`, và trạng thái tạm dừng `is_paused`.
- `UIButton`: Lớp thành phần giao diện đại diện cho các nút bấm (Chọn thuật toán, Play, Pause, Next, Prev) hỗ trợ hiệu ứng hover chuột và sự kiện click.
- `UIOverlay`: Lớp vẽ bảng thông số (Metrics HUD): Tên thuật toán, tổng chi phí, bước hiện tại, thời gian tính toán, số node mở rộng.

---

## 2. BỐ CỤC GIAO DIỆN & KỸ THUẬT CHIA TỶ LỆ ĐỘNG

Cửa sổ ứng dụng có kích thước chuẩn $1024 \times 768$ pixel, chia làm 2 khu vực chính:

```text
┌────────────────────────────────────────────────────────────────────────┐
│                      SOKOBAN AI SOLVER - TDTU                          │
├─────────────────────────────────────────┬──────────────────────────────┤
│                                         │  [ALGORITHM SELECTION]       │
│                                         │  ( ) UCS Search              │
│                                         │  (•) A* Search (Hungarian)   │
│                                         │                              │
│                                         │  [METRICS DASHBOARD]         │
│              GAME BOARD                 │  Map: example_map.txt        │
│        (Tự động tính tile_size          │  Total Cost: 48 actions      │
│         và căn giữa màn hình)           │  Current Step: [ 14 / 48 ]   │
│                                         │  Nodes Expanded: 28,600      │
│                                         │  Execution Time: 2,450 ms    │
│                                         │  Status: PAUSED              │
│                                         │                              │
│                                         │  [PLAYBACK CONTROLS]         │
│                                         │  [ |<< ] [ < ] [ || ] [ > ]  │
│                                         │  Space: Pause / Resume       │
│                                         │  Left/Right Arrow: Step      │
└─────────────────────────────────────────┴──────────────────────────────┘
```

### Kỹ thuật tính toán kích thước ô vuông tự động (Dynamic Tile Sizing):
Để bất kỳ bản đồ nào (từ $6 \times 6$ đến $20 \times 20$) đều hiển thị cân đối trong khung bàn cờ kích thước $W_{\text{board}} \times H_{\text{board}}$ ($680 \times 700$ px):
$$\text{tile\_size} = \min\left( \left\lfloor \frac{680}{cols} \right\rfloor, \left\lfloor \frac{700}{rows} \right\rfloor \right)$$
Tọa độ căn giữa bàn cờ:
$$\text{offset\_x} = \frac{680 - cols \times \text{tile\_size}}{2}, \quad \text{offset\_y} = \frac{700 - rows \times \text{tile\_size}}{2}$$
Tọa độ pixel của ô $(r, c)$ trên màn hình:
$$\text{pixel\_x} = \text{offset\_x} + c \times \text{tile\_size}, \quad \text{pixel\_y} = \text{offset\_y} + r \times \text{tile\_size}$$

---

## 3. ĐƯỜNG ỐNG VẼ LỚP HÌNH ẢNH (LAYERED RENDERING PIPELINE)

Thứ tự vẽ từ dưới lên trên để không bị đè lỗi hình ảnh:
1. **Layer 0 (Window Background):** Tô màu xám sáng hiện đại `#E8ECF1`.
2. **Layer 1 (Floor):** Vẽ các ô sàn di chuyển được `#FFFFFF` có viền mờ `#BDC3C7`.
3. **Layer 2 (Walls):** Vẽ khối tường `%` màu xanh đen `#2C3E50`.
4. **Layer 3 (Goals):** Vẽ biểu tượng đích `D` màu đỏ `#E74C3C` có viền chấm tròn.
5. **Layer 4 (Boxes):**
   - Hộp tự do: Màu vàng gỗ `#F39C12`.
   - Hộp trên đích (chế độ đơn): Màu xanh lá `#27AE60`.
   - Hộp do Agent A chiếm (đối kháng): Màu xanh dương `#2980B9`.
   - Hộp do Agent B chiếm (đối kháng): Màu đỏ son `#C0392B`.
6. **Layer 5 (Players):** Vẽ nhân vật người chơi `A` (Avatar người đội mũ thợ mỏ).
7. **Layer 6 (HUD Dashboard & Controls):** Vẽ bảng thông số bên phải và các nút bấm.

---

## 4. BỘ ĐIỀU KHIỂN PHÁT LẠI (PLAYBACK CONTROLLER STATE MACHINE)

```python
class PlaybackController:
    def __init__(self, states_history: list[GameState], step_delay_ms: int = 250):
        self.history = states_history
        self.current_idx = 0
        self.is_paused = True
        self.step_delay_ms = step_delay_ms
        self.last_update_time = 0

    def toggle_pause(self):
        self.is_paused = not self.is_paused

    def step_forward(self):
        if self.current_idx < len(self.history) - 1:
            self.current_idx += 1

    def step_backward(self):
        if self.current_idx > 0:
            self.current_idx -= 1

    def update(self, current_time_ms: int):
        if not self.is_paused:
            if current_time_ms - self.last_update_time >= self.step_delay_ms:
                if self.current_idx < len(self.history) - 1:
                    self.current_idx += 1
                    self.last_update_time = current_time_ms
                else:
                    self.is_paused = True # Tự dừng khi đến đích
```

---

## 5. HIỂN THỊ CHẾ ĐỘ ĐỐI KHÁNG 2 AGENT & PHÂN BIỆT MÀU HỘP (REQUIREMENT 8)

Trong chế độ đối kháng:
- Hiển thị 2 nhân vật: Agent A (Avatar xanh) và Agent B (Avatar đỏ).
- Phân biệt quyền sở hữu hộp trên GUI:
  - Khi hộp chưa vào đích: Màu vàng trung lập.
  - Khi Agent A đẩy hộp vào đích: Hộp lập tức đổi sang **Màu Xanh Dương**.
  - Khi Agent B đẩy hộp vào đích: Hộp lập tức đổi sang **Màu Đỏ**.
- Bảng tỷ số trực tiếp (Scoreboard): Hiển thị `Score: A [ 3 ] - [ 2 ] B` và số bước còn lại `Steps Left: [ 45 / 100 ]`.

---

## 6. CHECKLIST TƯƠNG THÍCH TUYỆT ĐỐI TRÊN MACOS 13.7.8 (VENTURA) INTEL CORE I5

Đề bài nhấn mạnh yêu cầu tương thích:
> *"Ensure that the project can be executed on macOS 13.7.8 (Ventura) with an Intel Core i5 processor. Carefully verify the versions of all relevant Python libraries."*

| Hạng mục kiểm tra | Nguy cơ lỗi trên macOS Ventura Intel | Giải pháp kỹ thuật đã áp dụng |
| :--- | :--- | :--- |
| **Phiên bản Pygame** | Pygame phiên bản cũ (2.1 - 2.3) bị lỗi OpenGL context crash và đơ chuột trên macOS Ventura chạy chip Intel x86_64. | Bắt buộc khai báo `pygame>=2.5.0` (hoặc `pygame-ce>=2.3.0`) trong `requirements.txt`. |
| **Xử lý đường dẫn file** | Sử dụng dấu gạch chéo ngược Windows `\` gây lỗi `FileNotFoundError` ngay khi mở ứng dụng. | Toàn bộ đường dẫn file map và hình ảnh sử dụng `pathlib.Path` hoặc `os.path.join`. |
| **Phông chữ hiển thị** | Gọi các phông độc quyền Windows như `Consolas`, `Segoe UI` làm ứng dụng ném ngoại lệ hoặc không hiển thị text. | Sử dụng phông hệ thống cross-platform: `pygame.font.SysFont("Helvetica", size)` hoặc `pygame.font.Font(None, size)`. |
| **Hỗ trợ màn hình Retina** | Màn hình Retina có tỷ lệ pixel gấp đôi (HiDPI) làm giao diện bị mờ và lệch tọa độ click chuột trên nút bấm. | Khởi tạo cửa sổ với cờ `pygame.SCALED`: `pygame.display.set_mode((1024, 768), pygame.SCALED)`. |
| **Hàng đợi sự kiện hệ thống** | Không gọi `pygame.event.pump()` hoặc thiếu xử lý `pygame.QUIT` khiến macOS báo ứng dụng bị treo (Beachball cursor). | Đảm bảo vòng lặp sự kiện gọi `pygame.event.get()` liên tục ở mỗi frame với tốc độ `clock.tick(60)`. |
