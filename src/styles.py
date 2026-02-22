"""
Styling and CSS management for H2C2 application
"""

def get_theme_colors(theme):
    """Get color scheme based on current theme"""
    if theme == 'dark':
        return {
            'app_bg': '#0a0e1a',
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
        padding-top: 1rem;
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
    
    /* Hide streamlit elements */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
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


def get_nav_css(theme, wrapper_class='nav-wrapper'):
    """Generate navigation bar CSS with theme support"""
    if theme == 'dark':
        nav_text = '#9ca3af'  # Light gray for normal text
        nav_accent = '#00ff41'  # Bright neon green for active/hover
        nav_hover = '#00ff41'  # Same bright green on hover
    else:  # light mode - use darker colors for visibility on white background
        nav_text = '#475569'  # Darker gray for better contrast
        nav_accent = '#2563eb'
        nav_hover = '#1d4ed8'
    
    return f"""
<style>
/* Force navigation row to use flexbox with center alignment */
[data-testid="stHorizontalBlock"]:has(.{wrapper_class}) {{
    display: flex !important;
    align-items: center !important;
    gap: 2rem;
    margin-bottom: 2rem;
    padding: 1rem 0;
}}

[data-testid="stHorizontalBlock"]:has(.{wrapper_class}) > div {{
    display: flex !important;
    align-items: center !important;
    width: auto !important;
    flex: 0 0 auto !important;
}}

/* NUCLEAR OPTION - Override ALL button states with maximum specificity */
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
    background: transparent !important;
    background-color: transparent !important;
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

/* Hover state - FORCE GREEN COLOR */
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
    background: transparent !important;
    background-color: transparent !important;
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
    background: transparent !important;
    border: 0px solid transparent !important;
    border-color: transparent !important;
    outline: 0px solid transparent !important;
    outline-color: transparent !important;
    box-shadow: none !important;
    color: {nav_text} !important;
}}- NO RED HIGHLIGHT */  
.{wrapper_class} button:active,
.{wrapper_class} button:active *,
.{wrapper_class} button[kind="secondary"]:active,
.{wrapper_class} button[kind="secondary"]:active *,
.{wrapper_class} button[data-testid="baseButton-secondary"]:active,
.{wrapper_class} button[data-testid="baseButton-secondary"]:active * {{
    background: transparent !important;
    background-color: transparent !important;
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
</style>
"""


def get_globe_button_css(theme_colors):
    """Generate theme-aware CSS for globe view controls, legend, and tooltips"""
    
    # Background colors for glass effect
    bg_glass = 'rgba(10,14,26,0.75)' if theme_colors['app_bg'] == '#0a0e1a' else 'rgba(241,245,249,0.9)'
    bg_tooltip = 'rgba(10,14,26,0.9)' if theme_colors['app_bg'] == '#0a0e1a' else 'rgba(255,255,255,0.95)'
    
    # Active/hover background
    bg_active = 'rgba(74,222,128,0.15)' if theme_colors['app_bg'] == '#0a0e1a' else 'rgba(37,99,235,0.15)'
    
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
