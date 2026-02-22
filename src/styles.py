"""
Styling and CSS management for H2C2 application
"""

def get_theme_colors(theme):
    """Get color scheme based on current theme"""
    if theme == 'dark':
        return {
            'app_bg': '#060911',
            'primary_text': '#ffffff',
            'secondary_text': '#9ca3af',
            'tertiary_text': '#64748b',
            'accent': '#4ade80',
            'accent_hover': '#ffffff',
            'hover_text': '#94a3b8',
            'entity_text': '#e2e8f0',
            'border_color': 'rgba(148, 163, 184, 0.2)',
            'border_subtle': 'rgba(148, 163, 184, 0.1)',
            'globe_gradient_start': '#0f172a',
            'globe_gradient_end': '#020617',
            'scrollbar_track': 'rgba(15, 23, 42, 0.5)',
            'scrollbar_thumb': '#475569',
            'scrollbar_thumb_hover': '#64748b',
            'expander_bg': 'rgba(15, 23, 42, 0.8)',
            'cta_card_bg': 'rgba(15, 23, 42, 0.6)',
            'cta_card_hover_bg': 'rgba(15, 23, 42, 0.8)',
            'border_accent': 'rgba(74, 222, 128, 0.2)',
            'border_accent_hover': 'rgba(74, 222, 128, 0.5)',
        }
    else:  # light mode
        return {
            'app_bg': '#ffffff',
            'primary_text': '#0f172a',
            'secondary_text': '#475569',
            'tertiary_text': '#94a3b8',
            'accent': '#2563eb',
            'accent_hover': '#1d4ed8',
            'hover_text': '#334155',
            'entity_text': '#1e293b',
            'border_color': 'rgba(148, 163, 184, 0.3)',
            'border_subtle': 'rgba(148, 163, 184, 0.15)',
            'globe_gradient_start': '#f1f5f9',
            'globe_gradient_end': '#e2e8f0',
            'scrollbar_track': 'rgba(226, 232, 240, 0.8)',
            'scrollbar_thumb': '#cbd5e1',
            'scrollbar_thumb_hover': '#94a3b8',
            'expander_bg': 'rgba(241, 245, 249, 0.9)',
            'cta_card_bg': 'rgba(241, 245, 249, 0.6)',
            'cta_card_hover_bg': 'rgba(241, 245, 249, 0.9)',
            'border_accent': 'rgba(37, 99, 235, 0.2)',
            'border_accent_hover': 'rgba(37, 99, 235, 0.5)',
        }


