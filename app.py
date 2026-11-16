import streamlit as st
from data import get_orders, get_components
from execution import selected_orders, validate_combination, create_execution
from ui import render_search, render_validation, render_job_order, render_log

st.set_page_config(page_title="JobOrder", page_icon="📋", layout="wide")

if "execution" not in st.session_state:
    st.session_state.execution = None
if "status" not in st.session_state:
    st.session_state.status = "DRAFT"
if "components" not in st.session_state:
    st.session_state.components = get_components()
if "log" not in st.session_state:
    st.session_state.log = []

with st.sidebar:
    st.title("JobOrder")
    page = st.radio("Navigation", ["Order Search", "Combined Blend", "Digital Job Order", "Execution Log"])
    st.caption("POC • sample SAP data")
    if st.session_state.execution:
        st.info(f"{st.session_state.execution['execution_id']}

{st.session_state.status}")

if page == "Order Search":
    render_search(get_orders())
elif page == "Combined Blend":
    render_validation()
elif page == "Digital Job Order":
    render_job_order()
else:
    render_log()
