import os
import psycopg
from dotenv import load_dotenv

load_dotenv()


class PostgresDB:
    def __init__(self):
        try:
            self.conn = psycopg.connect(os.getenv("DATABASE_URL"))
            self.conn.autocommit = True
        except Exception as e:
            print(f"Database initialization failed: {e}")
            raise e

    def close(self):
        try:
            self.conn.close()
        except Exception as e:
            print(f"Error closing database connection: {e}")

    # -----------------------
    # CREATE
    # -----------------------
    def connect(self):
        try:
            self.conn = psycopg.connect(os.getenv("DATABASE_URL"))
        except Exception as e:
            print(f"Database connection failed: {e}")
            raise e

    def insert(self, table: str, data: dict):
        try:
            if self.conn.closed:
                self.connect() 
            columns = ", ".join(data.keys())
            placeholders = ", ".join(["%s"] * len(data))

            query = f"""
                INSERT INTO {table} ({columns})
                VALUES ({placeholders})
            """
            print(query)

            with self.conn.cursor() as cur:
                cur.execute(query, tuple(data.values()))
        except Exception as e:
            print(f"Database insert error: {e}")
            raise e

    # -----------------------
    # READ
    # -----------------------
    def get_all(self, table: str):
        try:
            if self.conn.closed:
                self.connect()
            with self.conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {table}")
                columns = [d.name for d in cur.description]
                rows = cur.fetchall()

            return columns, rows
        except Exception as e:
            print(f"Database read error: {e}")
            raise e

    # def get_by_id(self, table: str, id_column: str, value):
    #     query = f"SELECT * FROM {table} WHERE {id_column}=%s"

    #     with self.conn.cursor() as cur:
    #         cur.execute(query, (value,))
            # return cur.fetchone()

    # -----------------------
    # UPDATE
    # -----------------------
    # def update(self, table: str, data: dict, where_column: str, where_value):
    #     set_clause = ", ".join(
    #         [f"{col}=%s" for col in data.keys()]
    #     )

    #     query = f"""
    #         UPDATE {table}
    #         SET {set_clause}
    #         WHERE {where_column}=%s
    #     """

    #     values = list(data.values())
    #     values.append(where_value)

    #     with self.conn.cursor() as cur:
    #         cur.execute(query, values)

    # # -----------------------
    # # DELETE
    # # -----------------------
    # def delete(self, table: str, where_column: str, where_value):
    #     query = f"DELETE FROM {table} WHERE {where_column}=%s"

    #     with self.conn.cursor() as cur:
    #         cur.execute(query, (where_value,))

    # # -----------------------
    # # UTILITIES
    # # -----------------------
    # def get_columns(self, table: str):
    #     query = """
    #         SELECT column_name
    #         FROM information_schema.columns
    #         WHERE table_schema='public'
    #         AND table_name=%s
    #         ORDER BY ordinal_position
    #     """

    #     with self.conn.cursor() as cur:
    #         cur.execute(query, (table,))
    #         return [row[0] for row in cur.fetchall()]
        

# try:
#     with psycopg.connect(conn_string) as conn:
#         print("Connection established")

#         with conn.cursor() as cur:
#         #     cur.execute("SELECT * FROM members;")
#         #     rows = cur.fetchall()

#         #     for row in rows:
#         #         print(row)
#             cur.execute("""
#             SELECT column_name
#             FROM information_schema.columns
#             WHERE table_schema = 'public'
#             AND table_name = 'members'
#             ORDER BY ordinal_position;
#             """)

#             columns = [row[0] for row in cur.fetchall()]
#             print(columns)
# except Exception as e:
#     print("Connection failed.")
#     print(e)