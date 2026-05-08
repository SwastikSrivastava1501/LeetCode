"""
recommender.py
--------------
Core recommendation engine for BT3116 Personalized Learning Path Recommender.

Project BT3116 · IILM University, Greater Noida · Session 2025-26
Team: Swastik Srivastava · Stuty Singh · Suryansh Singh · Suprit Dubey · Tanisha Priya
Guide: Dr. Jaswinder Singh Walia
"""

import numpy as np
import pandas as pd
import networkx as nx
import plotly.graph_objects as go
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ──────────────────────────────────────────────
# Dataset
# ──────────────────────────────────────────────

COURSES_DATA = [
    {"name": "Python Programming Fundamentals", "category": "Programming", "level": "Beginner",
     "bloom_level": 1, "skills": "python variables loops functions data types debugging", "duration": 20, "prerequisites": ""},
    {"name": "Data Structures and Algorithms", "category": "Programming", "level": "Intermediate",
     "bloom_level": 3, "skills": "python arrays linked lists trees graphs sorting searching recursion complexity", "duration": 35, "prerequisites": "Python Programming Fundamentals"},
    {"name": "Statistics for Data Science", "category": "Data Science", "level": "Beginner",
     "bloom_level": 2, "skills": "statistics probability distributions hypothesis testing mean variance regression", "duration": 25, "prerequisites": ""},
    {"name": "Machine Learning Fundamentals", "category": "AI/ML", "level": "Intermediate",
     "bloom_level": 3, "skills": "machine learning supervised unsupervised classification regression clustering scikit-learn", "duration": 40, "prerequisites": "Python Programming Fundamentals Statistics for Data Science"},
    {"name": "Deep Learning with TensorFlow", "category": "AI/ML", "level": "Advanced",
     "bloom_level": 5, "skills": "deep learning neural networks tensorflow keras CNNs RNNs backpropagation GPU", "duration": 50, "prerequisites": "Machine Learning Fundamentals"},
    {"name": "Natural Language Processing", "category": "AI/ML", "level": "Advanced",
     "bloom_level": 5, "skills": "NLP text processing tokenization transformers BERT sentiment analysis text classification", "duration": 45, "prerequisites": "Deep Learning with TensorFlow"},
    {"name": "HTML CSS Web Basics", "category": "Web Development", "level": "Beginner",
     "bloom_level": 1, "skills": "html css web design layouts flexbox grid responsive design", "duration": 18, "prerequisites": ""},
    {"name": "JavaScript Essentials", "category": "Web Development", "level": "Beginner",
     "bloom_level": 2, "skills": "javascript DOM events async promises fetch API ES6 web programming", "duration": 22, "prerequisites": "HTML CSS Web Basics"},
    {"name": "React.js Frontend Development", "category": "Web Development", "level": "Intermediate",
     "bloom_level": 3, "skills": "react components hooks state props JSX frontend SPA routing redux", "duration": 30, "prerequisites": "JavaScript Essentials"},
    {"name": "Node.js Backend Development", "category": "Web Development", "level": "Intermediate",
     "bloom_level": 3, "skills": "node.js express REST API backend server authentication JWT database MongoDB", "duration": 28, "prerequisites": "JavaScript Essentials"},
    {"name": "SQL and Database Design", "category": "Data Science", "level": "Beginner",
     "bloom_level": 2, "skills": "SQL databases tables queries joins normalization relational CRUD postgres mysql", "duration": 20, "prerequisites": ""},
    {"name": "Data Analysis with Pandas", "category": "Data Science", "level": "Intermediate",
     "bloom_level": 3, "skills": "pandas numpy data wrangling EDA analysis visualization matplotlib seaborn data cleaning", "duration": 25, "prerequisites": "Python Programming Fundamentals Statistics for Data Science"},
    {"name": "Computer Vision with OpenCV", "category": "AI/ML", "level": "Advanced",
     "bloom_level": 5, "skills": "computer vision OpenCV image processing detection classification object recognition CNN", "duration": 42, "prerequisites": "Deep Learning with TensorFlow"},
    {"name": "Cloud Computing with AWS", "category": "Cloud Computing", "level": "Intermediate",
     "bloom_level": 3, "skills": "AWS cloud EC2 S3 Lambda deployment DevOps microservices containerization", "duration": 32, "prerequisites": "Python Programming Fundamentals"},
    {"name": "Docker and Kubernetes", "category": "Cloud Computing", "level": "Advanced",
     "bloom_level": 4, "skills": "docker kubernetes containers orchestration CI/CD deployment scaling DevOps microservices", "duration": 35, "prerequisites": "Cloud Computing with AWS"},
    {"name": "MLOps and Model Deployment", "category": "AI/ML", "level": "Advanced",
     "bloom_level": 5, "skills": "MLOps model deployment pipeline CI/CD monitoring drift docker kubernetes FastAPI", "duration": 38, "prerequisites": "Machine Learning Fundamentals Docker and Kubernetes"},
    {"name": "Cybersecurity Essentials", "category": "Security", "level": "Beginner",
     "bloom_level": 2, "skills": "cybersecurity networking firewalls encryption authentication vulnerabilities OWASP", "duration": 22, "prerequisites": ""},
    {"name": "Ethical Hacking and Penetration Testing", "category": "Security", "level": "Advanced",
     "bloom_level": 5, "skills": "ethical hacking penetration testing Kali Linux CTF vulnerability exploitation security audit", "duration": 45, "prerequisites": "Cybersecurity Essentials"},
    {"name": "Reinforcement Learning", "category": "AI/ML", "level": "Advanced",
     "bloom_level": 6, "skills": "reinforcement learning Q-learning policy gradient reward agent environment OpenAI Gym", "duration": 48, "prerequisites": "Deep Learning with TensorFlow"},
    {"name": "Full Stack Web Development", "category": "Web Development", "level": "Advanced",
     "bloom_level": 5, "skills": "fullstack MERN react node mongodb REST API deployment authentication testing", "duration": 55, "prerequisites": "React.js Frontend Development Node.js Backend Development SQL and Database Design"},
]

