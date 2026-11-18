from datetime import datetime

def selected_orders(df):
    return df[df["Select"]].copy()

def validate_combination(df, tank_capacity):
    errors=[]
    if df.empty:
        return ["Select at least one SAP order."]
    for field, label in [("Material","material"),("Formula","formulation")]:
        populated=df[field].fillna("").astype(str)
        if populated.nunique() != 1:
            errors.append(f"Selected orders do not share the same {label}.")
    if float(df["Qty (L)"].sum()) > tank_capacity:
        errors.append("Combined quantity exceeds tank capacity.")
    return errors

def create_execution(df, tank="BT01"):
    first=df.iloc[0]
    return {
        "execution_id": f"JO-{datetime.now():%Y%m%d-%H%M%S}",
        "orders": df["SAP Order"].tolist(),
        "material": first["Material"], "description": first["Description"],
        "formula": first["Formula"], "quantity_l": float(df["Qty (L)"].sum()),
        "sales_orders": sorted(df["Sales Order"].dropna().astype(str).unique().tolist()),
        "po_numbers": sorted(df["PO No."].dropna().astype(str).unique().tolist()),
        "customer": first["Customer"], "customer_batch": first["Customer Batch / F.ID"],
        "gap_batch": first["GAP Batch"], "date_issue": first["Date Issue"],
        "density_30c": float(first["Density @30C"]), "tank": tank,
    }
