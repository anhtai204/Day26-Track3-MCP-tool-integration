# SQLite Lab MCP Server

Đây là một máy chủ Model Context Protocol (MCP) được xây dựng bằng FastMCP và Python, cho phép các AI Agent (như Claude, Gemini) tương tác trực tiếp với cơ sở dữ liệu SQLite.

## Tính năng
- **Tools**:
  - `search`: Tìm kiếm dữ liệu với bộ lọc (filters), giới hạn (limit).
  - `insert`: Thêm bản ghi mới vào database.
  - `aggregate`: Thực hiện các phép tính thống kê (count, sum, avg, min, max).
- **Resources**:
  - `schema://database`: Xem toàn bộ cấu trúc DB.
  - `schema://table/{table_name}`: Xem cấu trúc của một bảng cụ thể.
- **Bảo mật**: Tích hợp cơ chế validation tên bảng/cột và sử dụng parameterized queries để chống SQL Injection.

## Hướng dẫn cài đặt

### 1. Cài đặt môi trường
Yêu cầu Python 3.10 trở lên.
```bash
pip install mcp fastmcp
```

### 2. Khởi tạo Database
Chạy script để tạo file `lab.db` và dữ liệu mẫu:
```bash
python implementation/init_db.py
```

### 3. Chạy Server với MCP Inspector (Để kiểm thử)
```bash
npx @modelcontextprotocol/inspector python implementation/mcp_server.py
```
Sau đó mở trình duyệt tại `http://localhost:5173` để test các tool và resource.

## Cấu hình Client

### Gemini CLI
Để thêm server vào Gemini CLI:
```bash
gemini mcp add sqlite-lab python implementation/mcp_server.py --description "SQLite lab FastMCP server"
```

### Claude Desktop
Thêm đoạn sau vào file cấu hình của Claude Desktop (`%APPDATA%/Claude/claude_desktop_config.json` trên Windows):
```json
{
  "mcpServers": {
    "sqlite-lab": {
      "command": "python",
      "args": ["C:/PATH/TO/implementation/mcp_server.py"]
    }
  }
}
```

## Ví dụ sử dụng (Dành cho AI Agent)
- "Hãy liệt kê danh sách sinh viên lớp A1."
- "Thêm một sinh viên mới tên là 'Lê Văn D' vào lớp A2."
- "Tính điểm trung bình của tất cả sinh viên."
- "Cho tôi biết cấu trúc của bảng enrollments."
