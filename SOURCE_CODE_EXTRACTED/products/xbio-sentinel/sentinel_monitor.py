import streamlit as st
import requests, time, pandas as pd

st.set_page_config(page_title="X-BIO Sentinel", layout="wide")
st.title("📡 X-BIO SENTINEL: Live System Monitor")

status_res = None
try:
    status_res = requests.get("http://127.0.0.1:8080/status").json()
except:
    pass

c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Core Status", "ONLINE" if status_res else "OFFLINE")
with c2:
    st.metric("Integrity", "SEI-ENFORCED" if status_res else "DISABLED")
with c3:
    st.metric("Memory Vault", "SECURED (Supabase)")

st.subheader("🚀 Active Strategic Missions")
st.table(pd.DataFrame({"Mission": ["Memory Indexing", "Hardware Sync"], "Status": ["Complete", "Ready"]}))
time.sleep(5)
st.rerun()
