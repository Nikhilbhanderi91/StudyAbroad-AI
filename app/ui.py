import streamlit as st
import pandas as pd
from typing import Dict, Any, List, Optional
from pathlib import Path

def load_custom_css():
    """Injects the unified CSS design system."""
    css_path = Path(__file__).resolve().parent / "styles.css"
    if css_path.exists():
        with open(css_path, "r", encoding="utf-8") as f:
            css_code = f.read()
        st.markdown(f"<style>{css_code}</style>", unsafe_allow_html=True)

def render_hero_section():
    """Renders the top AI SaaS hero banner."""
    st.markdown("""
    <div class="saas-hero">
        <div class="hero-pill">✦ NEXT-GEN RAG & AGENTIC AI ADVISOR</div>
        <div class="hero-title">Your Journey. Smarter.<br>Your Future. Global.</div>
        <div class="hero-subtitle">
            Personalized university discovery, intelligent scholarship matching, and end-to-end admission guidance grounded in verified global datasets.
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_metric_cards(univ_count: int = 1827, scholarship_count: int = 10410, countries_count: int = 71, profile_match: str = "94%"):
    """Displays 4 quick SaaS metric tiles."""
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="metric-tile">
            <div class="metric-tile-icon">🎓</div>
            <div class="metric-tile-val">{univ_count:,}</div>
            <div class="metric-tile-lbl">Universities Tracked</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="metric-tile">
            <div class="metric-tile-icon">💰</div>
            <div class="metric-tile-val">{scholarship_count:,}</div>
            <div class="metric-tile-lbl">Scholarships Matched</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="metric-tile">
            <div class="metric-tile-icon">🌍</div>
            <div class="metric-tile-val">{countries_count}</div>
            <div class="metric-tile-lbl">Countries Analyzed</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class="metric-tile">
            <div class="metric-tile-icon">✦</div>
            <div class="metric-tile-val">{profile_match}</div>
            <div class="metric-tile-lbl">Profile Match Index</div>
        </div>
        """, unsafe_allow_html=True)

