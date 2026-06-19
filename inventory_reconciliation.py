import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"


def load_data():
    sku_master = pd.read_csv(DATA_DIR / "sku_master.csv")
    stock_movements = pd.read_csv(DATA_DIR / "stock_movements.csv")
    physical_count = pd.read_csv(DATA_DIR / "physical_count.csv")

    stock_movements["date"] = pd.to_datetime(stock_movements["date"])
    physical_count["date"] = pd.to_datetime(physical_count["date"])

    return sku_master, stock_movements, physical_count


def summarize_movements(stock_movements):
    movements = stock_movements.copy()

    movements["inward_qty"] = movements.apply(
        lambda row: row["quantity"]
        if row["movement_type"] == "INWARD"
        else 0,
        axis=1,
    )

    movements["sale_qty"] = movements.apply(
        lambda row: row["quantity"]
        if row["movement_type"] == "SALE"
        else 0,
        axis=1,
    )

    movements["good_return_qty"] = movements.apply(
        lambda row: row["quantity"]
        if row["movement_type"] == "RETURN" and row["condition"] == "Good"
        else 0,
        axis=1,
    )

    movements["damaged_qty"] = movements.apply(
        lambda row: row["quantity"]
        if row["movement_type"] == "DAMAGE"
        or (row["movement_type"] == "RETURN" and row["condition"] == "Damaged")
        else 0,
        axis=1,
    )

    summary = (
        movements.groupby("sku", as_index=False)
        .agg(
            inward_stock=("inward_qty", "sum"),
            outward_stock=("sale_qty", "sum"),
            good_returns=("good_return_qty", "sum"),
            damaged_stock=("damaged_qty", "sum"),
        )
    )

    return summary


def latest_physical_count(physical_count):
    sorted_count = physical_count.sort_values(["sku", "date"])
    latest = sorted_count.groupby("sku", as_index=False).tail(1)
    latest = latest[["sku", "date", "physical_stock", "counted_by", "remarks"]]
    latest = latest.rename(columns={"date": "physical_count_date"})
    return latest


def build_reconciliation():
    sku_master, stock_movements, physical_count = load_data()

    movement_summary = summarize_movements(stock_movements)
    latest_count = latest_physical_count(physical_count)

    report = sku_master.merge(movement_summary, on="sku", how="left")
    report = report.merge(latest_count, on="sku", how="left")

    numeric_cols = [
        "inward_stock",
        "outward_stock",
        "good_returns",
        "damaged_stock",
        "physical_stock",
    ]

    for col in numeric_cols:
        report[col] = report[col].fillna(0)

    report["calculated_closing_stock"] = (
        report["opening_stock"]
        + report["inward_stock"]
        + report["good_returns"]
        - report["outward_stock"]
        - report["damaged_stock"]
    )

    report["mismatch_qty"] = (
        report["physical_stock"] - report["calculated_closing_stock"]
    )

    report["mismatch_status"] = report["mismatch_qty"].apply(
        lambda x: "Mismatch" if x != 0 else "Matched"
    )

    report["low_stock_status"] = report.apply(
        lambda row: "Low Stock"
        if row["calculated_closing_stock"] <= row["min_stock"]
        else "Healthy",
        axis=1,
    )

    report["reorder_recommendation"] = report.apply(
        lambda row: row["reorder_qty"]
        if row["calculated_closing_stock"] <= row["min_stock"]
        else 0,
        axis=1,
    )

    report["stock_value_at_cost"] = (
        report["calculated_closing_stock"] * report["unit_cost"]
    )

    report["potential_sales_value"] = (
        report["calculated_closing_stock"] * report["selling_price"]
    )

    ordered_columns = [
        "sku",
        "product_name",
        "category",
        "location",
        "opening_stock",
        "inward_stock",
        "good_returns",
        "outward_stock",
        "damaged_stock",
        "calculated_closing_stock",
        "physical_stock",
        "mismatch_qty",
        "mismatch_status",
        "min_stock",
        "low_stock_status",
        "reorder_recommendation",
        "stock_value_at_cost",
        "potential_sales_value",
        "is_combo",
        "supplier",
    ]

    return report[ordered_columns]


def save_report():
    report = build_reconciliation()

    output_dir = BASE_DIR / "outputs"
    output_dir.mkdir(exist_ok=True)

    output_path = output_dir / "daily_stock_reconciliation.csv"
    report.to_csv(output_path, index=False)

    return output_path, report


if __name__ == "__main__":
    output_path, report = save_report()

    print("Daily stock reconciliation report generated successfully.")
    print(f"Output file: {output_path}")
    print()
    print(report.to_string(index=False))