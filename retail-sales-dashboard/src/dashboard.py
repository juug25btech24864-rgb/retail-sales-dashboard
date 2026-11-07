"""
Retail Sales Dashboard
Reads a CSV file, calculates sales KPIs, and creates charts using Matplotlib.
Run from the project root: python src/dashboard.py
"""
from pathlib import Path
import argparse
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CSV = ROOT / "data" / "retail_sales.csv"
OUTPUT_DIR = ROOT / "outputs"

REQUIRED_COLUMNS = {
    "Order_ID", "Date", "Product", "Category", "Region",
    "Quantity", "Unit_Price", "Discount", "Payment_Method"
}

def load_data(csv_path):
    """Load and validate the retail sales CSV."""
    df = pd.read_csv(csv_path)
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"CSV is missing required columns: {', '.join(sorted(missing))}")
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    numeric = ["Quantity", "Unit_Price", "Discount"]
    for col in numeric:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna(subset=["Date"] + numeric).copy()
    df = df[(df["Quantity"] > 0) & (df["Unit_Price"] >= 0)]
    df["Revenue"] = df["Quantity"] * df["Unit_Price"] * (1 - df["Discount"].clip(0, 1))
    df["Month"] = df["Date"].dt.to_period("M").astype(str)
    return df

def format_currency(value):
    return f"₹{value:,.0f}"

def create_dashboard(df, output_dir=OUTPUT_DIR):
    """Save a 2x2 Matplotlib dashboard and a text KPI report."""
    output_dir.mkdir(parents=True, exist_ok=True)

    total_revenue = df["Revenue"].sum()
    total_orders = df["Order_ID"].nunique()
    total_units = df["Quantity"].sum()
    avg_order_value = total_revenue / total_orders if total_orders else 0

    monthly = df.groupby("Month")["Revenue"].sum().sort_index()
    category = df.groupby("Category")["Revenue"].sum().sort_values(ascending=False)
    region = df.groupby("Region")["Revenue"].sum().sort_values(ascending=False)
    payment = df.groupby("Payment_Method")["Revenue"].sum().sort_values(ascending=False)

    plt.style.use("ggplot")
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle("RETAIL SALES DASHBOARD", fontsize=20, fontweight="bold")

    axes[0, 0].plot(monthly.index, monthly.values, marker="o", linewidth=2)
    axes[0, 0].set_title("Monthly Revenue")
    axes[0, 0].set_ylabel("Revenue (₹)")
    axes[0, 0].tick_params(axis="x", rotation=45)

    axes[0, 1].bar(category.index, category.values)
    axes[0, 1].set_title("Revenue by Product Category")
    axes[0, 1].set_ylabel("Revenue (₹)")
    axes[0, 1].tick_params(axis="x", rotation=20)

    axes[1, 0].bar(region.index, region.values)
    axes[1, 0].set_title("Revenue by Region")
    axes[1, 0].set_ylabel("Revenue (₹)")

    axes[1, 1].pie(payment.values, labels=payment.index, autopct="%1.1f%%", startangle=90)
    axes[1, 1].set_title("Revenue by Payment Method")

    fig.text(
        0.5, 0.015,
        f"Total Revenue: {format_currency(total_revenue)}   |   "
        f"Orders: {total_orders:,}   |   Units Sold: {total_units:,.0f}   |   "
        f"Average Order Value: {format_currency(avg_order_value)}",
        ha="center", fontsize=11, fontweight="bold"
    )
    fig.tight_layout(rect=[0, 0.05, 1, 0.94])
    image_path = output_dir / "retail_sales_dashboard.png"
    fig.savefig(image_path, dpi=180, bbox_inches="tight")
    plt.close(fig)

    report = [
        "RETAIL SALES SUMMARY",
        "=" * 40,
        f"Total Revenue       : {format_currency(total_revenue)}",
        f"Total Orders        : {total_orders:,}",
        f"Units Sold          : {total_units:,.0f}",
        f"Average Order Value : {format_currency(avg_order_value)}",
        f"Top Category        : {category.index[0] if not category.empty else 'N/A'}",
        f"Top Region          : {region.index[0] if not region.empty else 'N/A'}",
        f"Top Payment Method  : {payment.index[0] if not payment.empty else 'N/A'}",
        "",
        "Revenue by Category:",
    ]
    report.extend([f"  {name}: {format_currency(value)}" for name, value in category.items()])
    report_path = output_dir / "sales_summary.txt"
    report_path.write_text("\\n".join(report), encoding="utf-8")
    return image_path, report_path

def main():
    parser = argparse.ArgumentParser(description="Generate a retail sales dashboard from a CSV file.")
    parser.add_argument("--csv", default=str(DEFAULT_CSV), help="Path to the input sales CSV file")
    parser.add_argument("--output", default=str(OUTPUT_DIR), help="Folder for generated dashboard files")
    args = parser.parse_args()

    try:
        df = load_data(args.csv)
        if df.empty:
            raise ValueError("No valid sales records found in the CSV.")
        image_path, report_path = create_dashboard(df, Path(args.output))
        print(f"Dashboard created: {image_path}")
        print(f"Summary report created: {report_path}")
    except (FileNotFoundError, pd.errors.EmptyDataError, ValueError) as exc:
        raise SystemExit(f"Error: {exc}")

if __name__ == "__main__":
    main()
