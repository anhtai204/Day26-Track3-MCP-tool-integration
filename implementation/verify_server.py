from db import SQLiteAdapter
import json
import os

def verify():
    # Chạy từ thư mục implementation
    db_path = "lab.db"
    if not os.path.exists(db_path):
        # Thử lùi lại 1 cấp nếu chạy từ tests hoặc thư mục gốc
        db_path = "implementation/lab.db"
        
    db = SQLiteAdapter(db_path)
    
    print("--- 1. List Tables ---")
    tables = db.list_tables()
    print(tables)
    assert "students" in tables
    
    print("\n--- 2. Get Schema (students) ---")
    schema = db.get_table_schema("students")
    print(f"Columns: {[s['name'] for s in schema]}")
    
    print("\n--- 3. Search (Cohort A1) ---")
    results = db.search("students", filters={"cohort": "A1"})
    print(f"Found {len(results)} students")
    
    print("\n--- 4. Aggregate (Avg Grade) ---")
    agg = db.aggregate("enrollments", "avg", "grade")
    print(f"Avg Grade: {agg['value']}")

if __name__ == "__main__":
    verify()
