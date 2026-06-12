# Automated Data Cleaning & Recommendation System


## About the Project
The project involves fetching data from weather stations and analyzing it for the occurrence of anomalies.
Next, the data is quarantined, and after cleaning, it goes to the so-called Silver layer (Silver Data).
The implemented interface (UI) provides the user with intuitive system operation.
---

## Architecture and Data Flow
The data processing flow was designed based on four main zones:

* **Bronze (Raw Layer):** Here, raw data is saved in JSON format, fetched directly from the weather API.
* **Quarantine:** Isolated, critically erroneous records that did not meet the assumed rules end up in this zone. They are completely rejected from the dataset.
* **Silver (Cleaned Layer):** Data cleaned of "junk". Soft anomalies (detected using Z-Score deviations) are automatically patched - the erroneous value is replaced with a rolling average from the last 14 measurements.
* **Gold (Analytical Layer):** The destination for audit logs (Audit Trail). They document the history of anomaly occurrences and details of the actions taken by the system to repair them.

---

## Technologies
* **Language:** Python 
* **Data Processing:** Pandas, NumPy
* **Environment Variables:** python-dotenv
* **User Interface:** Streamlit (UI)
* **Environment Management:** UV
* **Infrastructure:** AWS Cloud integration (S3 / EC2) or local environment

---

## Repository Structure

```text
automated-data-cleaning-system/
├── config/                  # Configuration folder
│   ├── .env                 # Hidden file with passwords and API URL
│   ├── cleaning_rules.json  # Dictionary of hard physical validation rules
│   └── utils.py             # Helper functions and constants 
├── notebooks/               # Experiments and Jupyter environment
│   └── final_report.ipynb
├── src/                     # Main system source code
│   ├── data/                # Local file repository
│   │   ├── bronze/          # Raw data from API (divided by stations, e.g., GDN_01)
│   │   ├── quarantine/      # Rejected records
│   │   ├── silver/          # Processed and reconstructed data
│   │   └── gold/            # Repair history (Audit logs)
│   ├── expert_system/       # Rule-based logic
│   │   └── decision_engine.py  # Main script controlling the flow
│   ├── models/              # Analytical logic
│   │   ├── baseline_stats.py   # Statistical module (Z-score, rolling mean)
│   │   └── imputation_ml.py    # Anomaly patching algorithms
│   ├── pipeline/            # Data extraction and saving
│   │   ├── audit_loger.py      # Saving the history of changes
│   │   ├── ingestion.py        # Connection with the weather API
│   │   └── storage_manager.py  # I/O operations in Lakehouse layers
│   └── ui/                  # Visual interface
│       ├── constants.py
│       └── home.py             # Main Streamlit app file
├── video/                   # Multimedia materials
│   └── video.mp4
├── main.py                  # Main file to run the application 
├── pyproject.toml           # Project metadata and configuration
├── uv.lock                  # UV manager dependency lock file
└── README.md
```

---

## Instructions on How to Run the Project

We recommend using the extremely fast package manager `uv`.

**1. Clone the repository:**
```bash
git clone [https://github.com/TwojNick/automated-data-cleaning-system.git](https://github.com/Baranitto/automated-data-cleaning-system.git)
cd automated-data-cleaning-system
```

**2. Configure environment variables:**
In the `config/` folder, create a file named `.env` and fill it in with the following data:
```env
WEATHER_API_URL=enter_url_address_here
WEATHER_API_TOKEN=enter_your_token_here
```

**3. Create a virtual environment and install dependencies from the lock file:**
```bash
uv venv
uv sync
```

**4. Run the data cleaning flow (Data Pipeline):**
You can click the "Run" button in your IDE environment (e.g., PyCharm/VS Code) for the `main.py` file or run it from the terminal:
```bash
uv run python main.py
```

**5. Everything is ready, the application will automatically launch the browser with the UI to control the application**