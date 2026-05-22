import tkinter as tk
from pathlib import Path

from src.users import AuthManager
from src.warehouse import ClinicalDataWarehouse
from src.logger import UsageLogger
from src.ui import ClinicalDataWarehouseApp

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "Data"
OUTPUT_DIR = BASE_DIR / "output"

def main():
    auth = AuthManager(DATA_DIR / "credentials.csv")
    warehouse = ClinicalDataWarehouse(DATA_DIR)
    logger = UsageLogger(OUTPUT_DIR / "usage_log.csv")

    root = tk.Tk()
    ClinicalDataWarehouseApp(root, auth, warehouse, logger)
    root.mainloop()

if __name__ == "__main__":
    main()
