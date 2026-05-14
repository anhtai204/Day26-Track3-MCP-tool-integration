import sqlite3
import re

class ValidationError(Exception):
    """Raised when a request cannot be safely executed."""
    pass

class SQLiteAdapter:
    def __init__(self, db_path="lab.db"):
        self.db_path = db_path

    def connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _validate_identifier(self, name):
        """Đảm bảo tên bảng hoặc cột chỉ chứa chữ cái, số và dấu gạch dưới."""
        if not name or not re.match(r"^[a-zA-Z0-9_]+$", name):
            raise ValidationError(f"Invalid identifier: {name}")
        return name

    def list_tables(self):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
            return [row["name"] for row in cursor.fetchall()]

    def get_table_schema(self, table):
        self._validate_identifier(table)
        if table not in self.list_tables():
            raise ValidationError(f"Table not found: {table}")
            
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(f"PRAGMA table_info({table})")
            return [dict(row) for row in cursor.fetchall()]

    def search(self, table, columns=None, filters=None, limit=20, offset=0):
        """
        Tìm kiếm dữ liệu với validation.
        filters: dict {column: value}
        """
        self._validate_identifier(table)
        tables = self.list_tables()
        if table not in tables:
            raise ValidationError(f"Table not found: {table}")

        # Validate columns
        schema = self.get_table_schema(table)
        valid_cols = [s["name"] for s in schema]
        
        select_clause = "*"
        if columns:
            for col in columns:
                self._validate_identifier(col)
                if col not in valid_cols:
                    raise ValidationError(f"Column {col} not found in {table}")
            select_clause = ", ".join(columns)

        query = f"SELECT {select_clause} FROM {table}"
        params = []

        if filters:
            where_clauses = []
            for col, val in filters.items():
                self._validate_identifier(col)
                if col not in valid_cols:
                    raise ValidationError(f"Filter column {col} not found")
                where_clauses.append(f"{col} = ?")
                params.append(val)
            query += " WHERE " + " AND ".join(where_clauses)

        query += f" LIMIT {int(limit)} OFFSET {int(offset)}"

        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    def insert(self, table, values):
        """
        Insert dữ liệu. values: dict {column: value}
        """
        self._validate_identifier(table)
        if not values:
            raise ValidationError("Insert values cannot be empty")

        schema = self.get_table_schema(table)
        valid_cols = [s["name"] for s in schema]

        cols = []
        placeholders = []
        params = []

        for col, val in values.items():
            self._validate_identifier(col)
            if col not in valid_cols:
                raise ValidationError(f"Column {col} not found")
            cols.append(col)
            placeholders.append("?")
            params.append(val)

        query = f"INSERT INTO {table} ({', '.join(cols)}) VALUES ({', '.join(placeholders)})"
        
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return {"status": "success", "rowid": cursor.lastrowid}

    def aggregate(self, table, metric, column=None, filters=None):
        """
        metric: count, sum, avg, min, max
        """
        self._validate_identifier(table)
        valid_metrics = ["count", "sum", "avg", "min", "max"]
        if metric.lower() not in valid_metrics:
            raise ValidationError(f"Unsupported metric: {metric}")

        schema = self.get_table_schema(table)
        valid_cols = [s["name"] for s in schema]

        if column:
            self._validate_identifier(column)
            if column not in valid_cols:
                raise ValidationError(f"Column {column} not found")
            expr = f"{metric}({column})"
        else:
            expr = "count(*)"

        query = f"SELECT {expr} as result FROM {table}"
        params = []

        if filters:
            where_clauses = []
            for col, val in filters.items():
                self._validate_identifier(col)
                if col not in valid_cols:
                    raise ValidationError(f"Filter column {col} not found")
                where_clauses.append(f"{col} = ?")
                params.append(val)
            query += " WHERE " + " AND ".join(where_clauses)

        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            row = cursor.fetchone()
            return {"metric": metric, "column": column, "value": row["result"]}