# ──────────────────────────────────────────────
# Build model
# ──────────────────────────────────────────────

LEVEL_WEIGHT = {
    "Beginner": "beginner beginner",
    "Intermediate": "intermediate intermediate intermediate",
    "Advanced": "advanced advanced advanced advanced",
}
BLOOM_LABELS = {1: "remember", 2: "understand", 3: "apply", 4: "analyze", 5: "evaluate", 6: "create"}
LEVEL_ORDER  = {"Beginner": 1, "Intermediate": 2, "Advanced": 3}


def build_feature_string(row: pd.Series) -> str:
    """Weighted multi-attribute feature string for TF-IDF."""
    category  = (row["category"] + " ") * 3
    level_str = LEVEL_WEIGHT.get(row["level"], row["level"])
    bloom_str = (BLOOM_LABELS.get(row["bloom_level"], "") + " ") * 2
    skills    = row["skills"] * 2
    prereqs   = row["prerequisites"].replace(",", " ")
    duration  = "short" if row["duration"] < 25 else ("medium" if row["duration"] < 40 else "long")
    return f"{category} {level_str} {bloom_str} {skills} {prereqs} {duration}"


def build_model():
    """Returns (df, cosine_sim, course_index)."""
    df = pd.DataFrame(COURSES_DATA)
    df["feature_string"] = df.apply(build_feature_string, axis=1)

    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2), sublinear_tf=True, max_features=500, stop_words="english"
    )
    tfidf_matrix = vectorizer.fit_transform(df["feature_string"])
    cosine_sim   = cosine_similarity(tfidf_matrix, tfidf_matrix)
    course_index = pd.Series(df.index, index=df["name"]).drop_duplicates()

    return df, cosine_sim, course_index


