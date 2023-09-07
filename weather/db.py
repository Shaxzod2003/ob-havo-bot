import json


class DB:
    def __init__(self, file_name: str) -> None:
        self.file_name = file_name
        self.data = {}
        self.db_load()

    def db_load(self) -> None:
        with open(self.file_name, "r") as f:
            file_data = f.read()
            if file_data == "":
                self.data = {}
                return None
            self.data = json.loads(file_data)

    def save(self) -> None:
        with open(self.file_name, "w") as f:
            json.dump(self.data, f, indent=4)

    def is_user(self, chat_id: int) -> bool:
        return str(chat_id) in self.data

    def add_user(self, chat_id: int, first_name: str, last_name: str, username: str) -> None:
        if self.is_user(chat_id):
            return False
        self.data[chat_id] = {
            "first_name": first_name,
            "first_name": first_name,
            "last_name": last_name,
            "username": username,
        }
        self.save()
        self.db_load()

        return True
