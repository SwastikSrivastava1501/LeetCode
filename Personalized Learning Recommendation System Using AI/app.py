"""
app.py
------
Standalone Gradio application for BT3116 Personalized Learning Path Recommender.
Run with: python app.py

Project BT3116 · IILM University, Greater Noida · Session 2025-26
Team: Swastik Srivastava · Stuty Singh · Suryansh Singh · Suprit Dubey · Tanisha Priya
Guide: Dr. Jaswinder Singh Walia
"""

import numpy as np
import gradio as gr

from recommender import (
    get_recommendations,
    build_dag,
    get_all_courses,
    get_all_categories,
    get_all_levels,
)


# ──────────────────────────────────────────────
# CSS
# ──────────────────────────────────────────────

CUSTOM_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;600;700&display=swap');

:root {
  --bg-primary:   #0a0f1e;
  --bg-card:      #0f1a2e;
  --bg-input:     #111827;
  --accent-blue:  #38bdf8;
  --accent-violet:#a78bfa;
  --accent-green: #34d399;
  --accent-amber: #fbbf24;
  --text-primary: #f1f5f9;
  --text-muted:   #94a3b8;
  --border:       #1e3a5f;
}

body, .gradio-container {
  background: var(--bg-primary) !important;
  font-family: 'DM Sans', sans-serif !important;
  color: var(--text-primary) !important;
}

