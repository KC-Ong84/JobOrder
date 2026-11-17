import streamlit as st
import pandas as pd
from datetime import datetime
from execution import selected_orders, validate_combination, create_execution

CSS = """
<style>
.block-container{padding-top:1.2rem;max-width:1500px}
.jo-title{text-align:center;color:#173b57;font-size:1.35rem;font-weight:800;padding:.5rem;border-bottom:2px solid #173b57;margin-bottom:1rem}
.field-label{font-size:.72rem;color:#667887;font-weight:700;text-transform:uppercase}
.field-value{font-size:.98rem;color:#21323f;font-weight:700;margin-bottom:.8rem}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

def render_search(orders):
    st.title("Order Search")
    st.caption("POC: search and combine released SAP process orders.")
    c1,c2,c3=st.columns([2,1,1])
    query=c1.text_input("Material / description", "SFG")
    status=c2.selectbox("Order status", ["Released","All"])
    capacity=c3.number_input("Tank capacity (L)", min_value=1000, value=15000, step=1000)
    df=orders.copy()
    if query:
        q=query.lower()
        df=df[df.apply(lambda r:q in str(r["Material"]).lower() or q in str(r["Description"]).lower(),axis=1)]
    if status != "All": df=df[df["Status"]==status]
    edited=st.data_editor(df, hide_index=True, width="stretch", disabled=[c for c in df.columns if c!="Select"], key="order_select")
    picked=selected_orders(edited)
    total=float(picked["Qty (L)"].sum()) if not picked.empty else 0
    m1,m2,m3=st.columns(3)
    m1.metric("Selected orders",len(picked)); m2.metric("Combined quantity",f"{total:,.0f} L"); m3.metric("Capacity remaining",f"{capacity-total:,.0f} L")
    errors=validate_combination(picked, capacity)
    for e in errors: st.error(e)
    if st.button("Create combined JobOrder", type="primary", disabled=bool(errors)):
        st.session_state.execution=create_execution(picked)
        st.session_state.status="DRAFT"
        st.session_state.log.append([datetime.now(),st.session_state.execution["execution_id"],"DRAFT","Created from SAP orders"])
        st.success("JobOrder created. Continue to Combined Blend.")

def render_validation():
    st.title("Combined Blend")
    e=st.session_state.execution
    if not e:
        st.warning("Create a JobOrder from Order Search first."); return
    l,r=st.columns([1.6,1])
    checks=pd.DataFrame([
        ["Blend material",e["material"],"PASS"],
        ["Formulation",e["formula"],"PASS"],
        ["Base UoM","L / KG available","PASS"],
        ["Tank capacity",f'{e["quantity_l"]:,.0f} L <= 15,000 L',"PASS"],
        ["Active assignment","None","PASS"],
    ],columns=["Check","Result","Status"])
    l.dataframe(checks,hide_index=True,width="stretch")
    with r:
        st.subheader("Execution preview")
        st.metric("Source orders",len(e["orders"])); st.metric("Total blend",f'{e["quantity_l"]:,.0f} L')
        e["tank"]=st.selectbox("Resource / Tank",["TK-12","TK-14","TK-16"])
        st.write("Orders:",", ".join(e["orders"]))
        if st.button("Release JobOrder",type="primary"):
            st.session_state.status="RELEASED"
            st.session_state.log.append([datetime.now(),e["execution_id"],"RELEASED","Released for execution"])
            st.success("Released for execution.")

def render_job_order():
    st.title("Digital Job Order")
    e=st.session_state.execution
    if not e:
        st.warning("Create a JobOrder first."); return
    st.markdown('<div class="jo-title">GULF ASIA-PACIFIC PTE LTD • BLENDING JOB ORDER (GP01)</div>',unsafe_allow_html=True)
    fields=[("Material Description",e["description"]),("Material Code",e["material"]),("Process Order No."," + ".join(e["orders"])),("GAP Batch No.","SG7A265159"),("Status",st.session_state.status),("Demanded Quantity",f'{e["quantity_l"]:,.0f} L'),("Formula",e["formula"]),("Resource / Tank",e["tank"])]
    cols=st.columns(4)
    for i,(k,v) in enumerate(fields):
        cols[i%4].markdown(f'<div class="field-label">{k}</div><div class="field-value">{v}</div>',unsafe_allow_html=True)
    st.subheader("Raw Material Charging")
    edited=st.data_editor(st.session_state.components,hide_index=True,width="stretch",disabled=["Seq","Material Code","Material Description","Amt to Add (L)","Amt to Add (KG)","Percentage (%)"],key="component_editor")
    st.session_state.components=edited
    t1,t2,t3,t4=st.columns(4)
    start=t1.text_input("Actual Start","16 Nov 08:15")
    end=t2.text_input("Actual End","")
    heat=t3.number_input("Heating Temperature °C",value=55)
    blend=t4.number_input("Blending Time (min)",value=120)
    a,b,c,d=st.columns(4)
    prev=a.text_input("Previous Batch","SG7A265148")
    flush=b.selectbox("Flushing Required",["No","Yes"])
    flushed=c.text_input("Flushed With","")
    remark=d.text_input("Remark","")
    x,y,z=st.columns([1,1,2])
    if x.button("Save",type="primary"):
        st.session_state.status="IN PROGRESS"
        st.session_state.log.append([datetime.now(),e["execution_id"],"IN PROGRESS","Execution data saved"])
        st.toast("Saved in POC session")
    if y.button("Complete"):
        st.session_state.status="COMPLETED"
        st.session_state.log.append([datetime.now(),e["execution_id"],"COMPLETED","Ready for future Workato/SAP queue"])
        st.success("Completed. Production version would write to Snowflake and optionally create the outbound Workato queue record.")
    z.download_button("Download component CSV",edited.to_csv(index=False).encode(),file_name=f'{e["execution_id"]}_components.csv',mime="text/csv")

def render_log():
    st.title("Execution Log")
    if not st.session_state.log:
        st.info("No activity yet."); return
    df=pd.DataFrame(st.session_state.log,columns=["Timestamp","JobOrder","Status","Action"])
    st.dataframe(df,hide_index=True,width="stretch")
    st.caption("POC uses Session State. Production will persist this to BLEND_EXECUTION_LOG in Snowflake.")
