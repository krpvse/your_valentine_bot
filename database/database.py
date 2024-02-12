import sqlite3


class Database:
    def __init__(self, db_file: str):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def add_user(self, user_id: int) -> None:
        with self.connection:
            self.cursor.execute("INSERT OR IGNORE INTO profiles (user_id) VALUES (?)", (user_id,))

    def get_profile(self, user_id: int) -> list:
        return self.cursor.execute("SELECT * FROM profiles WHERE user_id = ?", (user_id,)).fetchone()

    def change_profile(self, user_id: int, name: str, description: str) -> None:
        with self.connection:
            self.cursor.execute("UPDATE profiles SET name = ?, description = ? WHERE user_id = ?", (name, description, user_id,))

    def get_valentine_cards(self, user_id: int) -> list:
        return self.cursor.execute("SELECT card FROM valentine_cards WHERE fk_profiles_user_id = ?", (user_id,)).fetchall()

    def save_valentine_card(self, user_id: int, card: str) -> None:
        with self.connection:
            self.cursor.execute("INSERT INTO valentine_cards (fk_profiles_user_id, card) VALUES (?, ?)", (user_id, card))
