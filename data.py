import pandas as pd

def get_orders():
    # POC only. Replace this function with a Snowflake query later.
    return pd.DataFrame([
        {"Select": True, "SAP Order":"11008476", "Material":"SFG-008921", "Description":"SFG-10W40 AW46", "Qty (L)":1460.0, "Date":"2026-11-16", "Status":"Released", "Formula":"V03"},
        {"Select": True, "SAP Order":"11008495", "Material":"SFG-008921", "Description":"SFGA1-10W40 AW46", "Qty (L)":6000.0, "Date":"2026-11-16", "Status":"Released", "Formula":"V03"},
        {"Select": False, "SAP Order":"11008502", "Material":"SFG-008921", "Description":"SFGB1-10W40 AW46", "Qty (L)":4000.0, "Date":"2026-11-17", "Status":"Released", "Formula":"V03"},
        {"Select": False, "SAP Order":"11008511", "Material":"SFG-009114", "Description":"SFGC AW 68", "Qty (L)":8500.0, "Date":"2026-11-16", "Status":"Released", "Formula":"V02"},
    ])

def get_components():
    return pd.DataFrame([
        {"Seq":10,"Material Code":"RM-410001","Material Description":"Base Oil 150N","Amt to Add (L)":4600.0,"Amt to Add (KG)":3970.0,"Percentage (%)":61.66,"Batch":"","Actual / Adjustment":0.0},
        {"Seq":20,"Material Code":"RM-410002","Material Description":"Base Oil 500N","Amt to Add (L)":2300.0,"Amt to Add (KG)":2025.0,"Percentage (%)":30.83,"Batch":"","Actual / Adjustment":0.0},
        {"Seq":30,"Material Code":"AD-510010","Material Description":"Additive Package","Amt to Add (L)":560.0,"Amt to Add (KG)":515.0,"Percentage (%)":7.51,"Batch":"","Actual / Adjustment":0.0},
    ])
