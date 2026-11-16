from datetime import datetime

def selected_orders(df):
    return df[df["Select"]].copy()

def validate_combination(df, tank_capacity):
    errors=[]
    if df.empty:
        errors.append("Select at least one SAP order.")
        return errors
    if df["Material"].nunique() != 1:
        errors.append("Selected orders do not have the same blend material.")
    if df["Formula"].nunique() != 1:
        errors.append("Selected orders do not have the same formulation version.")
    if float(df["Qty (L)"].sum()) > tank_capacity:
        errors.append("Combined quantity exceeds tank capacity.")
    return errors

def create_execution(df, tank="TK-12"):
    return {
        "execution_id": f"JO-{datetime.now():%Y%m%d-%H%M%S}",
        "orders": df["SAP Order"].tolist(),
        "material": df.iloc[0]["Material"],
        "description": df.iloc[0]["Description"],
        "formula": df.iloc[0]["Formula"],
        "quantity_l": float(df["Qty (L)"].sum()),
        "tank": tank,
    }