# Singleton model
_df, _cosine_sim, _course_index = build_model()


# ──────────────────────────────────────────────
# Recommendation
# ──────────────────────────────────────────────

def get_recommendations(course_name: str, top_k: int = 5,
                        filter_category: str = None, filter_level: str = None):
    """
    Returns (list[dict], error_string | None).
    Each dict has: rank, name, category, level, duration, similarity, explanation, prerequisites.
    """
    if course_name not in _course_index:
        return None, f"Course '{course_name}' not found in dataset."

    idx     = _course_index[course_name]
    current = _df.iloc[idx]

    sim_scores = sorted(enumerate(_cosine_sim[idx]), key=lambda x: x[1], reverse=True)
    sim_scores = [(i, s) for i, s in sim_scores if i != idx]

    results = []
    for i, score in sim_scores:
        candidate = _df.iloc[i]

        if filter_category and filter_category != "All" and candidate["category"] != filter_category:
            continue
        if filter_level and filter_level != "All" and candidate["level"] != filter_level:
            continue

        reasons = []
        if candidate["category"] == current["category"]:
            reasons.append(f"same domain ({candidate['category']})")
        shared = set(current["skills"].split()) & set(candidate["skills"].split())
        if shared:
            reasons.append(f"shared skills: {', '.join(list(shared)[:3])}")
        level_diff = LEVEL_ORDER.get(candidate["level"], 2) - LEVEL_ORDER.get(current["level"], 2)
        if level_diff == 1:
            reasons.append("natural difficulty progression (+1 level)")
        elif level_diff == 0:
            reasons.append("same difficulty level")
        if current["name"] in candidate["prerequisites"]:
            reasons.append("🔗 direct prerequisite satisfied")

        explanation = "Recommended because: " + "; ".join(reasons) if reasons else "Content similarity match"

        results.append({
            "rank":         len(results) + 1,
            "name":         candidate["name"],
            "category":     candidate["category"],
            "level":        candidate["level"],
            "duration":     f"{candidate['duration']}h",
            "similarity":   round(score * 100, 1),
            "explanation":  explanation,
            "prerequisites": candidate["prerequisites"] if candidate["prerequisites"] else "None",
        })

        if len(results) >= top_k:
            break

    return results, None


# ──────────────────────────────────────────────
# DAG
# ──────────────────────────────────────────────

LEVEL_COLOR = {"Beginner": "#22c55e", "Intermediate": "#f59e0b", "Advanced": "#ef4444"}


