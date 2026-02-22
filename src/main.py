import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import os
import json
import html as _h
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent.parent / ".env")
except ImportError:
    pass

from styles import get_theme_colors, get_main_css, get_nav_css
from analytics_page import render_analytics_page
from forecast_page import render_forecast_page
from about_page import render_about_page
from health_regions import generate_sample_entities, create_globe_html, create_home_globe_html

# ── Databricks Genie Configuration ────────────────────────────────────────────
DATABRICKS_HOST  = os.environ.get("DATABRICKS_HOST", "")
DATABRICKS_TOKEN = os.environ.get("DATABRICKS_TOKEN", "")
GENIE_SPACE_ID   = os.environ.get("GENIE_SPACE_ID", "")

# ── Page configuration ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Insight for Impact",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Session state ─────────────────────────────────────────────────────────────
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'

# Apply theme CSS (re-evaluated on every rerun so theme changes take effect)
theme_colors = get_theme_colors(st.session_state.theme)
st.markdown(get_main_css(theme_colors), unsafe_allow_html=True)


# ── Genie Python-side API helpers ─────────────────────────────────────────────

def _genie_call(message: str, conversation_id):
    """
    Call the Databricks Genie API from Python (server-side, no CORS).
    Returns (response_html: str, conversation_id: str).
    """
    import requests as _rq, time as _t

    if not DATABRICKS_HOST or not DATABRICKS_TOKEN or not GENIE_SPACE_ID:
        raise ValueError("Databricks credentials not configured. Check your .env file.")

    hdrs = {
        "Authorization": f"Bearer {DATABRICKS_TOKEN}",
        "Content-Type": "application/json",
    }
    base = f"https://{DATABRICKS_HOST}/api/2.0/genie/spaces/{GENIE_SPACE_ID}"

    if conversation_id is None:
        # POST .../start-conversation → { conversation: {id}, message: {id, status} }
        r = _rq.post(f"{base}/start-conversation", headers=hdrs,
                     json={"content": message}, timeout=30)
        r.raise_for_status()
        d = r.json()
        conversation_id = d["conversation"]["id"]
        msg_id = d["message"]["id"]
    else:
        # POST .../conversations/{id}/messages → message object {id, status}
        r = _rq.post(f"{base}/conversations/{conversation_id}/messages",
                     headers=hdrs, json={"content": message}, timeout=30)
        r.raise_for_status()
        d = r.json()
        msg_id = d["id"]

    # Poll GET .../messages/{msg_id} until COMPLETED
    poll_url = f"{base}/conversations/{conversation_id}/messages/{msg_id}"
    for _ in range(90):
        _t.sleep(2)
        pr = _rq.get(poll_url, headers=hdrs, timeout=30)
        pr.raise_for_status()
        m = pr.json()
        if m["status"] == "COMPLETED":
            return _parse_genie_resp(m), conversation_id
        if m["status"] == "FAILED":
            raise RuntimeError(m.get("error") or "Genie processing failed.")

    raise TimeoutError("Genie timed out after 3 minutes. Please retry.")


def _parse_genie_resp(msg: dict) -> str:
    """Convert a COMPLETED Genie message's attachments into display HTML."""
    attachments = msg.get("attachments") or []
    if not attachments:
        return ("I analyzed your query but found no results. "
                "Try asking about a specific country, sector, or funding metric.")

    parts = []
    for att in attachments:
        # ── Text answer ──────────────────────────────────────────────────────
        text_content = (att.get("text") or {}).get("content")
        if text_content:
            parts.append(_h.escape(text_content).replace("\n", "<br>"))

        # ── Generated SQL / query description ────────────────────────────────
        query = att.get("query") or {}
        if query.get("description"):
            parts.append(f'<em>&#128202;&nbsp;{_h.escape(query["description"])}</em>')
        if query.get("query"):
            parts.append(f'<div class="sqlblk">{_h.escape(query["query"])}</div>')

        # ── Table data ────────────────────────────────────────────────────────
        table = att.get("table")
        if table:
            tbl_html = _table_to_html(table)
            if tbl_html:
                parts.append(tbl_html)

    return "<br>".join(parts) if parts else "Analysis complete."