.app-header {
  background: linear-gradient(135deg, #0a1628 0%, #0f1f3d 50%, #0a1628 100%);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 32px 40px;
  margin-bottom: 24px;
  position: relative;
  overflow: hidden;
}
.app-header::before {
  content: '';
  position: absolute;
  top: -50%; left: -50%;
  width: 200%; height: 200%;
  background: radial-gradient(ellipse at 60% 40%, rgba(56,189,248,0.08) 0%, transparent 60%),
              radial-gradient(ellipse at 30% 70%, rgba(167,139,250,0.07) 0%, transparent 50%);
  pointer-events: none;
}
.app-title {
  font-family: 'Space Mono', monospace !important;
  font-size: 26px !important;
  font-weight: 700 !important;
  background: linear-gradient(90deg, #38bdf8, #a78bfa, #34d399);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0 !important;
  letter-spacing: -0.5px;
}
.app-subtitle {
  color: var(--text-muted) !important;
  font-size: 13px !important;
  margin-top: 6px !important;
  letter-spacing: 0.5px;
}

.gradio-group, .gr-group {
  background: var(--bg-card) !important;
  border: 1px solid var(--border) !important;
  border-radius: 12px !important;
}

select, .gr-dropdown select, textarea, input[type=range] {
  background: var(--bg-input) !important;
  border: 1px solid var(--border) !important;
  color: var(--text-primary) !important;
  border-radius: 8px !important;
  font-family: 'DM Sans', sans-serif !important;
}

label, .gr-label, .gr-form label {
  color: var(--accent-blue) !important;
  font-size: 12px !important;
  font-weight: 600 !important;
  letter-spacing: 0.8px !important;
  text-transform: uppercase !important;
}

button.primary {
  background: linear-gradient(135deg, #1d4ed8, #7c3aed) !important;
  border: none !important;
  border-radius: 10px !important;
  font-family: 'Space Mono', monospace !important;
  font-size: 13px !important;
  font-weight: 700 !important;
  letter-spacing: 1px !important;
  padding: 12px 28px !important;
  transition: all 0.25s ease !important;
  box-shadow: 0 4px 20px rgba(124, 58, 237, 0.4) !important;
}
button.primary:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 30px rgba(56, 189, 248, 0.5) !important;
}
button.secondary {
  background: transparent !important;
  border: 1px solid var(--border) !important;
  color: var(--text-muted) !important;
  border-radius: 10px !important;
  font-size: 12px !important;
}

.rec-card {
  background: linear-gradient(135deg, #0f1a2e 0%, #111827 100%);
  border: 1px solid #1e3a5f;
  border-radius: 12px;
  padding: 18px 22px;
  margin-bottom: 14px;
  position: relative;
  overflow: hidden;
}
.rec-card::before {
  content: '';
  position: absolute;
  left: 0; top: 0; bottom: 0;
  width: 4px;
  background: linear-gradient(180deg, #38bdf8, #a78bfa);
  border-radius: 4px 0 0 4px;
}
.rec-rank   { font-family: 'Space Mono', monospace; font-size: 28px; font-weight: 700; color: #1e3a5f; }
.rec-title  { font-weight: 700; font-size: 16px; color: #f1f5f9; }
.rec-meta   { font-size: 12px; color: #64748b; margin: 6px 0; }
.rec-badge  { display: inline-block; padding: 3px 10px; border-radius: 20px; font-size: 11px; font-weight: 600; margin-right: 6px; }
.badge-beg  { background: rgba(34,197,94,0.15);  color: #22c55e;  border: 1px solid #22c55e40; }
.badge-int  { background: rgba(245,158,11,0.15); color: #f59e0b;  border: 1px solid #f59e0b40; }
.badge-adv  { background: rgba(239,68,68,0.15);  color: #ef4444;  border: 1px solid #ef444440; }
.badge-cat  { background: rgba(56,189,248,0.10); color: #38bdf8;  border: 1px solid #38bdf840; }
.sim-bar-wrap { background: #1e293b; border-radius: 20px; height: 8px; margin: 10px 0; overflow: hidden; }
.sim-bar-fill { height: 100%; border-radius: 20px; background: linear-gradient(90deg, #38bdf8, #a78bfa); }
.rec-explain { font-size: 12px; color: #7c9bc2; margin-top: 8px; }
.rec-prereq  { font-size: 11px; color: #475569; margin-top: 5px; }

.stats-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-bottom: 20px; }
.stat-card  { background: linear-gradient(135deg, #0f1a2e, #111827); border: 1px solid #1e3a5f; border-radius: 10px; padding: 16px; text-align: center; }
.stat-val   { font-family: 'Space Mono', monospace; font-size: 24px; font-weight: 700; }
.stat-lbl   { font-size: 11px; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px; margin-top: 4px; }

.section-header {
  font-family: 'Space Mono', monospace;
  font-size: 11px;
  color: #38bdf8;
  letter-spacing: 2px;
  text-transform: uppercase;
  margin-bottom: 14px;
  padding-bottom: 8px;
  border-bottom: 1px solid #1e3a5f;
}
"""

LEVEL_BADGE = {"Beginner": "badge-beg", "Intermediate": "badge-int", "Advanced": "badge-adv"}

HEADER_HTML = """
<div class='app-header'>
  <div class='app-title'>⚡ AI Learning Path Recommender</div>
  <div class='app-subtitle'>
    PROJECT BT3116 &nbsp;·&nbsp; IILM UNIVERSITY, GREATER NOIDA &nbsp;·&nbsp;
    TF-IDF + COSINE SIMILARITY ENGINE
  </div>
</div>
"""


# ──────────────────────────────────────────────
# HTML builder
# ──────────────────────────────────────────────

def build_results_html(course_name, recs):
    if not recs:
        return "<p style='color:#ef4444;'>No recommendations found.</p>"

    avg_sim    = np.mean([r["similarity"] for r in recs])
    categories = set(r["category"] for r in recs)

    html = f"""
    <div style='padding:4px'>
      <div class='section-header'>📊 Result Summary — {course_name}</div>
      <div class='stats-grid'>
        <div class='stat-card'>
          <div class='stat-val' style='color:#38bdf8'>{len(recs)}</div>
          <div class='stat-lbl'>Recommendations</div>
        </div>
        <div class='stat-card'>
          <div class='stat-val' style='color:#a78bfa'>{avg_sim:.1f}%</div>
          <div class='stat-lbl'>Avg. Similarity</div>
        </div>
        <div class='stat-card'>
          <div class='stat-val' style='color:#34d399'>{len(categories)}</div>
          <div class='stat-lbl'>Domains Covered</div>
        </div>
      </div>
      <div class='section-header'>🎯 Ranked Recommendations</div>
    """

    for r in recs:
        badge_cls = LEVEL_BADGE.get(r["level"], "badge-int")
        bar_width = max(5, int(r["similarity"]))
        html += f"""
        <div class='rec-card'>
          <div style='display:flex; align-items:center; gap:14px;'>
            <div class='rec-rank'>#{r['rank']:02d}</div>
            <div style='flex:1'>
              <div class='rec-title'>{r['name']}</div>
              <div class='rec-meta'>
                <span class='rec-badge {badge_cls}'>{r['level']}</span>
                <span class='rec-badge badge-cat'>{r['category']}</span>
                <span style='color:#475569'>⏱ {r['duration']}</span>
              </div>
              <div class='sim-bar-wrap'>
                <div class='sim-bar-fill' style='width:{bar_width}%'></div>
              </div>
              <div style='display:flex; justify-content:space-between; font-size:11px; color:#475569;'>
                <span>Similarity Match</span>
                <span style='color:#38bdf8; font-family:Space Mono,monospace; font-weight:700'>{r['similarity']}%</span>
              </div>
              <div class='rec-explain'>💡 {r['explanation']}</div>
              <div class='rec-prereq'>🔗 Prerequisites: {r['prerequisites']}</div>
            </div>
          </div>
        </div>
        """

    html += "</div>"
    return html


# ──────────────────────────────────────────────
# Gradio callbacks
# ──────────────────────────────────────────────

def recommend_and_visualize(course_name, top_k, filter_cat, filter_level):
    recs, err = get_recommendations(course_name, int(top_k), filter_cat, filter_level)
    if err:
        return f"<p style='color:#ef4444;'>{err}</p>", None
    html = build_results_html(course_name, recs)
    dag  = build_dag(course_name, max_depth=3)
    return html, dag


# ──────────────────────────────────────────────
# Build UI
# ──────────────────────────────────────────────

ALL_COURSES = get_all_courses()
ALL_CATS    = get_all_categories()
ALL_LEVELS  = get_all_levels()


def build_app():
    with gr.Blocks(css=CUSTOM_CSS, title="AI Learning Path Recommender") as demo:

        gr.HTML(HEADER_HTML)

        with gr.Row():
            with gr.Column(scale=1):
                with gr.Group():
                    gr.HTML("<div style='padding:16px 18px 4px; font-family:Space Mono,monospace; font-size:11px; color:#38bdf8; letter-spacing:2px; text-transform:uppercase;'>🎛  Configuration</div>")
                    course_dd  = gr.Dropdown(choices=ALL_COURSES, value=ALL_COURSES[0],
                                             label="Select Your Current Course",
                                             info="The course you have completed or are taking")
                    k_slider   = gr.Slider(minimum=1, maximum=10, step=1, value=5,
                                           label="Number of Recommendations (Top-K)")
                    cat_dd     = gr.Dropdown(choices=ALL_CATS,    value="All", label="Filter by Domain Category")
                    level_dd   = gr.Dropdown(choices=ALL_LEVELS,  value="All", label="Filter by Difficulty Level")
                    submit_btn = gr.Button("🚀  Generate My Learning Path", variant="primary")
                    clear_btn  = gr.Button("↺  Reset",                      variant="secondary")

                with gr.Group():
                    gr.HTML("""
                    <div style='padding:14px 18px;'>
                      <div style='font-family:Space Mono,monospace; font-size:10px; color:#38bdf8; letter-spacing:2px; text-transform:uppercase; margin-bottom:12px;'>ℹ️  How It Works</div>
                      <div style='font-size:12px; color:#64748b; line-height:1.8;'>
                        <b style='color:#94a3b8;'>1. Feature Engineering</b><br>Multi-attribute weighted feature strings<br><br>
                        <b style='color:#94a3b8;'>2. TF-IDF Vectorization</b><br>Bigram TF-IDF with sublinear scaling<br><br>
                        <b style='color:#94a3b8;'>3. Cosine Similarity</b><br>20×20 similarity matrix<br><br>
                        <b style='color:#94a3b8;'>4. DAG Path Generator</b><br>NetworkX sequential learning graph<br><br>
                        <b style='color:#94a3b8;'>5. Evaluation</b><br>NDCG@K · MAP@K · Precision@K
                      </div>
                    </div>
                    """)

            with gr.Column(scale=2):
                with gr.Tabs():
                    with gr.TabItem("📋 Recommendations"):
                        rec_output = gr.HTML(label="Recommendations")
                    with gr.TabItem("🗺️ Learning Path DAG"):
                        dag_output = gr.Plot(label="Learning Path Graph")

        submit_btn.click(
            fn=recommend_and_visualize,
            inputs=[course_dd, k_slider, cat_dd, level_dd],
            outputs=[rec_output, dag_output],
        )

        def reset():
            return ALL_COURSES[0], 5, "All", "All", "", None

        clear_btn.click(fn=reset,
                        outputs=[course_dd, k_slider, cat_dd, level_dd, rec_output, dag_output])

        gr.HTML("""
        <div style='text-align:center; padding:20px 0 8px; color:#1e3a5f; font-size:11px; font-family:Space Mono,monospace; letter-spacing:1px;'>
          IILM UNIVERSITY · SCHOOL OF COMPUTER SCIENCE & ENGINEERING ·
          SWASTIK · STUTY · SURYANSH · SUPRIT · TANISHA · GUIDE: DR. J.S. WALIA
        </div>
        """)

    return demo


if __name__ == "__main__":
    app = build_app()
    app.launch(share=True, debug=False)
