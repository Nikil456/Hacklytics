import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np

# ── Session state ──────────────────────────────────────────────────────────────
if "active_page" not in st.session_state:
    st.session_state.active_page = "HEALTH REGIONS"

# Page configuration
st.set_page_config(
    page_title="H2C2 - Humanitarian Health Command Center",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    .stApp { background-color: #0a0e1a; }

    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
        padding-left: 1rem;
        padding-right: 1rem;
        max-width: 100%;
    }

    .element-container { margin: 0 !important; padding: 0 !important; }
    [data-testid="column"] { padding: 0.5rem !important; }
    div[data-testid="stHorizontalBlock"] { gap: 1rem !important; }

    .entity-list {
        background-color: transparent;
        padding: 0;
        height: calc(100vh - 200px);
        min-height: 500px;
        overflow-y: auto;
        border: none;
        margin-top: 0;
    }

    .entity-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid rgba(148, 163, 184, 0.2);
    }

    .entity-count { color: #4ade80; font-size: 0.875rem; font-weight: 600; letter-spacing: 0.1em; }
    .sort-dropdown { color: #94a3b8; font-size: 0.875rem; }

    .entity-item {
        color: #e2e8f0;
        padding: 1rem 0;
        margin: 0;
        cursor: pointer;
        transition: all 0.2s;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid rgba(148, 163, 184, 0.1);
    }

    .entity-item:hover { color: #ffffff; padding-left: 0.5rem; }
    .entity-name { font-size: 1.1rem; font-weight: 400; letter-spacing: 0.02em; }
    .entity-badge { color: #64748b; font-size: 0.9rem; font-weight: 400; min-width: 2rem; text-align: right; }

    .nav-item {
        color: #64748b;
        font-size: 0.75rem;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin: 0; padding: 0;
        line-height: 2;
    }
    .nav-item.active { color: #4ade80; }
    .nav-logo { color: #4ade80; font-size: 1.5rem; margin: 0; padding: 0; }

    /* Nav search */
    .nav-search-wrap { position: relative; display: flex; align-items: center; width: 100%; }

    .nav-search-input {
        width: 100%;
        background: rgba(15, 23, 42, 0.85);
        border: 1px solid rgba(74, 222, 128, 0.2);
        border-radius: 50px;
        padding: 0.42rem 3.2rem 0.42rem 1rem;
        color: #e2e8f0;
        font-family: 'Courier New', monospace;
        font-size: 0.72rem;
        outline: none;
        caret-color: #4ade80;
        transition: border-color 0.2s, box-shadow 0.2s;
        box-sizing: border-box;
        letter-spacing: 0.02em;
    }
    .nav-search-input::placeholder { color: #334155; }
    .nav-search-input:focus {
        border-color: rgba(74, 222, 128, 0.5);
        box-shadow: 0 0 0 3px rgba(74, 222, 128, 0.06), 0 0 18px rgba(74, 222, 128, 0.06);
    }

    .nav-search-btn {
        position: absolute; right: 5px;
        background: rgba(74, 222, 128, 0.1);
        border: 1px solid rgba(74, 222, 128, 0.3);
        border-radius: 50px;
        color: #4ade80;
        font-family: 'Courier New', monospace;
        font-size: 0.65rem; font-weight: 700;
        letter-spacing: 0.06em;
        padding: 0.3rem 0.75rem;
        cursor: pointer; text-transform: uppercase;
        transition: all 0.15s; white-space: nowrap;
    }
    .nav-search-btn:hover {
        background: rgba(74, 222, 128, 0.2);
        border-color: rgba(74, 222, 128, 0.6);
    }

    /* Nav button reset */
    button[kind="secondary"] {
        background: none !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
        font-size: 0.75rem !important;
        letter-spacing: 0.1em !important;
        text-transform: uppercase !important;
        font-family: inherit !important;
        transition: color 0.2s !important;
        color: #64748b !important;
    }
    button[kind="secondary"]:hover { color: #94a3b8 !important; }

    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: rgba(15, 23, 42, 0.5); }
    ::-webkit-scrollbar-thumb { background: #475569; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #64748b; }

    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }

    .streamlit-expanderHeader {
        background-color: transparent !important;
        color: #cbd5e1 !important;
        font-size: 0.7rem !important;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 600 !important;
        padding: 0.3rem 0 !important;
        border: none !important;
    }
    .streamlit-expanderHeader:hover { color: #4ade80 !important; }
    .streamlit-expanderContent {
        background-color: rgba(15, 23, 42, 0.8) !important;
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-radius: 4px;
        padding: 0.5rem !important;
        margin-top: 0.25rem;
    }
    details[open] summary svg { transform: rotate(180deg); }
</style>
""", unsafe_allow_html=True)


def generate_sample_entities():
    entities = [
        {'name': 'South Sudan', 'severity': 5, 'projects': 10, 'lat': 7,  'lon': 30,  'hvi': 8.9, 'fund': 34},
        {'name': 'Yemen',       'severity': 5, 'projects': 8,  'lat': 15, 'lon': 48,  'hvi': 9.2, 'fund': 28},
        {'name': 'Syria',       'severity': 4, 'projects': 12, 'lat': 35, 'lon': 38,  'hvi': 7.8, 'fund': 45},
        {'name': 'Afghanistan', 'severity': 5, 'projects': 15, 'lat': 34, 'lon': 67,  'hvi': 8.6, 'fund': 31},
        {'name': 'Somalia',     'severity': 4, 'projects': 7,  'lat': 5,  'lon': 46,  'hvi': 8.1, 'fund': 38},
        {'name': 'DR Congo',    'severity': 4, 'projects': 9,  'lat': -4, 'lon': 21,  'hvi': 7.9, 'fund': 42},
        {'name': 'Ethiopia',    'severity': 3, 'projects': 11, 'lat': 9,  'lon': 40,  'hvi': 6.5, 'fund': 52},
        {'name': 'Nigeria',     'severity': 3, 'projects': 6,  'lat': 9,  'lon': 8,   'hvi': 6.2, 'fund': 58},
        {'name': 'Haiti',       'severity': 3, 'projects': 5,  'lat': 19, 'lon': -72, 'hvi': 6.8, 'fund': 48},
        {'name': 'Ukraine',     'severity': 4, 'projects': 14, 'lat': 48, 'lon': 31,  'hvi': 7.3, 'fund': 65},
        {'name': 'Myanmar',     'severity': 3, 'projects': 8,  'lat': 21, 'lon': 95,  'hvi': 6.4, 'fund': 44},
        {'name': 'Venezuela',   'severity': 3, 'projects': 4,  'lat': 8,  'lon': -66, 'hvi': 6.1, 'fund': 36},
        {'name': 'Sudan',       'severity': 4, 'projects': 7,  'lat': 15, 'lon': 30,  'hvi': 7.6, 'fund': 40},
        {'name': 'Burkina Faso','severity': 3, 'projects': 6,  'lat': 12, 'lon': -2,  'hvi': 6.3, 'fund': 46},
        {'name': 'Mali',        'severity': 3, 'projects': 5,  'lat': 17, 'lon': -4,  'hvi': 6.7, 'fund': 43},
        {'name': 'Colombia',    'severity': 3, 'projects': 6,  'lat': 4,  'lon': -72, 'hvi': 6.4, 'fund': 41},
        {'name': 'Bangladesh',  'severity': 3, 'projects': 9,  'lat': 23, 'lon': 90,  'hvi': 6.6, 'fund': 47},
        {'name': 'Palestine',   'severity': 4, 'projects': 8,  'lat': 32, 'lon': 35,  'hvi': 7.5, 'fund': 39},
        {'name': 'Central African Rep.', 'severity': 4, 'projects': 5, 'lat': 7, 'lon': 21, 'hvi': 7.7, 'fund': 35},
        {'name': 'Niger',       'severity': 3, 'projects': 4,  'lat': 17, 'lon': 8,   'hvi': 6.5, 'fund': 42},
    ]
    return pd.DataFrame(entities)


def create_globe_html():
    severity_colors = {5: '#ef4444', 4: '#f59e0b', 3: '#3b82f6'}
    entities = generate_sample_entities()
    js_data = ",\n      ".join(
        f'{{ lat:{row["lat"]}, lng:{row["lon"]}, name:"{row["name"]}", '
        f'hvi:{row["hvi"]}, fund:{row["fund"]}, sev:"{row["severity"]}", '
        f'color:"{severity_colors[row["severity"]]}", projects:{row["projects"]} }}'
        for _, row in entities.iterrows()
    )
    globe_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  html, body {{ width:100%; height:100%; overflow:hidden; background:transparent; }}
  #globeViz {{ width:100%; height:100%; }}
  .overlay {{ position:fixed; z-index:100; font-family:'JetBrains Mono','Fira Code',monospace; font-size:10px; }}
  .glass {{
    background:rgba(10,14,26,0.75); border:1px solid rgba(74,222,128,0.2);
    border-radius:6px; backdrop-filter:blur(10px); padding:6px 10px; color:#94b4d4;
  }}
  #controls {{ top:14px; left:14px; display:flex; gap:6px; }}
  .vbtn {{
    background:rgba(10,14,26,0.75); border:1px solid rgba(74,222,128,0.2);
    border-radius:5px; padding:4px 12px; color:#94b4d4; cursor:pointer;
    font-family:'JetBrains Mono',monospace; font-size:10px; transition:all 0.15s;
  }}
  .vbtn.active, .vbtn:hover {{ background:rgba(74,222,128,0.15); border-color:rgba(74,222,128,0.5); color:#4ade80; }}
  #legend {{ bottom:8px; left:50%; transform:translateX(-50%); display:flex; gap:15px; }}
  .leg {{ display:flex; align-items:center; gap:6px; }}
  .ldot {{ width:10px; height:10px; border-radius:50%; flex-shrink:0; }}
  .globe-tooltip {{
    background:rgba(10,14,26,0.9) !important; border:1px solid rgba(74,222,128,0.3) !important;
    border-radius:5px !important; color:#94b4d4 !important;
    font-family:'JetBrains Mono',monospace !important; font-size:11px !important;
    padding:6px 10px !important; pointer-events:none; line-height:1.6;
  }}
  .tooltip-name {{ font-weight:700; color:#4ade80; margin-bottom:2px; }}
</style>
</head>
<body>
<div id="globeViz"></div>
<div class="overlay" id="controls">
  <button class="vbtn active" onclick="setView('world',this)">World</button>
  <button class="vbtn" onclick="setView('africa',this)">Africa</button>
  <button class="vbtn" onclick="setView('mideast',this)">Middle East</button>
  <button class="vbtn" onclick="setView('asia',this)">Asia</button>
  <button class="vbtn" onclick="setView('northamerica',this)">North America</button>
  <button class="vbtn" onclick="setView('southamerica',this)">South America</button>
</div>
<div class="overlay glass" id="legend">
  <div class="leg"><div class="ldot" style="background:#ef4444;"></div><span>Critical</span></div>
  <div class="leg"><div class="ldot" style="background:#f59e0b;"></div><span>High</span></div>
  <div class="leg"><div class="ldot" style="background:#3b82f6;"></div><span>Medium</span></div>
</div>
<script src="https://unpkg.com/globe.gl@2.30.0/dist/globe.gl.min.js"></script>
<script>
  const crisisData = [
    {js_data}
  ];
  const globe = Globe({{ animateIn: true }})
    .globeImageUrl('//unpkg.com/three-globe/example/img/earth-blue-marble.jpg')
    .bumpImageUrl('//unpkg.com/three-globe/example/img/earth-topology.png')
    .backgroundColor('rgba(10,14,26,0)')
    .showAtmosphere(false)
    .pointsData(crisisData)
    .pointLat('lat').pointLng('lng').pointColor('color')
    .pointAltitude(0.08).pointRadius(0.5).pointResolution(16)
    .ringsData(crisisData)
    .ringLat('lat').ringLng('lng')
    .ringColor(d => t => {{
      const hex = d.color.replace('#','');
      const r = parseInt(hex.slice(0,2),16);
      const g = parseInt(hex.slice(2,4),16);
      const b = parseInt(hex.slice(4,6),16);
      return `rgba(${{r}},${{g}},${{b}},${{Math.max(0,1-t)}})`;
    }})
    .ringMaxRadius(6).ringPropagationSpeed(2.5).ringRepeatPeriod(1300)
    .labelsData(crisisData)
    .labelLat('lat').labelLng('lng').labelText('name')
    .labelSize(0.6).labelDotRadius(0.4)
    .labelColor(() => 'rgba(232,240,254,0.95)')
    .labelResolution(3).labelAltitude(0.01)
    .pointLabel(d => `
      <div class="globe-tooltip">
        <div class="tooltip-name">${{d.name}}</div>
        <div>Health Vulnerability Index: <b>${{d.hvi}}</b></div>
        <div>Funding coverage: <b>${{d.fund}}%</b></div>
        <div>Projects: <b>${{d.projects}}</b></div>
        <div>Severity: <b style="color:${{d.color}}">Level ${{d.sev}}</b></div>
      </div>
    `)
    .onPointClick(d => globe.pointOfView({{ lat:d.lat, lng:d.lng, altitude:1.2 }}, 900))
    (document.getElementById('globeViz'));

  globe.controls().autoRotate      = true;
  globe.controls().autoRotateSpeed = 0.35;
  globe.controls().enableZoom      = true;
  globe.controls().minDistance     = 150;
  globe.controls().maxDistance     = 700;
  globe.pointOfView({{ lat:18, lng:30, altitude:2.4 }}, 800);

  let currentView = 'world';
  const el = document.getElementById('globeViz');
  el.addEventListener('mouseenter', () => {{ if (currentView==='world') globe.controls().autoRotate=false; }});
  el.addEventListener('mouseleave', () => {{ if (currentView==='world') globe.controls().autoRotate=true; }});

  const VIEWS = {{
    world:        {{ lat:18,  lng:30,  altitude:2.4 }},
    africa:       {{ lat:5,   lng:22,  altitude:1.4 }},
    mideast:      {{ lat:25,  lng:48,  altitude:1.4 }},
    asia:         {{ lat:30,  lng:70,  altitude:1.5 }},
    northamerica: {{ lat:35,  lng:-95, altitude:1.5 }},
    southamerica: {{ lat:-10, lng:-60, altitude:1.6 }},
  }};

  function setView(name, btn) {{
    currentView = name;
    document.querySelectorAll('.vbtn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    globe.pointOfView(VIEWS[name], 1000);
    globe.controls().autoRotate = (name === 'world');
  }}
</script>
</body>
</html>"""
    return globe_html


def render_about_page():
    about_html = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  html, body {
    width:100%; min-height:100%;
    background:#0a0e1a;
    font-family: Arial, Helvetica, sans-serif;
    color: #e2e8f0;
  }

  .page {
    max-width: 860px;
    margin: 0 auto;
    padding: 4rem 2rem 5rem;
  }

  .eyebrow {
    color: #4ade80;
    font-family: 'Courier New', monospace;
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    margin-bottom: 1.2rem;
  }

  h1 {
    color: #ffffff;
    font-size: 3rem;
    font-weight: 300;
    line-height: 1.1;
    margin-bottom: 0.4rem;
    letter-spacing: -0.02em;
  }

  .subtitle {
    color: #4ade80;
    font-family: 'Courier New', monospace;
    font-size: 0.8rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 2.5rem;
  }

  .rule {
    border: none;
    border-top: 1px solid rgba(148, 163, 184, 0.12);
    margin-bottom: 2.5rem;
  }

  .lead {
    color: #cbd5e1;
    font-size: 1.05rem;
    line-height: 1.75;
    margin-bottom: 1.6rem;
    font-weight: 300;
  }

  .lead b { color: #ffffff; font-weight: 500; }

  /* Three-pillar row */
  .pillars {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.5rem;
    margin-top: 3rem;
  }

  .pillar {
    padding: 1.4rem 1.2rem;
    background: rgba(15, 23, 42, 0.7);
    border: 1px solid rgba(148, 163, 184, 0.1);
    border-radius: 6px;
    transition: border-color 0.2s;
  }

  .pillar:hover { border-color: rgba(74, 222, 128, 0.25); }

  .pillar-icon {
    color: #4ade80;
    font-family: 'Courier New', monospace;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 0.75rem;
  }

  .pillar h3 {
    color: #f1f5f9;
    font-size: 0.95rem;
    font-weight: 500;
    margin-bottom: 0.6rem;
  }

  .pillar p {
    color: #64748b;
    font-size: 0.82rem;
    line-height: 1.65;
  }

  /* Stack row */
  .stack-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-top: 2.5rem;
  }

  .stack-tag {
    font-family: 'Courier New', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.06em;
    color: #64748b;
    border: 1px solid rgba(148, 163, 184, 0.12);
    border-radius: 4px;
    padding: 0.25rem 0.65rem;
  }

  .stack-label {
    font-family: 'Courier New', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #334155;
    margin-top: 2.5rem;
    margin-bottom: 0.6rem;
  }
</style>
</head>
<body>
<div class="page">

  <p class="eyebrow">Hacklytics 2026 &nbsp;·&nbsp; Databricks &times; United Nations</p>
  <h1>H2C2</h1>
  <p class="subtitle">Humanitarian Health Command Center</p>
  <hr class="rule" />

  <p class="lead">
    Every year, billions of dollars in humanitarian aid are allocated without a clear picture of
    where the need is greatest. Funding reaches some regions generously while others &mdash;
    equally devastated &mdash; are barely touched. <b>H2C2 exists to close that gap.</b>
  </p>

  <p class="lead">
    We join the UN&rsquo;s Humanitarian Needs Overview (HNO) and Humanitarian Response Plan (HRP)
    datasets into a single live intelligence layer. The result is a <b>Health Vulnerability Index</b>
    &mdash; a real-time score that shows, for every crisis region on Earth, how far medical funding
    lags behind the severity of the situation on the ground.
  </p>

  <p class="lead">
    From that foundation we built three tools: an interactive 3D globe that makes the data
    impossible to ignore, a natural-language interface so any official can ask a question
    without writing a single line of SQL, and a machine-learning engine that flags
    inefficient projects and forecasts where the next health desert will emerge
    before it becomes a headline.
  </p>

  <div class="pillars">
    <div class="pillar">
      <p class="pillar-icon">01 &mdash; The Map</p>
      <h3>Live Crisis Globe</h3>
      <p>A 3D rotating Earth colored by vulnerability. Zoom from a global view down to
         individual states and districts. Every pulse on the map is a real crisis, ranked
         by need vs. funding.</p>
    </div>
    <div class="pillar">
      <p class="pillar-icon">02 &mdash; The Genie</p>
      <h3>Ask in Plain Language</h3>
      <p>Powered by Databricks AI/BI Genie. Type a question &mdash; &ldquo;Why is South Sudan
         critical?&rdquo; or &ldquo;Find projects over $500 per person&rdquo; &mdash; and the
         system writes the SQL and returns the answer instantly.</p>
    </div>
    <div class="pillar">
      <p class="pillar-icon">03 &mdash; The Engine</p>
      <h3>Forecast &amp; Benchmark</h3>
      <p>An ML layer that predicts funding gaps six months out and uses KNN to surface
         peer projects that are doing more with less &mdash; giving auditors a concrete
         benchmark to act on today.</p>
    </div>
  </div>

  <p class="stack-label">Built with</p>
  <div class="stack-row">
    <span class="stack-tag">Databricks</span>
    <span class="stack-tag">Delta Lake</span>
    <span class="stack-tag">Unity Catalog</span>
    <span class="stack-tag">AI/BI Genie</span>
    <span class="stack-tag">Spark MLlib</span>
    <span class="stack-tag">Streamlit</span>
    <span class="stack-tag">globe.gl</span>
    <span class="stack-tag">UN HDX Data</span>
  </div>

</div>
</body>
</html>"""
    components.html(about_html, height=820, scrolling=True)


def run_app():
    page = st.session_state.active_page

    # ── Navigation ────────────────────────────────────────────────────────────
    nav_cols = st.columns([0.5, 1.5, 1.5, 1.5, 1.5, 3])

    with nav_cols[0]:
        st.markdown('<p class="nav-logo">◈</p>', unsafe_allow_html=True)

    with nav_cols[1]:
        hr_color = "#4ade80" if page == "HEALTH REGIONS" else "#64748b"
        st.markdown(f'<p class="nav-item" style="color:{hr_color}; cursor:pointer;">HEALTH REGIONS</p>', unsafe_allow_html=True)
        if st.button("‣", key="btn_hr", help="Health Regions"):
            st.session_state.active_page = "HEALTH REGIONS"
            st.rerun()

    with nav_cols[2]:
        st.markdown('<p class="nav-item">REGIONAL TARGETS</p>', unsafe_allow_html=True)

    with nav_cols[3]:
        st.markdown('<p class="nav-item">FUNDERS</p>', unsafe_allow_html=True)

    with nav_cols[4]:
        ab_color = "#4ade80" if page == "ABOUT" else "#64748b"
        st.markdown(f'<p class="nav-item" style="color:{ab_color}; cursor:pointer;">ABOUT</p>', unsafe_allow_html=True)
        if st.button("‣", key="btn_about", help="About"):
            st.session_state.active_page = "ABOUT"
            st.rerun()

    with nav_cols[5]:
        st.markdown("""
        <div class="nav-search-wrap">
            <input
                class="nav-search-input"
                type="text"
                id="genieSearch"
                placeholder="Ask the Genie — e.g. Why is South Sudan critical?"
                autocomplete="off"
                spellcheck="false"
            />
            <button class="nav-search-btn" onclick="genieRun()">Ask ↵</button>
        </div>
        <script>
            function genieRun() {
                var val = document.getElementById('genieSearch').value.trim();
                if (!val) return;
                console.log('Genie query:', val);
            }
            document.getElementById('genieSearch').addEventListener('keydown', function(e) {
                if (e.key === 'Enter') genieRun();
            });
        </script>
        """, unsafe_allow_html=True)

    # Hide the tiny arrow buttons — they're just click triggers
    st.markdown("""
    <style>
      button[kind="secondary"] { display:none !important; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div style='margin-bottom: 0.5rem;'></div>", unsafe_allow_html=True)

    # ── Page routing ──────────────────────────────────────────────────────────
    if page == "ABOUT":
        render_about_page()
        return

    # ── Health Regions (main page — untouched) ────────────────────────────────
    col1, col2 = st.columns([0.7, 3.5])

    with col1:
        col_filter1, col_filter2 = st.columns(2)

        with col_filter1:
            with st.expander("TYPES ▼", expanded=False):
                st.markdown("""
                <div style="color: #cbd5e1; font-size: 0.85rem;">
                ◈ Health Crisis<br>
                ◈ Nutrition Emergency<br>
                ◈ Water Shortage<br>
                ◈ Shelter Need<br>
                ◈ Protection Required
                </div>
                """, unsafe_allow_html=True)

        with col_filter2:
            with st.expander("TARGETS ▼", expanded=False):
                st.markdown("""
                <div style="color: #cbd5e1; font-size: 0.85rem;">
                ◈ All Regions<br>
                ◈ Africa<br>
                ◈ Middle East<br>
                ◈ Asia<br>
                ◈ Americas
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<div style='margin-bottom: 0.5rem;'></div>", unsafe_allow_html=True)

        entities = generate_sample_entities()
        total_entities = len(entities)

        entity_items_html = ""
        for _, entity in entities.iterrows():
            entity_items_html += f'''<div class="entity-item">
                <span class="entity-name">{entity['name']}</span>
                <span class="entity-badge">{entity['projects']}</span>
            </div>'''

        st.markdown(f'''<div class="entity-list">
            <div class="entity-header">
                <span class="entity-count">{total_entities} CRISIS REGIONS</span>
                <span class="sort-dropdown">A-Z ▼</span>
            </div>
            {entity_items_html}
        </div>''', unsafe_allow_html=True)

    with col2:
        globe_html = create_globe_html()

        st.markdown('''
        <div style="position: absolute; top: 80px; right: 20px; z-index: 1000; text-align: right; max-width: 420px; pointer-events: none;">
            <p style="color: #4ade80; font-size: 0.7rem; font-weight: 600; letter-spacing: 0.15em; text-transform: uppercase; margin: 0 0 8px 0; font-family: 'Courier New', monospace;">HUMANITARIAN HEALTH</p>
            <h1 style="color: #ffffff; font-size: 2rem; font-weight: 300; margin: 0 0 12px 0; line-height: 1.1;">CRISIS REGIONS</h1>
            <p style="color: #9ca3af; font-size: 0.85rem; line-height: 1.5; margin: 0;">
            Global surveillance and spyware companies that develop technologies to collect user data, monitor communications, and capture biometrics, enabling governments and corporations to track individuals.
            </p>
        </div>
        ''', unsafe_allow_html=True)

        components.html(globe_html, height=800, scrolling=False)


if __name__ == "__main__":
    run_app()
