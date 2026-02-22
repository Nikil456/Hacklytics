import streamlit as st
import plotly.graph_objects as go

from utils import (
    SEVERITY_ORDER, SEVERITY_COLORS,
    _AXIS_BASE, _chart_layout,
    chart_caption, section_header,
    load_country_metrics, load_sector_benchmarking,
)


# ── Chart builders ─────────────────────────────────────────────────────────────

def _build_chart_a(df):
    top10 = df.nlargest(10, 'Mismatch Score').sort_values('Mismatch Score')
    colors = [SEVERITY_COLORS.get(s, '#64748b') for s in top10['Severity Quartile']]

    hover = [
        f"<b>{name}</b><br>Mismatch Score: {ms:.3f}<br>People in Need: {int(n):,}<br>Severity: {sev}"
        for name, ms, n, sev in zip(
            top10['Country Name'], top10['Mismatch Score'],
            top10['In Need'], top10['Severity Quartile'],
        )
    ]

    fig = go.Figure(go.Bar(
        x=top10['Mismatch Score'],
        y=top10['Country Name'],
        orientation='h',
        marker=dict(color=colors, line=dict(width=0)),
        hovertemplate='%{customdata}<extra></extra>',
        customdata=hover,
        showlegend=False,
    ))

    for sev, col in SEVERITY_COLORS.items():
        fig.add_trace(go.Bar(
            x=[None], y=[None], orientation='h',
            name=sev, marker=dict(color=col),
            showlegend=True,
        ))

    layout = _chart_layout(
        title='Mismatch Leaderboard — Top 10 Overlooked Countries',
        height=420,
        xaxis=dict(**_AXIS_BASE, title='Mismatch Score'),
        yaxis=dict(**{**_AXIS_BASE, 'tickfont': dict(family='Courier New, monospace', color='#e2e8f0', size=12)}, title=''),
        legend=dict(
            orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1,
            font=dict(family='Courier New, monospace', color='#94a3b8', size=11),
        ),
        barmode='overlay',
    )
    fig.update_layout(**layout)
    return fig


def _build_chart_b(df):
    top5_names = df.nlargest(5, 'Mismatch Score')['Country Name'].tolist()

    fig = go.Figure()

    for sev in SEVERITY_ORDER:
        sub = df[df['Severity Quartile'] == sev]
        if sub.empty:
            continue
        fig.add_trace(go.Scatter(
            x=sub['Normalized Budget per PIN'],
            y=sub['Normalized Need Prevalence'],
            mode='markers',
            name=sev,
            marker=dict(
                color=SEVERITY_COLORS[sev],
                size=7,
                opacity=0.75,
                line=dict(width=0.5, color='rgba(255,255,255,0.2)'),
            ),
            hovertemplate=(
                '<b>%{text}</b><br>'
                'Funding Level: %{x:.3f}<br>'
                'Need Level: %{y:.3f}<extra></extra>'
            ),
            text=sub['Country Name'],
        ))

    for coord, axis in [(0.5, 'x'), (0.5, 'y')]:
        line_kw = dict(
            line=dict(color='rgba(148,163,184,0.25)', width=1, dash='dot'),
            layer='below',
        )
        if axis == 'x':
            fig.add_vline(x=coord, **line_kw)
        else:
            fig.add_hline(y=coord, **line_kw)

    quad_labels = [
        (0.12, 0.88, 'OVERLOOKED', '#ef4444'),
        (0.72, 0.12, 'WELL RESOURCED', '#4ade80'),
        (0.72, 0.88, 'HIGH NEED &<br>HIGH BUDGET', '#f59e0b'),
        (0.12, 0.12, 'LOW NEED &<br>LOW BUDGET', '#3b82f6'),
    ]
    for qx, qy, label, col in quad_labels:
        fig.add_annotation(
            x=qx, y=qy, text=label, showarrow=False,
            font=dict(family='Courier New, monospace', size=9, color=col),
            opacity=0.5,
        )

    top5 = df[df['Country Name'].isin(top5_names)]
    for _, row in top5.iterrows():
        fig.add_annotation(
            x=row['Normalized Budget per PIN'],
            y=row['Normalized Need Prevalence'],
            text=f"  {row['Country Name']}",
            showarrow=False,
            font=dict(family='Courier New, monospace', size=9, color='#e2e8f0'),
            xanchor='left',
        )

    layout = _chart_layout(
        title='Overlooked Quadrant — Need vs. Budget Landscape',
        height=420,
        xaxis=dict(**_AXIS_BASE, title='Funding Level (0 = Lowest, 1 = Highest)', range=[-0.05, 1.1]),
        yaxis=dict(**_AXIS_BASE, title='Need Level (0 = Lowest, 1 = Highest)', range=[-0.05, 1.1]),
        legend=dict(
            orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1,
            font=dict(family='Courier New, monospace', color='#94a3b8', size=11),
        ),
    )
    fig.update_layout(**layout)
    return fig


