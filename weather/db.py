from tinydb import TinyDB, Query
from tinydb.table import Document


class DB:
    def __init__(self, file_name: str):
        self.db = TinyDB(file_name, indent=4)
        self.users = self.db.table('users')

    def is_user(self, chat_id: str) -> bool:
        return self.users.contains(doc_id=chat_id)

    def add_user(self, chat_id: str, first_name: str, last_name: str, username: str):
        if self.is_user(chat_id):
            return False
        
        user = Document(
            value={
                'first_name': first_name,
                'last_name': last_name,
                'username': username
            },
            doc_id=chat_id
        )
        self.users.insert(user)

