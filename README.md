# JobOrder

Streamlit proof-of-concept for a digital blending job-order execution workflow.

## POC flow

1. Search sample released SAP orders
2. Select compatible orders
3. Create a combined JobOrder
4. Validate blend / formulation / tank capacity
5. Release a digital GP01-style job order
6. Enter batch and actual/adjustment information
7. Complete and retain an execution log for the browser session

## Repository

```text
JobOrder/
├── .streamlit/config.toml
├── app.py
├── data.py
├── execution.py
├── ui.py
├── requirements.txt
└── README.md
```

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Streamlit Community Cloud

- Repository: `KC-Ong84/JobOrder`
- Branch: `main`
- Main file path: `app.py`

## POC vs production

The POC deliberately has no Snowflake or SAP credentials. `data.py` holds sample SAP-like rows and `st.session_state` holds temporary execution state.

For the Snowflake version:

- replace `get_orders()` / `get_components()` with Snowflake queries;
- persist headers, source orders, component snapshots and logs into Snowflake tables;
- trigger controlled SAP write-back through an outbound queue consumed by Workato;
- keep SAP-derived requirement columns read-only in the UI.
