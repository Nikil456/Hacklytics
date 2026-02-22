import streamlit.components.v1 as components

from styles import get_about_css


def render_about_page(theme_colors):
    about_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>{get_about_css(theme_colors)}</style>
</head>
<body>
<div class="page">

  <!-- ── Hero ── -->
  <div class="hero">
    <p class="eyebrow">Hacklytics 2026 &nbsp;&middot;&nbsp; Databricks &times; United Nations</p>
    <h1>H2C2 &mdash; <span>Insight for Impact</span></h1>
    <p class="tagline">Humanitarian Health Command Center</p>

    <div class="hero-body">
      <p class="lead">
        Every year, billions of dollars in humanitarian aid are allocated without a clear picture of
        where the need is greatest. Funding reaches some regions generously while others &mdash;
        equally devastated &mdash; are barely touched.<br><br>
        <b>H2C2 closes that gap.</b> We fuse the UN&rsquo;s Humanitarian Needs Overview (HNO) and
        Humanitarian Response Plan (HRP) datasets into a single intelligence layer, then surface the
        mismatches that decision-makers miss.
      </p>
      <div class="stat-row">
        <div class="stat">
          <div class="stat-value">706</div>
          <div class="stat-label">High-neglect country-year instances identified</div>
        </div>
        <div class="stat">
          <div class="stat-value">165</div>
          <div class="stat-label">Countries in the forecasting pipeline</div>
        </div>
        <div class="stat">
          <div class="stat-value">2026&ndash;2030</div>
          <div class="stat-label">Five-year funding gap forecast horizon</div>
        </div>
      </div>
    </div>
  </div>

  <!-- ── What We Built ── -->
  <p class="section-label">What We Built</p>
  <p class="section-title">Four tools. One mission.</p>
  <p class="section-desc">
    Each component of H2C2 answers a different question a humanitarian analyst, donor, or UN official
    would ask when looking at the global crisis landscape.
  </p>

  <div class="features">
    <div class="feature">
      <p class="feature-num">01 &mdash; Dashboard</p>
      <h3>Live Crisis Globe</h3>
      <p>A 3D rotating Earth with pulsing markers at every active crisis zone.
         Colored by severity level &mdash; <b>red</b> for critical, <b>amber</b> for high,
         <b>blue</b> for medium. Click any point to zoom in; hover for the Health Vulnerability
         Index, funding coverage, and active project count.</p>
    </div>
    <div class="feature">
      <p class="feature-num">02 &mdash; Analytics</p>
      <h3>Crisis Funding Intelligence</h3>
      <p>Three interactive charts that measure the gap between <b>severity of need</b> and
         <b>resources allocated</b>. The Mismatch Leaderboard ranks the most overlooked countries.
         The Overlooked Quadrant maps every country by funding vs. need. The Sectoral Gap chart
         shows where the biggest coverage holes are by UN cluster.</p>
    </div>
    <div class="feature">
      <p class="feature-num">03 &mdash; Forecast</p>
      <h3>ML-Powered Funding Projections</h3>
      <p>A two-stage pipeline: <b>XGBoost</b> predicts humanitarian requirements from demographic
         signals (dependency ratio, population velocity, cost per beneficiary);
         <b>Prophet</b> extrapolates historical funding trends to 2030. The gap between the two
         surfaces where crises will be systematically underfunded before they make headlines.</p>
    </div>
    <div class="feature">
      <p class="feature-num">04 &mdash; Genie</p>
      <h3>Ask in Plain Language</h3>
      <p>Powered by <b>Databricks AI/BI Genie</b>. Any official can ask a natural-language
         question &mdash; &ldquo;Which countries have the highest mismatch score?&rdquo; or
         &ldquo;Show me funding gaps in Sub-Saharan Africa&rdquo; &mdash; and the system writes
         the SQL and returns a live answer instantly, no code required.</p>
    </div>
  </div>

  <hr class="divider">

  <!-- ── Data ── -->
  <p class="section-label">Data &amp; Methodology</p>
  <p class="section-title">Where the numbers come from.</p>
  <p class="section-desc">
    All figures are derived from publicly available UN humanitarian datasets processed through
    a reproducible Python pipeline.
  </p>

  <div class="data-grid">
    <div class="data-card">
      <p class="data-card-label">Primary Sources</p>
      <p class="data-card-value">UN OCHA Financial Tracking Service (FTS)<br>
        Humanitarian Needs Overview (HNO)<br>
        Humanitarian Response Plan (HRP)<br>
        UN HDX Population Data</p>
    </div>
    <div class="data-card">
      <p class="data-card-label">Model Architecture</p>
      <p class="data-card-value">XGBoost (requirements forecasting)<br>
        Walk-forward validation &mdash; train &le;2019<br>
        RMSE: 7.66M people &middot; $876M USD<br>
        Prophet (funding trend projection)</p>
    </div>
    <div class="data-card">
      <p class="data-card-label">Key Metrics Defined</p>
      <p class="data-card-value">Mismatch Score: normalized need minus normalized budget per PIN<br>
        Funding Gap: XGBoost requirements minus Prophet-projected funding<br>
        HVI: composite vulnerability index</p>
    </div>
  </div>

  <hr class="divider">

  <!-- ── Stack ── -->
  <p class="section-label">Tech Stack</p>
  <p class="section-title">Built on <a href="https://www.databricks.com/" target="_blank" style="color:inherit;text-decoration:none;">Databricks</a>.</p>

  <div class="stack-section">
    <div class="stack-group">
      <p class="stack-group-label">Data &amp; ML Platform</p>
      <div class="stack-row">
        <span class="stack-tag hi">Databricks</span>
        <span class="stack-tag hi">Delta Lake</span>
        <span class="stack-tag hi">Unity Catalog</span>
        <span class="stack-tag hi">AI/BI Genie</span>
        <span class="stack-tag">Spark MLlib</span>
        <span class="stack-tag">XGBoost</span>
        <span class="stack-tag">Prophet</span>
      </div>
    </div>
    <div class="stack-group">
      <p class="stack-group-label">Frontend &amp; Visualization</p>
      <div class="stack-row">
        <span class="stack-tag hi">Streamlit</span>
        <span class="stack-tag">Plotly</span>
        <span class="stack-tag">globe.gl</span>
        <span class="stack-tag">Three.js</span>
      </div>
    </div>
    <div class="stack-group">
      <p class="stack-group-label">Data Sources</p>
      <div class="stack-row">
        <span class="stack-tag">UN HDX</span>
        <span class="stack-tag">OCHA FTS</span>
        <span class="stack-tag">HNO / HRP Records 2000&ndash;2025</span>
      </div>
    </div>
  </div>

  <!-- ── Footer ── -->
  <div class="footer">
    <span class="footer-left">H2C2 &nbsp;&middot;&nbsp; Hacklytics 2026</span>
    <span class="footer-right">Georgia Tech &nbsp;&middot;&nbsp; Built for the <a href="https://www.un.org/en/" target="_blank" style="color:inherit;text-decoration:none;pointer-events:auto;">UN</a></span>
  </div>

</div>
</body>
</html>"""
    components.html(about_html, height=2400, scrolling=False)