def _table_to_html(tbl) -> str:
    """Render a Genie table attachment as a styled HTML table."""
    try:
        cols = tbl.get("columns") or []
        rows = tbl.get("rows") or []
        if not cols or not rows:
            return ""

        col_names = [
            c.get("name", str(c)) if isinstance(c, dict) else str(c)
            for c in cols
        ]
        th = "".join(f"<th>{_h.escape(n)}</th>" for n in col_names)

        tbody = []
        for row in rows[:25]:
            if isinstance(row, dict):
                vals = row.get("values") or list(row.values())
            else:
                vals = list(row) if hasattr(row, "__iter__") else [str(row)]
            td = "".join(
                f"<td>{_h.escape(str(v)) if v is not None else ''}</td>"
                for v in vals
            )
            tbody.append(f"<tr>{td}</tr>")

        if len(rows) > 25:
            tbody.append(
                f'<tr><td colspan="{len(col_names)}" '
                f'style="color:#64748b;text-align:center;font-size:0.68rem;">'
                f"&hellip;&nbsp;{len(rows) - 25} more rows</td></tr>"
            )

        return (
            '<div class="genie-tbl-wrap">'
            '<table class="genie-tbl">'
            f"<thead><tr>{th}</tr></thead>"
            f"<tbody>{''.join(tbody)}</tbody>"
            "</table></div>"
        )
    except Exception:
        return ""


# ── Genie Chatbot Widget ──────────────────────────────────────────────────────

