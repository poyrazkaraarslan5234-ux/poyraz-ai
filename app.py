import time, socket, platform, collections
import psutil
import pandas as pd
import streamlit as st

st.set_page_config(page_title="EDEX-PY", layout="wide")

CYAN, BG = "#aacfd1", "#05080d"
st.markdown(f"""
<style>
  .stApp {{ background:{BG}; color:{CYAN}; font-family:Consolas,monospace; }}
  h1,h2,h3,p,span,label,div {{ color:{CYAN}; }}
  .panel {{ border:1px solid {CYAN}; padding:12px; margin-bottom:12px; }}
  .clock {{ font-size:42px; letter-spacing:4px; }}
  pre {{ color:{CYAN}; }}
</style>
""", unsafe_allow_html=True)

if "cpu" not in st.session_state:
    st.session_state.cpu = collections.deque([0.0] * 60, maxlen=60)
    st.session_state.ram = collections.deque([0.0] * 60, maxlen=60)

@st.fragment(run_every=1)
def dashboard():
    st.session_state.cpu.append(psutil.cpu_percent())
    st.session_state.ram.append(psutil.virtual_memory().percent)
    net = psutil.net_io_counters()

    left, mid, right = st.columns([2, 4, 2])

    with left:
        st.markdown(f"<div class='panel'>CPU {st.session_state.cpu[-1]:.0f}%</div>",
                    unsafe_allow_html=True)
        st.line_chart(pd.DataFrame({"CPU": list(st.session_state.cpu)}),
                      height=140, color=CYAN)
        st.markdown(f"<div class='panel'>RAM {st.session_state.ram[-1]:.0f}%</div>",
                    unsafe_allow_html=True)
        st.line_chart(pd.DataFrame({"RAM": list(st.session_state.ram)}),
                      height=140, color=CYAN)

    with mid:
        st.markdown("<div class='panel'><b>SİSTEM GÜNLÜĞÜ</b></div>",
                    unsafe_allow_html=True)
        procs = sorted(psutil.process_iter(["name", "cpu_percent", "memory_percent"]),
                       key=lambda p: p.info["memory_percent"] or 0, reverse=True)[:12]
        st.dataframe(pd.DataFrame([p.info for p in procs]),
                     use_container_width=True, hide_index=True)

    with right:
        st.markdown(f"<div class='panel clock'>{time.strftime('%H:%M:%S')}</div>",
                    unsafe_allow_html=True)
        st.markdown(f"""<div class='panel'><pre>
HOST : {socket.gethostname()}
OS   : {platform.system()} {platform.release()}
UP   : {int(time.time() - psutil.boot_time()) // 3600} saat
SENT : {net.bytes_sent // 1048576} MB
RECV : {net.bytes_recv // 1048576} MB
</pre></div>""", unsafe_allow_html=True)

dashboard()
