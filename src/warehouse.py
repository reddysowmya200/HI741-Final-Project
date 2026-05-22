import csv
from pathlib import Path
from collections import Counter, defaultdict

import matplotlib.pyplot as plt

class ClinicalDataWarehouse:
    def __init__(self, data_dir: str | Path):
        self.data_dir = Path(data_dir)
        self.patients_path = self.data_dir / "patients.csv"
        self.encounters_path = self.data_dir / "encounters.csv"
        self.notes_path = self.data_dir / "notes.csv"
        self.procedures_path = self.data_dir / "procedures.csv"
        self.providers_path = self.data_dir / "providers.csv"
        self.departments_path = self.data_dir / "departments.csv"

        self.patients = self._read_csv(self.patients_path)
        self.encounters = self._read_csv(self.encounters_path)
        self.notes = self._read_csv(self.notes_path)
        self.procedures = self._read_csv(self.procedures_path)
        self.providers = self._read_csv(self.providers_path)
        self.departments = self._read_csv(self.departments_path)

    def _read_csv(self, path: Path) -> list[dict]:
        with path.open(newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))

    def _write_csv(self, path: Path, rows: list[dict], fieldnames: list[str]):
        with path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    def save_patients(self):
        fieldnames = ["patient_id", "age", "gender", "bmi", "a1c", "bp_sys", "bp_dia", "smoking"]
        self._write_csv(self.patients_path, self.patients, fieldnames)

    def retrieve_patient(self, patient_id: str) -> dict | None:
        matches = [p for p in self.patients if p["patient_id"] == patient_id]
        return matches[-1] if matches else None

    def add_patient(self, patient: dict) -> str:
        required = ["patient_id", "age", "gender", "bmi", "a1c", "bp_sys", "bp_dia", "smoking"]
        clean = {key: patient.get(key, "") for key in required}
        if not clean["patient_id"]:
            return "Patient ID is required."
        self.patients.append(clean)
        self.save_patients()
        return f"Patient {clean['patient_id']} added successfully."

    def remove_patient(self, patient_id: str) -> str:
        before = len(self.patients)
        self.patients = [p for p in self.patients if p["patient_id"] != patient_id]
        if len(self.patients) == before:
            return f"Patient {patient_id} not found."
        self.save_patients()
        return f"Patient {patient_id} removed from patients.csv."

    def count_visits_by_date(self, date: str) -> int:
        return sum(1 for e in self.encounters if e["encounter_date"] == date)

    def count_encounters_per_patient(self) -> list[tuple[str, int]]:
        counts = Counter(e["patient_id"] for e in self.encounters)
        return counts.most_common()

    def count_encounters_by_department(self) -> list[tuple[str, int]]:
        dept_names = {d["department_id"]: d["name"] for d in self.departments}
        counts = Counter(e["department_id"] for e in self.encounters)
        return [(dept_names.get(dept, dept), count) for dept, count in counts.most_common()]

    def view_note(self, patient_id: str, date: str) -> list[dict]:
        return [
            n for n in self.notes
            if n["patient_id"] == patient_id and n["note_date"] == date
        ]

    def monitor_provider_workload(self) -> list[tuple[str, int]]:
        provider_names = {p["provider_id"]: p["name"] for p in self.providers}
        counts = Counter(e["provider_id"] for e in self.encounters)
        return [(provider_names.get(provider, provider), count) for provider, count in counts.most_common()]

    def monitor_department_revenue(self) -> list[tuple[str, float]]:
        encounter_to_dept = {e["encounter_id"]: e["department_id"] for e in self.encounters}
        dept_names = {d["department_id"]: d["name"] for d in self.departments}
        revenue = defaultdict(float)

        for proc in self.procedures:
            dept_id = encounter_to_dept.get(proc["encounter_id"], "Unknown")
            revenue[dept_names.get(dept_id, dept_id)] += float(proc["cost"])

        return sorted(revenue.items(), key=lambda item: item[1], reverse=True)

    def key_statistics(self) -> str:
        """Create key statistics text and save visual charts using matplotlib."""
        total_patients = len(self.patients)
        total_encounters = len(self.encounters)
        total_notes = len(self.notes)
        total_procedures = len(self.procedures)

        ages = [float(p["age"]) for p in self.patients if p.get("age") not in [None, ""]]
        bmis = [float(p["bmi"]) for p in self.patients if p.get("bmi") not in [None, ""]]
        a1c_values = [float(p["a1c"]) for p in self.patients if p.get("a1c") not in [None, ""]]

        avg_age = sum(ages) / len(ages) if ages else 0
        avg_bmi = sum(bmis) / len(bmis) if bmis else 0
        avg_a1c = sum(a1c_values) / len(a1c_values) if a1c_values else 0

        smoking_count = sum(1 for p in self.patients if str(p.get("smoking", "")).lower() == "true")
        smoking_percent = (smoking_count / total_patients) * 100 if total_patients else 0

        chart_dir = self.data_dir.parent / "output" / "statistics_charts"
        chart_dir.mkdir(parents=True, exist_ok=True)

        chart_paths = self._create_statistics_charts(chart_dir)

        chart_list = "\n".join(f"- {path}" for path in chart_paths)

        return (
            "===== KEY STATISTICS =====\n\n"
            f"Total Patients: {total_patients}\n"
            f"Total Encounters: {total_encounters}\n"
            f"Total Clinical Notes: {total_notes}\n"
            f"Total Procedures: {total_procedures}\n\n"
            f"Average Age: {avg_age:.1f}\n"
            f"Average BMI: {avg_bmi:.1f}\n"
            f"Average A1C: {avg_a1c:.1f}\n"
            f"Smoking Patients: {smoking_count} ({smoking_percent:.1f}%)\n\n"
            "Matplotlib charts were saved here:\n"
            f"{chart_list}"
        )

    def _create_statistics_charts(self, chart_dir: Path) -> list[str]:
        """Generate visual statistics charts and return the saved file paths."""
        saved_paths = []

        # Chart 1: Patient gender distribution
        gender_counts = Counter(p["gender"] for p in self.patients)
        plt.figure(figsize=(7, 5))
        plt.bar(gender_counts.keys(), gender_counts.values())
        plt.title("Patient Gender Distribution")
        plt.xlabel("Gender")
        plt.ylabel("Number of Patients")
        plt.tight_layout()
        path = chart_dir / "patient_gender_distribution.png"
        plt.savefig(path)
        plt.close()
        saved_paths.append(str(path))

        # Chart 2: Encounter type distribution
        encounter_type_counts = Counter(e["encounter_type"] for e in self.encounters)
        plt.figure(figsize=(7, 5))
        plt.bar(encounter_type_counts.keys(), encounter_type_counts.values())
        plt.title("Encounters by Type")
        plt.xlabel("Encounter Type")
        plt.ylabel("Number of Encounters")
        plt.tight_layout()
        path = chart_dir / "encounters_by_type.png"
        plt.savefig(path)
        plt.close()
        saved_paths.append(str(path))

        # Chart 3: Department revenue
        revenue_rows = self.monitor_department_revenue()
        departments = [row[0] for row in revenue_rows]
        revenues = [row[1] for row in revenue_rows]
        plt.figure(figsize=(8, 5))
        plt.bar(departments, revenues)
        plt.title("Department Revenue")
        plt.xlabel("Department")
        plt.ylabel("Total Procedure Cost ($)")
        plt.xticks(rotation=30, ha="right")
        plt.tight_layout()
        path = chart_dir / "department_revenue.png"
        plt.savefig(path)
        plt.close()
        saved_paths.append(str(path))

        # Chart 4: Top 10 provider workload
        workload_rows = self.monitor_provider_workload()[:10]
        providers = [row[0] for row in workload_rows]
        encounter_counts = [row[1] for row in workload_rows]
        plt.figure(figsize=(9, 5))
        plt.bar(providers, encounter_counts)
        plt.title("Top 10 Provider Workload")
        plt.xlabel("Provider")
        plt.ylabel("Number of Encounters")
        plt.xticks(rotation=30, ha="right")
        plt.tight_layout()
        path = chart_dir / "provider_workload_top10.png"
        plt.savefig(path)
        plt.close()
        saved_paths.append(str(path))

        return saved_paths
