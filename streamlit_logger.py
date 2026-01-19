
import streamlit as st
from proglog import ProgressBarLogger

# ==============================
# Custom logger for Streamlit
# ==============================
class StreamlitLogger(ProgressBarLogger):
    def __init__(self):
        super().__init__()
        self.progress_bar = st.progress(0)
        self.progress_text = st.empty()

    def bars_callback(self, bar, attr, value, old_value=None):
        try:
            total = self.bars[bar]["total"]
            pct = int((value / max(total, 1)) * 100)
        except Exception:
            pct = 0

        self.progress_text.text(f"⏳ Processing {bar}: {pct}% ({value}/{total} units)")
        self.progress_bar.progress(min(max(pct, 0), 100))