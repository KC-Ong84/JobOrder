import pandas as pd


def get_orders():
    """Fully synthetic demo data. No actual SAP/customer/material/order values."""
    return pd.DataFrame([
        {"Select": True, "SAP Order": "POC100001", "Material": "FG-DEMO-001", "Description": "DEMO HYDRAULIC OIL 68", "Qty (L)": 2500.0, "Sales Order": "SO-DEMO-1001", "PO No.": "CUST-PO-DEMO-001", "Customer": "DEMO CUSTOMER A", "Customer Batch / F.ID": "CB-DEMO-001", "GAP Batch": "GB-DEMO-001", "Date Issue": "2026-11-18", "Date Required": "2026-11-20", "Density @30C": 0.8750, "Status": "Released", "Formula": "DEMO-V01"},
        {"Select": True, "SAP Order": "POC100002", "Material": "FG-DEMO-001", "Description": "DEMO HYDRAULIC OIL 68", "Qty (L)": 4500.0, "Sales Order": "SO-DEMO-1001", "PO No.": "CUST-PO-DEMO-001", "Customer": "DEMO CUSTOMER A", "Customer Batch / F.ID": "CB-DEMO-001", "GAP Batch": "GB-DEMO-001", "Date Issue": "2026-11-18", "Date Required": "2026-11-20", "Density @30C": 0.8750, "Status": "Released", "Formula": "DEMO-V01"},
        {"Select": False, "SAP Order": "POC100003", "Material": "FG-DEMO-001", "Description": "DEMO HYDRAULIC OIL 68", "Qty (L)": 3200.0, "Sales Order": "SO-DEMO-1002", "PO No.": "CUST-PO-DEMO-002", "Customer": "DEMO CUSTOMER A", "Customer Batch / F.ID": "CB-DEMO-002", "GAP Batch": "GB-DEMO-002", "Date Issue": "2026-11-18", "Date Required": "2026-11-21", "Density @30C": 0.8750, "Status": "Released", "Formula": "DEMO-V01"},
        {"Select": False, "SAP Order": "POC100004", "Material": "FG-DEMO-002", "Description": "DEMO GEAR OIL 90", "Qty (L)": 6000.0, "Sales Order": "SO-DEMO-1003", "PO No.": "CUST-PO-DEMO-003", "Customer": "DEMO CUSTOMER B", "Customer Batch / F.ID": "CB-DEMO-003", "GAP Batch": "GB-DEMO-003", "Date Issue": "2026-11-18", "Date Required": "2026-11-22", "Density @30C": 0.9050, "Status": "Released", "Formula": "DEMO-V02"},
    ])


def get_components():
    """Fully synthetic formulation/component data for the POC."""
    return pd.DataFrame([
        {"Seq": 10, "Material Code": "RM-DEMO-001", "Material Description": "DEMO BASE OIL LIGHT", "Amt to Add (L)": 4200.0, "Amt to Add (KG)": 3612.0, "Percentage (%)": 60.00, "UOM": "KG", "Batch": "BATCH-DEMO-A", "Raw Material Check By": "", "Actual Amount / Adjustment": 4200.0},
        {"Seq": 20, "Material Code": "RM-DEMO-002", "Material Description": "DEMO BASE OIL HEAVY", "Amt to Add (L)": 2450.0, "Amt to Add (KG)": 2205.0, "Percentage (%)": 35.00, "UOM": "KG", "Batch": "BATCH-DEMO-B", "Raw Material Check By": "", "Actual Amount / Adjustment": 2450.0},
        {"Seq": 30, "Material Code": "AD-DEMO-001", "Material Description": "DEMO ADDITIVE PACKAGE", "Amt to Add (L)": 350.0, "Amt to Add (KG)": 385.0, "Percentage (%)": 5.00, "UOM": "KG", "Batch": "BATCH-DEMO-C", "Raw Material Check By": "", "Actual Amount / Adjustment": 350.0},
    ])
