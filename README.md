# 🔍 CSV Filter Tool: High-Performance CLI Data Processor

**CSV Filter Tool** is a lightweight, production-ready Command Line Interface (CLI) utility built with Python and Pandas. It is designed to bridge the gap between massive, unstructured CSV files and actionable data subsets. Whether you are auditing retail sales, analyzing Citibike trips, or cleaning customer databases, this tool provides a fast, memory-efficient way to filter and preview data without opening heavy spreadsheet applications.

---

## 🎯 Project Goal
To provide a reliable, cross-platform data engineering utility that handles schema validation, dynamic data filtering (exact and partial matches), and automated result reporting for datasets of any size.

---

## 🧬 System Architecture
The tool follows a modular "Validate-Load-Filter-Export" pipeline:

1.  **Validation Engine:** Checks file existence, POSIX path integrity, and `.csv` extension compatibility.
2.  **Ingestion Layer:** Leverages `pandas` for high-speed I/O and automatic data type inference.
3.  **Dynamic Filtering:** * **Exact Match:** Uses vectorised equality checks for strings and numeric types.
    * **Partial Match:** Implements case-insensitive `str.contains` logic for fuzzy searching.
4.  **Reporting Layer:** Provides real-time console feedback including row counts and match percentages.
5.  **Output Layer:** Supports "Dry Run" (Preview) mode or physical file serialization.



---

## 🛠️ Technical Stack
| Layer | Tools | Purpose |
| :--- | :--- | :--- |
| **Language** | Python 3.12 | Core logic and CLI execution |
| **Processing** | Pandas | High-performance data manipulation |
| **I/O Management** | Pathlib | Cross-platform (Windows/WSL/Linux) file handling |
| **CLI Framework** | Argparse | Standardized command-line argument parsing |
| **Testing** | Subprocess, OS | Automated functional test suite |

---

## 📊 Performance & Results
* **Data Agnostic:** Successfully tested across diverse schemas including Citibike (Trip data), Retail Sales (Transactional), and CRM (Customer profiles).
* **Robust Error Handling:** Automatically identifies missing columns and suggests available alternatives to the user.
* **100% Test Coverage:** Passed all 8 automated functional tests covering edge cases like numeric filtering, missing files, and case-sensitivity.
* **Efficiency:** Capable of processing 10,000+ rows with sub-second execution times.

---

## 📂 Project Structure
```text
csv-filter-tool/
├── csv_filter.py          # Main CLI application
├── test_csv_filter.py     # 8-point automated test suite
├── data/                  # Storage for input/output CSVs
├── README.md              # Project documentation
├── QUICKSTART.md          # 60-second setup guide
├── EXAMPLES.md            # Advanced use cases and command list
└── docs/                  # Technical specifications
```

---

## ⚙️ Installation & Setup

### 1. Environment Setup
```bash
# Clone the repository
git clone [https://github.com/declerke/csv-filter-tool.git](https://github.com/declerke/csv-filter-tool.git)
cd csv-filter-tool

# Install dependencies
pip install pandas
```

### 2. Basic Usage
```bash
# General syntax
python csv_filter.py [input_file] --column [col_name] --value [search_term]

# Example: Filter for 'Electronics' and preview result
python csv_filter.py data/sales.csv --column Category --value Electronics --preview
```

### 3. Run Automated Tests
To verify the tool is working correctly in your environment:
```bash
python test_csv_filter.py
```

---

## 🎓 Skills Demonstrated
* **CLI Engineering:** Building professional command-line interfaces with help menus and argument validation.
* **Cross-Platform Compatibility:** Solving Windows/WSL `cp1252` encoding and shell quoting challenges.
* **Defensive Programming:** Implementing graceful failure modes when files or columns are missing.
* **Automated Testing:** Creating a self-contained test runner that generates and cleans up its own mock data.
