import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np

# Page configuration
st.set_page_config(
    page_title="H2C2 - Humanitarian Health Command Center",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS to match Surveillance Watch design
st.markdown("""
<style>
    /* Main app background - deep dark blue/black */
    .stApp {
        background-color: #0a0e1a;
    }
    
    /* Remove default padding */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
        padding-left: 1rem;
        padding-right: 1rem;
        max-width: 100%;
    }
    
    /* Remove extra spacing from streamlit elements */
    .element-container {
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* Remove column gaps */
    [data-testid="column"] {
        padding: 0.5rem !important;
    }
    
    div[data-testid="stHorizontalBlock"] {
        gap: 1rem !important;
    }
    
    /* Header styling */
    .main-header {
        color: #4ade80;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        margin-bottom: 0.25rem;
        margin-top: 0;
        font-family: 'Courier New', monospace;
    }
    
    .page-title {
        color: #ffffff;
        font-size: 2.5rem;
        font-weight: 300;
        margin-bottom: 0.5rem;
        margin-top: 0.25rem;
        line-height: 1.1;
    }
    
    .page-subtitle {
        color: #9ca3af;
        font-size: 0.95rem;
        line-height: 1.5;
        margin-bottom: 1rem;
        margin-top: 0;
        max-width: 90%;
    }
    
    /* Entity list styling - seamless blend with background */
    .entity-list {
        background-color: transparent;
        border-radius: 0;
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
        padding-left: 0;
        padding-right: 0;
    }
    
    .entity-count {
        color: #4ade80;
        font-size: 0.875rem;
        font-weight: 600;
        letter-spacing: 0.1em;
    }
    
    .sort-dropdown {
        color: #94a3b8;
        font-size: 0.875rem;
    }
    
    .entity-item {
        color: #e2e8f0;
        padding: 1rem 0;
        margin: 0;
        cursor: pointer;
        border-radius: 0;
        transition: all 0.2s;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid rgba(148, 163, 184, 0.1);
    }
    
    .entity-item:hover {
        background-color: transparent;
        color: #ffffff;
        padding-left: 0.5rem;
    }
    
    .entity-name {
        font-size: 1.1rem;
        font-weight: 400;
        letter-spacing: 0.02em;
    }
    
    .entity-badge {
        background-color: transparent;
        color: #64748b;
        padding: 0;
        border-radius: 0;
        font-size: 0.9rem;
        font-weight: 400;
        min-width: 2rem;
        text-align: right;
    }
    
    /* Globe container */
    .globe-container {
        position: relative;
        height: 600px;
        background: radial-gradient(circle at center, #0f172a 0%, #020617 100%);
        border-radius: 8px;
        border: 1px solid rgba(148, 163, 184, 0.1);
        overflow: hidden;
        margin-top: 0;
    }
    
    /* Top nav styling */
    .top-nav {
        margin-bottom: 1.5rem;
    }
    
    .nav-item {
        color: #64748b;
        font-size: 0.75rem;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        cursor: pointer;
        transition: color 0.2s;
        margin: 0;
        padding: 0;
    }
    
    .nav-item.active {
        color: #4ade80;
    }
    
    .nav-item:hover {
        color: #94a3b8;
    }
    
    .nav-logo {
        color: #4ade80;
        font-size: 1.5rem;
        margin: 0;
        padding: 0;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(15, 23, 42, 0.5);
    }
    
    ::-webkit-scrollbar-thumb {
        background: #475569;
        border-radius: 3px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #64748b;
    }
    
    /* Hide streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Filter buttons */
    .filter-section {
        margin-bottom: 0.25rem;
        margin-top: 0;
    }
    
    .filter-label {
        color: #cbd5e1;
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 0;
        margin-top: 0;
        font-weight: 600;
        display: inline-block;
        padding: 0.3rem 0;
        cursor: pointer;
        transition: color 0.2s;
    }
    
    .filter-label:hover {
        color: #4ade80;
    }
    
    .filter-container {
        margin-bottom: 1rem;
        margin-top: 0;
        padding-top: 0;
    }
    
    /* Expander styling to match the design */
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
    
    .streamlit-expanderHeader:hover {
        color: #4ade80 !important;
    }
    
    .streamlit-expanderContent {
        background-color: rgba(15, 23, 42, 0.8) !important;
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-radius: 4px;
        padding: 0.5rem !important;
        margin-top: 0.25rem;
    }
    
    details[open] summary svg {
        transform: rotate(180deg);
    }
</style>
""", unsafe_allow_html=True)

def generate_sample_entities():
    """Generate sample crisis regions for the entity list"""
    entities = [
        {'name': 'South Sudan', 'severity': 5, 'projects': 10, 'lat': 7, 'lon': 30, 'hvi': 8.9, 'fund': 34},
        {'name': 'Yemen', 'severity': 5, 'projects': 8, 'lat': 15, 'lon': 48, 'hvi': 9.2, 'fund': 28},
        {'name': 'Syria', 'severity': 4, 'projects': 12, 'lat': 35, 'lon': 38, 'hvi': 7.8, 'fund': 45},
        {'name': 'Afghanistan', 'severity': 5, 'projects': 15, 'lat': 34, 'lon': 67, 'hvi': 8.6, 'fund': 31},
        {'name': 'Somalia', 'severity': 4, 'projects': 7, 'lat': 5, 'lon': 46, 'hvi': 8.1, 'fund': 38},
        {'name': 'DR Congo', 'severity': 4, 'projects': 9, 'lat': -4, 'lon': 21, 'hvi': 7.9, 'fund': 42},
        {'name': 'Ethiopia', 'severity': 3, 'projects': 11, 'lat': 9, 'lon': 40, 'hvi': 6.5, 'fund': 52},
        {'name': 'Nigeria', 'severity': 3, 'projects': 6, 'lat': 9, 'lon': 8, 'hvi': 6.2, 'fund': 58},
        {'name': 'Haiti', 'severity': 3, 'projects': 5, 'lat': 19, 'lon': -72, 'hvi': 6.8, 'fund': 48},
        {'name': 'Ukraine', 'severity': 4, 'projects': 14, 'lat': 48, 'lon': 31, 'hvi': 7.3, 'fund': 65},
        {'name': 'Myanmar', 'severity': 3, 'projects': 8, 'lat': 21, 'lon': 95, 'hvi': 6.4, 'fund': 44},
        {'name': 'Venezuela', 'severity': 3, 'projects': 4, 'lat': 8, 'lon': -66, 'hvi': 6.1, 'fund': 36},
        {'name': 'Sudan', 'severity': 4, 'projects': 7, 'lat': 15, 'lon': 30, 'hvi': 7.6, 'fund': 40},
        {'name': 'Burkina Faso', 'severity': 3, 'projects': 6, 'lat': 12, 'lon': -2, 'hvi': 6.3, 'fund': 46},
        {'name': 'Mali', 'severity': 3, 'projects': 5, 'lat': 17, 'lon': -4, 'hvi': 6.7, 'fund': 43},
        {'name': 'Colombia', 'severity': 3, 'projects': 6, 'lat': 4, 'lon': -72, 'hvi': 6.4, 'fund': 41},
        {'name': 'Bangladesh', 'severity': 3, 'projects': 9, 'lat': 23, 'lon': 90, 'hvi': 6.6, 'fund': 47},
        {'name': 'Palestine', 'severity': 4, 'projects': 8, 'lat': 32, 'lon': 35, 'hvi': 7.5, 'fund': 39},
        {'name': 'Central African Rep.', 'severity': 4, 'projects': 5, 'lat': 7, 'lon': 21, 'hvi': 7.7, 'fund': 35},
        {'name': 'Niger', 'severity': 3, 'projects': 4, 'lat': 17, 'lon': 8, 'hvi': 6.5, 'fund': 42},
    ]
    return pd.DataFrame(entities)

def create_globe_html():
    """Create a 3D rotatable globe using globe.gl (Three.js-based)"""
    
    # Map severity to colors
    severity_colors = {
        5: '#ef4444',  # Critical - red
        4: '#f59e0b',  # High - orange
        3: '#3b82f6',  # Medium - blue
    }
    
    # Get entities data
    entities = generate_sample_entities()
    
    # Build JS crisis data array
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

  /* Overlay UI */
  .overlay {{
    position:fixed; z-index:100;
    font-family:'JetBrains Mono','Fira Code',monospace;
    font-size:10px;
  }}
  .glass {{
    background:rgba(10,14,26,0.75);
    border:1px solid rgba(74,222,128,0.2);
    border-radius:6px;
    backdrop-filter:blur(10px);
    padding:6px 10px;
    color:#94b4d4;
  }}
  /* View controls */
  #controls {{ top:14px; left:14px; display:flex; gap:6px; }}
  .vbtn {{
    background:rgba(10,14,26,0.75);
    border:1px solid rgba(74,222,128,0.2);
    border-radius:5px; padding:4px 12px;
    color:#94b4d4; cursor:pointer;
    font-family:'JetBrains Mono',monospace; font-size:10px;
    transition:all 0.15s;
  }}
  .vbtn.active, .vbtn:hover {{
    background:rgba(74,222,128,0.15);
    border-color:rgba(74,222,128,0.5);
    color:#4ade80;
  }}
  /* Legend - centered at bottom, closer to globe */
  #legend {{ 
    bottom: 8px; 
    left: 50%; 
    transform: translateX(-50%);
    display: flex;
    gap: 15px;
  }}
  .leg {{ display:flex; align-items:center; gap:6px; }}
  .ldot {{ width:10px; height:10px; border-radius:50%; flex-shrink:0; }}
  /* Tooltip override */
  .globe-tooltip {{
    background:rgba(10,14,26,0.9) !important;
    border:1px solid rgba(74,222,128,0.3) !important;
    border-radius:5px !important;
    color:#94b4d4 !important;
    font-family:'JetBrains Mono',monospace !important;
    font-size:11px !important;
    padding:6px 10px !important;
    pointer-events:none;
    line-height:1.6;
  }}
  .tooltip-name {{ font-weight:700; color:#4ade80; margin-bottom:2px; }}
</style>
</head>
<body>

<div id="globeViz"></div>

<!-- Controls overlay -->
<div class="overlay" id="controls">
  <button class="vbtn active" onclick="setView('world',this)">World</button>
  <button class="vbtn" onclick="setView('africa',this)">Africa</button>
  <button class="vbtn" onclick="setView('mideast',this)">Middle East</button>
  <button class="vbtn" onclick="setView('asia',this)">Asia</button>
  <button class="vbtn" onclick="setView('northamerica',this)">North America</button>
  <button class="vbtn" onclick="setView('southamerica',this)">South America</button>
</div>

<!-- Legend overlay - centered at bottom, closer to globe -->
<div class="overlay glass" id="legend">
  <div class="leg"><div class="ldot" style="background:#ef4444;"></div><span>Critical</span></div>
  <div class="leg"><div class="ldot" style="background:#f59e0b;"></div><span>High</span></div>
  <div class="leg"><div class="ldot" style="background:#3b82f6;"></div><span>Medium</span></div>
</div>

<!-- globe.gl from CDN -->
<script src="https://unpkg.com/globe.gl@2.30.0/dist/globe.gl.min.js"></script>

<script>
  const crisisData = [
    {js_data}
  ];

  // Build globe
  const globe = Globe({{ animateIn: true }})
    .globeImageUrl('//unpkg.com/three-globe/example/img/earth-blue-marble.jpg')
    .bumpImageUrl('//unpkg.com/three-globe/example/img/earth-topology.png')
    .backgroundColor('rgba(10,14,26,0)')
    .showAtmosphere(false)

    // Raised glowing points at each crisis location
    .pointsData(crisisData)
    .pointLat('lat')
    .pointLng('lng')
    .pointColor('color')
    .pointAltitude(0.08)
    .pointRadius(0.5)
    .pointResolution(16)

    // Propagating rings (pulsing SOS effect)
    .ringsData(crisisData)
    .ringLat('lat')
    .ringLng('lng')
    .ringColor(d => t => {{
      const hex = d.color.replace('#','');
      const r = parseInt(hex.slice(0,2),16);
      const g = parseInt(hex.slice(2,4),16);
      const b = parseInt(hex.slice(4,6),16);
      const alpha = Math.max(0, 1 - t);
      return `rgba(${{r}},${{g}},${{b}},${{alpha}})`;
    }})
    .ringMaxRadius(6)
    .ringPropagationSpeed(2.5)
    .ringRepeatPeriod(1300)

    // Floating labels
    .labelsData(crisisData)
    .labelLat('lat')
    .labelLng('lng')
    .labelText('name')
    .labelSize(0.6)
    .labelDotRadius(0.4)
    .labelColor(() => 'rgba(232,240,254,0.95)')
    .labelResolution(3)
    .labelAltitude(0.01)

    // Rich HTML tooltip
    .pointLabel(d => `
      <div class="globe-tooltip">
        <div class="tooltip-name">${{d.name}}</div>
        <div>Health Vulnerability Index: <b>${{d.hvi}}</b></div>
        <div>Funding coverage: <b>${{d.fund}}%</b></div>
        <div>Projects: <b>${{d.projects}}</b></div>
        <div>Severity: <b style="color:${{d.color}}">Level ${{d.sev}}</b></div>
      </div>
    `)

    // Click to zoom in
    .onPointClick(d => {{
      globe.pointOfView({{ lat: d.lat, lng: d.lng, altitude: 1.2 }}, 900);
    }})

    (document.getElementById('globeViz'));

  // Camera settings
  globe.controls().autoRotate      = true;
  globe.controls().autoRotateSpeed = 0.35;
  globe.controls().enableZoom      = true;
  globe.controls().minDistance     = 150;
  globe.controls().maxDistance     = 700;

  // Initial view centered on crisis belt
  globe.pointOfView({{ lat: 18, lng: 30, altitude: 2.4 }}, 800);

  // Track current view state
  let currentView = 'world';

  // Pause rotation on hover only if in world view, resume on leave only if in world view
  const el = document.getElementById('globeViz');
  el.addEventListener('mouseenter', () => {{
    if (currentView === 'world') {{
      globe.controls().autoRotate = false;
    }}
  }});
  el.addEventListener('mouseleave', () => {{
    if (currentView === 'world') {{
      globe.controls().autoRotate = true;
    }}
  }});

  // View preset buttons
  const VIEWS = {{
    world:        {{ lat: 18, lng: 30,  altitude: 2.4 }},
    africa:       {{ lat:  5, lng: 22,  altitude: 1.4 }},
    mideast:      {{ lat: 25, lng: 48,  altitude: 1.4 }},
    asia:         {{ lat: 30, lng: 70,  altitude: 1.5 }},
    northamerica: {{ lat: 35, lng: -95, altitude: 1.5 }},
    southamerica: {{ lat: -10, lng: -60, altitude: 1.6 }},
  }};

  function setView(name, btn) {{
    currentView = name;
    document.querySelectorAll('.vbtn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    globe.pointOfView(VIEWS[name], 1000);
    
    // Disable auto-rotation when viewing specific regions, enable for world view
    if (name === 'world') {{
      globe.controls().autoRotate = true;
    }} else {{
      globe.controls().autoRotate = false;
    }}
  }}
</script>
</body>
</html>"""
    return globe_html

def run_app():
    # Top navigation bar - more compact
    nav_cols = st.columns([0.5, 1.5, 1.5, 1.5, 1.5, 3])
    
    with nav_cols[0]:
        st.markdown('<p class="nav-logo">◈</p>', unsafe_allow_html=True)
    with nav_cols[1]:
        st.markdown('<p class="nav-item active">HEALTH REGIONS</p>', unsafe_allow_html=True)
    with nav_cols[2]:
        st.markdown('<p class="nav-item">REGIONAL TARGETS</p>', unsafe_allow_html=True)
    with nav_cols[3]:
        st.markdown('<p class="nav-item">FUNDERS</p>', unsafe_allow_html=True)
    with nav_cols[4]:
        st.markdown('<p class="nav-item">ABOUT</p>', unsafe_allow_html=True)
    
    st.markdown("<div style='margin-bottom: 0.5rem;'></div>", unsafe_allow_html=True)
    
    # Main content: Two columns - entity list on left, globe on right (even larger ratio)
    col1, col2 = st.columns([0.7, 3.5])
    
    # Left column - Entity list
    with col1:
        # Collapsible filter dropdowns
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
        
        # Entity list - build entire HTML as one block to avoid nested containers
        entities = generate_sample_entities()
        total_entities = len(entities)
        
        # Build all entity items as a single HTML string (no leading spaces)
        entity_items_html = ""
        for _, entity in entities.iterrows():
            entity_items_html += f'''<div class="entity-item">
                <span class="entity-name">{entity['name']}</span>
                <span class="entity-badge">{entity['projects']}</span>
            </div>'''
        
        # Render entire entity list as one HTML block - no nested st.markdown calls
        st.markdown(f'''<div class="entity-list">
            <div class="entity-header">
                <span class="entity-count">{total_entities} CRISIS REGIONS</span>
                <span class="sort-dropdown">A-Z ▼</span>
            </div>
            {entity_items_html}
        </div>''', unsafe_allow_html=True)
    
    # Right column - Globe with title overlay
    with col2:
        globe_html = create_globe_html()
        
        # Title overlay - position absolute to not take up space, closer to globe
        st.markdown('''
        <div style="position: absolute; top: 80px; right: 20px; z-index: 1000; text-align: right; max-width: 420px; pointer-events: none;">
            <p style="color: #4ade80; font-size: 0.7rem; font-weight: 600; letter-spacing: 0.15em; text-transform: uppercase; margin: 0 0 8px 0; font-family: 'Courier New', monospace;">HUMANITARIAN HEALTH</p>
            <h1 style="color: #ffffff; font-size: 2rem; font-weight: 300; margin: 0 0 12px 0; line-height: 1.1;">CRISIS REGIONS</h1>
            <p style="color: #9ca3af; font-size: 0.85rem; line-height: 1.5; margin: 0;">
            Global surveillance and spyware companies that develop technologies to collect user data, monitor communications, and capture biometrics, enabling governments and corporations to track individuals.
            </p>
        </div>
        ''', unsafe_allow_html=True)
        
        # Globe - adjusted size to fit without scrolling
        components.html(globe_html, height=800, scrolling=False)

if __name__ == "__main__":
    run_app()
