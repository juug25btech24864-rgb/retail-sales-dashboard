# Retail Sales Dashboard (Python + CSV + Matplotlib)

**Mini Project | Individual**

A beginner-friendly Python project that reads retail transaction data from a CSV file, calculates key sales metrics, and creates a visual dashboard using Matplotlib.

## Features
- Reads sales records from `data/retail_sales.csv` using Pandas.
- Validates required columns and cleans invalid numeric/date rows.
- Calculates revenue after discount for each transaction.
- Displays total revenue, number of orders, units sold, and average order value.
- Creates four charts:
  1. Monthly revenue trend
  2. Revenue by product category
  3. Revenue by region
  4. Revenue share by payment method
- Exports a PNG dashboard and a text summary into `outputs/`.

## Project structure
```text
retail-sales-dashboard/
├── data/
│   └── retail_sales.csv
├── outputs/                 # Generated files appear here
├── src/
│   └── dashboard.py
├── .gitignore
├── requirements.txt
└── README.md
```

## Requirements
- Python 3.9 or newer
- pandas
- matplotlib

## How to run

1. Download or clone this repository.
2. Open a terminal in the project folder.
3. (Recommended) Create and activate a virtual environment:

   **Windows**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

   **macOS / Linux**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

4. Install the libraries:
   ```bash
   pip install -r requirements.txt
   ```
5. Generate the dashboard:
   ```bash
   python src/dashboard.py
   ```

The output files will be saved in the `outputs` folder:
- `retail_sales_dashboard.png`
- `sales_summary.txt`

To use a different CSV:
```bash
python src/dashboard.py --csv path/to/your_sales.csv --output outputs
```

## CSV format
The input CSV must contain these columns:

| Column | Meaning |
|---|---|
| Order_ID | Unique transaction/order identifier |
| Date | Order date (`YYYY-MM-DD`) |
| Product | Product name |
| Category | Product category |
| Region | Sales region |
| Quantity | Units sold |
| Unit_Price | Price per unit, in rupees |
| Discount | Discount as a decimal (e.g. `0.10` means 10%) |
| Payment_Method | Payment type |

**Revenue formula:** `Quantity × Unit_Price × (1 − Discount)`

## Example observations
Run the dashboard to identify which month, category, region, and payment method contribute the most revenue. The sample dataset is synthetic and is included only for learning/demo purposes.

## GitHub upload
1. Create a new empty repository on GitHub, for example `retail-sales-dashboard`.
2. Extract this ZIP file.
3. Open a terminal inside the extracted project folder and run:

   ```bash
   git init
   git add .
   git commit -m "Add retail sales dashboard mini project"
   git branch -M main
   git remote add origin https://github.com/YOUR-USERNAME/retail-sales-dashboard.git
   git push -u origin main
   ```

4. Replace `YOUR-USERNAME` with your GitHub username.
5. Copy your repository URL and submit that link.

## Learning outcomes
- Reading and processing CSV files with Pandas
- Data cleaning and calculated columns
- Grouping and aggregating sales data
- Creating charts with Matplotlib
- Organizing and publishing a Python project with Git and GitHub
