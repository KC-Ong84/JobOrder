# JobOrder POC v2

Updated Streamlit POC aligned to the retained GP01 Job Order template.

## Retained SAP/header fields
Material description/code, sales or transfer order, PO number, customer batch/F.ID, GAP batch, customer, date issue, process order, density at 30C, demanded quantity and description.

## Captured shopfloor fields
Component batch, actual/adjusted amount, raw-material checker, resource, AWT, heating temperature, blending time, verification names, actual start/end timestamps, previous product/batch, flushing details, batch-label verification and remarks.

## Intentionally omitted
Date Required, Density at 15C, Packing Weight, MIN, MAX, Raw Material Sounding Quantity, Inspection Lot, Marking and Overblend.

## Deploy
- Repository: `KC-Ong84/JobOrder`
- Branch: `main`
- Main file: `app.py`

## Current persistence
This POC uses `st.session_state`. Production should store the header, components, captured execution fields and log in Snowflake.