def get_main_css(theme_colors):
    """Generate the main application CSS with theme support"""
    return f"""
<style>
    /* Import Inter font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Main app background and default font */
    .stApp {{
        background-color: {theme_colors['app_bg']};
        transition: background-color 0.3s ease;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }}
    
    /* Apply Inter to all text elements */
    * {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }}
    
    /* Global override for ALL button borders - this is the nuclear option */
    button[kind="secondary"],
    button[data-testid="baseButton-secondary"],
    button[kind="secondary"]:hover,
    button[data-testid="baseButton-secondary"]:hover,
    button[kind="secondary"]:focus,
    button[data-testid="baseButton-secondary"]:focus,
    button[kind="secondary"]:active,
    button[data-testid="baseButton-secondary"]:active,
    button[kind="secondary"]:focus-visible,
    button[data-testid="baseButton-secondary"]:focus-visible {{
        border: 0px solid transparent !important;
        border-color: transparent !important;
        border-width: 0px !important;
        outline: none !important;
        box-shadow: none !important;
        -webkit-tap-highlight-color: transparent !important;
        transition: color 0.6s ease !important;
    }}
    
    /* Override red hover/active color globally */
    button[kind="secondary"]:hover,
    button[data-testid="baseButton-secondary"]:hover,
    button[kind="secondary"]:active,
    button[data-testid="baseButton-secondary"]:active,
    button[kind="secondary"]:active:focus,
    button[data-testid="baseButton-secondary"]:active:focus {{
        border-color: transparent !important;
        color: #00ff41 !important;
        background-color: transparent !important;
        outline: none !important;
        box-shadow: none !important;
    }}
    
    /* Remove red click styling from button content */
    button[kind="secondary"] *,
    button[data-testid="baseButton-secondary"] *,
    button[kind="secondary"]:active *,
    button[data-testid="baseButton-secondary"]:active *,
    button[kind="secondary"]:focus *,
    button[data-testid="baseButton-secondary"]:focus * {{
        color: inherit !important;
        background: transparent !important;
        border: none !important;
        outline: none !important;
    }}
    
    /* Override button text elements specifically */
    button[kind="secondary"] p,
    button[kind="secondary"] div,
    button[kind="secondary"] span,
    button[data-testid="baseButton-secondary"] p,
    button[data-testid="baseButton-secondary"] div,
    button[data-testid="baseButton-secondary"] span {{
        color: inherit !important;
    }}
    
    button[kind="secondary"]:active p,
    button[kind="secondary"]:active div,
    button[kind="secondary"]:active span,
    button[data-testid="baseButton-secondary"]:active p,
    button[data-testid="baseButton-secondary"]:active div,
    button[data-testid="baseButton-secondary"]:active span {{
        color: #00ff41 !important;
    }}
    
    /* Remove default padding */
    .block-container {{
        padding-top: 0.25rem;
        padding-bottom: 0rem;
        padding-left: 1rem;
        padding-right: 1rem;
        max-width: 100%;
    }}
    
    /* Remove extra spacing from streamlit elements */
    .element-container {{
        margin: 0 !important;
        padding: 0 !important;
    }}
    
    /* Remove column gaps */
    [data-testid="column"] {{
        padding: 0.5rem !important;
    }}
    
    div[data-testid="stHorizontalBlock"] {{
        gap: 1rem !important;
    }}
    
    /* Header styling */
    .main-header {{
        color: {theme_colors['accent']};
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        margin-bottom: 0.25rem;
        margin-top: 0;
        font-family: 'Courier New', monospace;
        transition: color 0.3s ease;
    }}
    
    .page-title {{
        color: {theme_colors['primary_text']};
        font-size: 2.5rem;
        font-weight: 300;
        margin-bottom: 0.5rem;
        margin-top: 0.25rem;
        line-height: 1.1;
        transition: color 0.3s ease;
    }}
    
    .page-subtitle {{
        color: {theme_colors['secondary_text']};
        font-size: 0.95rem;
        line-height: 1.5;
        margin-bottom: 1rem;
        margin-top: 0;
        max-width: 90%;
        transition: color 0.3s ease;
    }}
    
    /* Entity list styling - seamless blend with background */
    .entity-list {{
        background-color: transparent;
        border-radius: 0;
        padding: 0;
        height: calc(100vh - 200px);
        min-height: 500px;
        overflow-y: auto;
        border: none;
        margin-top: 0;
        scrollbar-width: none; /* Firefox */
        -ms-overflow-style: none; /* IE and Edge */
    }}
    
    /* Hide scrollbar for Chrome, Safari and Opera */
    .entity-list::-webkit-scrollbar {{
        display: none;
    }}
    
    .entity-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid {theme_colors['border_color']};
        padding-left: 0;
        padding-right: 0;
    }}
    
    .entity-count {{
        color: {theme_colors['accent']};
        font-size: 0.875rem;
        font-weight: 600;
        letter-spacing: 0.1em;
        transition: color 0.3s ease;
    }}
    
    .sort-dropdown {{
        color: {theme_colors['tertiary_text']};
        font-size: 0.875rem;
        transition: color 0.3s ease;
    }}
    
    .entity-item {{
        color: {theme_colors['entity_text']};
        padding: 1rem 0;
        margin: 0;
        cursor: pointer;
        border-radius: 0;
        transition: all 0.2s;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid {theme_colors['border_subtle']};
    }}
    
    .entity-item:hover {{
        background-color: transparent;
        color: {theme_colors['primary_text']};
        padding-left: 0.5rem;
    }}
    
    .entity-name {{
        font-size: 1.1rem;
        font-weight: 400;
        letter-spacing: 0.02em;
    }}
    
    .entity-badge {{
        background-color: transparent;
        color: {theme_colors['tertiary_text']};
        padding: 0;
        border-radius: 0;
        font-size: 0.9rem;
        font-weight: 400;
        min-width: 2rem;
        text-align: right;
        transition: color 0.3s ease;
    }}
    
    /* Globe container */
    .globe-container {{
        position: relative;
        height: 600px;
        background: radial-gradient(circle at center, {theme_colors['globe_gradient_start']} 0%, {theme_colors['globe_gradient_end']} 100%);
        border-radius: 8px;
        border: 1px solid {theme_colors['border_subtle']};
        overflow: hidden;
        margin-top: 0;
        transition: background 0.3s ease;
    }}
    
    /* Top nav styling */
    .top-nav {{
        margin-bottom: 1.5rem;
    }}
    
    .nav-item {{
        color: {theme_colors['tertiary_text']};
        font-size: 0.75rem;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        cursor: pointer;
        transition: color 0.2s;
        margin: 0;
        padding: 0;
        line-height: 1;
        display: inline-block;
    }}
    
    .nav-item.active {{
        color: {theme_colors['accent']};
    }}
    
    .nav-item:hover {{
        color: {theme_colors['hover_text']};
    }}
    
    .nav-logo {{
        color: {theme_colors['accent']};
        font-size: 1.5rem;
        margin: 0;
        padding: 0;
        cursor: pointer;
        transition: all 0.3s;
    }}
    
    .nav-logo:hover {{
        color: {theme_colors['accent_hover']};
        transform: scale(1.1);
    }}
    
    /* Theme toggle button styling */
    .theme-toggle {{
        background: transparent;
        border: 1px solid {theme_colors['border_color']};
        color: {theme_colors['accent']};
        border-radius: 6px;
        padding: 0.4rem 0.8rem;
        font-size: 1rem;
        cursor: pointer;
        transition: all 0.3s;
    }}
    
    .theme-toggle:hover {{
        background: {theme_colors['border_subtle']};
        transform: scale(1.05);
    }}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {{
        width: 6px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: {theme_colors['scrollbar_track']};
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: {theme_colors['scrollbar_thumb']};
        border-radius: 3px;
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: {theme_colors['scrollbar_thumb_hover']};
    }}
    
    /* Completely remove Streamlit's built-in header bar (Deploy button, hamburger menu) */
    #MainMenu {{display: none !important;}}
    footer {{display: none !important;}}
    header[data-testid="stHeader"] {{display: none !important;}}
    [data-testid="stDecoration"] {{display: none !important;}}
    [data-testid="stToolbar"] {{display: none !important;}}

    /* Remove the top padding Streamlit reserves for the now-hidden header */
    [data-testid="stAppViewContainer"] > section.main {{
        padding-top: 0 !important;
    }}
    [data-testid="stAppViewContainer"] {{
        padding-top: 0 !important;
    }}
    
    /* Filter buttons */
    .filter-section {{
        margin-bottom: 0.25rem;
        margin-top: 0;
    }}
    
    .filter-label {{
        color: {theme_colors['entity_text']};
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
    }}
    
    .filter-label:hover {{
        color: {theme_colors['accent']};
    }}
    
    .filter-container {{
        margin-bottom: 1rem;
        margin-top: 0;
        padding-top: 0;
    }}
    
    /* Expander styling to match the design */
    .streamlit-expanderHeader,
    [data-testid="stExpander"] summary,
    [data-testid="stExpander"] summary p,
    [data-testid="stExpander"] summary span {{
        background-color: transparent !important;
        color: {theme_colors['entity_text']} !important;
        font-size: 0.7rem !important;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 600 !important;
        padding: 0.3rem 0 !important;
        border: none !important;
        transition: color 0.6s ease !important;
        text-align: center !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }}
    
    /* Hide the caret icon completely */
    [data-testid="stExpander"] summary svg,
    [data-testid="stExpander"] svg,
    .streamlit-expanderHeader svg,
    [data-testid="stExpander"] summary > svg,
    [data-testid="stExpander"] details summary svg {{
        display: none !important;
        visibility: hidden !important;
    }}
    
    /* Remove ALL container styling - every possible element */
    [data-testid="stExpander"] summary > *,
    [data-testid="stExpander"] summary div,
    [data-testid="stExpander"] summary span,
    [data-testid="stExpander"] details summary > *,
    .streamlit-expanderHeader > *,
    [data-testid="stExpander"] summary button,
    [data-testid="stExpander"] summary a {{
        background: transparent !important;
        background-color: transparent !important;
        background-image: none !important;
        border: none !important;
        border-width: 0px !important;
        border-style: none !important;
        border-color: transparent !important;
        outline: none !important;
        outline-width: 0px !important;
        box-shadow: none !important;
        padding: 0 !important;
        margin: 0 !important;
    }}
    
    /* Hover state for expander */
    .streamlit-expanderHeader:hover,
    [data-testid="stExpander"] summary:hover,
    [data-testid="stExpander"] summary:hover p,
    [data-testid="stExpander"] summary:hover span,
    [data-testid="stExpander"] summary:hover * {{
        color: #00ff41 !important;
        background-color: transparent !important;
        background: transparent !important;
        border: none !important;
        outline: none !important;
        box-shadow: none !important;
    }}
    

    
    .streamlit-expanderContent {{
        background-color: {theme_colors['expander_bg']} !important;
        border: 1px solid {theme_colors['border_color']};
        border-radius: 4px;
        padding: 0.5rem !important;
        margin-top: 0.25rem;
        transition: background-color 0.3s ease;
    }}
    
    details[open] summary svg {{
        transform: rotate(180deg);
    }}
    
    /* Home page hero section */
    .hero-container {{
        text-align: center;
        padding: 4rem 2rem 2rem 2rem;
        max-width: 1200px;
        margin: 0 auto;
    }}
    
    .hero-tagline {{
        color: {theme_colors['accent']};
        font-size: 5.5rem;
        font-weight: 700;
        margin-bottom: 2rem;
        letter-spacing: -0.03em;
        transition: color 0.3s ease;
        text-transform: uppercase;
    }}
    
    .hero-title {{
        color: {theme_colors['primary_text']};
        font-size: 2rem;
        font-weight: 500;
        line-height: 1.4;
        margin-bottom: 2rem;
        text-transform: none;
        letter-spacing: 0;
        transition: color 0.3s ease;
    }}
    
    .hero-description {{
        color: {theme_colors['secondary_text']};
        font-size: 1.1rem;
        line-height: 1.7;
        max-width: 900px;
        margin: 0 auto 3rem auto;
        transition: color 0.3s ease;
    }}
    
    .cta-cards {{
        display: flex;
        gap: 1.5rem;
        justify-content: center;
        margin: 3rem auto;
        max-width: 1400px;
        flex-wrap: wrap;
    }}
    
    .cta-card {{
        background: {theme_colors['cta_card_bg']};
        border: 1px solid {theme_colors['border_accent']};
        border-radius: 8px;
        padding: 1.25rem 1.75rem;
        flex: 1;
        min-width: 350px;
        max-width: 450px;
        transition: all 0.3s;
    }}
    
    .cta-card:hover {{
        background: {theme_colors['cta_card_hover_bg']};
        border-color: {theme_colors['border_accent_hover']};
        transform: translateY(-5px);
    }}
    
    .cta-card-title {{
        color: {theme_colors['accent']};
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-weight: 600;
        margin-bottom: 0.4rem;
        transition: color 0.3s ease;
    }}
    
    .cta-card-description {{
        color: {theme_colors['entity_text']};
        font-size: 0.9rem;
        line-height: 1.5;
        transition: color 0.3s ease;
    }}
    
    .home-globe-container {{
        margin-top: 2rem;
        max-width: 100%;
    }}
    
    /* Smooth transitions for page changes */
    .fade-in {{
        animation: fadeIn 0.5s ease-in;
    }}
    
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(20px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
</style>
"""