def render_genie_chatbot():
    """
    Floating Genie chat widget.
    - All Genie API calls run server-side in Python (avoids browser CORS).
    - A CSS-hidden Streamlit form captures the user's message and triggers a rerun.
    - The JS widget handles display only; it triggers the hidden form on send.
    - Chat history is stored in st.session_state and baked into the HTML on every render.
    """
    # ── Session state ─────────────────────────────────────────────────────────
    if "genie_history" not in st.session_state:
        st.session_state.genie_history = []
    if "genie_conv_id" not in st.session_state:
        st.session_state.genie_conv_id = None

    # ── Process any pending message (blocking Python API call, no CORS) ──────
    pending = st.session_state.pop("genie_pending_msg", None)
    if pending:
        st.session_state.genie_history.append({
            "role": "user",
            "html": _h.escape(pending).replace("\n", "<br>"),
            "err": False,
        })
        with st.spinner("Genie is analyzing your query…"):
            try:
                resp_html, conv_id = _genie_call(pending, st.session_state.genie_conv_id)
                st.session_state.genie_conv_id = conv_id
                st.session_state.genie_history.append(
                    {"role": "bot", "html": resp_html, "err": False}
                )
            except Exception as exc:
                st.session_state.genie_history.append({
                    "role": "bot",
                    "html": f"&#9888;&nbsp;{_h.escape(str(exc))}",
                    "err": True,
                })

    # ── Hidden Streamlit form (offscreen via CSS) ─────────────────────────────
    # JS finds this input by placeholder and triggers it when the user sends.
    st.markdown("""
<style>
[data-testid="stForm"]:has(input[placeholder="__genie__"]) {
    position:fixed!important;left:-9999px!important;top:0!important;
    width:1px!important;height:1px!important;overflow:hidden!important;
    opacity:0!important;
}
[data-testid="stForm"]:has(input[placeholder="__genie__"]) button,
[data-testid="stForm"]:has(input[placeholder="__genie__"]) input {
    pointer-events:auto!important;
}
</style>""", unsafe_allow_html=True)

    with st.form("__genie_capture__", clear_on_submit=True):
        captured = st.text_input(
            "genie", placeholder="__genie__",
            label_visibility="collapsed", key="genie_capture_input"
        )
        do_send = st.form_submit_button("send")

    if do_send and captured.strip():
        st.session_state.genie_pending_msg = captured.strip()
        st.rerun()

    # ── Build messages HTML from Python session state ─────────────────────────
    history_html = ""
    for msg in st.session_state.genie_history:
        role      = msg.get("role", "bot")
        content   = msg.get("html", "")
        err_class = " gerr" if msg.get("err") else ""
        ico       = "&#9658;" if role == "user" else "&#9672;"
        history_html += (
            f'<div class="gmsg {role}">'
            f'<div class="gmsg-ico">{ico}</div>'
            f'<div class="gbubble{err_class}">{content}</div>'
            f"</div>"
        )

    # ── CSS ───────────────────────────────────────────────────────────────────
    css_str = """
  #genie-widget {
    position: fixed;
    bottom: 28px;
    right: 28px;
    z-index: 2147483647;
    font-family: 'Courier New', Courier, monospace;
  }
  #genie-toggle {
    display: flex;
    align-items: center;
    gap: 10px;
    background: linear-gradient(135deg, #0d1f0d 0%, #0a1a1f 100%);
    border: 1.5px solid rgba(74,222,128,0.65);
    border-radius: 34px;
    padding: 14px 24px 14px 18px;
    cursor: pointer;
    color: #4ade80;
    font-size: 0.9rem;
    font-weight: 700;
    letter-spacing: 0.13em;
    text-transform: uppercase;
    box-shadow: 0 0 28px rgba(74,222,128,0.25), 0 6px 28px rgba(0,0,0,0.7);
    transition: all 0.25s ease;
    user-select: none;
    outline: none;
  }
  #genie-toggle:hover {
    background: linear-gradient(135deg, #0f2a0f 0%, #0a2030 100%);
    border-color: rgba(74,222,128,0.9);
    box-shadow: 0 0 40px rgba(74,222,128,0.38), 0 8px 36px rgba(0,0,0,0.8);
    transform: translateY(-2px);
  }
  .genie-btn-dot {
    width: 10px; height: 10px; background: #4ade80; border-radius: 50%;
    box-shadow: 0 0 9px #4ade80; animation: gpulse 2s infinite; flex-shrink: 0;
  }
  @keyframes gpulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%       { opacity: 0.45; transform: scale(0.72); }
  }
  #genie-panel {
    display: none; flex-direction: column;
    width: 490px; height: 590px;
    background: rgba(10,14,26,0.98);
    border: 1px solid rgba(74,222,128,0.32); border-radius: 18px;
    overflow: hidden;
    box-shadow: 0 0 52px rgba(74,222,128,0.15), 0 28px 72px rgba(0,0,0,0.88);
    margin-bottom: 16px; animation: gslide 0.28s ease; position: relative;
  }
  #genie-panel.open { display: flex; }
  @keyframes gslide {
    from { opacity: 0; transform: translateY(22px); }
    to   { opacity: 1; transform: translateY(0); }
  }
  #genie-header {
    display: flex; align-items: center; justify-content: space-between;
    padding: 17px 19px 15px;
    background: linear-gradient(135deg, rgba(13,20,36,0.99) 0%, rgba(10,26,20,0.99) 100%);
    border-bottom: 1px solid rgba(74,222,128,0.18); flex-shrink: 0;
  }
  .ghdr-left { display: flex; align-items: center; gap: 12px; }
  .gavatar {
    width: 38px; height: 38px;
    background: linear-gradient(135deg, #0d3321, #0a2030);
    border: 1px solid rgba(74,222,128,0.55); border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 19px; box-shadow: 0 0 14px rgba(74,222,128,0.24); flex-shrink: 0;
  }
  .gtname { color: #e2e8f0; font-size: 0.9rem; font-weight: 700; letter-spacing: 0.1em; display: block; }
  .gtsub  { color: #4ade80; font-size: 0.68rem; letter-spacing: 0.07em; opacity: 0.82; display: block; margin-top: 1px; }
  .ghdr-status { width: 8px; height: 8px; background: #4ade80; border-radius: 50%; box-shadow: 0 0 8px #4ade80; animation: gpulse 2s infinite; }
  #genie-closebtn {
    background: none; border: none; color: #475569; cursor: pointer;
    font-size: 1.18rem; padding: 3px 7px; border-radius: 5px; line-height: 1;
    transition: color 0.2s; outline: none; margin-left: 8px;
  }
  #genie-closebtn:hover { color: #e2e8f0; }
  #genie-prompts {
    display: flex; flex-wrap: wrap; gap: 7px; padding: 12px 17px;
    border-bottom: 1px solid rgba(148,163,184,0.07); flex-shrink: 0;
  }
  .gchip {
    background: rgba(74,222,128,0.07); border: 1px solid rgba(74,222,128,0.22);
    border-radius: 22px; padding: 5px 12px; font-size: 0.67rem; color: #94a3b8;
    cursor: pointer; letter-spacing: 0.04em; transition: all 0.2s; white-space: nowrap;
    font-family: 'Courier New', Courier, monospace;
  }
  .gchip:hover { background: rgba(74,222,128,0.15); border-color: rgba(74,222,128,0.52); color: #4ade80; }
  #genie-messages {
    flex: 1; overflow-y: auto; padding: 17px;
    display: flex; flex-direction: column; gap: 14px;
    scrollbar-width: thin; scrollbar-color: rgba(74,222,128,0.18) transparent;
  }
  #genie-messages::-webkit-scrollbar { width: 4px; }
  #genie-messages::-webkit-scrollbar-track { background: transparent; }
  #genie-messages::-webkit-scrollbar-thumb { background: rgba(74,222,128,0.2); border-radius: 2px; }
  .gmsg { display: flex; gap: 9px; max-width: 93%; }
  .gmsg.user { align-self: flex-end; flex-direction: row-reverse; }
  .gmsg.bot  { align-self: flex-start; }
  .gmsg-ico {
    width: 27px; height: 27px; border-radius: 7px; flex-shrink: 0;
    display: flex; align-items: center; justify-content: center;
    font-size: 13px; margin-top: 2px;
  }
  .gmsg.bot  .gmsg-ico { background: linear-gradient(135deg,#0d3321,#0a2030); border: 1px solid rgba(74,222,128,0.38); color: #4ade80; }
  .gmsg.user .gmsg-ico { background: rgba(74,222,128,0.13); border: 1px solid rgba(74,222,128,0.32); color: #4ade80; }
  .gbubble { padding: 10px 14px; border-radius: 11px; font-size: 0.82rem; line-height: 1.58; max-width: 100%; word-break: break-word; }
  .gmsg.bot  .gbubble { background: rgba(15,25,45,0.93); border: 1px solid rgba(74,222,128,0.12); color: #cbd5e1; }
  .gmsg.user .gbubble { background: rgba(74,222,128,0.12); border: 1px solid rgba(74,222,128,0.26); color: #e2e8f0; }
  .gbubble em { color: #4ade80; font-style: normal; font-size: 0.74rem; }
  .gbubble .sqlblk {
    background: rgba(0,0,0,0.45); border: 1px solid rgba(74,222,128,0.16); border-radius: 7px;
    padding: 7px 10px; font-size: 0.71rem; color: #86efac; margin-top: 7px;
    font-family: 'Courier New', Courier, monospace; overflow-x: auto; white-space: pre-wrap;
  }
  .gbubble.gerr { background: rgba(239,68,68,0.1); border: 1px solid rgba(239,68,68,0.28); color: #fca5a5; }
  .genie-tbl-wrap { overflow-x: auto; margin-top: 8px; border-radius: 7px; }
  .genie-tbl { width: 100%; border-collapse: collapse; font-size: 0.72rem; }
  .genie-tbl th { background: rgba(74,222,128,0.1); color: #4ade80; padding: 5px 9px; text-align: left; border-bottom: 1px solid rgba(74,222,128,0.2); white-space: nowrap; }
  .genie-tbl td { color: #94a3b8; padding: 4px 9px; border-bottom: 1px solid rgba(148,163,184,0.07); }
  .genie-tbl tr:hover td { background: rgba(74,222,128,0.04); }
  #genie-typing { display: none; align-self: flex-start; align-items: center; gap: 9px; padding: 0 2px; }
  #genie-typing.on { display: flex; }
  .gdots { display: flex; gap: 5px; background: rgba(15,25,45,0.93); border: 1px solid rgba(74,222,128,0.12); border-radius: 11px; padding: 10px 15px; }
  .gdot { width: 6px; height: 6px; background: #4ade80; border-radius: 50%; animation: gbounce 1.2s infinite; }
  .gdot:nth-child(2) { animation-delay: 0.22s; }
  .gdot:nth-child(3) { animation-delay: 0.44s; }
  @keyframes gbounce {
    0%,80%,100% { transform: translateY(0); opacity: 0.32; }
    40%          { transform: translateY(-7px); opacity: 1; }
  }
  #genie-inputrow {
    display: flex; align-items: center; gap: 9px; padding: 14px 17px;
    border-top: 1px solid rgba(74,222,128,0.14); background: rgba(8,12,22,0.97); flex-shrink: 0;
  }
  #genie-input {
    flex: 1; background: rgba(15,25,45,0.93); border: 1px solid rgba(74,222,128,0.23);
    border-radius: 9px; padding: 10px 14px; color: #e2e8f0; font-size: 0.82rem;
    font-family: 'Courier New', Courier, monospace; outline: none; transition: border-color 0.2s;
  }
  #genie-input:focus { border-color: rgba(74,222,128,0.58); }
  #genie-input::placeholder { color: #475569; }
  #genie-input:disabled { opacity: 0.5; }
  #genie-sendbtn {
    width: 40px; height: 40px; background: linear-gradient(135deg, #166534, #0a2030);
    border: 1px solid rgba(74,222,128,0.44); border-radius: 9px; cursor: pointer;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0; transition: all 0.2s; color: #4ade80; outline: none;
  }
  #genie-sendbtn:hover { background: linear-gradient(135deg, #15803d, #0e3040); border-color: rgba(74,222,128,0.75); transform: scale(1.05); }
  #genie-sendbtn:disabled { opacity: 0.36; cursor: not-allowed; transform: none; }
"""

    # ── HTML ──────────────────────────────────────────────────────────────────
    html_str = """
<div id="genie-widget">
  <div id="genie-panel">
    <div id="genie-header">
      <div class="ghdr-left">
        <div class="gavatar">&#9672;</div>
        <div>
          <span class="gtname">H2C2 GENIE</span>
          <span class="gtsub">Powered by Databricks AI/BI</span>
        </div>
      </div>
      <div style="display:flex;align-items:center;gap:7px;">
        <div class="ghdr-status"></div>
        <button id="genie-closebtn" title="Close">&#10005;</button>
      </div>
    </div>
    <div id="genie-prompts">
      <span class="gchip">Which regions are most underfunded?</span>
      <span class="gchip">Top crisis countries by severity</span>
      <span class="gchip">Funding gap forecast 2026</span>
      <span class="gchip">High neglect risk countries</span>
    </div>
    <div id="genie-messages">
      <div class="gmsg bot">
        <div class="gmsg-ico">&#9672;</div>
        <div class="gbubble">
          Hello. I&apos;m Genie, your AI assistant for the Humanitarian Health Command Center.<br><br>
          Ask me anything about crisis regions, funding gaps, severity scores, or forecasts &mdash; I&apos;ll query the live data for you.
        </div>
      </div>
    </div>
    <div id="genie-typing">
      <div class="gmsg-ico" style="width:27px;height:27px;border-radius:7px;background:linear-gradient(135deg,#0d3321,#0a2030);border:1px solid rgba(74,222,128,0.38);display:flex;align-items:center;justify-content:center;font-size:13px;color:#4ade80;flex-shrink:0;margin-top:2px;">&#9672;</div>
      <div class="gdots"><div class="gdot"></div><div class="gdot"></div><div class="gdot"></div></div>
    </div>
    <div id="genie-inputrow">
      <input id="genie-input" type="text" placeholder="Ask about humanitarian data..." maxlength="500" />
      <button id="genie-sendbtn" title="Send">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round">
          <line x1="22" y1="2" x2="11" y2="13"></line>
          <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
        </svg>
      </button>
    </div>
  </div>
  <button id="genie-toggle">
    <div class="genie-btn-dot"></div>
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
      <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
    </svg>
    ASK GENIE
  </button>
</div>
"""

    # ── JS: display only — no fetch calls, triggers hidden Streamlit form ─────
    js_logic = """
function initGenieWidget(historyHtml) {
  var pDoc = window.parent.document;

  var panel   = pDoc.getElementById('genie-panel');
  var toggle  = pDoc.getElementById('genie-toggle');
  var closeBtn= pDoc.getElementById('genie-closebtn');
  var msgsEl  = pDoc.getElementById('genie-messages');
  var typingEl= pDoc.getElementById('genie-typing');
  var inputEl = pDoc.getElementById('genie-input');
  var sendBtn = pDoc.getElementById('genie-sendbtn');
  var chips   = pDoc.querySelectorAll('.gchip');

  // Append conversation history after the welcome message already in the HTML template
  if (historyHtml && historyHtml.trim()) {
    msgsEl.insertAdjacentHTML('beforeend', historyHtml);
    setTimeout(function(){ msgsEl.scrollTop = msgsEl.scrollHeight; }, 30);
  }

  // Toggle
  toggle.addEventListener('click', function() {
    var isOpen = panel.classList.toggle('open');
    if (isOpen) {
      setTimeout(function(){ inputEl.focus(); }, 60);
      setTimeout(function(){ msgsEl.scrollTop = msgsEl.scrollHeight; }, 30);
    }
  });
  closeBtn.addEventListener('click', function() { panel.classList.remove('open'); });

  // Chips
  chips.forEach(function(chip) {
    chip.addEventListener('click', function() {
      inputEl.value = chip.textContent.trim();
      panel.classList.add('open');
      inputEl.focus();
    });
  });

  // Send — passes message to Python via hidden Streamlit form
  inputEl.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); triggerSend(); }
  });
  sendBtn.addEventListener('click', triggerSend);

  function triggerSend() {
    var txt = inputEl.value.trim();
    if (!txt) return;
    inputEl.value = '';

    // Optimistic: show user message + typing indicator immediately
    var userRow = pDoc.createElement('div');
    userRow.className = 'gmsg user';
    userRow.innerHTML =
      '<div class="gmsg-ico">&#9658;</div>' +
      '<div class="gbubble">' + escHtml(txt) + '</div>';
    msgsEl.appendChild(userRow);
    typingEl.classList.add('on');
    msgsEl.scrollTop = msgsEl.scrollHeight;

    // Disable input while waiting
    inputEl.disabled = true;
    sendBtn.disabled = true;

    // Find hidden Streamlit text input by placeholder
    var hiddenInput = pDoc.querySelector('input[placeholder="__genie__"]');
    if (!hiddenInput) {
      typingEl.classList.remove('on');
      inputEl.disabled = false;
      sendBtn.disabled = false;
      var errRow = pDoc.createElement('div');
      errRow.className = 'gmsg bot';
      errRow.innerHTML = '<div class="gmsg-ico">&#9672;</div><div class="gbubble gerr">&#9888; Widget bridge not found. Please refresh the page.</div>';
      msgsEl.appendChild(errRow);
      return;
    }

    // Set value via React native setter (required for Streamlit React inputs)
    var nativeSetter = Object.getOwnPropertyDescriptor(
      window.parent.HTMLInputElement.prototype, 'value'
    ).set;
    nativeSetter.call(hiddenInput, txt);
    hiddenInput.dispatchEvent(new Event('input', { bubbles: true }));

    // Walk up DOM to find the Streamlit form container and click its button
    var el = hiddenInput;
    while (el && !(el.getAttribute && el.getAttribute('data-testid') === 'stForm')) {
      el = el.parentElement;
    }
    if (el) {
      var btn = el.querySelector('button');
      if (btn) btn.click();
    }
  }

  function escHtml(s) {
    return String(s)
      .replace(/&/g,'&amp;').replace(/</g,'&lt;')
      .replace(/>/g,'&gt;').replace(/"/g,'&quot;');
  }
}
"""

    # ── Injector script: always re-injects widget with fresh Python history ───
    script = f"""<script>
(function() {{
  var pDoc = window.parent.document;

  // Preserve open/closed state across rerenders
  var wasOpen = false;
  var existingPanel = pDoc.getElementById('genie-panel');
  if (existingPanel) wasOpen = existingPanel.classList.contains('open');

  // Remove stale widget (to inject fresh history from Python)
  var old = pDoc.getElementById('genie-widget');
  if (old) old.remove();
  var oldCss = pDoc.getElementById('genie-widget-css');
  if (oldCss) oldCss.remove();

  // Inject CSS
  var s = pDoc.createElement('style');
  s.id = 'genie-widget-css';
  s.textContent = {json.dumps(css_str)};
  pDoc.head.appendChild(s);

  // Inject HTML
  var c = pDoc.createElement('div');
  c.innerHTML = {json.dumps(html_str)};
  pDoc.body.appendChild(c);

  // Restore open state
  if (wasOpen) pDoc.getElementById('genie-panel').classList.add('open');

  {js_logic}

  // Pass current chat history (rendered by Python) into the widget
  initGenieWidget({json.dumps(history_html)});
}})();
</script>"""

    components.html(script, height=0, scrolling=False)


