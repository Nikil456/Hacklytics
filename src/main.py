import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
from styles import get_theme_colors, get_main_css, get_nav_css, get_globe_button_css

# Page configuration
st.set_page_config(
    page_title="Insight for Impact",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state for page navigation
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'

# Initialize theme state (default to dark mode)
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'

# Get theme colors and apply CSS
theme_colors = get_theme_colors(st.session_state.theme)
st.markdown(get_main_css(theme_colors), unsafe_allow_html=True)

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

def create_home_globe_html():
    """Create a clean Earth globe for the home page (no crisis markers or filters)"""
    
    globe_html = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  html, body { width:100%; height:100%; overflow:hidden; background:transparent; }
  #globeViz { width:100%; height:100%; }
</style>
</head>
<body>

<div id="globeViz"></div>

<!-- globe.gl from CDN -->
<script src="https://unpkg.com/globe.gl@2.30.0/dist/globe.gl.min.js"></script>

<script>
  // Build clean globe with no data
  const globe = Globe({ animateIn: true })
    .globeImageUrl('//unpkg.com/three-globe/example/img/earth-blue-marble.jpg')
    .bumpImageUrl('//unpkg.com/three-globe/example/img/earth-topology.png')
    .backgroundColor('rgba(10,14,26,0)')
    .showAtmosphere(false)
    (document.getElementById('globeViz'));

  // Camera settings
  globe.controls().autoRotate      = true;
  globe.controls().autoRotateSpeed = 0.35;
  globe.controls().enableZoom      = true;
  globe.controls().minDistance     = 150;
  globe.controls().maxDistance     = 700;

  // Initial view - zoomed in to fill the frame better
  globe.pointOfView({ lat: 10, lng: 20, altitude: 1.8 }, 800);

  // Pause rotation on hover, resume on leave
  const el = document.getElementById('globeViz');
  el.addEventListener('mouseenter', () => {
    globe.controls().autoRotate = false;
  });
  el.addEventListener('mouseleave', () => {
    globe.controls().autoRotate = true;
  });
</script>
</body>
</html>"""
    return globe_html

def create_globe_html(theme_colors):
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
    
    # Get theme-aware CSS for buttons, legend, and tooltips
    button_css = get_globe_button_css(theme_colors)
    
    globe_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  html, body {{ width:100%; height:100%; overflow:hidden; background:transparent; }}
  #globeViz {{ width:100%; height:100%; }}

{button_css}
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

def show_home_page():
    """Display the home page with hero section and background globe"""
    
    # Top navigation bar - all items as buttons for consistent alignment
    st.markdown(get_nav_css(st.session_state.theme, 'nav-wrapper'), unsafe_allow_html=True)
    
    # Create navigation wrapper - all items as buttons for consistency
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
        st.button('ANALYTICS', key='nav_analytics')
    
    with cols[3]:
        st.button('FORECASTS', key='nav_forecasts')
    
    with cols[4]:
        st.button('ABOUT', key='nav_about')
    
    with cols[6]:
        st.markdown('<div style="color: #9ca3af; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.1em; padding-top: 0.5rem; text-align: right; white-space: nowrap;">built for the UN</div>', unsafe_allow_html=True)
    
    # with cols[6]:
    #     # Theme toggle button
    #     theme_icon = '☀️' if st.session_state.theme == 'dark' else '🌙'
    #     if st.button(theme_icon, key='theme_toggle_home'):
    #         st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'
    #         st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Hero section with fade-in animation
    st.markdown('''
    <div class="hero-container fade-in">
        <h1 class="hero-tagline">INSIGHT FOR IMPACT</h1>
        <p class="hero-title">They need help. It's time to respond where it matters.</p>
        <p class="hero-description">
        An intelligent command center revealing critical insights into global health crises. 
        Track vulnerability patterns, optimize funding allocation, and predict future humanitarian needs 
        across vulnerable populations worldwide.
        </p>
    </div>
    ''', unsafe_allow_html=True)
    
    # CTA Cards with transparent backgrounds
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
    
    # Add CSS and wrapper for background globe
    st.markdown('''
    <style>
    /* Prevent scrolling on home page */
    section[data-testid="stAppViewContainer"] {
        overflow: hidden !important;
        height: 100vh !important;
    }
    .main .block-container {
        overflow: hidden !important;
        height: 100vh !important;
        padding-bottom: 0 !important;
        position: relative !important;
    }
    
    /* Make content appear above globe */
    .hero-container,
    .cta-cards {
        position: relative !important;
        z-index: 10 !important;
        padding-bottom: 2rem !important;
    }
    
    /* Target all element containers after the marker */
    .home-globe-marker ~ [data-testid="element-container"],
    [data-testid="element-container"]:has(iframe[srcdoc*="globeViz"]) {
        position: fixed !important;
        top: 55vh !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        width: 300% !important;
        height: 75vh !important;
        z-index: 1 !important;
        pointer-events: none !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    .home-globe-marker ~ [data-testid="element-container"] iframe,
    [data-testid="element-container"]:has(iframe[srcdoc*="globeViz"]) iframe {
        opacity: 0.6 !important;
        width: 100% !important;
        height: 100% !important;
    }
    </style>
    <div class="home-globe-marker"></div>
    ''', unsafe_allow_html=True)
    
    # Render globe - the CSS above will position it
    globe_html = create_home_globe_html()
    components.html(globe_html, height=1000, scrolling=False)

def show_dashboard_page():
    """Display the main dashboard with globe and crisis regions"""
    
    # Get theme colors for inline styling
    theme_colors = get_theme_colors(st.session_state.theme)
    
    # Top navigation bar - same styling as home page
    st.markdown(get_nav_css(st.session_state.theme, 'nav-wrapper-dashboard'), unsafe_allow_html=True)
    
    # Create navigation wrapper - all items as buttons for consistency
    st.markdown('<div class="nav-wrapper-dashboard">', unsafe_allow_html=True)
    cols = st.columns([0.5, 1.2, 1.2, 1.2, 0.8, 3.8, 1.3])
    
    with cols[0]:
        if st.button('◈', key='dashboard_logo'):
            st.session_state.current_page = 'home'
            st.rerun()
    
    with cols[1]:
        st.button('DASHBOARD', key='nav_dashboard_active')
    
    with cols[2]:
        st.button('ANALYTICS', key='nav_analytics_dash')
    
    with cols[3]:
        st.button('FORECASTS', key='nav_forecasts_dash')
    
    with cols[4]:
        st.button('ABOUT', key='nav_about_dash')
    
    with cols[6]:
        st.markdown('<div style="color: #9ca3af; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.1em; padding-top: 0.5rem; text-align: right; white-space: nowrap;">built for the UN</div>', unsafe_allow_html=True)
    
    # with cols[6]:
    #     # Theme toggle button
    #     theme_icon = '☀️' if st.session_state.theme == 'dark' else '🌙'
    #     if st.button(theme_icon, key='theme_toggle_dashboard'):
    #         st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'
    #         st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Main content: Two columns - entity list on left, globe on right (even larger ratio)
    col1, col2 = st.columns([0.7, 3.5])
    
    # Left column - Entity list
    with col1:
        # Collapsible filter dropdowns
        col_filter1, col_filter2 = st.columns(2)
        
        with col_filter1:
            with st.expander("TYPES", expanded=False):
                st.markdown(f"""
                <div style="color: {theme_colors['entity_text']}; font-size: 0.85rem;">
                ◈ Health Crisis<br>
                ◈ Nutrition Emergency<br>
                ◈ Water Shortage<br>
                ◈ Shelter Need<br>
                ◈ Protection Required
                </div>
                """, unsafe_allow_html=True)
        
        with col_filter2:
            with st.expander("TARGETS", expanded=False):
                st.markdown(f"""
                <div style="color: {theme_colors['entity_text']}; font-size: 0.85rem;">
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
        globe_html = create_globe_html(theme_colors)
        
        # Title overlay - position absolute to not take up space, closer to globe
        # st.markdown(f'''
        # <div style="position: absolute; top: 80px; right: 20px; z-index: 1000; text-align: right; max-width: 420px; pointer-events: none;">
        #     <p style="color: {theme_colors['accent']}; font-size: 0.7rem; font-weight: 600; letter-spacing: 0.15em; text-transform: uppercase; margin: 0 0 8px 0; font-family: 'Courier New', monospace;">HUMANITARIAN HEALTH</p>
        #     <h1 style="color: {theme_colors['primary_text']}; font-size: 2rem; font-weight: 300; margin: 0 0 12px 0; line-height: 1.1;">CRISIS REGIONS</h1>
        #     <p style="color: {theme_colors['secondary_text']}; font-size: 0.85rem; line-height: 1.5; margin: 0;">
        #     Global surveillance and spyware companies that develop technologies to collect user data, monitor communications, and capture biometrics, enabling governments and corporations to track individuals.
        #     </p>
        # </div>
        # ''', unsafe_allow_html=True)
        
        # Globe - adjusted size to fit without scrolling
        components.html(globe_html, height=800, scrolling=False)

def run_app():
    """Main app entry point - handles page routing"""
    if st.session_state.current_page == 'home':
        show_home_page()
    elif st.session_state.current_page == 'dashboard':
        show_dashboard_page()
    else:
        show_dashboard_page()

if __name__ == "__main__":
    run_app()
