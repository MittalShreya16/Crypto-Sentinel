"""
Crypto-Sentinel
"""
import streamlit as st
from agent import run_agent, get_verdict_emoji, get_risk_color

st.set_page_config(
    page_title="Crypto-Sentinel",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif; }
#MainMenu {visibility:hidden;} footer {visibility:hidden;} header {visibility:hidden;}

.stApp {
    background: #060614;
    background-image:
        radial-gradient(ellipse 600px 500px at 0% 0%, rgba(99,102,241,0.2) 0%, transparent 60%),
        radial-gradient(ellipse 500px 400px at 100% 30%, rgba(168,85,247,0.15) 0%, transparent 60%),
        radial-gradient(ellipse 400px 400px at 50% 100%, rgba(14,165,233,0.1) 0%, transparent 60%),
        radial-gradient(ellipse 300px 300px at 80% 80%, rgba(236,72,153,0.08) 0%, transparent 60%),
        linear-gradient(180deg, #060614 0%, #080820 50%, #060614 100%);
}

/* Grid overlay */
.stApp::before {
    content: '';
    position: fixed; top: 0; left: 0; width: 100%; height: 100%;
    background-image:
        linear-gradient(rgba(99,102,241,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(99,102,241,0.03) 1px, transparent 1px);
    background-size: 50px 50px;
    pointer-events: none; z-index: 0;
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background: rgba(6,6,20,0.97) !important;
    border-right: 1px solid rgba(99,102,241,0.12) !important;
}
[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
[data-testid="stSidebar"] .stButton button {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    color: #64748b !important; text-align: left !important;
    border-radius: 10px !important; box-shadow: none !important;
    font-size: 13px !important;
}
[data-testid="stSidebar"] .stButton button:hover {
    background: rgba(99,102,241,0.12) !important;
    border-color: rgba(99,102,241,0.35) !important;
    color: white !important; transform: none !important;
    box-shadow: none !important;
}

/* HERO */
.hero-outer {
    background: linear-gradient(135deg, rgba(15,12,41,0.98) 0%, rgba(48,43,99,0.95) 50%, rgba(36,36,62,0.98) 100%);
    border-radius: 28px; padding: 60px 48px 52px; text-align: center;
    margin-bottom: 28px; position: relative; overflow: hidden;
    border: 1px solid rgba(99,102,241,0.22);
    box-shadow: 0 25px 80px rgba(0,0,0,0.6), inset 0 0 100px rgba(99,102,241,0.04);
}
.hero-outer::before {
    content: ''; position: absolute; inset: 0;
    background:
        radial-gradient(ellipse 60% 80% at 15% 50%, rgba(99,102,241,0.14) 0%, transparent 60%),
        radial-gradient(ellipse 60% 80% at 85% 50%, rgba(168,85,247,0.1) 0%, transparent 60%);
}
.hero-outer::after {
    content: ''; position: absolute;
    top: 0; left: 10%; right: 10%; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(99,102,241,0.7), rgba(168,85,247,0.7), transparent);
}
.hero-badge {
    display: inline-flex; align-items: center; gap: 8px;
    background: rgba(99,102,241,0.1); border: 1px solid rgba(99,102,241,0.28);
    border-radius: 50px; padding: 8px 20px; font-size: 11px; color: #a5b4fc;
    font-weight: 600; letter-spacing: 2px; text-transform: uppercase;
    margin-bottom: 24px; position: relative; z-index: 1;
}
.live-dot {
    width: 7px; height: 7px; border-radius: 50%; background: #6366f1;
    animation: blink 1.5s ease-in-out infinite; display: inline-block;
}
@keyframes blink { 0%,100%{opacity:1;box-shadow:0 0 6px #6366f1;} 50%{opacity:0.3;box-shadow:none;} }
.hero-title {
    font-size: 3.5em; font-weight: 700; line-height: 1.08;
    letter-spacing: -2px; margin-bottom: 16px; position: relative; z-index: 1;
    background: linear-gradient(135deg, #fff 0%, #c7d2fe 40%, #a78bfa 70%, #e879f9 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.hero-sub {
    color: #475569; font-size: 1.05em; max-width: 540px;
    margin: 0 auto; line-height: 1.75; position: relative; z-index: 1;
}

/* GLASS CARD */
.glass-card {
    background: rgba(255,255,255,0.022);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 20px; padding: 28px;
    backdrop-filter: blur(20px); margin-bottom: 16px;
}
.card-label {
    font-size: 10px; font-weight: 700; color: #334155;
    text-transform: uppercase; letter-spacing: 2px; margin-bottom: 16px;
}

/* STAT CARDS — Native Streamlit columns */
.stat-block {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 18px; padding: 20px 16px;
    text-align: center; transition: all 0.2s;
    position: relative; overflow: hidden;
}
.stat-block::before {
    content: ''; position: absolute; bottom: 0; left: 0; right: 0; height: 2px;
}
.sb-p::before { background: linear-gradient(90deg, #6366f1, #8b5cf6); }
.sb-v::before { background: linear-gradient(90deg, #8b5cf6, #a855f7); }
.sb-c::before { background: linear-gradient(90deg, #0ea5e9, #38bdf8); }
.sb-pk::before { background: linear-gradient(90deg, #ec4899, #f472b6); }
.stat-icon-bg {
    width: 48px; height: 48px; border-radius: 14px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.3em; margin: 0 auto 12px;
}
.sib-p { background: rgba(99,102,241,0.18); }
.sib-v { background: rgba(168,85,247,0.18); }
.sib-c { background: rgba(14,165,233,0.18); }
.sib-pk { background: rgba(236,72,153,0.18); }
.stat-val { font-size: 1.5em; font-weight: 700; color: white; display: block; line-height: 1; }
.stat-lbl { font-size: 10px; color: #475569; text-transform: uppercase; letter-spacing: 1.5px; margin-top: 5px; display: block; }

/* MAIN BUTTON */
.stButton button {
    background: linear-gradient(135deg, #6366f1, #8b5cf6, #a855f7) !important;
    border: none !important; border-radius: 14px !important;
    color: white !important; font-weight: 600 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    box-shadow: 0 4px 20px rgba(99,102,241,0.35) !important;
    transition: all 0.2s !important;
}
.stButton button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 32px rgba(99,102,241,0.55) !important;
}

/* TEXTAREA */
.stTextArea textarea {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(99,102,241,0.25) !important;
    border-radius: 14px !important; color: #e2e8f0 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 13px !important; line-height: 1.7 !important;
}
.stTextArea textarea:focus {
    border-color: rgba(99,102,241,0.6) !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.1) !important;
}
label { color: #475569 !important; }

/* VERDICT */
.verdict-box {
    border-radius: 20px; padding: 28px; margin-bottom: 20px;
    position: relative; overflow: hidden;
}
.vb-scam { background: linear-gradient(135deg, rgba(239,68,68,0.1), transparent); border: 1px solid rgba(239,68,68,0.28); }
.vb-safe { background: linear-gradient(135deg, rgba(34,197,94,0.1), transparent); border: 1px solid rgba(34,197,94,0.28); }
.vb-warn { background: linear-gradient(135deg, rgba(234,179,8,0.1), transparent); border: 1px solid rgba(234,179,8,0.28); }
.vb-top { position: absolute; top: 0; left: 0; right: 0; height: 3px; }
.vt-scam { background: linear-gradient(90deg, #ef4444, #dc2626); }
.vt-safe { background: linear-gradient(90deg, #22c55e, #16a34a); }
.vt-warn { background: linear-gradient(90deg, #eab308, #ca8a04); }
.v-emoji { font-size: 2.8em; display: block; margin-bottom: 10px; }
.v-text { font-size: 1.5em; font-weight: 700; color: white; }
.v-meta { font-size: 12px; color: #475569; margin-top: 8px; }
.risk-chip {
    display: inline-block; padding: 3px 12px; border-radius: 50px;
    font-size: 11px; font-weight: 700; letter-spacing: 0.5px; margin-left: 10px; vertical-align: middle;
}
.rc-c { background: rgba(239,68,68,0.18); color: #f87171; border: 1px solid rgba(239,68,68,0.3); }
.rc-h { background: rgba(249,115,22,0.18); color: #fb923c; border: 1px solid rgba(249,115,22,0.3); }
.rc-m { background: rgba(234,179,8,0.18); color: #facc15; border: 1px solid rgba(234,179,8,0.3); }
.rc-l { background: rgba(34,197,94,0.18); color: #4ade80; border: 1px solid rgba(34,197,94,0.3); }

.reason-item {
    background: rgba(255,255,255,0.028); border: 1px solid rgba(255,255,255,0.06);
    border-radius: 12px; padding: 12px 14px; margin-bottom: 8px;
    font-size: 13px; color: #94a3b8; line-height: 1.6;
    display: flex; gap: 10px; align-items: flex-start;
}
.rec-block {
    background: rgba(99,102,241,0.08); border: 1px solid rgba(99,102,241,0.2);
    border-radius: 14px; padding: 14px 16px; margin-top: 14px;
}
.rec-lbl { font-size: 10px; font-weight: 700; color: #6366f1; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 6px; }
.rec-txt { font-size: 13px; color: #a5b4fc; line-height: 1.6; }

/* EMPTY STATE */
.empty-box { text-align: center; padding: 80px 20px; }
.e-icon { font-size: 3.5em; display: block; margin-bottom: 16px; opacity: 0.25; }
.e-title { font-size: 15px; font-weight: 600; color: #334155; margin-bottom: 8px; }
.e-sub { font-size: 12px; color: #1e293b; line-height: 1.6; }

/* METRIC CARD */
.metric-card {
    background: rgba(255,255,255,0.025); border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px; padding: 24px; text-align: center;
    position: relative; overflow: hidden;
}
.metric-card::before { content:''; position:absolute; top:0; left:0; right:0; height:2px; }
.mc-p::before { background: linear-gradient(90deg,#6366f1,#8b5cf6); }
.mc-r::before { background: linear-gradient(90deg,#ef4444,#dc2626); }
.mc-g::before { background: linear-gradient(90deg,#22c55e,#16a34a); }
.mc-y::before { background: linear-gradient(90deg,#eab308,#ca8a04); }
.m-num { font-size: 2.4em; font-weight: 700; color: white; display: block; }
.m-lbl { font-size: 10px; color: #475569; text-transform: uppercase; letter-spacing: 1.5px; margin-top: 4px; }

/* HISTORY */
.hist-item {
    background: rgba(255,255,255,0.025); border: 1px solid rgba(255,255,255,0.06);
    border-radius: 14px; padding: 16px 20px; margin-bottom: 8px;
    display: flex; justify-content: space-between; align-items: center; gap: 16px;
}
.hist-txt { font-size: 12px; color: #475569; font-family: 'JetBrains Mono', monospace; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 400px; }
.hist-badge { font-size: 11px; font-weight: 700; padding: 4px 12px; border-radius: 50px; white-space: nowrap; }

/* ABOUT */
.about-step {
    background: rgba(255,255,255,0.025); border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px; padding: 24px; text-align: center; transition: all 0.2s;
}
.about-step:hover { border-color: rgba(99,102,241,0.4); background: rgba(99,102,241,0.05); transform: translateY(-3px); }
.as-num {
    display: inline-flex; align-items: center; justify-content: center;
    width: 36px; height: 36px; border-radius: 50%;
    background: rgba(99,102,241,0.18); border: 1px solid rgba(99,102,241,0.3);
    font-size: 13px; font-weight: 700; color: #a5b4fc; margin-bottom: 12px;
}
.as-title { font-size: 14px; font-weight: 600; color: #e2e8f0; margin-bottom: 8px; }
.as-desc { font-size: 12px; color: #475569; line-height: 1.65; }
.feat-card {
    background: rgba(255,255,255,0.025); border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px; padding: 20px; margin-bottom: 10px;
    display: flex; gap: 16px; align-items: flex-start;
}
.fc-icon { font-size: 1.6em; flex-shrink: 0; }
.fc-title { font-size: 14px; font-weight: 600; color: #e2e8f0; margin-bottom: 4px; }
.fc-desc { font-size: 12px; color: #475569; line-height: 1.6; }

::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #060614; }
::-webkit-scrollbar-thumb { background: rgba(99,102,241,0.25); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ───────────────────────────────────────────────
if 'history' not in st.session_state:
    st.session_state.history = []
if 'page' not in st.session_state:
    st.session_state.page = "Detector"

# ── SIDEBAR ─────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:24px 0 36px">
        <div style="font-size:3em;margin-bottom:10px;filter:drop-shadow(0 0 20px rgba(99,102,241,0.6))">🛡️</div>
        <div style="font-size:1.15em;font-weight:700;color:white;letter-spacing:-0.5px">Crypto-Sentinel</div>
        <div style="font-size:10px;color:#334155;margin-top:5px;text-transform:uppercase;letter-spacing:2px">Scam Detection Agent</div>
    </div>
    """, unsafe_allow_html=True)

    for icon, name in [("🔍","Detector"),("📊","Dashboard"),("📜","History"),("ℹ️","About")]:
        if st.button(f"{icon}  {name}", key=f"nav_{name}", use_container_width=True):
            st.session_state.page = name
            st.rerun()

    st.markdown("""
    <div style="margin-top:28px;padding:14px 16px;background:rgba(99,102,241,0.06);border:1px solid rgba(99,102,241,0.12);border-radius:12px">
        <div style="font-size:10px;color:#4338ca;font-weight:700;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:10px">⚡ Powered By</div>
        <div style="font-size:12px;color:#334155;line-height:2.1">🤖 Google Gemini API<br>🔗 LangChain Agents<br>🌐 Blockchain APIs<br>🎨 Streamlit</div>
    </div>
    <div style="margin-top:20px;font-size:11px;color:#1e293b;text-align:center">
        Built by <a href="https://github.com/MittalShreya16" style="color:#4f46e5;text-decoration:none;font-weight:600">Shreya Mittal</a>
    </div>
    """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# PAGE 1 — DETECTOR
# ════════════════════════════════════════════════════════════════
if st.session_state.page == "Detector":

    # Hero section
    st.markdown("""
    <div class="hero-outer">
        <div class="hero-badge"><span class="live-dot"></span> AI-Powered Security · Live</div>
        <div class="hero-title">Detect Crypto Scams<br>Instantly</div>
        <div class="hero-sub">Paste any suspicious crypto message, wallet address, or URL. Our AI agent analyzes it in seconds using advanced LLM reasoning and blockchain intelligence.</div>
    </div>
    """, unsafe_allow_html=True)

    # ── STATS — using Streamlit columns (renders correctly!) ──
    s1, s2, s3, s4 = st.columns(4, gap="small")
    stats = [
        (s1, "sb-p", "sib-p", "🤖", "3 Tools", "AI Agents"),
        (s2, "sb-v", "sib-v", "⚡", "< 5s", "Speed"),
        (s3, "sb-c", "sib-c", "🔮", "Gemini", "LLM Model"),
        (s4, "sb-pk", "sib-pk", "🎯", "Auto", "Detection"),
    ]
    for col, sb, sib, icon, val, lbl in stats:
        with col:
            st.markdown(f"""
            <div class="stat-block {sb}">
                <div class="stat-icon-bg {sib}">{icon}</div>
                <span class="stat-val">{val}</span>
                <span class="stat-lbl">{lbl}</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='margin-bottom:20px'></div>", unsafe_allow_html=True)

    col1, col2 = st.columns([1.1, 0.9], gap="large")

    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-label">📥 Paste Suspicious Content</div>', unsafe_allow_html=True)

        user_input = st.text_area(
            "Input",
            height=160,
            placeholder="Paste here:\n• Suspicious crypto message or post\n• Wallet address (BTC / ETH / SOL / TRON)\n• Suspicious URL or link",
            label_visibility="collapsed"
        )

        c1b, c2b = st.columns([2, 1])
        with c1b:
            analyze = st.button("🔍  Analyze with AI Agent", type="primary", use_container_width=True)
        with c2b:
            if st.button("✕  Clear", use_container_width=True):
                st.rerun()

        st.markdown('<div class="card-label" style="margin-top:20px">⚡ Quick Examples</div>', unsafe_allow_html=True)
        examples = [
            ("🚨 SCAM MSG", "🚀 URGENT! Elon Musk crypto giveaway! Send 0.1 BTC get 1 BTC back! Act NOW!"),
            ("🔗 PHISH URL", "http://bitcoin-giveaway-elon2024.com/claim-reward"),
            ("👛 ETH WALLET", "0x742d35Cc6634C0532925a3b844Bc454e4438f44e"),
            ("✅ LEGIT NEWS", "Bitcoin ETF approved by SEC — milestone for institutional adoption."),
        ]
        for label, ex in examples:
            st.markdown(f'<div style="font-size:10px;color:#334155;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:5px;margin-top:10px">{label}</div>', unsafe_allow_html=True)
            if st.button(ex[:68]+("..." if len(ex)>68 else ""), key=f"ex_{label}", use_container_width=True):
                st.session_state['load_ex'] = ex
                st.rerun()

        if 'load_ex' in st.session_state:
            user_input = st.session_state.pop('load_ex')

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="glass-card" style="min-height:520px">', unsafe_allow_html=True)
        st.markdown('<div class="card-label">🛡️ AI Verdict</div>', unsafe_allow_html=True)

        if not analyze or not user_input or not user_input.strip():
            st.markdown("""
            <div class="empty-box">
                <span class="e-icon">🔐</span>
                <div class="e-title">Ready to Analyze</div>
                <div class="e-sub">Paste suspicious content on the left<br>and click Analyze to get your AI verdict</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            with st.spinner("🤖 Agent reasoning..."):
                result = run_agent(user_input.strip())
                st.session_state.history.append({
                    "input": user_input.strip()[:80],
                    "verdict": result.get("verdict","UNKNOWN"),
                    "risk": result.get("risk_level","UNKNOWN"),
                    "tool": result.get("tool_used","Agent")
                })

            verdict = result.get("verdict","UNKNOWN").upper()
            risk = result.get("risk_level","UNKNOWN").upper()
            tool = result.get("tool_used","AI Agent")
            input_type = result.get("input_type","Content")
            reasons = result.get("reasons",[])
            recommendation = result.get("recommendation","")

            if any(x in verdict for x in ["SCAM","SUSPICIOUS","CRITICAL"]):
                vcss, vtop, icon = "vb-scam", "vt-scam", "🚨"
            elif any(x in verdict for x in ["SAFE","LEGITIMATE"]):
                vcss, vtop, icon = "vb-safe", "vt-safe", "✅"
            else:
                vcss, vtop, icon = "vb-warn", "vt-warn", "⚠️"

            rcss = {"CRITICAL":"rc-c","HIGH":"rc-h","MEDIUM":"rc-m","LOW":"rc-l"}.get(risk,"rc-m")

            st.markdown(f"""
            <div class="verdict-box {vcss}">
                <div class="vb-top {vtop}"></div>
                <span class="v-emoji">{icon}</span>
                <div class="v-text">{verdict}<span class="risk-chip {rcss}">{risk}</span></div>
                <div class="v-meta">🤖 {tool} &nbsp;·&nbsp; 📋 {input_type}</div>
            </div>
            """, unsafe_allow_html=True)

            if reasons:
                st.markdown('<div class="card-label">🔍 Why We Flagged This</div>', unsafe_allow_html=True)
                for r in reasons:
                    st.markdown(f'<div class="reason-item"><span style="flex-shrink:0;margin-top:1px">⚠️</span>{r}</div>', unsafe_allow_html=True)

            if recommendation:
                st.markdown(f"""
                <div class="rec-block">
                    <div class="rec-lbl">💡 Recommendation</div>
                    <div class="rec-txt">{recommendation}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# PAGE 2 — DASHBOARD
# ════════════════════════════════════════════════════════════════
elif st.session_state.page == "Dashboard":
    st.markdown('<div style="font-size:1.8em;font-weight:700;color:white;margin-bottom:4px">📊 Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:13px;color:#334155;margin-bottom:24px">Your session overview</div>', unsafe_allow_html=True)

    h = st.session_state.history
    total = len(h)
    scams = sum(1 for x in h if any(v in x['verdict'].upper() for v in ['SCAM','SUSPICIOUS']))
    safe = sum(1 for x in h if any(v in x['verdict'].upper() for v in ['SAFE','LEGITIMATE']))

    c1,c2,c3,c4 = st.columns(4)
    for col, cls, icon, val, lbl in [
        (c1,"mc-p","🔍",total,"Total Analyzed"),
        (c2,"mc-r","🚨",scams,"Scams Found"),
        (c3,"mc-g","✅",safe,"Safe Content"),
        (c4,"mc-y","⚠️",total-scams-safe,"Unknown"),
    ]:
        with col:
            st.markdown(f'<div class="metric-card {cls}"><div style="font-size:2em;margin-bottom:8px">{icon}</div><span class="m-num">{val}</span><div class="m-lbl">{lbl}</div></div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="glass-card" style="margin-top:16px">
        <div class="card-label">🤖 Agent Tools</div>
        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:14px">
            <div style="background:rgba(99,102,241,0.07);border:1px solid rgba(99,102,241,0.15);border-radius:16px;padding:22px;text-align:center">
                <div style="font-size:2em;margin-bottom:10px">💬</div>
                <div style="font-size:13px;font-weight:600;color:#e2e8f0;margin-bottom:6px">Text Classifier</div>
                <div style="font-size:12px;color:#475569;line-height:1.6">Detects scam patterns in crypto messages using Gemini LLM reasoning</div>
            </div>
            <div style="background:rgba(168,85,247,0.07);border:1px solid rgba(168,85,247,0.15);border-radius:16px;padding:22px;text-align:center">
                <div style="font-size:2em;margin-bottom:10px">👛</div>
                <div style="font-size:13px;font-weight:600;color:#e2e8f0;margin-bottom:6px">Wallet Checker</div>
                <div style="font-size:12px;color:#475569;line-height:1.6">Validates addresses and queries blockchain APIs for suspicious activity</div>
            </div>
            <div style="background:rgba(14,165,233,0.07);border:1px solid rgba(14,165,233,0.15);border-radius:16px;padding:22px;text-align:center">
                <div style="font-size:2em;margin-bottom:10px">🔗</div>
                <div style="font-size:13px;font-weight:600;color:#e2e8f0;margin-bottom:6px">URL Analyzer</div>
                <div style="font-size:12px;color:#475569;line-height:1.6">Scans for phishing URLs and fake crypto domains using pattern analysis</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# PAGE 3 — HISTORY
# ════════════════════════════════════════════════════════════════
elif st.session_state.page == "History":
    st.markdown('<div style="font-size:1.8em;font-weight:700;color:white;margin-bottom:4px">📜 History</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:13px;color:#334155;margin-bottom:24px">All analyses from this session</div>', unsafe_allow_html=True)

    if not st.session_state.history:
        st.markdown("""
        <div class="empty-box">
            <span class="e-icon">📭</span>
            <div class="e-title">No history yet</div>
            <div class="e-sub">Go to Detector and analyze something first</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        if st.button("🗑️ Clear History"):
            st.session_state.history = []
            st.rerun()
        for i, item in enumerate(reversed(st.session_state.history)):
            v = item['verdict'].upper()
            if any(x in v for x in ['SCAM','SUSPICIOUS']):
                vc,vbg = "#f87171","rgba(239,68,68,0.15)"
            elif any(x in v for x in ['SAFE','LEGITIMATE']):
                vc,vbg = "#4ade80","rgba(34,197,94,0.15)"
            else:
                vc,vbg = "#facc15","rgba(234,179,8,0.15)"
            st.markdown(f"""
            <div class="hist-item">
                <div style="flex:1;min-width:0">
                    <div style="font-size:10px;color:#334155;text-transform:uppercase;letter-spacing:1px;margin-bottom:4px">#{len(st.session_state.history)-i} · {item['tool']}</div>
                    <div class="hist-txt">{item['input']}</div>
                </div>
                <div style="text-align:right;flex-shrink:0">
                    <div class="hist-badge" style="background:{vbg};color:{vc};border:1px solid {vc}40">{v}</div>
                    <div style="font-size:10px;color:#334155;margin-top:4px">{item['risk']} RISK</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# PAGE 4 — ABOUT
# ════════════════════════════════════════════════════════════════
elif st.session_state.page == "About":
    st.markdown('<div style="font-size:1.8em;font-weight:700;color:white;margin-bottom:4px">ℹ️ About</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:13px;color:#334155;margin-bottom:24px">How Crypto-Sentinel works</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="glass-card">
        <div class="card-label">🤖 Agent Pipeline</div>
        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px">
            <div class="about-step"><div class="as-num">1</div><div class="as-title">Input Detection</div><div class="as-desc">Classifies input as message, wallet, or URL automatically</div></div>
            <div class="about-step"><div class="as-num">2</div><div class="as-title">Tool Routing</div><div class="as-desc">Routes to Text Classifier, Wallet Checker, or URL Analyzer</div></div>
            <div class="about-step"><div class="as-num">3</div><div class="as-title">LLM Analysis</div><div class="as-desc">Gemini Pro reasons using expert security prompts</div></div>
            <div class="about-step"><div class="as-num">4</div><div class="as-title">Structured Output</div><div class="as-desc">Returns verdict, risk level, reasons, and recommendation</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    feats = [
        ("💬","Text Classifier","Analyzes crypto messages using Google Gemini LLM. Detects urgency tactics, fake giveaways, celebrity impersonation, and phishing attempts."),
        ("👛","Wallet Checker","Validates wallet formats (BTC/ETH/SOL/TRON). Queries blockchain APIs and uses LLM to detect suspicious wallet patterns."),
        ("🔗","URL Analyzer","Scans URLs for suspicious keywords, fake domains, and phishing indicators. Checks against known legitimate crypto domains."),
        ("🤖","Gemini Engine","Powered by Google Gemini Pro — uses expert-crafted security prompts for high-accuracy scam detection."),
        ("⚡","Auto Routing","Automatically detects input type — just paste and analyze. No manual selection needed."),
        ("📊","Risk System","Four-tier risk: CRITICAL → HIGH → MEDIUM → LOW with reasons and actionable advice."),
    ]
    for i,(icon,title,desc) in enumerate(feats):
        with col1 if i%2==0 else col2:
            st.markdown(f'<div class="feat-card"><div class="fc-icon">{icon}</div><div><div class="fc-title">{title}</div><div class="fc-desc">{desc}</div></div></div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="glass-card" style="text-align:center;margin-top:8px">
        <div style="font-size:12px;color:#334155;line-height:2.2">
            ⚠️ For educational purposes only. Always verify with official sources.<br>
            Built by <strong style="color:#6366f1">Shreya Mittal</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)
