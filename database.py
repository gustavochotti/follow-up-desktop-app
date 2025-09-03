# database.py
import sqlite3
import pandas as pd
from config import DB_FILE, DATE_FMT
from utils import _only_digits

def init_db():
    with sqlite3.connect(DB_FILE) as con:
        cur = con.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL, phone TEXT, email TEXT, course TEXT,
                visit_date TEXT, status TEXT, followup_date TEXT, notes TEXT
            )
            """
        )
        cur.execute("PRAGMA table_info(contacts)")
        cols = {row[1] for row in cur.fetchall()}
        
        def add_col(col_name, col_type="TEXT"):
            cur.execute(f"ALTER TABLE contacts ADD COLUMN {col_name} {col_type}")
        
        for col in ["monthly_fee", "how_found", "course_for", "attended_by"]:
            if col not in cols:
                add_col(col)
        con.commit()

class DatabaseManager:
    def __init__(self, db_file):
        self.db_file = db_file

    def _get_conn(self):
        return sqlite3.connect(self.db_file)

    def add_contact(self, data):
        with self._get_conn() as con:
            cur = con.cursor()
            cur.execute(
                """INSERT INTO contacts (name, phone, email, course, visit_date, status, 
                                        monthly_fee, how_found, course_for, attended_by, notes) 
                   VALUES (?,?,?,?,?,?,?,?,?,?,?)""", data
            )
            con.commit()

    def update_contact(self, data):
        with self._get_conn() as con:
            cur = con.cursor()
            cur.execute(
                """UPDATE contacts SET name=?, phone=?, email=?, course=?, visit_date=?, status=?, 
                                      monthly_fee=?, how_found=?, course_for=?, attended_by=?, notes=? 
                   WHERE id=?""", data
            )
            con.commit()

    def delete_contact(self, contact_id):
        with self._get_conn() as con:
            cur = con.cursor()
            cur.execute("DELETE FROM contacts WHERE id=?", (contact_id,))
            con.commit()

    def get_contacts(self, filters=None):
        with self._get_conn() as con:
            cur = con.cursor()
            base_select = "SELECT id, name, phone, email, course, visit_date, status, monthly_fee, how_found, course_for, attended_by, notes FROM contacts"
            
            clause = ""
            params = []
            if filters:
                clause = filters.get('clause', '')
                params = filters.get('params', [])
            
            query = base_select + clause + " ORDER BY id DESC"
            cur.execute(query, params)
            return cur.fetchall()

    def get_distinct_values(self, column):
        with self._get_conn() as con:
            cur = con.cursor()
            try:
                cur.execute(f"SELECT DISTINCT {column} FROM contacts WHERE {column} IS NOT NULL AND {column} <> '' ORDER BY {column}")
                return [r[0] for r in cur.fetchall() if r[0]]
            except sqlite3.OperationalError:
                return []

    def get_data_as_dataframe(self):
        with self._get_conn() as con:
            df = pd.read_sql_query("SELECT * FROM contacts", con)
            df['visit_date_dt'] = pd.to_datetime(df['visit_date'], format=DATE_FMT, errors='coerce')
            return df

    def delete_contacts_by_ids(self, ids):
        with self._get_conn() as con:
            cur = con.cursor()
            cur.executemany("DELETE FROM contacts WHERE id = ?", [(id,) for id in ids])
            con.commit()
            return len(ids)