from fastmcp import FastMCP
from db import SQLiteAdapter, ValidationError
import json
from typing import Optional, List, Dict

# Khởi tạo MCP Server
mcp = FastMCP("SQLite Lab Server")
db = SQLiteAdapter("lab.db")

# --- Tools ---

@mcp.tool()
def search(table: str, columns: Optional[List[str]] = None, filters: Optional[Dict] = None, limit: int = 20, offset: int = 0) -> str:
    """
    Tìm kiếm dữ liệu trong một bảng.
    - table: tên bảng (ví dụ: students)
    - columns: danh sách cột cần lấy (mặc định lấy hết)
    - filters: dict các điều kiện lọc (ví dụ: {"cohort": "A1"})
    - limit: số lượng bản ghi tối đa
    - offset: vị trí bắt đầu
    """
    try:
        results = db.search(table, columns, filters, limit, offset)
        return json.dumps(results, indent=2)
    except ValidationError as e:
        return f"Error: {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"

@mcp.tool()
def insert(table: str, values: dict) -> str:
    """
    Thêm một bản ghi mới vào bảng.
    - table: tên bảng
    - values: dict chứa dữ liệu (ví dụ: {"name": "John", "email": "john@test.com", "cohort": "A2"})
    """
    try:
        result = db.insert(table, values)
        return json.dumps(result, indent=2)
    except ValidationError as e:
        return f"Error: {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"

@mcp.tool()
def aggregate(table: str, metric: str, column: Optional[str] = None, filters: Optional[Dict] = None) -> str:
    """
    Thực hiện các phép toán thống kê trên bảng.
    - table: tên bảng
    - metric: phép toán (count, sum, avg, min, max)
    - column: tên cột cần tính toán (bắt buộc trừ count)
    - filters: điều kiện lọc trước khi thống kê
    """
    try:
        result = db.aggregate(table, metric, column, filters)
        return json.dumps(result, indent=2)
    except ValidationError as e:
        return f"Error: {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"

# --- Resources ---

@mcp.resource("schema://database")
def get_db_schema() -> str:
    """Trả về toàn bộ cấu trúc database (tất cả các bảng)."""
    schema_info = {}
    tables = db.list_tables()
    for table in tables:
        schema_info[table] = db.get_table_schema(table)
    return json.dumps(schema_info, indent=2)

@mcp.resource("schema://table/{table_name}")
def get_table_schema(table_name: str) -> str:
    """Trả về cấu trúc của một bảng cụ thể."""
    try:
        schema = db.get_table_schema(table_name)
        return json.dumps(schema, indent=2)
    except ValidationError as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    mcp.run()
