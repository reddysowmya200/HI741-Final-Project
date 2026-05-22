import csv
from datetime import datetime
from pathlib import Path

class UsageLogger:
    def __init__(self, log_path: str | Path):
        self.log_path = Path(log_path)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.log_path.exists():
            with self.log_path.open("w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["username", "role", "login_time", "action", "status"])

    def log(self, username: str, role: str, action: str, status: str = "success"):
        with self.log_path.open("a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                username,
                role,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                action,
                status,
            ])