def get_nav_css(theme, wrapper_class='nav-wrapper', app_bg=None):
    """Generate navigation bar CSS with theme support"""
    if theme == 'dark':
        nav_text = '#9ca3af'
        nav_accent = '#00ff41'
        nav_hover = '#00ff41'
        nav_bg = app_bg or '#060911'
    else:
        nav_text = '#475569'
        nav_accent = '#2563eb'
        nav_hover = '#1d4ed8'
        nav_bg = '#f8fafc'
    
    return f"""
<style>
/* Force navigation row to use flexbox with center alignment */
[data-testid="stHorizontalBlock"]:has(.{wrapper_class}) {{
    display: flex !important;
    align-items: center !important;
    gap: 2rem;
    margin-bottom: 1rem;
    padding: 0.25rem 0;
}}

[data-testid="stHorizontalBlock"]:has(.{wrapper_class}) > div {{
    display: flex !important;
    align-items: center !important;
    width: auto !important;
    flex: 0 0 auto !important;
}}

/* Force every element inside the nav wrapper to match the page background */
.{wrapper_class} *,
.{wrapper_class} button,
.{wrapper_class} button *,
.{wrapper_class} .stButton button,
.{wrapper_class} .stButton button *,
.{wrapper_class} button[kind="secondary"],
.{wrapper_class} button[kind="secondary"] *,
.{wrapper_class} button[data-testid="baseButton-secondary"],
.{wrapper_class} button[data-testid="baseButton-secondary"] *,
.{wrapper_class} .row-widget.stButton button,
.{wrapper_class} .row-widget.stButton button *,
div.{wrapper_class} button,
div.{wrapper_class} button * {{
    background: {nav_bg} !important;
    background-color: {nav_bg} !important;
    background-image: none !important;
    border: 0px solid transparent !important;
    border-color: transparent !important;
    border-width: 0px !important;
    border-style: none !important;
    border-top: none !important;
    border-bottom: none !important;
    border-left: none !important;
    border-right: none !important;
    outline: 0px solid transparent !important;
    outline-color: transparent !important;
    outline-width: 0px !important;
    box-shadow: none !important;
    text-decoration: none !important;
}}

/* Normal state colors */
.{wrapper_class} button[kind="secondary"],
.{wrapper_class} button[data-testid="baseButton-secondary"],
.{wrapper_class} button[kind="secondary"] *,
.{wrapper_class} button[data-testid="baseButton-secondary"] * {{
    color: {nav_text} !important;
    transition: color 0.6s ease !important;
    padding: 0.5rem 0.75rem !important;
    margin: 0 !important;
    line-height: 1 !important;
    height: auto !important;
    min-height: auto !important;
    -webkit-tap-highlight-color: transparent !important;
    cursor: pointer !important;
    white-space: nowrap !important;
}}

/* Hover state */
.{wrapper_class} button:hover,
.{wrapper_class} button:hover *,
.{wrapper_class} .stButton button:hover,
.{wrapper_class} .stButton button:hover *,
.{wrapper_class} button[kind="secondary"]:hover,
.{wrapper_class} button[kind="secondary"]:hover *,
.{wrapper_class} button[data-testid="baseButton-secondary"]:hover,
.{wrapper_class} button[data-testid="baseButton-secondary"]:hover *,
div.{wrapper_class} button:hover,
div.{wrapper_class} button:hover * {{
    background: {nav_bg} !important;
    background-color: {nav_bg} !important;
    background-image: none !important;
    border: 0px solid transparent !important;
    border-color: transparent !important;
    border-width: 0px !important;
    outline: 0px solid transparent !important;
    outline-color: transparent !important;
    box-shadow: none !important;
    -webkit-tap-highlight-color: transparent !important;
    color: {nav_accent} !important;
}}

/* Focus state */
.{wrapper_class} button:focus,
.{wrapper_class} button:focus-visible,
.{wrapper_class} button[kind="secondary"]:focus,
.{wrapper_class} button[kind="secondary"]:focus-visible {{
    background: {nav_bg} !important;
    background-color: {nav_bg} !important;
    border: 0px solid transparent !important;
    border-color: transparent !important;
    outline: 0px solid transparent !important;
    outline-color: transparent !important;
    box-shadow: none !important;
    color: {nav_text} !important;
}}

/* Active state — no red highlight */
.{wrapper_class} button:active,
.{wrapper_class} button:active *,
.{wrapper_class} button[kind="secondary"]:active,
.{wrapper_class} button[kind="secondary"]:active *,
.{wrapper_class} button[data-testid="baseButton-secondary"]:active,
.{wrapper_class} button[data-testid="baseButton-secondary"]:active * {{
    background: {nav_bg} !important;
    background-color: {nav_bg} !important;
    background-image: none !important;
    border: 0px solid transparent !important;
    border-color: transparent !important;
    outline: 0px solid transparent !important;
    box-shadow: none !important;
    color: {nav_accent} !important;
    transform: none !important;
    -webkit-tap-highlight-color: transparent !important;
}}

/* Logo button special styling */
.{wrapper_class} .stButton:first-child button,
.{wrapper_class} .stButton:first-child button * {{
    color: {nav_accent} !important;
    font-size: 1.5rem !important;
    border: 0px solid transparent !important;
}}

.{wrapper_class} .stButton:first-child button:hover,
.{wrapper_class} .stButton:first-child button:hover * {{
    color: {nav_hover} !important;
    transform: scale(1.1);
    border: 0px solid transparent !important;
}}

/* Active nav item (2nd button = dashboard) */
.{wrapper_class} .stButton:nth-child(2) button,
.{wrapper_class} .stButton:nth-child(2) button * {{
    color: {nav_accent} !important;
    border: 0px solid transparent !important;
}}

/* Hide zero-height iframe containers that cause extra spacing above nav */
[data-testid="element-container"]:has(iframe[height="0"]) {{
    display: none !important;
    height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
}}
</style>
"""


