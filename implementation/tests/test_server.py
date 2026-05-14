import pytest
import os
import sqlite3
from implementation.db import SQLiteAdapter, ValidationError
from implementation.init_db import init_db

TEST_DB = "test_lab.db"

@pytest.fixture(scope="module", autouse=True)
def setup_test_db():
    # Sử dụng init_db để tạo cấu trúc dữ liệu cho test_lab.db
    # Chúng ta cần patch DB_PATH trong init_db hoặc đơn giản là tự tạo ở đây
    conn = sqlite3.connect(TEST_DB)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY, name TEXT, cohort TEXT)")
    cursor.execute("DELETE FROM students")
    cursor.execute("INSERT INTO students (name, cohort) VALUES ('Alice', 'A1'), ('Bob', 'A2')")
    conn.commit()
    conn.close()
    
    yield
    
    # Đóng tất cả các handle trước khi xóa (trên Windows có thể bị lock)
    import gc
    gc.collect()
    
    try:
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)
    except PermissionError:
        pass # Bỏ qua nếu Windows giữ file

def test_list_tables():
    adapter = SQLiteAdapter(TEST_DB)
    tables = adapter.list_tables()
    assert "students" in tables

def test_search_success():
    adapter = SQLiteAdapter(TEST_DB)
    results = adapter.search("students", filters={"cohort": "A1"})
    assert len(results) == 1
    assert results[0]["name"] == "Alice"

def test_search_invalid_table():
    adapter = SQLiteAdapter(TEST_DB)
    with pytest.raises(ValidationError, match="Table not found"):
        adapter.search("unknown_table")

def test_search_invalid_identifier():
    adapter = SQLiteAdapter(TEST_DB)
    with pytest.raises(ValidationError, match="Invalid identifier"):
        adapter.search("students; DROP TABLE students;")

def test_insert_success():
    adapter = SQLiteAdapter(TEST_DB)
    res = adapter.insert("students", {"name": "Charlie", "cohort": "A1"})
    assert res["status"] == "success"
    
    results = adapter.search("students", filters={"name": "Charlie"})
    assert len(results) == 1

def test_aggregate_count():
    adapter = SQLiteAdapter(TEST_DB)
    res = adapter.aggregate("students", "count")
    # Ban đầu 2, sau insert 1 -> 3
    assert res["value"] >= 2
