# Kịch bản Demo Chi tiết: SQLite MCP Server

Dưới đây là kịch bản "từng bước một" để bạn quay video demo Lab 26.

## 0. Chuẩn bị (Trước khi bấm quay)
*   Chạy: `python implementation/init_db.py`
*   Chạy: `npx @modelcontextprotocol/inspector python implementation/mcp_server.py`
*   Mở: `http://localhost:5173`
*   Phóng to màn hình (Ctrl +) để text to và rõ.

---

## 1. Mở đầu (0:00 - 0:15)
*   **Hành động**: Để màn hình ở trang chủ Inspector hoặc Terminal.
*   **Lời thoại**: "Xin chào, đây là demo cho Lab 26: Xây dựng MCP Server tích hợp cơ sở dữ liệu SQLite sử dụng thư viện FastMCP trong Python."
*   **Thao tác**: Nhấn nút **Connect** (nếu chưa kết nối). Nhìn xuống cửa sổ Log để thấy dòng `Created server transport`.

## 2. Khám phá Tài nguyên (0:15 - 0:40)
*   **Hành động**: Nhấp vào biểu tượng **Resources** (hình văn bản) ở menu bên trái.
*   **Thao tác**: Chọn `schema://database` từ danh sách. Nhấn nút **Read Resource**.
*   **Lời thoại**: "Điểm mạnh của MCP là khả năng cung cấp Resources. Tại đây, tôi cung cấp cấu trúc toàn bộ database để Agent hiểu mình có thể làm gì."

## 3. Thực thi Công cụ (0:40 - 1:40)
*   **Hành động**: Nhấp vào biểu tượng **Tools** (hình cái búa/cờ lê).

### Bước 3.1: Tìm kiếm (Search Tool)
*   **Thao tác**: Chọn tool `search`.
*   **Điền tham số**: `table: students`, `filters: {"cohort": "A1"}`.
*   **Thao tác**: Nhấn **Call Tool**.
*   **Lời thoại**: "Công cụ search cho phép tìm kiếm có điều kiện. Tôi đang tìm các sinh viên lớp A1."

### Bước 3.2: Thêm dữ liệu (Insert Tool)
*   **Thao tác**: Chọn tool `insert`.
*   **Điền tham số**: `table: students`, `values: {"name": "Alex Demo", "email": "alex@mcp.com", "cohort": "A2"}`.
*   **Thao tác**: Nhấn **Call Tool**.
*   **Lời thoại**: "Tiếp theo, tôi sử dụng tool insert để thêm một sinh viên mới vào database. Server xác nhận đã thêm thành công."

### Bước 3.3: Thống kê (Aggregate Tool)
*   **Thao tác**: Chọn tool `aggregate`.
*   **Điền tham số**: `table: enrollments`, `metric: avg`, `column: grade`.
*   **Thao tác**: Nhấn **Call Tool**.
*   **Lời thoại**: "Cuối cùng, tool aggregate giúp tính toán nhanh. Ở đây tôi tính điểm trung bình của toàn bộ học viên."

## 4. Bảo mật và Kết thúc (1:40 - 2:00)
*   **Hành động**: Chọn tool `search`, nhập tên bảng không tồn tại (ví dụ: `secret_db`).
*   **Thao tác**: Nhấn **Call Tool**.
*   **Lời thoại**: "Server cũng xử lý lỗi rất tốt khi gặp yêu cầu không hợp lệ. Như vậy phần demo của tôi đã hoàn thành. Cảm ơn các bạn!"