def _build_chart_c(sector_df):
    top10 = sector_df.nlargest(10, 'In Need').sort_values('In Need', ascending=True)

    hover_need = [
        f"<b>{name}</b><br>People in Need: {int(n):,}<br>Coverage: {c:.0%}"
        for name, n, c in zip(top10['Sector Name'], top10['In Need'], top10['Coverage'])
    ]
    hover_tgt = [
        f"<b>{name}</b><br>People Targeted: {int(t):,}<br>Coverage: {c:.0%}"
        for name, t, c in zip(top10['Sector Name'], top10['Targeted'], top10['Coverage'])
    ]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=top10['In Need'],
        y=top10['Sector Name'],
        orientation='h',
        name='People in Need',
        marker=dict(color='rgba(239,68,68,0.8)', line=dict(width=0)),
        hovertemplate='%{customdata}<extra></extra>',
        customdata=hover_need,
    ))
    fig.add_trace(go.Bar(
        x=top10['Targeted'],
        y=top10['Sector Name'],
        orientation='h',
        name='People Targeted',
        marker=dict(color='rgba(74,222,128,0.75)', line=dict(width=0)),
        hovertemplate='%{customdata}<extra></extra>',
        customdata=hover_tgt,
    ))

    layout = _chart_layout(
        title='Sectoral Coverage Gaps — People in Need vs. Targeted',
        height=440,
        barmode='group',
        xaxis=dict(
            **_AXIS_BASE,
            title='Number of People',
            tickformat=',.0s',
        ),
        yaxis=dict(**{**_AXIS_BASE, 'tickfont': dict(family='Courier New, monospace', color='#e2e8f0', size=12)}, title=''),
        legend=dict(
            orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1,
            font=dict(family='Courier New, monospace', color='#94a3b8', size=11),
        ),
        margin=dict(l=12, r=12, t=52, b=16),
    )
    fig.update_layout(**layout)
    return fig


# ── Page renderer ──────────────────────────────────────────────────────────────