def get_globe_button_css(theme_colors):
    """Generate theme-aware CSS for globe view controls, legend, and tooltips"""
    
    # Use dark variants for any non-white background (dark mode)
    _is_dark = theme_colors['app_bg'] != '#ffffff'

    # Background colors for glass effect
    bg_glass   = 'rgba(6,9,17,0.75)'    if _is_dark else 'rgba(241,245,249,0.9)'
    bg_tooltip = 'rgba(6,9,17,0.9)'     if _is_dark else 'rgba(255,255,255,0.95)'

    # Active/hover background
    bg_active  = 'rgba(74,222,128,0.15)' if _is_dark else 'rgba(37,99,235,0.15)'
    
    return f"""
  /* Overlay UI */
  .overlay {{
    position:fixed; z-index:100;
    font-family:'JetBrains Mono','Fira Code',monospace;
    font-size:10px;
  }}
  .glass {{
    background:{bg_glass};
    border:1px solid {theme_colors['border_accent']};
    border-radius:6px;
    backdrop-filter:blur(10px);
    padding:6px 10px;
    color:{theme_colors['secondary_text']};
  }}
  /* View controls */
  #controls {{ top:14px; left:14px; display:flex; gap:12px; flex-wrap: wrap; }}
  .vbtn {{
    background:{bg_glass};
    border:1px solid {theme_colors['border_accent']};
    border-radius:8px; 
    padding:12px 24px;
    color:{theme_colors['secondary_text']}; 
    cursor:pointer;
    font-family:'JetBrains Mono',monospace; 
    font-size:10px;
    font-weight:500;
    transition:all 0.15s;
  }}
  .vbtn.active, .vbtn:hover {{
    background:{bg_active};
    border-color:{theme_colors['border_accent_hover']};
    color:{theme_colors['accent']};
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
    background:{bg_tooltip} !important;
    border:1px solid {theme_colors['border_accent_hover']} !important;
    border-radius:5px !important;
    color:{theme_colors['secondary_text']} !important;
    font-family:'JetBrains Mono',monospace !important;
    font-size:11px !important;
    padding:6px 10px !important;
    pointer-events:none;
    line-height:1.6;
  }}
  .tooltip-name {{ font-weight:700; color:{theme_colors['accent']}; margin-bottom:2px; }}
"""


