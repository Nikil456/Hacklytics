import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

from styles import get_globe_button_css


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
    """Crisis globe with pulsing markers, region controls, and theme-aware styling."""
    severity_colors = {5: '#ef4444', 4: '#f59e0b', 3: '#3b82f6'}
    entities   = generate_sample_entities()
    button_css = get_globe_button_css(theme_colors)

    js_data = ",\n      ".join(
        f'{{ lat:{row["lat"]}, lng:{row["lon"]}, name:"{row["name"]}", '
        f'hvi:{row["hvi"]}, fund:{row["fund"]}, sev:"{row["severity"]}", '
        f'color:"{severity_colors[row["severity"]]}", projects:{row["projects"]} }}'
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