def render_analytics_page():
    df = load_country_metrics()
    sector_df = load_sector_benchmarking()

    st.markdown("""
    <div style="padding: 1.2rem 0 0.75rem 0;">
        <p style="color:#4ade80; font-family:'Courier New',monospace; font-size:0.75rem;
                  font-weight:700; letter-spacing:0.22em; text-transform:uppercase; margin:0 0 0.5rem 0;">
            HUMANITARIAN ANALYTICS
        </p>
        <h2 style="color:#ffffff; font-size:2.6rem; font-weight:300; margin:0 0 0.6rem 0; letter-spacing:-0.02em;">
            Crisis Funding Intelligence
        </h2>
        <p style="color:#94a3b8; font-size:0.95rem; max-width:780px; line-height:1.75; margin:0;">
            Not all humanitarian crises receive equal attention. These visualizations measure the gap between
            <span style="color:#e2e8f0; font-weight:500;">the severity of human need</span> and
            <span style="color:#e2e8f0; font-weight:500;">the financial resources allocated</span> per person —
            surfacing overlooked emergencies that require immediate advocacy and action.
        </p>
    </div>
    <div style="border-top:1px solid rgba(148,163,184,0.1); margin: 0.75rem 0 1.5rem 0;"></div>
    """, unsafe_allow_html=True)

    with st.expander("▸  HOW TO READ THIS DASHBOARD — Metric Definitions", expanded=False):
        st.markdown("""
        <div style="display:grid; grid-template-columns:repeat(2,1fr); gap:1rem 2.5rem; padding:0.5rem 0;">
            <div>
                <p style="color:#4ade80; font-family:'Courier New',monospace; font-size:0.7rem;
                          letter-spacing:0.12em; text-transform:uppercase; margin:0 0 0.3rem 0;">Need Prevalence</p>
                <p style="color:#94a3b8; font-size:0.88rem; line-height:1.7; margin:0 0 0.8rem 0;">
                    <em>People in Need ÷ Total Population.</em> Measures how deeply a country is affected
                    relative to its size. A score of 0.8 means 80% of the population requires humanitarian assistance.
                </p>
            </div>
            <div>
                <p style="color:#4ade80; font-family:'Courier New',monospace; font-size:0.7rem;
                          letter-spacing:0.12em; text-transform:uppercase; margin:0 0 0.3rem 0;">Budget per Person in Need (PIN)</p>
                <p style="color:#94a3b8; font-size:0.88rem; line-height:1.7; margin:0 0 0.8rem 0;">
                    <em>Revised Requirements (USD) ÷ People in Need.</em> How many dollars are budgeted for
                    every person requiring assistance. A low number signals underfunding relative to the scale of need.
                </p>
            </div>
            <div>
                <p style="color:#4ade80; font-family:'Courier New',monospace; font-size:0.7rem;
                          letter-spacing:0.12em; text-transform:uppercase; margin:0 0 0.3rem 0;">Mismatch Score</p>
                <p style="color:#94a3b8; font-size:0.88rem; line-height:1.7; margin:0 0 0.8rem 0;">
                    <em>Normalized Need Prevalence − Normalized Budget per PIN.</em> The core metric of this dashboard.
                    A <span style="color:#ef4444; font-weight:500;">high positive score</span> (near +1) means a country has
                    extreme needs but very little funding — it is "overlooked."
                    A <span style="color:#4ade80; font-weight:500;">negative score</span> means funding is proportionally
                    adequate or generous relative to need.
                </p>
            </div>
            <div>
                <p style="color:#4ade80; font-family:'Courier New',monospace; font-size:0.7rem;
                          letter-spacing:0.12em; text-transform:uppercase; margin:0 0 0.3rem 0;">Severity Quartile</p>
                <p style="color:#94a3b8; font-size:0.88rem; line-height:1.7; margin:0 0 0.8rem 0;">
                    Countries are ranked by Need Prevalence and divided into four equal groups:
                    <span style="color:#3b82f6; font-weight:500;">Low</span> ·
                    <span style="color:#f59e0b; font-weight:500;">Medium</span> ·
                    <span style="color:#f97316; font-weight:500;">High</span> ·
                    <span style="color:#ef4444; font-weight:500;">Critical</span>.
                    This grouping is used to color-code every chart consistently.
                </p>
            </div>
            <div>
                <p style="color:#4ade80; font-family:'Courier New',monospace; font-size:0.7rem;
                          letter-spacing:0.12em; text-transform:uppercase; margin:0 0 0.3rem 0;">Targeting Efficiency</p>
                <p style="color:#94a3b8; font-size:0.88rem; line-height:1.7; margin:0 0 0.8rem 0;">
                    <em>People Targeted ÷ People in Need.</em> Values above 1.0 indicate over-targeting
                    (aid reaches more than the estimated need). Values below 1.0 indicate a coverage gap.
                </p>
            </div>
            <div>
                <p style="color:#4ade80; font-family:'Courier New',monospace; font-size:0.7rem;
                          letter-spacing:0.12em; text-transform:uppercase; margin:0 0 0.3rem 0;">Sectoral Clusters</p>
                <p style="color:#94a3b8; font-size:0.88rem; line-height:1.7; margin:0 0 0.8rem 0;">
                    The UN organizes humanitarian response into thematic "clusters": Food Security, Health,
                    Protection, Water &amp; Sanitation, etc. Each cluster has separate funding and targeting
                    plans, which can diverge significantly from the scale of actual need.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    total_countries = len(df)
    critical_count = (df['Severity Quartile'] == 'Critical').sum()
    max_mismatch = df['Mismatch Score'].max()
    worst_country = df.loc[df['Mismatch Score'].idxmax(), 'Country Name']

    s1, s2, s3, s4 = st.columns(4)
    for col, label, value, sub in [
        (s1, 'COUNTRIES ANALYZED', str(total_countries), 'with complete data'),
        (s2, 'CRITICAL SEVERITY', str(critical_count), 'require urgent action'),
        (s3, 'MAX MISMATCH SCORE', f'{max_mismatch:.3f}', 'highest gap detected'),
        (s4, 'MOST OVERLOOKED', worst_country, 'highest mismatch country'),
    ]:
        col.markdown(f"""
        <div style="background:rgba(15,23,42,0.7); border:1px solid rgba(148,163,184,0.1);
                    border-radius:6px; padding:1.1rem 1.3rem; border-left:2px solid rgba(74,222,128,0.5);">
            <p style="color:#4ade80; font-family:'Courier New',monospace; font-size:0.67rem;
                      letter-spacing:0.15em; text-transform:uppercase; margin:0 0 0.35rem 0;">{label}</p>
            <p style="color:#ffffff; font-size:1.8rem; font-weight:300; margin:0 0 0.2rem 0; line-height:1.1;">{value}</p>
            <p style="color:#475569; font-size:0.76rem; margin:0; font-family:'Courier New',monospace;">{sub}</p>
        </div>
        """, unsafe_allow_html=True)

    section_header(
        'CHART A + B — COUNTRY ANALYSIS',
        'Who is Being Overlooked?',
        'The left chart ranks countries by their Mismatch Score — the wider the bar, the more underfunded '
        'a country is relative to its crisis severity. The right chart maps every country into one of four '
        'quadrants: countries in the <strong style="color:#ef4444;">top-left</strong> have critical needs '
        'but very little funding and deserve the most advocacy attention.',
    )
    col_a, col_b = st.columns(2, gap='medium')
    with col_a:
        st.plotly_chart(_build_chart_a(df), use_container_width=True, config={'displayModeBar': False})
        chart_caption(
            'Bars represent Mismatch Score (0–1 scale). '
            'Color indicates Severity Quartile. Hover over a bar for full details.'
        )
    with col_b:
        st.plotly_chart(_build_chart_b(df), use_container_width=True, config={'displayModeBar': False})
        chart_caption(
            'Each dot is a country. Dotted lines divide the space into four quadrants. '
            'Top-5 most overlooked countries are labeled. Hover for country name and scores.'
        )

    section_header(
        'CHART C — SECTOR ANALYSIS',
        'Where Are the Biggest Coverage Gaps by Sector?',
        'Each humanitarian sector (Food Security, Health, Protection, etc.) has its own response plan. '
        'This chart compares how many people <em>need</em> assistance in each sector versus how many '
        'are actually <em>targeted</em> for aid. A large red bar with a small green bar signals a critical '
        'gap — the sector is overwhelmed and under-resourced.',
    )
    st.plotly_chart(_build_chart_c(sector_df), use_container_width=True, config={'displayModeBar': False})
    chart_caption(
        'Top 10 sectors by total people in need, sorted largest to smallest. '
        'Red = total people requiring assistance. Green = people actually targeted by response plans. '
        'Hover for exact numbers and coverage percentage.'
    )

    st.markdown("""
    <div style="border-top:1px solid rgba(148,163,184,0.1); margin-top:1.5rem; padding:1.5rem 0 0.5rem 0;">
        <p style="color:#4ade80; font-family:'Courier New',monospace; font-size:0.67rem;
                  letter-spacing:0.18em; text-transform:uppercase; margin:0 0 1rem 0;">KEY FINDINGS</p>
        <div style="display:grid; grid-template-columns:repeat(3,1fr); gap:1rem;">
            <div style="background:rgba(15,23,42,0.5); border:1px solid rgba(148,163,184,0.08);
                        border-left:2px solid rgba(239,68,68,0.5); border-radius:5px; padding:1rem 1.1rem;">
                <p style="color:#ef4444; font-family:'Courier New',monospace; font-size:0.68rem;
                          letter-spacing:0.1em; text-transform:uppercase; margin:0 0 0.5rem 0;">01 — Overlooked Crises</p>
                <p style="color:#94a3b8; font-size:0.9rem; line-height:1.7; margin:0;">
                    <span style="color:#e2e8f0; font-weight:500;">Sudan</span> holds the highest Mismatch Score
                    (0.59) — 64% of its 47.5M population is in need, yet the humanitarian budget amounts to just
                    <span style="color:#e2e8f0; font-weight:500;">~$1,342 per person</span>.
                    <span style="color:#e2e8f0; font-weight:500;">Afghanistan</span> follows at 0.53:
                    57% of its population requires assistance with only ~$1,174 budgeted per person in need —
                    the lowest Budget per PIN of any Critical-tier country.
                </p>
            </div>
            <div style="background:rgba(15,23,42,0.5); border:1px solid rgba(148,163,184,0.08);
                        border-left:2px solid rgba(245,158,11,0.5); border-radius:5px; padding:1rem 1.1rem;">
                <p style="color:#f59e0b; font-family:'Courier New',monospace; font-size:0.68rem;
                          letter-spacing:0.1em; text-transform:uppercase; margin:0 0 0.5rem 0;">02 — Targeting Efficiency Gap</p>
                <p style="color:#94a3b8; font-size:0.9rem; line-height:1.7; margin:0;">
                    <span style="color:#e2e8f0; font-weight:500;">Colombia</span> is the most undertargeted
                    country in the dataset — response plans reach only
                    <span style="color:#e2e8f0; font-weight:500;">22% of the 9M people in need</span>,
                    leaving 7.1M without a targeting commitment. DRC similarly targets just 51.7% of
                    its 21.2M caseload. Both countries show that scale of need alone does not guarantee
                    proportional operational coverage.
                </p>
            </div>
            <div style="background:rgba(15,23,42,0.5); border:1px solid rgba(148,163,184,0.08);
                        border-left:2px solid rgba(59,130,246,0.5); border-radius:5px; padding:1rem 1.1rem;">
                <p style="color:#3b82f6; font-family:'Courier New',monospace; font-size:0.68rem;
                          letter-spacing:0.1em; text-transform:uppercase; margin:0 0 0.5rem 0;">03 — Funding Paradox</p>
                <p style="color:#94a3b8; font-size:0.9rem; line-height:1.7; margin:0;">
                    <span style="color:#e2e8f0; font-weight:500;">Somalia</span> — a Critical-severity crisis —
                    receives <span style="color:#e2e8f0; font-weight:500;">~$4,287 per person in need</span>,
                    more than any other country in the dataset. Meanwhile
                    <span style="color:#e2e8f0; font-weight:500;">Guatemala</span>, rated Low severity,
                    receives just ~$335 per PIN. This inversion signals that funding decisions are
                    driven partly by geopolitical visibility rather than the depth of humanitarian need alone.
                </p>
            </div>
        </div>
    </div>
    <div style="height:3rem;"></div>
    """, unsafe_allow_html=True)
