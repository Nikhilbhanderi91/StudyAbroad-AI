import streamlit as st
import pandas as pd
from typing import Dict, Any, List, Optional
from pathlib import Path
from utils.profile import StudentProfile

def load_custom_css():
    """Injects the streamlined conversational CSS design system."""
    css_path = Path(__file__).resolve().parent / "styles.css"
    if css_path.exists():
        with open(css_path, "r", encoding="utf-8") as f:
            css_code = f.read()
        st.markdown(f"<style>{css_code}</style>", unsafe_allow_html=True)

def render_profile_progress_bar(completeness_pct: int, profile: StudentProfile):
    """Renders a top progress indicator with collapsible summary."""
    st.markdown(f"""
    <div style="background:rgba(21, 29, 46, 0.9); border:1px solid rgba(255,255,255,0.08); border-radius:12px; padding:0.75rem 1.25rem; margin-bottom:1.25rem; display:flex; justify-content:space-between; align-items:center;">
        <div style="display:flex; align-items:center; gap:0.75rem;">
            <span style="font-size:1.1rem; color:#A5B4FC;">✦</span>
            <div>
                <span style="font-weight:700; font-size:0.92rem; color:#F8FAFC;">Profile Strength: {completeness_pct}%</span>
                <span style="font-size:0.8rem; color:#94A3B8; margin-left:0.5rem;">({profile.name} &bull; {profile.preferred_country} &bull; {profile.preferred_field})</span>
            </div>
        </div>
        <div style="width:140px; background:rgba(255,255,255,0.1); border-radius:9999px; height:8px; overflow:hidden;">
            <div style="width:{completeness_pct}%; background:linear-gradient(90deg, #6366F1, #10B981); height:100%; border-radius:9999px;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_profile_card_inline(profile: StudentProfile):
    """Renders a verified student profile card inside the chat stream."""
    st.markdown(f"""
    <div class="glass-card" style="margin: 0.8rem 0; border-left: 4px solid #6366F1;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.6rem;">
            <span style="font-weight:800; font-size:1.05rem; color:#FFFFFF;">✦ VERIFIED STUDY ABROAD PROFILE</span>
            <span class="match-badge">✓ Profile Ready</span>
        </div>
        <div style="display:grid; grid-template-columns: repeat(3, 1fr); gap:0.6rem; font-size:0.88rem; color:#E2E8F0; margin-top:0.6rem;">
            <div>👤 <b>Name:</b> {profile.name}</div>
            <div>🎓 <b>CGPA:</b> {profile.cgpa}</div>
            <div>📚 <b>Field:</b> {profile.preferred_field}</div>
            <div>🎯 <b>Degree:</b> {profile.degree_level}</div>
            <div>📍 <b>Country:</b> {profile.preferred_country}</div>
            <div>💰 <b>Budget:</b> ₹{profile.budget_in_inr():,.0f} INR</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_university_card_inline(u: Dict[str, Any], key_prefix: str = "u"):
    """Renders an interactive University card directly in the chat stream."""
    univ_name = u.get("university", "Unknown University")
    country = u.get("country", "Global")
    rank = u.get("rank_2025", u.get("rank", "N/A"))
    cost_usd = u.get("estimated_annual_cost_usd", u.get("total_estimated_cost", 30000))
    score = u.get("recommendation_score", 85.0)
    reason = u.get("reason", "Strong alignment with academic profile and target program.")
    program = u.get("program", "Computer Science")

    st.markdown(f"""
    <div class="univ-card" style="margin-top:0.75rem;">
        <div class="univ-header">
            <div>
                <div class="univ-name">🎓 {univ_name}</div>
                <div class="univ-location">📍 {country} &bull; 📚 {program}</div>
            </div>
            <div class="match-badge">✦ {score:.0f}% Profile Match</div>
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
    """, unsafe_allow_html=True)

    is_saved = univ_name in st.session_state.get("saved_universities", [])
    btn_label = "❤️ Saved to Journey" if is_saved else "🤍 Save University"
    if st.button(btn_label, key=f"{key_prefix}_save_{univ_name}"):
        if "saved_universities" not in st.session_state:
            st.session_state.saved_universities = []
        if is_saved:
            st.session_state.saved_universities.remove(univ_name)
            st.toast(f"Removed {univ_name} from saved", icon="🗑️")
        else:
            st.session_state.saved_universities.append(univ_name)
            st.toast(f"Saved {univ_name} to your Journey!", icon="❤️")
        st.rerun()

def render_scholarship_card_inline(s: Dict[str, Any], key_prefix: str = "s"):
    """Renders a modern Scholarship card directly in the chat stream."""
    name = s.get("scholarship_name", "Global Study Grant")
    loc = s.get("location", "International")
    amount = s.get("amount", "Partial / Full Funding")
    deadline = s.get("deadline", "Check portal")
    score = s.get("match_score", 80.0)
    desc = s.get("description", "")
    link = s.get("link", "")

    link_markup = f'<a href="{link}" target="_blank" style="color:#818CF8; font-weight:600; text-decoration:none; font-size:0.85rem;">🔗 Official Application Link &rarr;</a>' if link and str(link).startswith("http") else '<span style="color:#64748B; font-size:0.85rem;">Portal verification required</span>'

    st.markdown(f"""
    <div class="univ-card" style="margin-top:0.75rem;">
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
                <div class="univ-stat-lbl">Funding Amount</div>
            </div>
            <div class="univ-stat-item">
                <div class="univ-stat-val">{deadline}</div>
                <div class="univ-stat-lbl">Application Deadline</div>
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

    is_saved = name in st.session_state.get("saved_scholarships", [])
    btn_label = "❤️ Saved Scholarship" if is_saved else "🤍 Save Scholarship"
    if st.button(btn_label, key=f"{key_prefix}_save_{name[:20]}"):
        if "saved_scholarships" not in st.session_state:
            st.session_state.saved_scholarships = []
        if is_saved:
            st.session_state.saved_scholarships.remove(name)
            st.toast(f"Removed {name}", icon="🗑️")
        else:
            st.session_state.saved_scholarships.append(name)
            st.toast(f"Saved {name} to your Journey!", icon="❤️")
        st.rerun()

def render_agent_activity_tracer(agent_meta: Dict[str, Any]):
    """Renders agent execution metrics and retrieved RAG sources in an expander."""
    with st.expander("🔍 Agentic Execution Trace & Vector Citations", expanded=False):
        c1, c2, c3 = st.columns(3)
        c1.metric("Identified Intent", agent_meta.get("detected_intent", "General Query").replace("_", " ").title())
        c2.metric("Execution Latency", f"{agent_meta.get('latency_ms', 0):.0f} ms")
        c3.metric("RAG Citations", len(agent_meta.get("retrieved_documents", [])))

        if agent_meta.get("tool_execution_logs"):
            st.markdown("**🛠️ Tools Orchestrated:**")
            for log in agent_meta.get("tool_execution_logs", []):
                st.caption(f"✓ `{log.get('tool')}` — Status: `{log.get('status')}` ({log.get('execution_ms')} ms)")

        if agent_meta.get("retrieved_documents"):
            st.markdown("<div style='font-size:0.85rem; font-weight:700; margin-top:0.6rem; color:#A5B4FC;'>📚 Verified RAG Knowledge Chunks:</div>", unsafe_allow_html=True)
            for i, doc in enumerate(agent_meta.get("retrieved_documents")[:3], 1):
                st.markdown(f"""
                <div style="background:rgba(11, 16, 32, 0.7); border:1px solid rgba(255,255,255,0.06); padding:0.6rem 0.8rem; border-radius:6px; margin-top:0.4rem; font-size:0.82rem;">
                    <b>Doc {i}: {doc.get('topic')}</b> (Relevance: <code>{doc.get('similarity_score', 0):.3f}</code> | Source: <code>{doc.get('source_file')}</code>)<br>
                    <span style="color:#94A3B8;">{doc.get('text', '')[:160]}...</span>
                </div>
                """, unsafe_allow_html=True)
