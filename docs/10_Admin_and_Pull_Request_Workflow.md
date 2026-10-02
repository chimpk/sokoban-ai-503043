# Quy Trình Trưởng Nhóm (Admin) và Pull Request Workflow

Để đảm bảo source code của dự án được bảo vệ, hạn chế rủi ro hỏng code gốc khi ghép code (merge conflict), toàn bộ dự án sẽ tuân thủ nghiêm ngặt **Quy trình Pull Request**. 

## 1. Quyền hạn của Trưởng nhóm (Admin)
Chỉ định 01 thành viên làm **Admin** (Trưởng nhóm hoặc người cứng kỹ thuật nhất) sở hữu quyền quản trị Repository trên GitHub.

Admin có các quyền hạn và trách nhiệm sau:
- **Thiết lập Rule Protection (Bảo vệ nhánh gốc):** Khoá nhánh `main`. Không ai (kể cả Admin) được quyền `git push` trực tiếp lên nhánh này.
- **Merge Code:** Chỉ có Admin (hoặc người được uỷ quyền) mới được bấm nút "Merge Pull Request" sau khi code đã được review.
- **Giải quyết Conflict:** Hỗ trợ các thành viên xử lý conflict khi có 2 nhánh thay đổi chung một file.

## 2. Thiết lập Branch Protection trên GitHub (Dành cho Admin)
Để ép buộc dùng Pull Request, Admin cần vào GitHub Repo thực hiện:
1. Vào mục **Settings** > **Branches** > **Add branch protection rule**.
2. Ô *Branch name pattern* nhập: `main`.
3. Tick chọn **Require a pull request before merging**.
4. Tick chọn **Require approvals** (Chọn số lượng: 1).
5. Nhấn **Create**.

## 3. Quy trình làm việc (Dành cho toàn bộ thành viên)

Không ai được code trực tiếp trên nhánh `main`.

**Bước 1: Chuyển sang nhánh cá nhân trước khi code**
```bash
git fetch origin
git checkout main
git pull origin main
git checkout -b feature/memberX-ten-chuc-nang
```

**Bước 2: Code và đẩy lên nhánh cá nhân**
Sau khi hoàn thành tính năng:
```bash
git add .
git commit -m "feat(module): Hoàn thành chức năng X"
git push origin feature/memberX-ten-chuc-nang
```

**Bước 3: Tạo Pull Request (PR)**
- Lên giao diện GitHub, tạo một Pull Request từ nhánh `feature/memberX-ten-chuc-nang` vào nhánh `main`.
- Điền đầy đủ thông tin vào Form **Pull Request Template** đã được thiết lập sẵn.

**Bước 4: Review và Merge (Admin)**
- Một thành viên khác hoặc Admin sẽ đọc code trên PR.
- Nếu code ok, bấm **Approve**.
- Cuối cùng, Admin sẽ nhấn nút **Merge pull request** để đưa code vào `main`.
- Sau khi merge xong, có thể xóa nhánh `feature` cũ.