# ── Shared inner-page navigation ──────────────────────────────────────────────

def _render_inner_nav(key_suffix: str):
    """Navigation bar shared by dashboard, analytics, forecast, and about pages."""
    st.markdown(get_nav_css(st.session_state.theme, 'nav-wrapper-dashboard'), unsafe_allow_html=True)
    st.markdown('<div class="nav-wrapper-dashboard">', unsafe_allow_html=True)
    cols = st.columns([0.5, 1.2, 1.2, 1.2, 0.8, 3.8, 1.3])

    with cols[0]:
        if st.button('◈', key=f'logo_{key_suffix}'):
            st.session_state.current_page = 'home'
            st.rerun()
    with cols[1]:
        if st.button('DASHBOARD', key=f'nav_dash_{key_suffix}'):
            st.session_state.current_page = 'dashboard'
            st.rerun()
    with cols[2]:
        if st.button('ANALYTICS', key=f'nav_analytics_{key_suffix}'):
            st.session_state.current_page = 'analytics'
            st.rerun()
    with cols[3]:
        if st.button('FORECASTS', key=f'nav_forecast_{key_suffix}'):
            st.session_state.current_page = 'forecast'
            st.rerun()
    with cols[4]:
        if st.button('ABOUT', key=f'nav_about_{key_suffix}'):
            st.session_state.current_page = 'about'
            st.rerun()
    with cols[6]:
        st.markdown(
            '<div style="color:#9ca3af;font-size:0.75rem;text-transform:uppercase;'
            'letter-spacing:0.1em;padding-top:0.5rem;text-align:right;white-space:nowrap;">'
            'built for the <a href="https://www.un.org/en/" target="_blank" '
            'style="color:inherit;text-decoration:none;">UN</a></div>',
            unsafe_allow_html=True,
        )
    st.markdown('</div>', unsafe_allow_html=True)


