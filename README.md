# Clinical Data Warehouse Tkinter UI

## How to run

```bash
python main.py
```

If the Data folder is missing, generate the data first:

```bash
python data_generator.py
```

Move the generated CSV files into the `Data/` folder if needed.

##  Test logins

Clinician:
- username: `alice`
- password: `pass123`

Nurse:
- username: `nina`
- password: `pass201`

Admin:
- username: `dave`
- password: `pass000`

Management:
- username: `carol`
- password: `pass789`

##  Program description

This project is a Tkinter-based Clinical Data Warehouse UI. It validates user credentials, checks user roles, displays role-based actions, and allows authorized users to retrieve, add, remove, and view patient-related data. It also supports administrative and management analytics such as encounter counts, provider workload, and department revenue.

##  Project structure

```text
clinical-data-warehouse/
├── main.py
├── data_generator.py
├── requirements.txt
├── README.md
├── UML_CDW.drawio.pdf
├── Data/
│   ├── credentials.csv
│   ├── patients.csv
│   ├── providers.csv
│   ├── departments.csv
│   ├── encounters.csv
│   ├── procedures.csv
│   └── notes.csv
├── output/
│   ├── usage_log.csv
│   └── statistics_charts/
│       ├── department_revenue.png
│       ├── encounters_by_type.png
│       ├── patient_gender_distribution.png
│       └── provider_workload_top10.png
└── src/
    ├── __init__.py
    ├── users.py
    ├── warehouse.py
    ├── logger.py
    └── ui.py
```

## Features

- User authentication and role validation
- Tkinter-based graphical user interface
- Add, remove, and retrieve patient information
- View patient clinical notes
- Count patient visits
- Generate statistics and charts
- Monitor department revenue
- Monitor provider workload
- Persistent CSV file updates
- Usage statistics logging

##  UML design

Classes to include in the UML diagram:

- `User`
  - attributes: `username`, `role`
- `AuthManager`
  - attributes: `credentials_path`
  - methods: `validate`
- `UsageLogger`
  - attributes: `log_path`
  - methods: `log`
- `ClinicalDataWarehouse`
  - attributes: CSV paths and loaded data lists
  - methods: `retrieve_patient`, `add_patient`, `remove_patient`, `count_visits_by_date`, `view_note`, `key_statistics`, `monitor_provider_workload`, `monitor_department_revenue`
- `ClinicalDataWarehouseApp`
  - attributes: `root`, `auth`, `warehouse`, `logger`, `current_user`
  - methods: `show_login`, `login`, `show_menu`, and UI action methods

##  Output files

- `Data/patients.csv`: updated after adding or removing patients.
- `output/usage_log.csv`: records login attempts and user actions.


##  Key Statistics Charts
The Key Statistics button uses matplotlib to create charts in `output/statistics_charts/`. Install required packages with `pip install -r requirements.txt`.


##  Notes
- This project was developed for the HI 741 Final Project assignment.
- The application uses Python and Tkinter for the user interface.
- Patient data updates are stored persistently in CSV files.
- Usage statistics and failed login attempts are recorded in `output/usage_log.csv`.

##  Author
Venkata Sowmya Priya - HI 741 Spring 2025

##  Due Date
May 22, 2026 - 11:59 PM CT
