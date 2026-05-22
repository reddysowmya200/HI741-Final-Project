import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

class ClinicalDataWarehouseApp:
    def __init__(self, root, auth_manager, warehouse, usage_logger):
        self.root = root
        self.auth = auth_manager
        self.warehouse = warehouse
        self.logger = usage_logger
        self.current_user = None

        self.root.title("Clinical Data Warehouse")
        self.root.geometry("760x520")
        self.show_login()

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_login(self):
        self.clear()
        frame = ttk.Frame(self.root, padding=30)
        frame.pack(expand=True)

        ttk.Label(frame, text="Clinical Data Warehouse Login", font=("Arial", 18, "bold")).grid(row=0, column=0, columnspan=2, pady=15)

        ttk.Label(frame, text="Username").grid(row=1, column=0, sticky="w", pady=5)
        self.username_entry = ttk.Entry(frame, width=30)
        self.username_entry.grid(row=1, column=1, pady=5)

        ttk.Label(frame, text="Password").grid(row=2, column=0, sticky="w", pady=5)
        self.password_entry = ttk.Entry(frame, width=30, show="*")
        self.password_entry.grid(row=2, column=1, pady=5)

        ttk.Button(frame, text="Log In", command=self.login).grid(row=3, column=0, columnspan=2, pady=15)

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        user = self.auth.validate(username, password)

        if not user:
            self.logger.log(username or "unknown", "unknown", "login", "failed")
            messagebox.showerror("Login failed", "Invalid username or password.")
            return

        self.current_user = user
        self.logger.log(user.username, user.role, "login", "success")
        self.show_menu()

    def show_menu(self):
        self.clear()
        ttk.Label(
            self.root,
            text=f"Welcome {self.current_user.username} ({self.current_user.role})",
            font=("Arial", 16, "bold"),
        ).pack(pady=15)

        button_frame = ttk.Frame(self.root, padding=15)
        button_frame.pack()

        role = self.current_user.role

        if role in ["clinician", "nurse"]:
            actions = [
                ("Retrieve Patient", self.retrieve_patient),
                ("Add Patient", self.add_patient),
                ("Remove Patient", self.remove_patient),
                ("Count Visits", self.count_visits),
                ("View Note", self.view_note),
                ("Key Statistics", self.key_statistics),
            ]
        elif role == "admin":
            actions = [
                ("Count Encounters Per Patient", self.count_encounters_per_patient),
                ("Count Encounters By Department", self.count_encounters_by_department),
                ("Monitor Provider Workload", self.monitor_provider_workload),
            ]
        elif role == "management":
            actions = [
                ("Monitor Department Revenue", self.monitor_department_revenue),
                ("Key Statistics", self.key_statistics),
            ]
        else:
            actions = []

        for i, (text, command) in enumerate(actions):
            ttk.Button(button_frame, text=text, command=command, width=35).grid(row=i, column=0, pady=5)

        ttk.Button(button_frame, text="Exit", command=self.root.destroy, width=35).grid(row=len(actions), column=0, pady=20)

        self.output = tk.Text(self.root, width=90, height=18)
        self.output.pack(padx=15, pady=10)

    def display(self, text):
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, text)

    def log_action(self, action):
        self.logger.log(self.current_user.username, self.current_user.role, action, "success")

    def retrieve_patient(self):
        patient_id = simpledialog.askstring("Retrieve Patient", "Enter Patient ID:")
        if not patient_id:
            return
        patient = self.warehouse.retrieve_patient(patient_id)
        self.log_action("retrieve_patient")
        if not patient:
            self.display(f"Patient {patient_id} not found.")
            return
        self.display("\n".join(f"{key}: {value}" for key, value in patient.items()))

    def add_patient(self):
        fields = ["patient_id", "age", "gender", "bmi", "a1c", "bp_sys", "bp_dia", "smoking"]
        patient = {}
        for field in fields:
            value = simpledialog.askstring("Add Patient", f"Enter {field}:")
            if value is None:
                return
            patient[field] = value
        result = self.warehouse.add_patient(patient)
        self.log_action("add_patient")
        self.display(result)

    def remove_patient(self):
        patient_id = simpledialog.askstring("Remove Patient", "Enter Patient ID:")
        if not patient_id:
            return
        result = self.warehouse.remove_patient(patient_id)
        self.log_action("remove_patient")
        self.display(result)

    def count_visits(self):
        date = simpledialog.askstring("Count Visits", "Enter date (YYYY-MM-DD):")
        if not date:
            return
        count = self.warehouse.count_visits_by_date(date)
        self.log_action("count_visits")
        self.display(f"Total visits on {date}: {count}")

    def view_note(self):
        patient_id = simpledialog.askstring("View Note", "Enter Patient ID:")
        if not patient_id:
            return
        date = simpledialog.askstring("View Note", "Enter date (YYYY-MM-DD):")
        if not date:
            return
        notes = self.warehouse.view_note(patient_id, date)
        self.log_action("view_note")
        if not notes:
            self.display("No notes found.")
            return
        text = ""
        for note in notes:
            text += f"Note ID: {note['note_id']}\nType: {note['note_type']}\nDate: {note['note_date']}\nText: {note['note_text']}\n\n"
        self.display(text)

    def key_statistics(self):
        self.log_action("generate_key_statistics")
        self.display(self.warehouse.key_statistics())

    def count_encounters_per_patient(self):
        self.log_action("count_encounters_per_patient")
        rows = self.warehouse.count_encounters_per_patient()
        self.display("\n".join(f"{patient}: {count}" for patient, count in rows[:50]))

    def count_encounters_by_department(self):
        self.log_action("count_encounters_by_department")
        rows = self.warehouse.count_encounters_by_department()
        self.display("\n".join(f"{department}: {count}" for department, count in rows))

    def monitor_provider_workload(self):
        self.log_action("monitor_provider_workload")
        rows = self.warehouse.monitor_provider_workload()
        self.display("\n".join(f"{provider}: {count} encounters" for provider, count in rows))

    def monitor_department_revenue(self):
        self.log_action("monitor_department_revenue")
        rows = self.warehouse.monitor_department_revenue()
        self.display("\n".join(f"{department}: ${revenue:,.2f}" for department, revenue in rows))
