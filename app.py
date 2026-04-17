import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import datetime
from intel_engine import scan_contract_safety, get_gas_advice, get_forensic_profile
from whatsapp_alerts import send_whatsapp_alert

# --- APP CONFIG & CYBER THEME CSS ---
st.set_page_config(page_title="EtherPulse Pro | Elite Sentinel", layout="wide", page_icon="⚡")

st.markdown("""
    <style>
    .main { background-color: #0b0e14; color: #00f2fe; font-family: 'Courier New', Courier, monospace; }
    [data-testid="stSidebar"] { background-color: #0d1117; border-right: 1px solid #10b981; }
    h1, h2, h3, h4, .stCaption { color: #00f2fe !important; font-family: 'Courier New', Courier, monospace; text-transform: uppercase; }
    .stCaption { color: #10b981 !important; font-size: 0.8rem; }
    .stMetric { background-color: #111419; border: 1px solid #10b981; padding: 10px 15px; border-radius: 5px; color: #00f2fe !important; }
    [data-testid="stMetricLabel"], [data-testid="stMetricValue"], [data-testid="stMetricDelta"] { color: #00f2fe !important; }
    .stTextInput>div>div>input { background-color: #0b0e14; border: 1px solid #10b981; color: #00f2fe; }
    .stButton>button { background-color: #0b0e14; border: 1px solid #10b981; color: #10b981; width: 100%; text-transform: uppercase; font-size: 0.9rem; border-radius: 3px;}
    .stButton>button:hover { border-color: #00f2fe; color: #00f2fe; }
    .info-box { background-color: rgba(16, 185, 129, 0.1); border: 1px solid #10b981; padding: 15px; border-radius: 5px; color: #00f2fe; }
    .dataframe { font-family: 'Courier New', Courier, monospace; font-size: 0.8rem; background-color: #0b0e14; border: 1px solid #10b981;}
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: [LEFT_PANEL] SENTINEL HUD ---
with st.sidebar:
    st.markdown("# ⚡ETHERPULSE")
    st.caption("ELITE SENTINEL // v5.0.0")
    st.divider()
    
    st.caption("// LINKAGE_")
    phone = st.text_input("INPUT NUMBER_ (Ex: +91999...)", placeholder="+91...")
    if st.button("EXECUTE // LINK SENTINEL"):
        if phone:
            success = send_whatsapp_alert("✅ Link Established. Sentinel is now monitoring your subnet.", phone)
            if success: st.success("TUNNEL_LINKED")

    st.divider()
    
    st.caption("// INTELLIGENCE_SCANNER_")
    addr = st.text_input("TARGET ADDRESS_", value="0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045")
    
    if addr:
        report = scan_contract_safety(addr)
        st.markdown(f"<div class='info-box'>{report}</div>", unsafe_allow_html=True)

# --- MAIN DASHBOARD: [RIGHT_PANEL] ---
head_col1, head_col2 = st.columns([4, 1])
with head_col1:
    st.markdown("### // **BLOCKCHAIN CYBER-FORENSICS & INTELLIGENCE PLATFORM**")
    st.caption("DIGITAL_GRIT // SENTINEL CORE")
with head_col2:
    st.caption("GAS")
    st.markdown("**12Gwei**")

st.divider()
advice = get_gas_advice(12)
st.markdown(f"<p style='color: #10b981;'>💡 ADVISOR: {advice}</p>", unsafe_allow_html=True)

col_radar, col_logs = st.columns([1, 1])

with col_radar:
    st.markdown("#### **FORENSIC RADAR [VISUALIZER]**")
    st.caption("// VECTOR_DNA_PROFILE")
    
    # DYNAMIC DATA FETCH
    risk_values = get_forensic_profile(addr)
    # FIX: Close the loop by adding the first value to the end of the list
    radar_data = risk_values + [risk_values[0]]
    radar_labels = ['Security Risk', 'Whale Volume', 'Bot Activity', 'DNA Integrity', 'Security Risk']

    fig = go.Figure(go.Scatterpolar(
        r=radar_data,
        theta=radar_labels,
        fill='toself',
        fillcolor='rgba(0, 242, 254, 0.2)',
        line_color='#00f2fe',
        marker=dict(size=12, color="#ffffff", line=dict(color='#00f2fe', width=2))
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], gridcolor="#10b981", color="#00f2fe", ticks=""),
            angularaxis=dict(gridcolor="#10b981", color="#10b981"),
            bgcolor="rgba(0,0,0,0)"
        ),
        showlegend=False,
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=450,
        margin=dict(l=40, r=40, t=40, b=40)
    )
    st.plotly_chart(fig, use_container_width=True)

with col_logs:
    st.markdown("#### **SENTINEL_TERMINAL [LOGS]**")
    st.caption("// SYSTEM_MESSAGES")
    now = datetime.datetime.now()
    st.code(f"""
[BOOT] EtherPulse Elite Sentinel v5.0.0...
[OK] Connection secure...
[{now.strftime("%H:%M:%S")}] Scanning public address: {addr[:10]}...
[OK] Heuristics applied.
> SYSTEM_READY
""", language="bash")
    
    st.divider()
    st.markdown("#### **EMERGENCY_ALERTS_**")
    if st.button("INITIATE // WHALE SIMULATION"):
        if phone:
            send_whatsapp_alert("🐋 WHALE ALERT: 1,500 ETH ($3.4M) detected.", phone)
            st.toast("Security Alert Broadcasted!")

# --- BOTTOM SECTION: PULSE MONITOR GRID ---
st.divider()
st.markdown("#### **LIVE PULSE MONITOR [GRID]**")
try:
    df = pd.read_csv("cleaned_data.csv")
    st.dataframe(df[['tx_hash', 'eth_value', 'gas_gwei']].tail(10), use_container_width=True, hide_index=True)
except:
    st.markdown("<p style='color: #10b981;'>// BACKUP_DATA_STREAM ACTIVE</p>", unsafe_allow_html=True)
    df_backup = pd.DataFrame({'tx_hash': ['0x74...f44e'], 'eth_value': [1.52], 'gas_gwei': [12]})
    st.dataframe(df_backup, use_container_width=True, hide_index=True)

st.divider()
st.markdown("<p style='text-align: center; color: #10b981; font-size: 0.8rem; letter-spacing: 2px;'>DEVELOPED BY AAKASH JHA // ETHERPULSE SECURITY RESEARCH</p>", unsafe_allow_html=True)