def build_dag(start_course: str, max_depth: int = 4):
    """Builds and returns a Plotly figure showing the learning path DAG."""
    G = nx.DiGraph()

    def add_path(course_name, depth):
        if depth > max_depth or course_name not in _course_index:
            return
        idx = _course_index[course_name]
        G.add_node(course_name,
                   level=_df.iloc[idx]["level"],
                   category=_df.iloc[idx]["category"])
        recs, _ = get_recommendations(course_name, top_k=3)
        if recs:
            for r in recs[:2]:
                next_c = r["name"]
                if not G.has_edge(course_name, next_c):
                    G.add_edge(course_name, next_c, weight=r["similarity"])
                    add_path(next_c, depth + 1)

    add_path(start_course, 0)
    if len(G.nodes) == 0:
        return None

    try:
        pos = nx.spring_layout(G, k=2.5, seed=42)
    except Exception:
        pos = nx.shell_layout(G)

    edge_x, edge_y = [], []
    for u, v in G.edges():
        x0, y0 = pos[u]; x1, y1 = pos[v]
        edge_x += [x0, x1, None]; edge_y += [y0, y1, None]

    edge_trace = go.Scatter(x=edge_x, y=edge_y, mode="lines",
                            line=dict(width=1.5, color="#94a3b8"), hoverinfo="none")

    node_x      = [pos[n][0] for n in G.nodes()]
    node_y      = [pos[n][1] for n in G.nodes()]
    node_colors = [LEVEL_COLOR.get(G.nodes[n].get("level", "Beginner"), "#6366f1") for n in G.nodes()]
    node_text   = [f"<b>{n}</b><br>{G.nodes[n].get('category','')}<br>{G.nodes[n].get('level','')}" for n in G.nodes()]
    node_labels = [n if n == start_course else (n[:22] + ".." if len(n) > 24 else n) for n in G.nodes()]

    node_trace = go.Scatter(
        x=node_x, y=node_y, mode="markers+text",
        text=node_labels, textposition="top center",
        textfont=dict(size=10, color="white"),
        hovertext=node_text, hoverinfo="text",
        marker=dict(size=22, color=node_colors, line=dict(width=2, color="white")),
    )

    fig = go.Figure(
        data=[edge_trace, node_trace],
        layout=go.Layout(
            title=dict(text=f"Learning Path DAG — Starting: {start_course}",
                       font=dict(size=14, color="#e2e8f0")),
            paper_bgcolor="#0f172a", plot_bgcolor="#0f172a",
            font=dict(color="#e2e8f0"), showlegend=False,
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            margin=dict(l=20, r=20, t=60, b=20), height=480,
        ),
    )
    for level, color in LEVEL_COLOR.items():
        fig.add_trace(go.Scatter(x=[None], y=[None], mode="markers",
                                 marker=dict(size=12, color=color),
                                 name=level, showlegend=True))
    return fig


# ──────────────────────────────────────────────
# Evaluation
# ──────────────────────────────────────────────

def build_ground_truth():
    gt = {}
    for _, row in _df.iterrows():
        relevant = [
            other["name"] for _, other in _df.iterrows()
            if other["name"] != row["name"] and (
                other["category"] == row["category"] or row["name"] in other["prerequisites"]
            )
        ]
        gt[row["name"]] = relevant
    return gt


def precision_at_k(recommended, relevant, k):
    return len([x for x in recommended[:k] if x in relevant]) / k if k > 0 else 0.0


def average_precision_at_k(recommended, relevant, k):
    hits, score = 0, 0.0
    for i, item in enumerate(recommended[:k]):
        if item in relevant:
            hits += 1
            score += hits / (i + 1)
    return score / min(len(relevant), k) if relevant else 0.0


def ndcg_at_k(recommended, relevant, k):
    dcg  = sum(1 / np.log2(i + 2) for i, item in enumerate(recommended[:k]) if item in relevant)
    idcg = sum(1 / np.log2(i + 2) for i in range(min(len(relevant), k)))
    return dcg / idcg if idcg > 0 else 0.0


def evaluate_system(k_values=(1, 3, 5, 7, 10)):
    ground_truth = build_ground_truth()
    results = {k: {"precision": [], "map": [], "ndcg": []} for k in k_values}

    for course in _df["name"]:
        recs, err = get_recommendations(course, top_k=max(k_values))
        if not recs:
            continue
        rec_names = [r["name"] for r in recs]
        relevant  = ground_truth.get(course, [])
        for k in k_values:
            results[k]["precision"].append(precision_at_k(rec_names, relevant, k))
            results[k]["map"].append(average_precision_at_k(rec_names, relevant, k))
            results[k]["ndcg"].append(ndcg_at_k(rec_names, relevant, k))

    summary = {
        k: {
            "precision": np.mean(results[k]["precision"]),
            "map":       np.mean(results[k]["map"]),
            "ndcg":      np.mean(results[k]["ndcg"]),
        }
        for k in k_values
    }
    return summary


# ──────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────

def get_all_courses():
    return sorted(_df["name"].tolist())

def get_all_categories():
    return ["All"] + sorted(_df["category"].unique().tolist())

def get_all_levels():
    return ["All", "Beginner", "Intermediate", "Advanced"]
