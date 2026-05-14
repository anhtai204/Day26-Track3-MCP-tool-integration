from db import SQLiteAdapter
import json

def test():
    db = SQLiteAdapter("lab.db")
    
    print("--- 1. List Tables ---")
    print(db.list_tables())
    
    print("\n--- 2. Get Schema (Students) ---")
    print(json.dumps(db.get_table_schema("students"), indent=2))
    
    print("\n--- 3. Search Students in Cohort A1 ---")
    results = db.search("students", filters={"cohort": "A1"})
    print(json.dumps(results, indent=2))
    
    print("\n--- 4. Insert New Student ---")
    try:
        new_id = db.insert("students", {"name": "Test User", "email": "test@user.com", "cohort": "A3"})
        print(f"Inserted: {new_id}")
    except Exception as e:
        print(f"Insert failed: {e}")
        
    print("\n--- 5. Aggregate: Average Grade ---")
    agg = db.aggregate("enrollments", "avg", "grade")
    print(json.dumps(agg, indent=2))
    
    print("\n--- 6. Test Validation Error (Invalid Table) ---")
    try:
        db.search("non_existent_table")
    except Exception as e:
        print(f"Caught expected error: {e}")

if __name__ == "__main__":
    test()