# ── Home page (landing) ───────────────────────────────────────────────────────

def show_home_page():
    """Landing page with hero section and background globe."""
    st.markdown(get_nav_css(st.session_state.theme, 'nav-wrapper'), unsafe_allow_html=True)
    st.markdown('<div class="nav-wrapper">', unsafe_allow_html=True)
    cols = st.columns([0.5, 1.2, 1.2, 1.2, 0.8, 3.8, 1.3])

    with cols[0]:
        if st.button('◈', key='home_logo'):
            st.session_state.current_page = 'home'
            st.rerun()
    with cols[1]:
        if st.button('DASHBOARD', key='nav_dashboard'):
            st.session_state.current_page = 'dashboard'
            st.rerun()
    with cols[2]:
        if st.button('ANALYTICS', key='nav_analytics'):
            st.session_state.current_page = 'analytics'
            st.rerun()
    with cols[3]:
        if st.button('FORECASTS', key='nav_forecasts'):
            st.session_state.current_page = 'forecast'
            st.rerun()
    with cols[4]:
        if st.button('ABOUT', key='nav_about'):
            st.session_state.current_page = 'about'
            st.rerun()
    with cols[6]:
        st.markdown(
            '<div style="color:#9ca3af;font-size:0.75rem;text-transform:uppercase;'
            'letter-spacing:0.1em;padding-top:0.5rem;text-align:right;white-space:nowrap;">'
            'built for the <a href="https://www.un.org/en/" target="_blank" '
            'style="color:inherit;text-decoration:none;">UN</a></div>',
            unsafe_allow_html=True,
        )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('''
    <div class="hero-container fade-in">
        <h1 class="hero-tagline">INSIGHT FOR IMPACT</h1>
        <p class="hero-title">They need help. It\'s time to respond where it matters.</p>
        <p class="hero-description">
        An intelligent command center revealing critical insights into global health crises.
        Track vulnerability patterns, optimize funding allocation, and predict future humanitarian needs
        across vulnerable populations worldwide.
        </p>
    </div>
    ''', unsafe_allow_html=True)

    st.markdown('''
    <div class="cta-cards" style="position: relative; z-index: 10;">
        <div class="cta-card" style="background: rgba(15, 20, 35, 0.7) !important; backdrop-filter: blur(10px);">
            <div class="cta-card-title">MONITOR CRISIS REGIONS</div>
            <div class="cta-card-description">
            Track real-time health vulnerability across 20+ crisis regions with interactive visualization.
            </div>
        </div>
        <div class="cta-card" style="background: rgba(15, 20, 35, 0.7) !important; backdrop-filter: blur(10px);">
            <div class="cta-card-title">OPTIMIZE FUNDING</div>
            <div class="cta-card-description">
            Identify inefficiencies and maximize impact per dollar with AI-powered benchmarking.
            </div>
        </div>
        <div class="cta-card" style="background: rgba(15, 20, 35, 0.7) !important; backdrop-filter: blur(10px);">
            <div class="cta-card-title">PREDICT FUTURE NEEDS</div>
            <div class="cta-card-description">
            Forecast humanitarian resource demands with ML-powered vulnerability projections.
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    st.markdown('''
    <style>
    section[data-testid="stAppViewContainer"] { overflow: hidden !important; height: 100vh !important; }
    .main .block-container { overflow: hidden !important; height: 100vh !important;
        padding-bottom: 0 !important; position: relative !important; }
    .hero-container, .cta-cards { position: relative !important; z-index: 10 !important;
        padding-bottom: 2rem !important; }
    .home-globe-marker ~ [data-testid="element-container"],
    [data-testid="element-container"]:has(iframe[srcdoc*="globeViz"]) {
        position: fixed !important; top: 55vh !important; left: 50% !important;
        transform: translateX(-50%) !important; width: 300% !important; height: 75vh !important;
        z-index: 1 !important; pointer-events: none !important; margin: 0 !important; padding: 0 !important; }
    .home-globe-marker ~ [data-testid="element-container"] iframe,
    [data-testid="element-container"]:has(iframe[srcdoc*="globeViz"]) iframe {
        opacity: 0.6 !important; width: 100% !important; height: 100% !important; }
    </style>
    <div class="home-globe-marker"></div>
    ''', unsafe_allow_html=True)

    components.html(create_home_globe_html(), height=1000, scrolling=False)


# ── Dashboard / Health Regions page ──────────────────────────────────────────

def show_dashboard_page():
    """Crisis regions dashboard with themed globe and entity list."""
    _render_inner_nav('dashboard')

    col1, col2 = st.columns([0.7, 3.5])

    with col1:
        with st.expander("TYPES    ▼", expanded=False):
            st.markdown(f"""
            <div style="color: {theme_colors['entity_text']}; font-size: 0.85rem; padding-bottom: 0.75rem;">
            ◈ Health Crisis<br>◈ Nutrition Emergency<br>◈ Water Shortage<br>
            ◈ Shelter Need<br>◈ Protection Required
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='margin-bottom: 0.5rem;'></div>", unsafe_allow_html=True)

        entities       = generate_sample_entities()
        total_entities = len(entities)
        sev_dot = {5: '#ef4444', 4: '#f59e0b', 3: '#3b82f6', 2: '#4ade80'}
        entity_items_html = ""
        for _, entity in entities.iterrows():
            dot_color = sev_dot.get(entity['severity'], '#64748b')
            entity_items_html += (
                f'<div class="entity-item">'
                f'<span class="entity-name" style="display:flex;align-items:center;gap:0.5rem;">'
                f'<span style="width:7px;height:7px;border-radius:50%;background:{dot_color};'
                f'flex-shrink:0;display:inline-block;"></span>'
                f'{entity["name"]}</span>'
                f'<span class="entity-badge">{entity["in_need"]}</span>'
                f'</div>'
            )

        st.markdown(f'''<div class="entity-list">
            <div class="entity-header">
                <span class="entity-count">{total_entities} CRISIS REGIONS</span>
                <span class="sort-dropdown">SEVERITY ▼</span>
            </div>
            {entity_items_html}
        </div>''', unsafe_allow_html=True)

    with col2:
        components.html(create_globe_html(theme_colors), height=800, scrolling=False)


# ── App entry point ───────────────────────────────────────────────────────────

def run_app():
    page = st.session_state.current_page

    # Genie chatbot only on dashboard, analytics, and forecast pages.
    # On all other pages actively remove any leftover widget from the DOM,
    # because it is injected directly into window.parent.document and persists
    # across Streamlit's client-side page switches.
    if page in ('dashboard', 'analytics', 'forecast'):
        render_genie_chatbot()
    else:
        components.html("""<script>
(function() {
  var w = window.parent.document.getElementById('genie-widget');
  if (w) w.remove();
  var s = window.parent.document.getElementById('genie-widget-css');
  if (s) s.remove();
})();
</script>""", height=0, scrolling=False)

    if page == 'home':
        show_home_page()
    elif page == 'dashboard':
        show_dashboard_page()
    elif page == 'analytics':
        _render_inner_nav('analytics')
        render_analytics_page()
    elif page == 'forecast':
        _render_inner_nav('forecast')
        render_forecast_page()
    elif page == 'about':
        _render_inner_nav('about')
        render_about_page()
    else:
        show_home_page()


if __name__ == "__main__":
    run_app()