# ── Model pipeline diagram iframe CSS ─────────────────────────────────────────
PIPELINE_CSS = """
*{margin:0;padding:0;box-sizing:border-box;}
body{background:transparent;font-family:'Courier New',monospace;padding:14px 4px 10px;}
.flow{display:flex;align-items:flex-start;gap:0;width:100%;}
.stage{flex:1;background:rgba(15,23,42,0.85);border-radius:7px;padding:16px 18px;}
.s1{border:1px solid rgba(74,222,128,0.3);}
.s2{border:1px solid rgba(148,163,184,0.18);}
.s3{border:1px solid rgba(168,139,250,0.25);margin-bottom:10px;}
.s4b{border:1px solid rgba(251,191,36,0.25);}
.s5{border:1px solid rgba(74,222,128,0.45);}
.arrow{display:flex;align-items:center;justify-content:center;padding:20px 8px 0;color:#334155;font-size:20px;flex-shrink:0;}
.label{font-size:10px;letter-spacing:0.14em;text-transform:uppercase;margin:0 0 6px 0;}
.l-green{color:#4ade80;}
.l-purple{color:#a78bfa;}
.l-amber{color:#fbbf24;}
.title{color:#e2e8f0;font-size:14px;font-weight:500;margin:0 0 6px 0;font-family:Arial,sans-serif;}
.desc{color:#64748b;font-size:12px;line-height:1.6;margin:0;}
.split{flex:1;display:flex;flex-direction:column;gap:10px;}
.note{color:#475569;font-size:11.5px;line-height:1.6;margin-top:12px;}
.note span{color:#94a3b8;}
.hi{color:#e2e8f0;}
.red{color:#ef4444;}
"""

