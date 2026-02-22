import os

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

from styles import get_globe_button_css

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')

# Geographic centroids for every ISO3 code in the dataset
_ISO3_COORDS = {
    'AFG': (34,   67,  'Afghanistan'),
    'BFA': (12,   -2,  'Burkina Faso'),
    'CAF': ( 7,   21,  'Cent. African Rep.'),
    'CMR': ( 5,   12,  'Cameroon'),
    'COD': (-4,   21,  'DR Congo'),
    'COL': ( 4,  -72,  'Colombia'),
    'GTM': (15,  -90,  'Guatemala'),
    'HND': (15,  -87,  'Honduras'),
    'HTI': (19,  -72,  'Haiti'),
    'MLI': (17,   -4,  'Mali'),
    'MMR': (21,   95,  'Myanmar'),
    'MOZ': (-18,  35,  'Mozambique'),
    'NER': (17,    8,  'Niger'),
    'NGA': ( 9,    8,  'Nigeria'),
    'SDN': (15,   30,  'Sudan'),
    'SLV': (13,  -89,  'El Salvador'),
    'SOM': ( 5,   46,  'Somalia'),
    'SSD': ( 7,   30,  'South Sudan'),
    'TCD': (15,   19,  'Chad'),
    'UKR': (48,   31,  'Ukraine'),
    'VEN': ( 8,  -66,  'Venezuela'),
    'YEM': (15,   48,  'Yemen'),
}

_SEVERITY_NUM = {'Critical': 5, 'High': 4, 'Medium': 3, 'Low': 2}
_SEVERITY_COLORS = {5: '#ef4444', 4: '#f59e0b', 3: '#3b82f6', 2: '#4ade80'}


def _infer_quartile(severity_score: float) -> str:
    """Assign severity quartile from the raw severity score for rows where
    the metrics CSV has no Severity Quartile (missing population data)."""
    if severity_score >= 2.0:
        return 'Critical'
    if severity_score >= 0.8:
        return 'High'
    if severity_score >= 0.3:
        return 'Medium'
    return 'Low'


def _fmt_millions(n: float) -> str:
    if n >= 1e6:
        return f"{n / 1e6:.1f}M"
    return f"{n / 1e3:.0f}K"


@st.cache_data
def generate_sample_entities() -> pd.DataFrame:
    summary  = pd.read_csv(os.path.join(DATA_DIR, 'country_level_summary (1).csv'))
    metrics  = pd.read_csv(os.path.join(DATA_DIR, 'humanitarian_analysis_country_metrics.csv'))

    # Keep only the columns we need from metrics
    metrics = metrics[['Country ISO3', 'Severity Quartile', 'Mismatch Score']].copy()

    df = summary.merge(metrics, on='Country ISO3', how='left')

    rows = []
    for _, row in df.iterrows():
        iso3 = row['Country ISO3']
        if iso3 not in _ISO3_COORDS:
            continue

        lat, lon, name = _ISO3_COORDS[iso3]

        # Severity quartile — use metrics value, fall back to inferred
        quartile = row.get('Severity Quartile')
        if not isinstance(quartile, str) or pd.isna(quartile):
            quartile = _infer_quartile(float(row['Severity_Score']))
        sev = _SEVERITY_NUM.get(quartile, 3)

        # Targeting coverage %
        in_need  = float(row['In Need'])
        targeted = float(row['Targeted']) if pd.notna(row['Targeted']) else 0.0
        fund     = round(targeted / in_need * 100, 1) if in_need > 0 else 0.0

        # Mismatch score (HVI proxy); derive for rows where it's missing
        mismatch = row.get('Mismatch Score')
        if pd.isna(mismatch):
            hvi = round(min(float(row['Severity_Score']) / 4.0, 1.0), 2)
        else:
            hvi = round(float(mismatch), 2)

        rows.append({
            'name':          name,
            'iso3':          iso3,
            'severity':      sev,
            'sev_label':     quartile,
            'lat':           lat,
            'lon':           lon,
            'hvi':           hvi,
            'fund':          fund,
            'in_need':       _fmt_millions(in_need),
            # 'projects' kept for backward compat with the sidebar badge
            'projects':      _fmt_millions(in_need),
        })

    df_out = pd.DataFrame(rows)
    # Sort: Critical → High → Medium → Low, then alphabetically
    df_out['_sort'] = df_out['severity'].map({5: 0, 4: 1, 3: 2, 2: 3})
    df_out = df_out.sort_values(['_sort', 'name']).drop(columns='_sort').reset_index(drop=True)
    return df_out


def create_home_globe_html():
    """Clean Earth globe for the home/landing page — no crisis markers."""
    return """<!DOCTYPE html>
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
<script src="https://unpkg.com/globe.gl@2.30.0/dist/globe.gl.min.js"></script>
<script>
  const globe = Globe({ animateIn: true })
    .globeImageUrl('//unpkg.com/three-globe/example/img/earth-blue-marble.jpg')
    .bumpImageUrl('//unpkg.com/three-globe/example/img/earth-topology.png')
    .backgroundColor('rgba(10,14,26,0)')
    .showAtmosphere(false)
    (document.getElementById('globeViz'));

  globe.controls().autoRotate      = true;
  globe.controls().autoRotateSpeed = 0.35;
  globe.controls().enableZoom      = true;
  globe.controls().minDistance     = 150;
  globe.controls().maxDistance     = 700;
  globe.pointOfView({ lat: 10, lng: 20, altitude: 1.8 }, 800);

  const el = document.getElementById('globeViz');
  el.addEventListener('mouseenter', () => { globe.controls().autoRotate = false; });
  el.addEventListener('mouseleave', () => { globe.controls().autoRotate = true; });
</script>
</body>
</html>"""


def create_globe_html(theme_colors):
    """Crisis globe with real humanitarian data, pulsing markers, region controls."""
    entities   = generate_sample_entities()
    button_css = get_globe_button_css(theme_colors)

    js_data = ",\n      ".join(
        f'{{ lat:{row["lat"]}, lng:{row["lon"]}, name:"{row["name"]}", '
        f'iso3:"{row["iso3"]}", hvi:{row["hvi"]}, fund:{row["fund"]}, '
        f'sev:{row["severity"]}, sev_label:"{row["sev_label"]}", '
        f'color:"{_SEVERITY_COLORS[row["severity"]]}", in_need:"{row["in_need"]}" }}'
        for _, row in entities.iterrows()
    )

    return f"""<!DOCTYPE html>
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
  <div class="leg"><div class="ldot" style="background:#4ade80;"></div><span>Low</span></div>
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
        <div>People in Need: <b>${{d.in_need}}</b></div>
        <div>Targeting Coverage: <b>${{d.fund}}%</b></div>
        <div>Mismatch Score: <b>${{d.hvi}}</b></div>
        <div>Severity: <b style="color:${{d.color}}">${{d.sev_label}}</b></div>
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
