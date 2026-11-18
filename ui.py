import streamlit as st
import pandas as pd
from datetime import datetime, date, time
from execution import selected_orders, validate_combination, create_execution

st.markdown("""
<style>
.block-container{padding-top:1rem;max-width:1550px}
.jo-title{text-align:center;color:#173b57;font-size:1.35rem;font-weight:800;padding:.45rem;border-bottom:2px solid #173b57;margin-bottom:.8rem}
.retained{background:#e8f4ee;padding:.55rem .8rem;border-radius:.4rem;color:#1e6b50}
.removed{background:#f5f6f7;padding:.55rem .8rem;border-radius:.4rem;color:#677783}
.sap-section-title{margin-top:.7rem;margin-bottom:.45rem;padding:.55rem .8rem;border:1px solid #d9e2e8;border-left:4px solid #173b57;background:#f5f8fa;color:#173b57;font-size:.90rem;font-weight:750;letter-spacing:.02em}
.sap-section-title span{float:right;color:#71808c;font-size:.72rem;font-weight:650}
.sap-pair{display:grid;grid-template-columns:minmax(150px,42%) minmax(0,58%);align-items:center;min-height:46px;margin-bottom:.42rem;border:1px solid #dde5ea;border-radius:6px;background:#fff;overflow:hidden}
.sap-label{align-self:stretch;display:flex;align-items:center;padding:.55rem .70rem;background:#f0f4f7;color:#4f6270;font-size:.79rem;font-weight:700;border-right:1px solid #dde5ea}
.sap-value{padding:.55rem .75rem;color:#172b3a;font-size:.93rem;font-weight:600;word-break:break-word}
</style>""", unsafe_allow_html=True)


def _log(action):
    e = st.session_state.execution
    st.session_state.log.append([datetime.now(), e["execution_id"], st.session_state.status, action])


def render_search(orders):
    st.title("Order Search")
    q = st.text_input("Material / description / process order", "")
    c1, c2 = st.columns(2)
    status = c1.selectbox("Order status", ["Released", "All"])
    capacity = c2.number_input("Tank capacity (L)", 1000, 50000, 15000, 500)
    df = orders.copy()
    if q:
        x = q.lower()
        df = df[df.apply(lambda r: any(x in str(r[c]).lower() for c in ["Material", "Description", "SAP Order"]), axis=1)]
    if status != "All":
        df = df[df["Status"] == status]
    show = ["Select", "SAP Order", "Material", "Description", "Qty (L)", "Sales Order", "Customer", "GAP Batch", "Date Required", "Status", "Formula"]
    edited = st.data_editor(df[show], hide_index=True, width="stretch", disabled=[c for c in show if c != "Select"], key="order_select")
    picked_ids = edited.loc[edited["Select"], "SAP Order"].tolist()
    picked = df[df["SAP Order"].isin(picked_ids)]
    total = float(picked["Qty (L)"].sum()) if not picked.empty else 0
    m1, m2, m3 = st.columns(3)
    m1.metric("Selected orders", len(picked)); m2.metric("Combined quantity", f"{total:,.0f} L"); m3.metric("Capacity remaining", f"{capacity-total:,.0f} L")
    errors = validate_combination(picked, capacity)
    for error in errors: st.error(error)
    if st.button("Create combined JobOrder", type="primary", disabled=bool(errors)):
        st.session_state.execution = create_execution(picked)
        st.session_state.status = "DRAFT"
        _log("Created from SAP process orders")
        st.success("Created. Continue to Combined Blend.")


def render_validation():
    st.title("Combined Blend")
    e = st.session_state.execution
    if not e:
        st.warning("Create a JobOrder first."); return
    checks = pd.DataFrame([
        ["Blend material", e["material"], "PASS"], ["Formula", e["formula"], "PASS"],
        ["Customer", e["customer"], "PASS"], ["GAP batch", e["gap_batch"] or "To be assigned", "PASS"],
        ["Tank capacity", f'{e["quantity_l"]:,.0f} L <= 15,000 L', "PASS"]], columns=["Check", "Result", "Status"])
    l, r = st.columns([1.6, 1]); l.dataframe(checks, hide_index=True, width="stretch")
    with r:
        st.metric("Source orders", len(e["orders"])); st.metric("Total blend", f'{e["quantity_l"]:,.0f} L')
        e["tank"] = st.selectbox("Resource", ["BT01", "BT02", "BT03"])
        if st.button("Release JobOrder", type="primary"):
            st.session_state.status = "RELEASED"; _log("Released for execution"); st.success("Released.")