# ── About page iframe CSS ──────────────────────────────────────────────────────
_ABOUT_CSS_BASE = """
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
  * { margin:0; padding:0; box-sizing:border-box; }
  html, body { width:100%; min-height:100%; background:__APP_BG__;
    font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif; color:#e2e8f0; }

  .page { max-width:960px; margin:0 auto; padding:3rem 2.5rem 6rem; }

  /* ── Hero ── */
  .hero { border-bottom:1px solid rgba(148,163,184,0.1); padding-bottom:2.5rem; margin-bottom:2.5rem; }
  .eyebrow { color:#4ade80; font-family:'Courier New',monospace; font-size:0.62rem;
    font-weight:700; letter-spacing:0.22em; text-transform:uppercase; margin-bottom:1rem;
    display:flex; align-items:center; gap:0.6rem; }
  .eyebrow::before { content:''; display:inline-block; width:28px; height:1px; background:#4ade80; }
  h1 { color:#ffffff; font-size:3.2rem; font-weight:300; line-height:1.05;
    letter-spacing:-0.03em; margin-bottom:0.5rem; }
  h1 span { color:#4ade80; }
  .tagline { color:#64748b; font-family:'Courier New',monospace; font-size:0.78rem;
    letter-spacing:0.1em; text-transform:uppercase; margin-bottom:1.8rem; }
  .hero-body { display:grid; grid-template-columns:1fr 1fr; gap:2rem; }
  .lead { color:#94a3b8; font-size:0.95rem; line-height:1.8; font-weight:300; }
  .lead b { color:#e2e8f0; font-weight:500; }
  .stat-row { display:flex; flex-direction:column; gap:1rem; }
  .stat { background:rgba(15,23,42,0.7); border:1px solid rgba(148,163,184,0.1);
    border-left:2px solid rgba(74,222,128,0.5); border-radius:5px; padding:0.9rem 1.1rem; }
  .stat-value { color:#ffffff; font-size:1.6rem; font-weight:300; line-height:1; margin-bottom:0.2rem; }
  .stat-label { color:#475569; font-family:'Courier New',monospace; font-size:0.62rem;
    letter-spacing:0.12em; text-transform:uppercase; }

  /* ── Section headings ── */
  .section-label { color:#4ade80; font-family:'Courier New',monospace; font-size:0.6rem;
    letter-spacing:0.2em; text-transform:uppercase; margin-bottom:0.3rem; }
  .section-title { color:#e2e8f0; font-size:1.1rem; font-weight:400; margin-bottom:0.3rem; }
  .section-desc { color:#64748b; font-size:0.82rem; line-height:1.65; margin-bottom:1.5rem; max-width:640px; }
  .divider { border:none; border-top:1px solid rgba(148,163,184,0.08); margin:2.5rem 0; }

  /* ── Feature cards ── */
  .features { display:grid; grid-template-columns:repeat(2,1fr); gap:1rem; margin-bottom:0.5rem; }
  .feature { background:rgba(15,23,42,0.6); border:1px solid rgba(148,163,184,0.09);
    border-radius:7px; padding:1.3rem 1.4rem; transition:border-color 0.2s; }
  .feature:hover { border-color:rgba(74,222,128,0.2); }
  .feature-num { color:#4ade80; font-family:'Courier New',monospace; font-size:0.6rem;
    letter-spacing:0.14em; text-transform:uppercase; margin-bottom:0.6rem; }
  .feature h3 { color:#f1f5f9; font-size:0.95rem; font-weight:500; margin-bottom:0.5rem; }
  .feature p { color:#64748b; font-size:0.82rem; line-height:1.65; }
  .feature p b { color:#94a3b8; font-weight:500; }

  /* ── Data section ── */
  .data-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:1rem; }
  .data-card { background:rgba(15,23,42,0.5); border:1px solid rgba(148,163,184,0.08);
    border-radius:6px; padding:1rem 1.1rem; }
  .data-card-label { color:#475569; font-family:'Courier New',monospace; font-size:0.58rem;
    letter-spacing:0.14em; text-transform:uppercase; margin-bottom:0.35rem; }
  .data-card-value { color:#cbd5e1; font-size:0.85rem; line-height:1.55; }

  /* ── Stack ── */
  .stack-section { margin-top:2rem; }
  .stack-group { margin-bottom:1.2rem; }
  .stack-group-label { color:#334155; font-family:'Courier New',monospace; font-size:0.6rem;
    letter-spacing:0.14em; text-transform:uppercase; margin-bottom:0.5rem; }
  .stack-row { display:flex; flex-wrap:wrap; gap:0.4rem; }
  .stack-tag { font-family:'Courier New',monospace; font-size:0.67rem; letter-spacing:0.05em;
    color:#64748b; border:1px solid rgba(148,163,184,0.12); border-radius:4px;
    padding:0.22rem 0.6rem; transition:all 0.15s; }
  .stack-tag:hover { border-color:rgba(74,222,128,0.3); color:#4ade80; }
  .stack-tag.hi { border-color:rgba(74,222,128,0.25); color:#4ade80; }

  /* ── Footer ── */
  .footer { margin-top:3rem; padding-top:1.5rem; border-top:1px solid rgba(148,163,184,0.08);
    display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:0.5rem; }
  .footer-left { color:#334155; font-family:'Courier New',monospace; font-size:0.65rem;
    letter-spacing:0.1em; }
  .footer-right { color:#1e293b; font-family:'Courier New',monospace; font-size:0.62rem;
    letter-spacing:0.08em; text-transform:uppercase; }
"""


def get_about_css(theme_colors):
    """Return about-page iframe CSS with the app background color injected."""
    app_bg = theme_colors.get('app_bg', '#060911')
    return _ABOUT_CSS_BASE.replace('__APP_BG__', app_bg)
