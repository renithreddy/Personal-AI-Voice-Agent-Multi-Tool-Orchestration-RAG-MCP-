"""
J.A.R.V.I.S. -- Personal AI Voice Agent
Streamlit frontend (Phase 1, Step 2 -- restyled)

New deps for this file:
    pip install psutil
    (add `psutil` to requirements.txt)

Requires streamlit >= 1.37 for st.fragment(run_every=...).
If you get an AttributeError on st.fragment, run: pip install -U streamlit
"""

import time
from collections import deque

import psutil
import requests
import streamlit as st

# --------------------------------------------------------------------------
# CONFIG
# --------------------------------------------------------------------------
BACKEND_URL = "http://localhost:8000/chat"

st.set_page_config(
    page_title="J.A.R.V.I.S.",
    page_icon="🔷",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Prime psutil's internal CPU counter so the first real reading isn't 0%.
psutil.cpu_percent(interval=None)

# Small inline line-icons (kept monochrome so they inherit the theme color)
ICON_CPU = """<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2"><rect x="6" y="6" width="12" height="12" rx="1"/><line x1="9" y1="2" x2="9" y2="6"/><line x1="15" y1="2" x2="15" y2="6"/><line x1="9" y1="18" x2="9" y2="22"/><line x1="15" y1="18" x2="15" y2="22"/><line x1="2" y1="9" x2="6" y2="9"/><line x1="2" y1="15" x2="6" y2="15"/><line x1="18" y1="9" x2="22" y2="9"/><line x1="18" y1="15" x2="22" y2="15"/></svg>"""
ICON_MEM = """<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2"><ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v6c0 1.7 3.6 3 8 3s8-1.3 8-3V5"/><path d="M4 11v6c0 1.7 3.6 3 8 3s8-1.3 8-3v-6"/></svg>"""
ICON_NET = """<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2"><polyline points="2,12 7,12 10,4 14,20 17,12 22,12"/></svg>"""
ICON_PWR = """<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2"><polygon points="13,2 3,14 11,14 9,22 21,10 13,10"/></svg>"""


# --------------------------------------------------------------------------
# THEME
# --------------------------------------------------------------------------
def inject_theme() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&family=Rajdhani:wght@400;500;600&family=Share+Tech+Mono&display=swap');

        :root {
            --bg-deep: #02060c;
            --bg-panel: #081020;
            --bg-panel-2: #0b1626;
            --accent: #2fd8ff;
            --accent-dim: #103246;
            --text-main: #d9f3ff;
            --text-muted: #5d84a0;
            --good: #3ddc91;
            --warn: #ffbd5c;
            --bad: #ff6363;
        }

        html, body, [data-testid="stAppViewContainer"] {
            background: radial-gradient(ellipse at top, #071330 0%, var(--bg-deep) 65%) !important;
            color: var(--text-main);
            font-family: 'Rajdhani', sans-serif;
        }
        #MainMenu, footer, [data-testid="stToolbar"] { visibility: hidden; }
        [data-testid="stHeader"] { background: transparent !important; }
        .block-container { padding-top: 1.6rem; }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #050c18 0%, #03070f 100%) !important;
            border-right: 1px solid var(--accent-dim);
        }

        h1, h2, h3 { font-family: 'Orbitron', sans-serif !important; letter-spacing: 1px; }
        p, span, div, label { color: var(--text-main); }

        /* ---------------- BOOT SCREEN ---------------- */
        .boot-overlay {
            position: fixed; inset: 0; z-index: 9999;
            background: radial-gradient(ellipse at center, #071330 0%, var(--bg-deep) 70%);
            display: flex; flex-direction: column; align-items: center; justify-content: center;
        }
        .boot-ring-wrap { position: relative; width: 140px; height: 140px; margin-bottom: 26px; }
        .boot-ring {
            position: absolute; inset: 0; border-radius: 50%;
            border: 2px solid rgba(47, 216, 255, 0.32);
        }
        .boot-spin { position: absolute; inset: 0; border-radius: 50%; transform-origin: 50% 50%; }
        .boot-dot {
            position: absolute; top: -4px; left: 50%; transform: translateX(-50%);
            width: 9px; height: 9px; border-radius: 50%;
            background: var(--accent);
            box-shadow: 0 0 10px 2px var(--accent);
        }
        .boot-title {
            font-family: 'Orbitron', sans-serif; font-size: 2.3rem; font-weight: 700;
            color: var(--accent); letter-spacing: 6px;
            text-shadow: 0 0 18px rgba(47, 216, 255, 0.65);
        }
        .boot-sub {
            font-family: 'Share Tech Mono', monospace; font-size: 0.72rem;
            color: var(--text-muted); letter-spacing: 3px; margin-top: 8px;
        }
        .boot-progress-wrap { width: 380px; margin-top: 32px; }
        .boot-progress-label {
            display: flex; justify-content: space-between;
            font-family: 'Share Tech Mono', monospace; font-size: 0.78rem;
            color: var(--accent); letter-spacing: 2px; margin-bottom: 6px;
        }
        .boot-progress-track { width: 100%; height: 3px; background: rgba(47, 216, 255, 0.12); border-radius: 2px; }
        .boot-progress-fill {
            height: 100%; background: var(--accent); border-radius: 2px;
            box-shadow: 0 0 8px var(--accent);
        }

        /* ---------------- NAV ICONS ---------------- */
        [data-testid="stSidebar"] .stButton button {
            background: var(--bg-panel) !important;
            border: 1px solid var(--accent-dim) !important;
            color: var(--text-main) !important;
            border-radius: 10px !important;
            font-size: 1.05rem !important;
            padding: 0.45rem 0 !important;
            transition: all 0.15s ease;
        }
        [data-testid="stSidebar"] .stButton button:hover {
            border-color: var(--accent) !important;
            box-shadow: 0 0 12px rgba(47, 216, 255, 0.35);
            color: var(--accent) !important;
        }

        /* ---------------- METRICS CARD ---------------- */
        .metrics-card {
            position: relative;
            background: linear-gradient(180deg, var(--bg-panel-2), var(--bg-panel));
            border: 1px solid var(--accent-dim);
            border-radius: 10px;
            padding: 18px 18px 14px 18px;
            margin: 6px 0 18px 0;
        }
        .metrics-card .corner { position: absolute; width: 12px; height: 12px; }
        .c-tl { top: -1px; left: -1px; border-top: 2px solid var(--accent); border-left: 2px solid var(--accent); }
        .c-tr { top: -1px; right: -1px; border-top: 2px solid var(--accent); border-right: 2px solid var(--accent); }
        .c-bl { bottom: -1px; left: -1px; border-bottom: 2px solid var(--accent); border-left: 2px solid var(--accent); }
        .c-br { bottom: -1px; right: -1px; border-bottom: 2px solid var(--accent); border-right: 2px solid var(--accent); }
        .metrics-title {
            font-family: 'Orbitron', sans-serif; font-size: 0.74rem; letter-spacing: 2px;
            color: var(--accent); margin-bottom: 14px;
        }
        .metric-row {
            display: flex; align-items: center; gap: 10px;
            font-family: 'Share Tech Mono', monospace; font-size: 0.8rem;
            color: var(--text-main); padding: 5px 0;
            border-bottom: 1px solid rgba(47, 216, 255, 0.08);
        }
        .metric-row svg { color: var(--accent); flex-shrink: 0; }
        .metric-label { flex: 1; color: var(--text-muted); letter-spacing: 1px; }
        .metric-value { font-weight: 600; }
        .metric-bars { display: flex; align-items: flex-end; gap: 3px; height: 44px; margin-top: 14px; }
        .metric-bar {
            flex: 1; min-height: 4%;
            background: linear-gradient(180deg, var(--accent), #0c4860);
            border-radius: 2px 2px 0 0;
            transition: height 0.5s ease;
        }

        /* ---------------- CHAT ---------------- */
        [data-testid="stChatMessage"] {
            background: var(--bg-panel) !important;
            border: 1px solid var(--accent-dim) !important;
            border-radius: 12px !important;
        }
        [data-testid="stChatInput"] {
            border: 1px solid var(--accent-dim) !important;
            border-radius: 12px !important;
        }
        [data-testid="stChatInput"] textarea { background: var(--bg-panel) !important; color: var(--text-main) !important; }

        .jarvis-header { display: flex; align-items: center; gap: 12px; margin-bottom: 0.2rem; }
        .status-dot {
            width: 8px; height: 8px; border-radius: 50%; background: var(--good);
            display: inline-block; box-shadow: 0 0 8px var(--good);
            animation: pulse 2s ease-in-out infinite;
        }
        @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.35; } }
        </style>
        """,
        unsafe_allow_html=True,
    )


# --------------------------------------------------------------------------
# BOOT SEQUENCE (shown once per browser session)
# --------------------------------------------------------------------------
def render_boot_sequence() -> None:
    slot = st.empty()
    steps = 50  # 0 -> 100 in increments of 2
    for i in range(steps + 1):
        pct = i * 2
        angle = pct * 7.2  # ~2 full rotations across the whole sequence
        slot.markdown(
            f"""
            <div class="boot-overlay">
              <div class="boot-ring-wrap">
                <div class="boot-ring"></div>
                <div class="boot-spin" style="transform: rotate({angle}deg);">
                  <div class="boot-dot"></div>
                </div>
              </div>
              <div class="boot-title">J.A.R.V.I.S.</div>
              <div class="boot-sub">PERSONAL&nbsp;AI&nbsp;VOICE&nbsp;AGENT</div>
              <div class="boot-progress-wrap">
                <div class="boot-progress-label"><span>INITIALIZING</span><span>{pct}%</span></div>
                <div class="boot-progress-track">
                  <div class="boot-progress-fill" style="width:{pct}%;"></div>
                </div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        time.sleep(0.045)
    time.sleep(0.3)
    slot.empty()


# --------------------------------------------------------------------------
# SIDEBAR -- branding + module nav icons
# --------------------------------------------------------------------------
def render_sidebar_header() -> None:
    st.markdown(
        '<div class="jarvis-header">'
        '<span style="font-family:\'Orbitron\',sans-serif;font-size:1.15rem;color:var(--accent);letter-spacing:2px;">J.A.R.V.I.S.</span>'
        '<span class="status-dot"></span>'
        "</div>",
        unsafe_allow_html=True,
    )

    st.caption("PERSONAL AI VOICE AGENT · ONLINE")
    st.write("")

    nav_items = [
        ("💬", "Chat", None),
        ("⛅", "Weather", "Weather tool lands in Phase 1 · Step 3"),
        ("📧", "Mail", "Gmail tool lands in Phase 1 · Step 4"),
        ("🎙️", "Voice", "Voice I/O lands in Phase 1 · Step 5"),
    ]

    cols = st.columns(4)

    for col, (icon, label, note) in zip(cols, nav_items):
        with col:
            clicked = st.button(
                icon,
                key=f"nav_{label}",
                help=label if note is None else f"{label} — {note}",
                use_container_width=True,
            )

            if clicked and note:
                st.toast(note, icon="🛰️")

    st.divider()

# --------------------------------------------------------------------------
# SIDEBAR -- live system metrics (real psutil data, auto-refreshes)
# --------------------------------------------------------------------------
@st.fragment(run_every="2s")
def render_metrics_panel() -> None:

    if "net_history" not in st.session_state:
        st.session_state.net_history = deque([4] * 24, maxlen=24)

    if "_last_net" not in st.session_state:
        st.session_state._last_net = None

    cpu = psutil.cpu_percent(interval=None)
    mem = psutil.virtual_memory().percent
    net = psutil.net_io_counters()
    now = time.time()

    prev = st.session_state._last_net

    if prev is not None:
        elapsed = max(now - prev["t"], 0.5)
        rate_mb = (
            (net.bytes_sent - prev["sent"])
            + (net.bytes_recv - prev["recv"])
        ) / elapsed / (1024 * 1024)
    else:
        rate_mb = 0.0

    st.session_state._last_net = {
        "t": now,
        "sent": net.bytes_sent,
        "recv": net.bytes_recv,
    }

    st.session_state.net_history.append(max(cpu, 4))

    if cpu < 70 and mem < 80:
        status = "OPTIMAL"
        color = "var(--good)"
    elif cpu < 90 and mem < 95:
        status = "ELEVATED"
        color = "var(--warn)"
    else:
        status = "CRITICAL"
        color = "var(--bad)"

    bars = "".join(
        f'<div class="metric-bar" style="height:{v:.0f}%;"></div>'
        for v in st.session_state.net_history
    )

    html = f"""
    <div class="metrics-card">
      <span class="corner c-tl"></span>
      <span class="corner c-tr"></span>
      <span class="corner c-bl"></span>
      <span class="corner c-br"></span>

      <div class="metrics-title">
          SYSTEM METRICS
      </div>

      <div class="metric-row">
        {ICON_CPU}
        <span class="metric-label">CPU USAGE</span>
        <span class="metric-value">{cpu:.0f}%</span>
      </div>

      <div class="metric-row">
        {ICON_MEM}
        <span class="metric-label">MEMORY</span>
        <span class="metric-value">{mem:.0f}%</span>
      </div>

      <div class="metric-row">
        {ICON_NET}
        <span class="metric-label">NETWORK</span>
        <span class="metric-value">{rate_mb:.2f} MB/s</span>
      </div>

      <div class="metric-row">
        {ICON_PWR}
        <span class="metric-label">STATUS</span>
        <span class="metric-value" style="color:{color};">
            {status}
        </span>
      </div>

      <div class="metric-bars">
        {bars}
      </div>

    </div>
    """

    st.markdown(html, unsafe_allow_html=True)
# --------------------------------------------------------------------------
# MAIN CHAT AREA
# --------------------------------------------------------------------------
def render_main_chat() -> None:
    st.markdown(
        '<div class="jarvis-header">'
        '<h1 style="margin:0;font-size:2.1rem;">J.A.R.V.I.S.</h1>'
        '<span class="status-dot"></span>'
        "</div>",
        unsafe_allow_html=True,
    )
    st.caption("Phase 1 · Text chat -- voice modules coming online soon")
    st.write("")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_input = st.chat_input("Ask me anything...")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = requests.post(BACKEND_URL, json={"message": user_input}, timeout=30)
                    response.raise_for_status()
                    reply = response.json()["reply"]
                except requests.exceptions.RequestException as exc:
                    reply = (
                        f"⚠️ Couldn't reach the backend at `{BACKEND_URL}`. "
                        f"Is `uvicorn main:app --reload` running in another terminal? ({exc})"
                    )
            st.write(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})


# --------------------------------------------------------------------------
# ENTRYPOINT
# --------------------------------------------------------------------------
def main() -> None:
    inject_theme()

    if "booted" not in st.session_state:
        st.session_state.booted = False
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if not st.session_state.booted:
        render_boot_sequence()
        st.session_state.booted = True
        st.rerun()
    else:
        with st.sidebar:
            render_sidebar_header()
            render_metrics_panel()

        render_main_chat()


main()