import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import datetime
from intel_engine import scan_contract_safety, get_gas_advice, get_forensic_profile
from whatsapp_alerts import send_whatsapp_alert

# --- APP CONFIG & CYBER THEME CSS ---
st.set_page_config(page_title="EtherPulse Pro | Elite Sentinel", layout="wide", page_icon="⚡")

# Remove standard Streamlit padding and style the terminal
st.markdown("""
    <style>
    /* Global Page Styling */
    .main { background-color: #0b0e14; color: #00f2fe; font-family: 'Courier New', Courier, monospace; }
    [data-testid="stSidebar"] { background-color: #0d1117; border-right: 1px solid #10b981; }
    
    /* Global Text and Header Styling */
    h1, h2, h3, h4, .stCaption { color: #00f2fe !important; font-family: 'Courier New', Courier, monospace; text-transform: uppercase; }
    .stCaption { color: #10b981 !important; font-size: 0.8rem; }
    
    /* Metrics Box Styling (Matching screenshot) */
    .stMetric { background-color: #111419; border: 1px solid #10b981; padding: 10px 15px; border-radius: 5px; color: #00f2fe !important; }
    [data-testid="stMetricLabel"], [data-testid="stMetricValue"], [data-testid="stMetricDelta"] { color: #00f2fe !important; }
    
    /* Input and Buttons (Terminal Style) */
    .stTextInput>div>div>input { background-color: #0b0e14; border: 1px solid #10b981; color: #00f2fe; }
    .stButton>button { background-color: #0b0e14; border: 1px solid #10b981; color: #10b981; width: 100%; text-transform: uppercase; font-size: 0.9rem; border-radius: 3px;}
    .stButton>button:hover { border-color: #00f2fe; color: #00f2fe; }
    
    /* Glassmorphism Sidebar Info Box */
    .info-box { background-color: rgba(16, 185, 129, 0.1); border: 1px solid #10b981; padding: 15px; border-radius: 5px; color: #00f2fe; }
    
    /* Custom Table Styling (Terminal Grid) */
    .dataframe { font-family: 'Courier New', Courier, monospace; font-size: 0.8rem; background-color: #0b0e14; border: 1px solid #10b981;}
    .dataframe th { background-color: #111419; color: #10b981; text-transform: uppercase;}
    .dataframe td { color: #00f2fe; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: [LEFT_PANEL] SENTINEL HUD ---
with st.sidebar:
    st.markdown("# ⚡ETHERPULSE")
    st.caption("ELITE SENTINEL // v5.0.0")
    
    # Text-log of current status
    st.markdown("---")
    st.caption("// MODULES_")
    st.markdown("- > **FORENSICS SCANNER [ACTIVE]**")
    st.markdown("- > NEURAL PULSE MONITOR [SLEEP]")
    st.markdown("- > WHALE INTELLIGENCE [LISTEN]")
    st.markdown("- > GAS ADVISOR [ONLINE]")
    
    st.divider()
    
    st.caption("// LINKAGE_")
    st.markdown("Link an encrypted WhatsApp tunnel.")
    phone = st.text_input("INPUT NUMBER_ (Ex: +91999...)", placeholder="+91...")
    if st.button("EXECUTE // LINK SENTINEL"):
        if phone:
            success = send_whatsapp_alert("✅ Link Established. Sentinel is now monitoring your subnet.", phone)
            if success: st.success("TUNNEL_LINKED")

    st.divider()
    
    # THE SCANNER INPUT
    st.caption("// INTELLIGENCE_SCANNER_")
    st.markdown("Enter target address.")
    addr = st.text_input("TARGET ADDRESS_", placeholder="0x...")
    
    if addr:
        report = scan_contract_safety(addr)
        st.markdown(f"<div class='info-box'>{report}</div>", unsafe_allow_html=True)

# --- MAIN DASHBOARD: [RIGHT_PANEL] CYBER-FORENSICS PLATFORM ---

# TOP HEADER: Minimal and precise text grid
head_col1, head_col2 = st.columns([4, 1])
with head_col1:
    st.markdown("### // **BLOCKCHAIN CYBER-FORENSICS & INTELLIGENCE PLATFORM**")
    st.caption("DIGITAL_GRIT // SENTINEL CORE")

with head_col2:
    # Minimal metrics in the corner (Matches visual density of screenshot)
    st.caption("GAS")
    st.markdown("**12Gwei**")
    st.caption("NETWORK LOAD")
    st.markdown("**LOW**")

st.divider()

# Advisor block
advice = get_gas_advice(12)
st.markdown(f"<p style='color: #10b981;'>💡 ADVISOR: {advice}</p>", unsafe_allow_html=True)

# --- MIDDLE SECTION: FORENSIC RADAR & SENTINEL LOGS ---
col_radar, col_logs = st.columns([1, 1])

with col_radar:
    st.markdown("#### **FORENSIC RADAR [VISUALIZER]**")
    st.caption("// VECTOR_DNA_PROFILE")
    
    # Get values based on input fromsidebar
    risk_values = get_forensic_profile(addr)

    # Styling the Radar chart for maximalist/experimental look (image_6.png style)
    fig = go.Figure(go.Scatterpolar(
        r=risk_values,
        theta=['Security Risk', 'Whale Volume', 'Bot Activity', 'DNA Integrity'],
        fill='toself',
        fillcolor='rgba(0, 242, 254, 0.2)', # Slight cyan fill
        line_color='#00f2fe', # Neon Cyan line
        marker=dict(size=12, color="#ffffff", line=dict(color='#00f2fe', width=2)) # Large markers with neon outline
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
        height=500,
        margin=dict(l=20, r=20, t=20, b=20)
    )

    st.plotly_chart(fig, use_container_width=True)

with col_logs:
    st.markdown("#### **SENTINEL_TERMINAL [LOGS]**")
    st.caption("// SYSTEM_MESSAGES")
    
    # Fake terminal text to match high text density of screenshot
    now = datetime.datetime.now()
    st.code(f"""
[BOOT] EtherPulse Elite Sentinel v5.0.0...
[OK] Neural Pulse Monitor...
[OK] Whale Intelligence Module...
[WARN] Network traffic baseline +12%...
[INFO] Establishing blockchain handshake...
[OK] Connection secure...
[{now.strftime("%H:%M:%S")}] Scanning public addresses...
[INFO] Monitoring [LISTEN] mode...
> SYSTEM_READY
""", language="bash")
    
    st.divider()
    
    # The Whale alert simulation button
    st.markdown("#### **EMERGENCY_ALERTS_**")
    st.caption("// WHALE_INTEL_ BROADCAST_")
    if st.button("INITIATE // WHALE SIMULATION"):
        if phone:
            send_whatsapp_alert("🐋 WHALE ALERT: 1,500 ETH ($3.4M) moved from cold storage to Exchange.", phone)
        st.toast("Security Alert Broadcasted!")
    st.caption("WARNING: This will push a real alert.")

# --- BOTTOM SECTION: PULSE MONITOR GRID ---
st.divider()
st.markdown("#### **LIVE PULSE MONITOR [GRID]**")
st.caption("// TRANSACTION_STREAM_HEAD")

# Data Loading with custom terminal style table
try:
    df = pd.read_csv("cleaned_data.csv")
    df = df[['tx_hash', 'eth_value', 'gas_gwei']] # only show relevant columns
    # Minimal formatting for the terminal grid look
    df_styled = df.tail(10).style.set_properties(**{
        'background-color': '#0b0e14',
        'color': '#00f2fe',
        'border-color': '#10b981',
        'font-family': 'Courier New'
    })
    
    st.dataframe(df.tail(10), use_container_width=True, hide_index=True)
except:
    # Emergency backup if file is missing
    st.markdown("<p style='color: #10b981;'>// BACKUP_DATA_STREAM</p>", unsafe_allow_html=True)
    df = pd.DataFrame({
        'tx_hash': ['0x742d...f44e', '0x321a...88b2', '0x992b...cc11', '0x112c...aa90'],
        'eth_value': [1.52, 450.0, 0.05, 12.4],
        'gas_gwei': [12, 15, 11, 12]
    })
    st.dataframe(df.tail(10), use_container_width=True, hide_index=True)

# Footer
st.divider()
st.markdown("<p style='text-align: center; color: #10b981; font-size: 0.8rem; letter-spacing: 2px;'>DEVELOPED BY AAKASH JHA // ETHERPULSE SECURITY RESEARCH // ALL_RIGHTS_RESERVED</p>", unsafe_allow_html=True)