import pandas as pd

def get_orders():
    # Synthetic SAP-like POC data. Replace with Snowflake queries later.
    return pd.DataFrame([
        {"Select": True, "SAP Order":"11008476", "Material":"10304100100009001", "Description":"GULF HARMONY AW 68", "Qty (L)":1460.0, "Sales Order":"4020002506", "PO No.":"PO 2026-1002 (COSTA)", "Customer":"GULF OIL PANAMA", "Customer Batch / F.ID":"", "GAP Batch":"SGAA265117", "Date Issue":"2026-11-05", "Date Required":"2026-11-26", "Density @30C":0.8700, "Status":"Released", "Formula":"V03"},
        {"Select": True, "SAP Order":"11008495", "Material":"10304100100009001", "Description":"GULF HARMONY AW 68", "Qty (L)":6000.0, "Sales Order":"4020002506", "PO No.":"PO 2026-1002 (COSTA)", "Customer":"GULF OIL PANAMA", "Customer Batch / F.ID":"", "GAP Batch":"SGAA265117", "Date Issue":"2026-11-05", "Date Required":"2026-11-26", "Density @30C":0.8700, "Status":"Released", "Formula":"V03"},
        {"Select": False, "SAP Order":"11008502", "Material":"10304100100009001", "Description":"GULF HARMONY AW 68", "Qty (L)":4000.0, "Sales Order":"4020002507", "PO No.":"PO 2026-1003", "Customer":"GULF OIL PANAMA", "Customer Batch / F.ID":"", "GAP Batch":"", "Date Issue":"2026-11-06", "Date Required":"2026-11-27", "Density @30C":0.8700, "Status":"Released", "Formula":"V03"},
    ])

def get_components():
    # Columns follow the retained GP01 template. MIN, MAX and sounding qty are intentionally omitted.
    return pd.DataFrame([
        {"Seq":10,"Material Code":"10101301600107001","Material Description":"SN150 (ARAMCO PRIMA 150S)","Amt to Add (L)":3505.0,"Amt to Add (KG)":3049.0,"Percentage (%)":47.01,"UOM":"KG","Batch":"B007","Raw Material Check By":"","Actual Amount / Adjustment":3505.0},
        {"Seq":20,"Material Code":"10102300400203001","Material Description":"500N (EM)","Amt to Add (L)":2763.0,"Amt to Add (KG)":2404.0,"Percentage (%)":37.04,"UOM":"KG","Batch":"T205","Raw Material Check By":"","Actual Amount / Adjustment":2762.0},
        {"Seq":30,"Material Code":"10206303443136150","Material Description":"GA3136 - DRUM","Amt to Add (L)":160.0,"Amt to Add (KG)":160.0,"Percentage (%)":2.47,"UOM":"KG","Batch":"K38006267","Raw Material Check By":"","Actual Amount / Adjustment":160.0},
        {"Seq":40,"Material Code":"10209300342200150","Material Description":"GA2200 - DRUM","Amt to Add (L)":47.0,"Amt to Add (KG)":47.0,"Percentage (%)":0.72,"UOM":"KG","Batch":"0102849954","Raw Material Check By":"","Actual Amount / Adjustment":47.0},
        {"Seq":50,"Material Code":"10211300342130150","Material Description":"GA2130 - DRUM","Amt to Add (L)":4.0,"Amt to Add (KG)":4.0,"Percentage (%)":0.06,"UOM":"KG","Batch":"0000231754","Raw Material Check By":"","Actual Amount / Adjustment":4.0},
    ])
