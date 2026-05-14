import sqlite3
import os

DB_PATH = "lab.db"

def init_db():
    # Xóa DB cũ nếu tồn tại để reset
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f"Removed existing {DB_PATH}")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Tạo bảng students
    cursor.execute("""
    CREATE TABLE students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        cohort TEXT NOT NULL
    )
    """)

    # 2. Tạo bảng courses
    cursor.execute("""
    CREATE TABLE courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT
    )
    """)

    # 3. Tạo bảng enrollments
    cursor.execute("""
    CREATE TABLE enrollments (
        student_id INTEGER,
        course_id INTEGER,
        grade REAL,
        PRIMARY KEY (student_id, course_id),
        FOREIGN KEY (student_id) REFERENCES students (id),
        FOREIGN KEY (course_id) REFERENCES courses (id)
    )
    """)

    # Chèn dữ liệu mẫu
    students = [
        ("Nguyen Van A", "a@example.com", "A1"),
        ("Tran Thi B", "b@example.com", "A1"),
        ("Le Van C", "c@example.com", "A2"),
    ]
    cursor.executemany("INSERT INTO students (name, email, cohort) VALUES (?, ?, ?)", students)

    courses = [
        ("Python Basics", "Introduction to Python programming"),
        ("MCP Deep Dive", "Building Model Context Protocol servers"),
        ("SQL for Data Science", "Relational database management"),
    ]
    cursor.executemany("INSERT INTO courses (title, description) VALUES (?, ?)", courses)

    enrollments = [
        (1, 1, 9.5),
        (1, 2, 8.0),
        (2, 1, 7.5),
        (3, 3, 10.0),
    ]
    cursor.executemany("INSERT INTO enrollments (student_id, course_id, grade) VALUES (?, ?, ?)", enrollments)

    conn.commit()
    conn.close()
    print(f"Database {DB_PATH} initialized successfully with seed data.")

if __name__ == "__main__":
    init_db()