def render_job_order():
    st.title("Digital Job Order")
    e = st.session_state.execution
    if not e:
        st.warning("Create a JobOrder first."); return
    st.markdown('<div class="jo-title">GULF ASIA-PACIFIC PTE LTD • JOB-ORDER (GP01)</div>', unsafe_allow_html=True)
    st.caption("SAP-derived fields are displayed as read-only. Shopfloor fields replace handwritten entries on the obsolete form.")

    header_rows = [
        (("Material Description", e["description"]), ("Sales Order / Transfer Order", ", ".join(e["sales_orders"]))),
        (("Material Code", e["material"]), ("PO No.", ", ".join(e["po_numbers"]))),
        (("Customer Batch No. / F.ID", e["customer_batch"] or "To be captured"), ("GAP Batch No.", e["gap_batch"] or "To be assigned")),
        (("Customer Name", e["customer"]), ("Date Issue", e["date_issue"])),
        (("Process Order No.", " + ".join(e["orders"])), ("Density @30C", f'{e["density_30c"]:.4f}')),
        (("Demanded Quantity", f'{e["quantity_l"]:,.0f} L'), ("Description", e["description"])),
    ]
    st.markdown('<div class="sap-section-title">SAP ORDER INFORMATION <span>READ ONLY</span></div>', unsafe_allow_html=True)
    for left, right in header_rows:
        left_col, right_col = st.columns(2, gap="large")
        with left_col:
            st.markdown(f'<div class="sap-pair"><div class="sap-label">{left[0]}</div><div class="sap-value">{left[1]}</div></div>', unsafe_allow_html=True)
        with right_col:
            st.markdown(f'<div class="sap-pair"><div class="sap-label">{right[0]}</div><div class="sap-value">{right[1]}</div></div>', unsafe_allow_html=True)

    st.subheader("Formulation / Raw Material Charging")
    edited = st.data_editor(st.session_state.components, hide_index=True, width="stretch",
        disabled=["Seq", "Material Code", "Material Description", "Amt to Add (L)", "Amt to Add (KG)", "Percentage (%)", "UOM"],
        column_config={"Batch": st.column_config.TextColumn(required=True), "Raw Material Check By": st.column_config.TextColumn(), "Actual Amount / Adjustment": st.column_config.NumberColumn(format="%.2f")}, key="component_editor")
    st.session_state.components = edited
    totals = pd.DataFrame([{"Material Description":"TOTAL", "Amt to Add (L)":edited["Amt to Add (L)"].sum(), "Amt to Add (KG)":edited["Amt to Add (KG)"].sum(), "Percentage (%)":edited["Percentage (%)"].sum(), "Actual Amount / Adjustment":edited["Actual Amount / Adjustment"].sum()}])
    st.dataframe(totals, hide_index=True, width="stretch")

    st.subheader("Execution Details")
    a,b,c,d = st.columns(4)
    resource = a.selectbox("Resource", ["BT01","BT02","BT03"], index=["BT01","BT02","BT03"].index(e["tank"]) if e["tank"] in ["BT01","BT02","BT03"] else 0)
    awt = b.number_input("AWT", min_value=0.0, value=0.0, step=0.1)
    heat = c.number_input("Heating Temperature (°C)", min_value=0.0, value=55.0, step=1.0)
    blend_time = d.number_input("Blending Time (minutes)", min_value=0, value=120, step=5)
    a,b,c,d = st.columns(4)
    start_date = a.date_input("Actual Start Date", value=date.today()); start_time = b.time_input("Actual Start Time", value=time(8,0)); end_date = c.date_input("Actual End Date", value=date.today()); end_time = d.time_input("Actual End Time", value=time(10,0))
    a,b,c = st.columns(3)
    heating_verified = a.text_input("Heating Temperature Verified By"); blending_verified = b.text_input("Blending Time Verified By"); batch_label_verified = c.text_input("Batch Number Verified Against Label By")

    st.subheader("Previous Batch and Flushing")
    a,b,c,d = st.columns(4)
    previous_product = a.text_input("Previous Product Blended in Tank"); previous_batch = b.text_input("Previous Batch No."); flushing_required = c.selectbox("Flushing Required", ["No","Yes"]); flushed_with = d.text_input("Flushed With", disabled=flushing_required=="No")
    a,b,c = st.columns(3)
    flushing_qty = a.number_input("Flushing Quantity", min_value=0.0, value=0.0, step=1.0, disabled=flushing_required=="No"); flushing_date = b.date_input("Flushing Date", value=date.today(), disabled=flushing_required=="No"); remark = c.text_area("Remark", height=70)
    st.markdown('<div class="retained"><b>Captured shopfloor data:</b> component batch, actual/adjusted quantity, raw material checker, resource, AWT, heating temperature, blending time, verification names, start/end timestamps, previous product/batch, flushing details and remarks.</div>', unsafe_allow_html=True)

    save_payload = {"resource":resource,"awt":awt,"heating_temperature":heat,"blending_time_minutes":blend_time,"actual_start":f"{start_date} {start_time}","actual_end":f"{end_date} {end_time}","heating_verified_by":heating_verified,"blending_verified_by":blending_verified,"batch_label_verified_by":batch_label_verified,"previous_product":previous_product,"previous_batch":previous_batch,"flushing_required":flushing_required,"flushed_with":flushed_with,"flushing_quantity":flushing_qty,"flushing_date":str(flushing_date),"remark":remark}
    x,y,z = st.columns([1,1,2])
    if x.button("Save JobOrder", type="primary"):
        st.session_state.order_capture = save_payload; st.session_state.status = "IN PROGRESS"; _log("JobOrder fields saved in POC session"); st.success("Saved in current POC session.")
    if y.button("Complete JobOrder"):
        st.session_state.order_capture = save_payload; st.session_state.status = "COMPLETED"; _log("Completed and ready for Snowflake persistence / Workato queue"); st.success("Completed.")
    export = edited.copy(); export["JobOrder"] = e["execution_id"]
    z.download_button("Download Component Record", export.to_csv(index=False).encode(), file_name=f'{e["execution_id"]}_components.csv', mime="text/csv")


def render_log():
    st.title("Execution Log")
    if not st.session_state.log:
        st.info("No activity yet."); return
    st.dataframe(pd.DataFrame(st.session_state.log, columns=["Timestamp","JobOrder","Status","Action"]), hide_index=True, width="stretch")
    if st.session_state.order_capture:
        st.subheader("Latest Captured Order Fields"); st.json(st.session_state.order_capture)
    st.caption("POC persistence is Session State only. Production should commit these values to Snowflake tables.")