def render_university_card(u: Dict[str, Any], show_save: bool = True, key_prefix: str = "univ"):
    """Renders an interactive high-conversion University Card."""
    univ_name = u.get("university", "Unknown University")
    country = u.get("country", "Global")
    rank = u.get("rank_2025", u.get("rank", "N/A"))
    cost_usd = u.get("estimated_annual_cost_usd", u.get("total_estimated_cost", 30000))
    score = u.get("recommendation_score", 85.0)
    reason = u.get("reason", "Strong alignment with academic profile and target program.")
    program = u.get("program", "Computer Science")

    card_html = f"""
    <div class="univ-card">
        <div class="univ-header">
            <div>
                <div class="univ-name">{univ_name}</div>
                <div class="univ-location">📍 {country} &bull; 🎓 {program}</div>
            </div>
            <div class="match-badge">✦ {score:.0f}% Match</div>
        </div>
        <div class="univ-stats-grid">
            <div class="univ-stat-item">
                <div class="univ-stat-val">#{rank}</div>
                <div class="univ-stat-lbl">QS Rank 2025</div>
            </div>
            <div class="univ-stat-item">
                <div class="univ-stat-val">${cost_usd:,.0f}</div>
                <div class="univ-stat-lbl">Est. Cost (USD/yr)</div>
            </div>
            <div class="univ-stat-item">
                <div class="univ-stat-val">₹{(cost_usd * 83.5 / 100000):.1f} L</div>
                <div class="univ-stat-lbl">Est. Cost (INR/yr)</div>
            </div>
        </div>
        <div class="univ-reason-box">
            <b>💡 AI Fit Rationale:</b> {reason}
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)
    
    if show_save:
        col1, col2 = st.columns([4, 1])
        with col2:
            is_saved = univ_name in st.session_state.get("saved_universities", [])
            btn_label = "❤️ Saved" if is_saved else "🤍 Save"
            if st.button(btn_label, key=f"{key_prefix}_save_{univ_name}"):
                if "saved_universities" not in st.session_state:
                    st.session_state.saved_universities = []
                if is_saved:
                    st.session_state.saved_universities.remove(univ_name)
                    st.toast(f"Removed {univ_name} from saved items", icon="🗑️")
                else:
                    st.session_state.saved_universities.append(univ_name)
                    st.toast(f"Saved {univ_name} to your Journey!", icon="❤️")
                st.rerun()

def render_scholarship_card(s: Dict[str, Any], show_save: bool = True, key_prefix: str = "sch"):
    """Renders a modern Scholarship Card."""
    name = s.get("scholarship_name", "Global Study Grant")
    loc = s.get("location", "International")
    amount = s.get("amount", "Partial / Full Funding")
    deadline = s.get("deadline", "Check official deadline")
    score = s.get("match_score", 80.0)
    desc = s.get("description", "")
    link = s.get("link", "")

    link_markup = f'<a href="{link}" target="_blank" style="color:#818CF8; font-weight:600; text-decoration:none; font-size:0.85rem;">🔗 Official Application Portal &rarr;</a>' if link and str(link).startswith("http") else '<span style="color:#64748B; font-size:0.85rem;">Portal verification required</span>'

    st.markdown(f"""
    <div class="univ-card">
        <div class="univ-header">
            <div>
                <div class="univ-name">🎁 {name}</div>
                <div class="univ-location">🌍 {loc} &bull; ⏳ Deadline: {deadline}</div>
            </div>
            <div class="match-badge">✦ {score:.0f}% Match</div>
        </div>
        <div class="univ-stats-grid">
            <div class="univ-stat-item">
                <div class="univ-stat-val">${amount}</div>
                <div class="univ-stat-lbl">Award Funding</div>
            </div>
            <div class="univ-stat-item">
                <div class="univ-stat-val">{deadline}</div>
                <div class="univ-stat-lbl">Intake Session</div>
            </div>
            <div class="univ-stat-item">
                <div class="univ-stat-val">Verified</div>
                <div class="univ-stat-lbl">Dataset Status</div>
            </div>
        </div>
        <p style="font-size:0.85rem; color:#94A3B8; margin: 0.6rem 0;">{desc[:220]}...</p>
        <div style="margin-top:0.4rem;">{link_markup}</div>
    </div>
    """, unsafe_allow_html=True)

    if show_save:
        col1, col2 = st.columns([4, 1])
        with col2:
            is_saved = name in st.session_state.get("saved_scholarships", [])
            btn_label = "❤️ Saved" if is_saved else "🤍 Save"
            if st.button(btn_label, key=f"{key_prefix}_save_{name[:20]}"):
                if "saved_scholarships" not in st.session_state:
                    st.session_state.saved_scholarships = []
                if is_saved:
                    st.session_state.saved_scholarships.remove(name)
                    st.toast(f"Removed {name} from saved scholarships", icon="🗑️")
                else:
                    st.session_state.saved_scholarships.append(name)
                    st.toast(f"Saved {name} to your Journey!", icon="❤️")
                st.rerun()

def render_agent_activity_tracer(agent_meta: Dict[str, Any]):
    """Renders agent execution metrics and retrieved RAG sources."""
    with st.expander("🔍 Agentic Execution Trace & Vector Citations", expanded=False):
        c1, c2, c3 = st.columns(3)
        c1.metric("Identified Intent", agent_meta.get("detected_intent", "General Query").replace("_", " ").title())
        c2.metric("Execution Latency", f"{agent_meta.get('latency_ms', 0):.0f} ms")
        c3.metric("RAG Citations", len(agent_meta.get("retrieved_documents", [])))

        st.markdown("**🛠️ Tools Orchestrated:**")
        cols = st.columns(max(len(agent_meta.get("tool_execution_logs", [])), 1))
        for i, log in enumerate(agent_meta.get("tool_execution_logs", [])):
            with cols[i % len(cols)]:
                st.caption(f"✓ `{log.get('tool')}` ({log.get('execution_ms')}ms)")

        if agent_meta.get("retrieved_documents"):
            st.markdown("<div style='font-size:0.85rem; font-weight:700; margin-top:0.6rem; color:#A5B4FC;'>📚 Verified RAG Knowledge Chunks:</div>", unsafe_allow_html=True)
            for i, doc in enumerate(agent_meta.get("retrieved_documents")[:3], 1):
                st.markdown(f"""
                <div style="background:rgba(11, 16, 32, 0.7); border:1px solid rgba(255,255,255,0.06); padding:0.6rem 0.8rem; border-radius:6px; margin-top:0.4rem; font-size:0.82rem;">
                    <b>Doc {i}: {doc.get('topic')}</b> (Relevance: <code>{doc.get('similarity_score', 0):.3f}</code> | Source: <code>{doc.get('source_file')}</code>)<br>
                    <span style="color:#94A3B8;">{doc.get('text', '')[:160]}...</span>
                </div>
                """, unsafe_allow_html=True)
