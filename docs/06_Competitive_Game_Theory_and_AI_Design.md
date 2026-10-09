# 06. LÝ THUYẾT TRÒ CHƠI ĐỐI KHÁNG 2 AGENT, CƠ CHẾ XỬ LÝ XUNG ĐỘT & THIẾT KẾ THUẬT TOÁN AI
## (COMPETITIVE TWO-AGENT GAME THEORY, CONFLICT RESOLUTION & AI STRATEGY)

> **Tài liệu phục vụ trực tiếp cho:**  
> - **Requirement 6 (1.0 điểm):** Tái mô hình hóa bài toán thành bài toán đối kháng 2 Agent.  
> - **Requirement 7 (1.0 điểm):** Thiết kế thuật toán điều khiển Agent với giới hạn thời gian $\le 1000$ ms.  
> - **Requirement 8 (1.0 điểm):** Nâng cấp GUI hỗ trợ đối kháng, đổi màu hộp, tách biệt file mã nguồn thi đấu.

---

## MỤC LỤC
1. [Mô Hình Hóa Toán Học Trò Chơi Đối Kháng (Requirement 6)](#1-mô-hình-hóa-toán-học-trò-chơi-đối-kháng-requirement-6)
2. [Ma Trận Phân Xử Xung Đột Đồng Thời (Simultaneous Conflict Resolver)](#2-ma-trận-phân-xử-xung-đột-đồng-thời-simultaneous-conflict-resolver)
3. [Luật Cướp Hộp & Cơ Chế Tính Điểm Động](#3-luật-cướp-hộp--cơ-chế-tính-điểm-động)
4. [Thiết Kế Thuật Toán AI Cho 2 Agent (Requirement 7)](#4-thiết-kế-thuật-toán-ai-cho-2-agent-requirement-7)
5. [Cơ Chế Bảo Vệ Giới Hạn Thời Gian 1,000 ms (Timeout Guard)](#5-cơ-chế-bảo-vệ-giới-hạn-thời-gian-1000-ms-timeout-guard)
6. [Thiết Kế Bản Đồ Đối Kháng Chuẩn & Kiến Trúc Module Độc Lập (Requirement 8)](#6-thiết-kế-bản-đồ-đối-kháng-chuẩn--kiến-trúc-module-độc-lập-requirement-8)

---

## 1. MÔ HÌNH HÓA TOÁN HỌC TRÒ CHƠI ĐỐI KHÁNG (REQUIREMENT 6)

### 1.1. Định nghĩa bài toán
Trò chơi Sokoban đối kháng là một trò chơi có tổng không bằng không (non-zero-sum game), thông tin hoàn hảo (perfect information), và hành động đồng thời (simultaneous moves) giữa 2 Agent: $\text{Agent A}$ và $\text{Agent B}$ diễn ra trên cùng một lưới bản đồ mê cung $M$.

### 1.2. Không gian trạng thái đối kháng ($S_{\text{comp}}$)
Một trạng thái của trò chơi tại bước thời gian $t$ được định nghĩa bằng bộ 7 thành phần:
$$S_t = \langle p_A, p_B, B, O, score_A, score_B, t \rangle$$
Trong đó:
- $p_A = (r_A, c_A) \in \text{Floors}$: Tọa độ vị trí của $\text{Agent A}$ trên sàn.
- $p_B = (r_B, c_B) \in \text{Floors}$: Tọa độ vị trí của $\text{Agent B}$ trên sàn ($p_A \neq p_B$).
- $B = \{b_1, b_2, \dots, b_K\} \subset \text{Floors}$: Tập tọa độ của $K$ chiếc hộp trên bản đồ.
- $O: B \to \{\text{'A'}, \text{'B'}, \text{None}\}$: Hàm ánh xạ quyền sở hữu (Ownership) của từng chiếc hộp. Một chiếc hộp chỉ có chủ sở hữu khi nó đang nằm trên một ô đích $D$, và chủ sở hữu là Agent đã thực hiện cú đẩy cuối cùng đưa hộp vào đích đó.
- $score_A, score_B \in \mathbb{N}$: Điểm số hiện tại của hai Agent ($score_A = |\{b \in B \mid O(b) = \text{'A'}\}|$).
- $t \in [0, n]$: Bước đếm thời gian hiện tại.
- $n$: Số bước tối đa của ván đấu do người dùng nhập từ bàn phím khi bắt đầu game.

### 1.3. Không gian hành động (Action Space)
Tại mỗi bước thời gian $t$, mỗi Agent độc lập chọn một hành động từ tập hành động hữu hạn:
$$\mathcal{A} = \{\text{"North"}, \text{"South"}, \text{"West"}, \text{"East"}, \text{"Wait"}\}$$
Hành động liên hợp của hệ thống tại bước $t$:
$$\mathbf{a}_t = (a_A, a_B) \in \mathcal{A} \times \mathcal{A}$$

---

## 2. MA TRẬN PHÂN XỬ XUNG ĐỘT ĐỒNG THỜI (SIMULTANEOUS CONFLICT RESOLVER)

Do hai Agent đưa ra quyết định cùng lúc, các hành động độc lập có thể dẫn đến vi phạm quy luật vật lý không gian (va chạm vào nhau hoặc cùng tranh chấp một chiếc hộp).
Hệ thống sử dụng **Bộ phân xử xung đột (Conflict Resolver)** theo các quy tắc ưu tiên nghiêm ngặt sau:

```
                  ┌────────────────────────────────────────┐
                  │    Hành động đồng thời (a_A, a_B)      │
                  └──────────────────┬─────────────────────┘
                                     │
                 ┌───────────────────┴───────────────────┐
                 ▼                                       ▼
     [Kiểm tra Va chạm Người]                 [Kiểm tra Đẩy Hộp]
     - Vertex Collision?                     - Cùng đẩy 1 hộp?
     - Swap / Edge Collision?                - Đẩy hộp vào nhau?
                 │                                       │
                 └───────────────────┬───────────────────┘
                                     ▼
                  ┌────────────────────────────────────────┐
                  │   Quyết định Trạng thái kế tiếp S'     │
                  │   (Hủy bước, Đứng yên, hoặc Dịch chuyển)│
                  └────────────────────────────────────────┘
```

### 2.1. Quy tắc 1: Xung đột đỉnh (Vertex Collision)
- **Tình huống:** Cả hai Agent cùng chọn di chuyển vào cùng một ô sàn trống $X$:
  $$p_A + \Delta(a_A) = X \quad \text{và} \quad p_B + \Delta(a_B) = X$$
- **Phân xử:** **Từ chối cả hai hành động.** Cả $\text{Agent A}$ và $\text{Agent B}$ đều bị giữ nguyên ở vị trí cũ:
  $$p'_A = p_A, \quad p'_B = p_B$$

### 2.2. Quy tắc 2: Xung đột cạnh / Đổi chỗ (Swap / Edge Collision)
- **Tình huống:** Hai Agent đứng ở hai ô kề nhau và cùng bước vào ô của nhau:
  $$p_A + \Delta(a_A) = p_B \quad \text{và} \quad p_B + \Delta(a_B) = p_A$$
- **Phân xử:** Đề bài cấm tuyệt đối hai Agent đi xuyên qua nhau. **Từ chối cả hai hành động.** Cả hai đứng yên:
  $$p'_A = p_A, \quad p'_B = p_B$$

### 2.3. Quy tắc 3: Tranh chấp đẩy hộp (Box Contention Collision)
- **Tình huống:** Cả hai Agent cùng áp sát một chiếc hộp $b$ và cùng cố gắng đẩy chiếc hộp đó (theo cùng một hướng hoặc hai hướng khác nhau):
  $$p_A + \Delta(a_A) = b \quad \text{và} \quad p_B + \Delta(a_B) = b$$
- **Phân xử:** Hai lực tác động đồng thời triệt tiêu lẫn nhau. **Chiếc hộp $b$ không di chuyển.** Cả hai Agent đều bị chặn lại ở vị trí cũ:
  $$b' = b, \quad p'_A = p_A, \quad p'_B = p_B$$

### 2.4. Quy tắc 4: Đẩy hộp vào vị trí Agent đối thủ (Push into Opponent)
- **Tình huống:** $\text{Agent A}$ đẩy một chiếc hộp $b$ vào ô $Y$. Tại ô $Y$ hiện tại đang có $\text{Agent B}$ đứng.
- **Phân xử:**
  - Nếu trong cùng lượt đó, $\text{Agent B}$ thực hiện một hành động di chuyển hợp lệ rời khỏi ô $Y$ sang ô khác $\implies$ Ô $Y$ được giải phóng, cú đẩy của $\text{Agent A}$ **thành công**, hộp $b$ dịch chuyển vào $Y$.
  - Nếu $\text{Agent B}$ chọn `"Wait"`, hoặc bước đi của $\text{Agent B}$ bị hủy do va chạm khác (vẫn kẹt lại tại $Y$) $\implies$ Cú đẩy của $\text{Agent A}$ bị **từ chối** do ô $Y$ bị chặn, hộp $b$ và $\text{Agent A}$ đứng yên.

---

## 3. LUẬT CƯỚP HỘP & CƠ CHẾ TÍNH ĐIỂM ĐỘNG

Đề bài nêu rõ yêu cầu chiến thuật:
> *"An agent can move a box that has already been placed in its designated position by the other agent out of that position and then place the box again."*

### 3.1. Vòng đời quyền sở hữu của một chiếc hộp
1. **Trạng thái Tự do (Neutral Box):**
   - Hộp nằm ngoài các ô đích: $b \notin \text{Goals}$.
   - Quyền sở hữu: $O(b) = \text{None}$.
   - Màu sắc hiển thị trên GUI: **Màu Vàng Gỗ (Neutral Wood)**.
2. **Trạng thái Ghi điểm (Scored Box):**
   - Khi $\text{Agent A}$ thực hiện cú đẩy đưa hộp $b$ từ ô thường vào một ô đích $g \in \text{Goals}$:
     $$O(b) \leftarrow \text{'A'}, \quad score_A \leftarrow score_A + 1$$
   - Màu sắc hiển thị trên GUI: Chuyển sang **Màu Xanh Dương (Blue Box)**.
   - Tương tự, nếu $\text{Agent B}$ đẩy hộp vào đích:
     $$O(b) \leftarrow \text{'B'}, \quad score_B \leftarrow score_B + 1$$
   - Màu sắc hiển thị trên GUI: Chuyển sang **Màu Đỏ (Red Box)**.
3. **Cơ chế Cướp hộp (Unseating / Stealing):**
   - Giả sử hộp $b$ đang có $O(b) = \text{'A'}$ (nằm trên đích).
   - $\text{Agent B}$ di chuyển đến và đẩy hộp $b$ rời khỏi ô đích ra một ô sàn thường $b' \notin \text{Goals}$:
     $$O(b) \leftarrow \text{None}, \quad score_A \leftarrow score_A - 1$$
   - Ngay lập tức, điểm của $\text{Agent A}$ bị giảm đi 1, hộp $b$ trở lại màu vàng trung lập.
   - Nếu ở các lượt tiếp theo, $\text{Agent B}$ đẩy chiếc hộp này vào một ô đích khác, điểm số sẽ được cộng cho $\text{Agent B}$ ($score_B \leftarrow score_B + 1$).

### 3.2. Điều kiện kết thúc & Xếp hạng
Trận đấu kết thúc khi xảy ra một trong hai điều kiện:
1. Số bước đã thực hiện đạt giới hạn: $t == n$.
2. Toàn bộ các hộp trên bản đồ đều đã nằm trong các ô đích: $\forall b \in B, b \in \text{Goals}$.

**Kết quả:**
- Nếu $score_A > score_B \implies$ **Agent A Chiến Thắng (Winner: Agent A)**.
- Nếu $score_B > score_A \implies$ **Agent B Chiến Thắng (Winner: Agent B)**.
- Nếu $score_A == score_B \implies$ **Hòa (Draw)**.

---

## 4. THIẾT KẾ THUẬT TOÁN AI CHO 2 AGENT (REQUIREMENT 7)

Đề bài yêu cầu ứng dụng các thuật toán đã học trong chương trình:
> *"Design an algorithm to control the agents based on one or more of the algorithms covered in the lectures, such as BFS, UCS, DFS, DLS, IDS, GBFS, or A\*."*

Để tạo nên một trận đấu đối kháng hấp dẫn, kịch tính và thể hiện rõ sự tương phản chiến thuật, nhóm thiết kế 2 Agent với 2 trường phái tư duy AI khác biệt:

### 4.1. Agent A: Real-Time Hungarian A* (Chiến lược Kiến tạo & Tối ưu)
- **Triết lý:** Tập trung tối đa vào hiệu suất ghi điểm cá nhân, tìm đường đi ngắn nhất đến các hộp tiềm năng và tránh xung đột với đối thủ.
- **Quy trình ra quyết định:**
  1. **Lọc mục tiêu khả thi:** Xác định danh sách các hộp chưa thuộc về mình (gồm các hộp tự do $O(b) = \text{None}$ và các hộp đối thủ đang chiếm giữ $O(b) = \text{'B'}$).
  2. **Ghép cặp tối ưu (Goal Allocation):** Sử dụng ma trận khoảng cách tĩnh BFS để tìm cặp $(b^*, g^*)$ sao cho tổng chi phí:
     $$\text{Cost} = \text{Dist}(p_A, \text{PushPos}(b^*)) + \text{Dist}(b^*, g^*)$$
     là nhỏ nhất.
  3. **Lập kế hoạch đường đi bằng A\*:**
     - Tìm đường từ vị trí $p_A$ hiện tại đến vị trí đứng đẩy $\text{PushPos}(b^*)$.
     - Trong đồ thị tìm kiếm, xem vị trí hiện tại của $\text{Agent B}$ là một vật cản tạm thời để tránh va chạm.
  4. Trả về hành động đầu tiên trên đường đi tìm được.

### 4.2. Agent B: Greedy Best-First Search with Disruption (Chiến lược Cơ hội & Phá bĩnh)
- **Triết lý:** Tận dụng tối đa sai lầm của đối phương, ưu tiên cướp các hộp mà Agent A đã bỏ công đưa về đích hoặc phong tỏa hành lang di chuyển của Agent A.
- **Quy trình ra quyết định:**
  1. **Đánh giá mức độ đe dọa (Threat Assessment):**
     - Dự đoán hộp $b_A$ mà Agent A đang hướng tới.
     - Nếu Agent B có khoảng cách đến $b_A$ gần hơn hoặc bằng Agent A $\implies$ Kích hoạt chế độ tranh chấp (Race condition), cố gắng đẩy hộp đó theo hướng khác.
  2. **Chiến thuật Cướp điểm (Steal Scored Box):**
     - Nếu Agent A đã có điểm ($score_A > 0$), Agent B tính toán khoảng cách đến các hộp có $O(b) = \text{'A'}$.
     - Nếu khoảng cách $\le 4$ bước, Agent B ưu tiên chạy lại đẩy hộp đó ra khỏi đích để trừ điểm đối thủ.
  3. **Tìm đường bằng Greedy Best-First Search (GBFS):**
     - Hàm Heuristic: $h(n) = \text{Dist}_{\text{BFS}}(\text{current}, \text{target})$.
     - Ưu điểm: Tốc độ tìm kiếm cực nhanh ($< 5$ ms), phản ứng linh hoạt trong từng lượt bước ngắn hạn.

---

## 5. CƠ CHẾ BẢO VỆ GIỚI HẠN THỜI GIAN 1,000 MS (TIMEOUT GUARD)

Đề bài đặt ra hạn chế kỹ thuật:
> *"The time limit for each decision-making step is 1,000 ms."*

Nếu một Agent tính toán quá 1,000 ms, hệ thống sẽ xử thua hoặc phạt đứng yên. Để đảm bảo an toàn tuyệt đối 100%, nhóm thiết kế một lớp bao bọc an toàn thời gian (**Timeout Guard Wrapper**):

```python
import time
from typing import Callable

class TimeoutGuard:
    SAFETY_MARGIN_MS = 100  # Dành 100ms cho độ trễ hệ thống và I/O
    HARD_LIMIT_MS = 1000

    @classmethod
    def execute_with_guard(cls, agent_func: Callable, state: CompetitiveState) -> str:
        start_time = time.perf_counter()
        soft_deadline = start_time + (cls.HARD_LIMIT_MS - cls.SAFETY_MARGIN_MS) / 1000.0
        
        try:
            # Truyền deadline thời gian mềm vào hàm tính toán của Agent
            action = agent_func(state, soft_deadline)
        except TimeoutError:
            # Nếu thuật toán bên trong tự kích hoạt ngắt an toàn
            action = "Wait"
        except Exception:
            action = "Wait"

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        if elapsed_ms > cls.HARD_LIMIT_MS:
            # Cảnh báo vi phạm ngưỡng thời gian
            return "Wait"
            
        return action if action in ["North", "South", "East", "West", "Wait"] else "Wait"
```

**Cơ chế ngắt bên trong Agent:**
Trong các vòng lặp tìm kiếm `while frontier:` của A* hoặc GBFS, sau mỗi chu kỳ 50 node mở rộng, Agent thực hiện kiểm tra:
```python
if time.perf_counter() > soft_deadline:
    # Lập tức ngắt tìm kiếm và trả về hành động tốt nhất của node có h nhỏ nhất hiện tại
    return best_action_so_far
```

---

## 6. THIẾT KẾ BẢN ĐỒ ĐỐI KHÁNG CHUẨN & KIẾN TRÚC MODULE ĐỘC LẬP (REQUIREMENT 8)

### 6.1. Thiết kế Bản đồ Đối kháng Cân bằng (`maps/competitive_map.txt`)
Đề bài quy định: *"You may design a larger map to provide a suitable environment for the two agents to compete."*

Nhóm thiết kế bản đồ đối kháng kích thước $14 \times 14$ có tính đối xứng tâm (Central Symmetry), đảm bảo cự ly xuất phát của 2 Agent đến các hộp và các đích là hoàn toàn công bằng:

```text
%%%%%%%%%%%%%%%%
%  D   D  D   D%
% %%%%    %%%% %
% %  B    B  % %
%   %  %%  %   %
% A   %  %   B %
% %%%%    %%%% %
% %%%%    %%%% %
% B   %  %   A %
%   %  %%  %   %
% %  B    B  % %
% %%%%    %%%% %
%  D   D  D   D%
%%%%%%%%%%%%%%%%
```
- Gồm 6 chiếc hộp và 8 ô đích phân bố đối xứng.
- Có các hành lang thông nhau tạo cơ hội cản đường, đẩy hộp và cướp hộp hấp dẫn.

### 6.2. Kiến trúc Tách Biệt File Mã Nguồn (Pluggable Competition Interface)
Đề bài yêu cầu:
> *"The algorithms controlling the two agents must be implemented in separate source code files, allowing student groups to compete against each other."*

Cấu trúc file được tách bạch hoàn toàn:
```text
source/
├── competitive/
│   ├── engine.py       # Trọng tài điều phối, kiểm soát lượt, gọi TimeoutGuard
│   ├── conflict.py     # Bộ phân xử va chạm đồng thời
│   └── state.py        # Đối tượng CompetitiveState
└── agents/
    ├── base_agent.py   # Lớp trừu tượng định nghĩa Interface
    ├── agent_a.py      # Thuật toán độc quyền của Nhóm (Team AI)
    └── agent_b.py      # Thuật toán của Nhóm Đối thủ (Chỉ cần thay file này là đấu được ngay)
```

Khi muốn tổ chức thi đấu với một nhóm sinh viên khác:
1. Nhóm đối thủ chỉ cần cung cấp duy nhất file `agent_b.py` kế thừa lớp `BaseAgent`.
2. Trọng tài `engine.py` tự động import `agent_a.py` và `agent_b.py` qua giao diện chuẩn mà không cần sửa đổi bất kỳ dòng code hệ thống nào.
3. Trên GUI Pygame, Agent A được hiển thị avatar xanh, các hộp do Agent A ghi điểm mang màu xanh; Agent B được hiển thị avatar đỏ, các hộp do Agent B ghi điểm mang màu đỏ.
