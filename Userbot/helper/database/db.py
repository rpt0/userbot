import json
import os
import sqlite3
import stat
import threading
from datetime import datetime, timedelta, timezone

from config import db_name

db_path = os.path.abspath(f"./{db_name}.db")


class DatabaseClient:
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path
        self._connection = sqlite3.connect(db_path, check_same_thread=False)
        self.lock = threading.Lock()
        self._initialize_database()
        self._set_permissions()

    def _initialize_database(self):
        with self._connection as conn:
            cursor = conn.cursor()
            # Creating tables
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS user_prefixes (
                    user_id INTEGER PRIMARY KEY,
                    prefix TEXT
                )
            """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS floods (
                    gw INTEGER,
                    user_id INTEGER,
                    flood TEXT,
                    PRIMARY KEY (gw, user_id)
                )
            """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS variabel (
                    _id INTEGER PRIMARY KEY,
                    vars TEXT
                )
            """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS expired (
                    _id INTEGER PRIMARY KEY,
                    expire_date TEXT
                )
            """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS userdata (
                    user_id INTEGER PRIMARY KEY,
                    depan TEXT,
                    belakang TEXT,
                    username TEXT,
                    mention TEXT,
                    full TEXT,
                    _id INTEGER
                )
            """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS ubotdb (
                    user_id TEXT PRIMARY KEY,
                    api_id TEXT,
                    api_hash TEXT,
                    session_string TEXT
                )
            """
            )

    def _set_permissions(self):
        try:
            # Ubah izin file menjadi 666 (rw-rw-rw-)
            os.chmod(
                self.db_path,
                stat.S_IRUSR
                | stat.S_IWUSR
                | stat.S_IRGRP
                | stat.S_IROTH
                | stat.S_IWGRP
                | stat.S_IWOTH,
            )
            print(f"Permissions for {self.db_path} set to 666.")
        except Exception as e:
            print(f"Failed to set permissions: {e}")

    def close(self):
        if self._connection:
            self._connection.close()
            print("Database connection closed.")

    def _check_connection(self):
        if not self._connection:
            raise sqlite3.ProgrammingError("Database connection is closed.")

    # Replacing get_pref
    def get_pref(self, user_id):
        self._check_connection()
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT prefix FROM user_prefixes WHERE user_id = ?", (user_id,)
            )
            result = cursor.fetchone()

            return json.loads(result[0]) if result else [".", "-", "!", "+", "?"]

    # Replacing set_pref
    def set_pref(self, user_id, prefix):
        self._check_connection()
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT OR REPLACE INTO user_prefixes (user_id, prefix)
                VALUES (?, ?)
            """,
                (user_id, json.dumps(prefix)),
            )

    # Replacing rem_pref
    def rem_pref(self, user_id):
        self._check_connection()
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM user_prefixes WHERE user_id = ?", (user_id,))

    # Replacing set_var
    def set_var(self, bot_id, vars_name, value, query="vars"):
        self._check_connection()
        json_value = json.dumps(value)  # Convert dictionary to JSON string
        with self.lock:
            with self._connection as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT OR REPLACE INTO variabel (_id, vars)
                    VALUES (?, json_set(COALESCE((SELECT vars FROM variabel WHERE _id = ?), '{}'), ?, ?))
                    """,
                    (
                        bot_id,
                        bot_id,
                        f"$.{query}.{vars_name}",
                        json_value,
                    ),  # Use JSON string
                )

        # Method to get a variable (with JSON deserialization)

    def get_var(self, bot_id, vars_name, query="vars"):
        self._check_connection()
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT vars FROM variabel WHERE _id = ?", (bot_id,))
            document = cursor.fetchone()

            if document:
                data = json.loads(document[0])  # Parse JSON string to dictionary
                value = data.get(query, {}).get(vars_name)
                # Check if the value is a JSON string and try to decode it
                try:
                    return json.loads(value) if isinstance(value, str) else value
                except json.JSONDecodeError:
                    return value  # If decoding fails, return the value as is
            return None

    # Replacing remove_var
    def remove_var(self, bot_id, vars_name, query="vars"):
        self._check_connection()
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE variabel SET vars = json_remove(vars, ?) WHERE _id = ?
            """,
                (f"$.{query}.{vars_name}", bot_id),
            )

    # Replacing all_var
    def all_var(self, user_id, query="vars"):
        self._check_connection()
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT vars FROM variabel WHERE _id = ?", (user_id,))
            result = cursor.fetchone()

            return json.loads(result[0]).get(query) if result else None

    # Replacing rm_all
    def rm_all(self, bot_id):
        self._check_connection()
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM variabel WHERE _id = ?", (bot_id,))

    # Replacing get_list_from_var
    def get_list_from_var(self, user_id, vars_name, query="vars"):
        self._check_connection()
        vars_data = self.get_var(user_id, vars_name, query)
        return [int(x) for x in str(vars_data).split()] if vars_data else []

    # Replacing add_to_var
    def add_to_var(self, user_id, vars_name, value, query="vars"):
        self._check_connection()
        vars_list = self.get_list_from_var(user_id, vars_name, query)
        vars_list.append(value)
        self.set_var(user_id, vars_name, " ".join(map(str, vars_list)), query)

    # Replacing remove_from_var
    def remove_from_var(self, user_id, vars_name, value, query="vars"):
        self._check_connection()
        vars_list = self.get_list_from_var(user_id, vars_name, query)
        if value in vars_list:
            vars_list.remove(value)
            self.set_var(user_id, vars_name, " ".join(map(str, vars_list)), query)

    # Replacing get_expired_date
    def get_expired_date(self, user_id):
        self._check_connection()
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT expire_date FROM expired WHERE _id = ?", (user_id,))
            result = cursor.fetchone()

            return (
                datetime.strptime(result[0], "%Y-%m-%d %H:%M:%S.%f%z")
                if result and result[0]
                else None
            )
        # return result[0] if result else None

    def set_expired_date(self, user_id, expire_date):
        if isinstance(expire_date, str):
            try:
                # Try parsing with timezone
                expire_date = datetime.strptime(expire_date, "%Y-%m-%d %H:%M:%S.%f%z")
            except ValueError:
                # If parsing fails, assume it's without timezone and add +07:00
                expire_date = datetime.strptime(expire_date, "%Y-%m-%d %H:%M:%S.%f")
                expire_date = expire_date.replace(tzinfo=timezone(timedelta(hours=7)))

        # Format the date with the timezone
        formatted_date = expire_date.strftime("%Y-%m-%d %H:%M:%S.%f%z")

        self._check_connection()
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT OR REPLACE INTO expired (_id, expire_date) VALUES (?, ?)
                """,
                (user_id, formatted_date),
            )

    # Replacing rem_expired_date
    def rem_expired_date(self, user_id):
        self._check_connection()
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE expired SET expire_date = NULL WHERE _id = ?
            """,
                (user_id,),
            )

    # Replacing cek_userdata
    def cek_userdata(self, user_id: int) -> bool:
        self._check_connection()
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM userdata WHERE user_id = ?", (user_id,))
            result = cursor.fetchone()

            return bool(result)

    def get_userdata(self, user_id: int):
        self._check_connection()
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM userdata WHERE user_id = ?", (user_id,))
            result = cursor.fetchone()

            # Jika hasil ditemukan, buat dictionary secara manual dari tuple
            if result:
                return {
                    "user_id": result[0],
                    "depan": result[1],
                    "belakang": result[2],
                    "username": result[3],
                    "mention": result[4],
                    "full": result[5],
                    "_id": result[6],
                }
            return None

    # Replacing add_userdata
    def add_userdata(self, user_id: int, depan, belakang, username, mention, full, _id):
        self._check_connection()
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT OR REPLACE INTO userdata (user_id, depan, belakang, username, mention, full, _id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
                (user_id, depan, belakang, username, mention, full, _id),
            )

    def add_ubot(self, user_id, api_id, api_hash, session_string):
        self._check_connection()
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT OR REPLACE INTO ubotdb (user_id, api_id, api_hash, session_string)
                VALUES (?, ?, ?, ?)
                """,
                (user_id, api_id, api_hash, session_string),
            )

    def remove_ubot(self, user_id):
        self._check_connection()
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM ubotdb WHERE user_id = ?", (user_id,))

    def get_userbots(self):
        self._check_connection()
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM ubotdb WHERE user_id IS NOT NULL")
            data = [
                {
                    "name": str(user_id),
                    "api_id": api_id,
                    "api_hash": api_hash,
                    "session_string": session_string,
                }
                for user_id, api_id, api_hash, session_string in cursor.fetchall()
            ]

            return data

    def update_ub(self, user_id, api_id, api_hash):
        self._check_connection()
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE ubotdb
                SET api_id = ?, api_hash = ?
                WHERE user_id = ?
                """,
                (api_id, api_hash, user_id),
            )

    # Replacing get_flood
    def get_flood(self, gw: int, user_id: int):
        self._check_connection()
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT flood FROM floods WHERE gw = ? AND user_id = ?", (gw, user_id)
            )
            result = cursor.fetchone()

            return result[0] if result else None

    # Replacing set_flood
    def set_flood(self, gw: int, user_id: int, flood: str):
        self._check_connection()
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT OR REPLACE INTO floods (gw, user_id, flood)
                VALUES (?, ?, ?)
            """,
                (gw, user_id, flood),
            )

    # Replacing rem_flood
    def rem_flood(self, gw: int, user_id: int):
        self._check_connection()
        with self._connection as conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM floods WHERE gw = ? AND user_id = ?", (gw, user_id)
            )


dB = DatabaseClient(db_path)
