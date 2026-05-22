import csv
from dataclasses import dataclass
from pathlib import Path

@dataclass
class User:
    username: str
    role: str

class AuthManager:
    def __init__(self, credentials_path: str | Path):
        self.credentials_path = Path(credentials_path)

    def validate(self, username: str, password: str) -> User | None:
        with self.credentials_path.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["username"] == username and row["password"] == password:
                    return User(username=row["username"], role=row["role"])
        return None
