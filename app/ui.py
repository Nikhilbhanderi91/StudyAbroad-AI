import streamlit as st
import pandas as pd
from typing import Dict, Any, List, Optional
from pathlib import Path
from utils.profile import StudentProfile

def load_custom_css():
    """Injects the ultra-premium 2026 CSS design system."""
    css_path = Path(__file__).resolve().parent / "styles.css"
    if css_path.exists():
        with open(css_path, "r", encoding="utf-8") as f:
            css_code = f.read()
        st.markdown(f"<style>{css_code}</style>", unsafe_allow_html=True)

def render_top_header():
    """Renders the sleek animated AI Orb top navigation bar."""
    st.markdown(
        '<div class="ai-header-bar">'
        '<div class="ai-orb-wrapper">'
        '<div class="ai-orb">✦</div>'
        '<div>'
        '<div class="ai-brand-title">StudyAbroad AI</div>'
        '<div style="font-size:0.75rem; color:#94A3B8;">Your AI Copilot for Studying Abroad</div>'
        '</div>'
        '</div>'
        '<div class="ai-status-pill">'
        '<span class="status-dot"></span> AI Online &bull; RAG Ready'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

def render_welcome_hero():
    """Renders the centered futuristic landing hero when chat is fresh."""
    st.markdown(
        '<div class="welcome-hero">'
        '<div class="welcome-badge">✦ NEXT-GEN AI ADVISOR</div>'
        '<div class="welcome-title">Your AI Copilot for<br>Studying Abroad.</div>'
        '<div class="welcome-subtitle">'
        'Discover universities, scholarships, real-time cost estimations, and custom admission roadmaps powered by RAG + Agentic AI.'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

def render_quick_action_cards():
    """Renders 4 interactive quick action cards."""
    st.markdown(
        '<div class="quick-action-grid">'
        '<div class="quick-action-card">'
        '<span class="qa-icon">🎓</span>'
        '<div class="qa-title">Find Universities</div>'
        '<div class="qa-desc">Discover top global universities matching your GPA & budget.</div>'
        '</div>'
        '<div class="quick-action-card">'
        '<span class="qa-icon">💎</span>'
        '<div class="qa-title">Find Scholarships</div>'
        '<div class="qa-desc">Explore 10,400+ grants, criteria, and funding amounts.</div>'
        '</div>'
        '<div class="quick-action-card">'
        '<span class="qa-icon">💰</span>'
        '<div class="qa-title">Cost Breakdown</div>'
        '<div class="qa-desc">Estimate total tuition, rent, living costs, and visa fees.</div>'
        '</div>'
        '<div class="quick-action-card">'
        '<span class="qa-icon">🗺️</span>'
        '<div class="qa-title">Build My Roadmap</div>'
        '<div class="qa-desc">Generate a personalized milestone application timeline.</div>'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

def render_profile_progress_bar(completeness_pct: int, profile: StudentProfile):
    """Renders a sleek top progress indicator with student metrics."""
    country_lbl = profile.preferred_country or 'Target Country'
    field_lbl = profile.preferred_field or 'Field'
    st.markdown(
        f'<div style="background:rgba(21, 29, 46, 0.85); backdrop-filter:blur(16px); border:1px solid rgba(255,255,255,0.08); border-radius:14px; padding:0.75rem 1.25rem; margin-bottom:1.25rem; display:flex; justify-content:space-between; align-items:center;">'
        f'<div style="display:flex; align-items:center; gap:0.75rem;">'
        f'<span style="font-size:1.1rem; color:#22D3EE;">✦</span>'
        f'<div>'
        f'<span style="font-weight:700; font-size:0.92rem; color:#F8FAFC;">Profile Strength: {completeness_pct}%</span>'
        f'<span style="font-size:0.8rem; color:#94A3B8; margin-left:0.5rem;">({profile.name} &bull; {country_lbl} &bull; {field_lbl})</span>'
        f'</div>'
        f'</div>'
        f'<div style="width:140px; background:rgba(255,255,255,0.08); border-radius:9999px; height:8px; overflow:hidden;">'
        f'<div style="width:{completeness_pct}%; background:linear-gradient(90deg, #6366F1, #22D3EE); height:100%; border-radius:9999px;"></div>'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True
    )

def render_profile_card_inline(profile: StudentProfile):
    """Renders a verified student profile card with glowing glassmorphism."""
    budget_inr = (profile.budget_in_inr() / 100000)
    st.markdown(
        f'<div class="profile-card-glow">'
        f'<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.4rem;">'
        f'<span style="font-family:\'Space Grotesk\',sans-serif; font-weight:800; font-size:1.05rem; color:#FFFFFF;">✦ VERIFIED STUDY ABROAD PROFILE</span>'
        f'<span style="background:rgba(16,185,129,0.15); border:1px solid rgba(16,185,129,0.3); color:#34D399; padding:0.2rem 0.6rem; border-radius:9999px; font-size:0.78rem; font-weight:700;">✓ Ready for Analysis</span>'
        f'</div>'
        f'<div class="profile-stat-grid">'
        f'<div class="profile-stat-box"><div class="val">{profile.name}</div><div class="lbl">Student</div></div>'
        f'<div class="profile-stat-box"><div class="val">{profile.cgpa}</div><div class="lbl">Academic CGPA</div></div>'
        f'<div class="profile-stat-box"><div class="val">₹{budget_inr:.1f}L</div><div class="lbl">Total Budget</div></div>'
        f'<div class="profile-stat-box"><div class="val">{profile.preferred_country}</div><div class="lbl">Target Country</div></div>'
        f'<div class="profile-stat-box"><div class="val">{profile.preferred_field}</div><div class="lbl">Major / Field</div></div>'
        f'<div class="profile-stat-box"><div class="val">{profile.degree_level}</div><div class="lbl">Degree Level</div></div>'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True
    )

def render_university_card_copilot(u: Dict[str, Any], key_prefix: str = "u"):
    """Renders an ultra-premium university match card with pure one-line HTML to avoid Markdown parsing bugs."""
    univ_name = u.get("university", "Unknown University")
    country = u.get("country", "Global")
    rank = u.get("rank_2025", u.get("rank", "N/A"))
    cost_usd = u.get("estimated_annual_cost_usd", u.get("total_estimated_cost", 30000))
    try:
        cost_usd = float(cost_usd)
    except Exception:
        cost_usd = 30000.0
    score = float(u.get("recommendation_score", 85.0))
    reason = u.get("reason", "Strong alignment with academic profile and target program.")
    program = u.get("program", "Computer Science")
    cost_inr = (cost_usd * 83.5 / 100000)

    html_code = (
        f'<div class="univ-card-copilot">'
        f'<div class="univ-card-header">'
        f'<div>'
        f'<div style="font-weight:700; font-size:1.15rem; color:#FFFFFF;">🎓 {univ_name}</div>'
        f'<div style="font-size:0.85rem; color:#94A3B8; margin-top:0.2rem;">📍 {country} &bull; 📚 {program}</div>'
        f'</div>'
        f'<div class="score-badge-circle">'
        f'<span class="num">{score:.0f}%</span>'
        f'<span class="lbl">MATCH</span>'
        f'</div>'
        f'</div>'
        f'<div class="fit-breakdown-bar">'
        f'<div class="fit-progress-row">'
        f'<span>⭐ QS Global Rank: <b>#{rank}</b></span>'
        f'<span>💵 Est. Cost: <b>${cost_usd:,.0f} USD (₹{cost_inr:.1f}L)</b></span>'
        f'</div>'
        f'<div class="fit-progress-row" style="margin-top:0.3rem;">'
        f'<span style="color:#94A3B8;">Academic & Budget Compatibility:</span>'
        f'<div class="fit-meter"><div class="fit-fill" style="width:{min(score, 100):.1f}%;"></div></div>'
        f'</div>'
        f'</div>'
        f'<div style="background:rgba(99,102,241,0.08); border-left:3px solid #6366F1; border-radius:0 6px 6px 0; padding:0.55rem 0.8rem; font-size:0.82rem; color:#CBD5E1;">'
        f'<b>💡 AI Fit Rationale:</b> {reason}'
        f'</div>'
        f'</div>'
    )
    st.markdown(html_code, unsafe_allow_html=True)

    is_saved = univ_name in st.session_state.get("saved_universities", [])
    btn_label = "❤️ Saved" if is_saved else "🤍 Save University"
    if st.button(btn_label, key=f"{key_prefix}_save_{univ_name}"):
        if "saved_universities" not in st.session_state:
            st.session_state.saved_universities = []
        if is_saved:
            st.session_state.saved_universities.remove(univ_name)
            st.toast(f"Removed {univ_name}", icon="🗑️")
        else:
            st.session_state.saved_universities.append(univ_name)
            st.toast(f"Saved {univ_name} to your Journey!", icon="❤️")
        st.rerun()

def render_scholarship_card_copilot(s: Dict[str, Any], key_prefix: str = "s"):
    """Renders a futuristic scholarship card with pure single-line HTML."""
    name = s.get("scholarship_name", "Global Study Grant")
    loc = s.get("location", "International")
    amount = s.get("amount", "Partial / Full Funding")
    deadline = s.get("deadline", "Check portal")
    score = float(s.get("match_score", 80.0))
    desc = s.get("description", "")
    link = s.get("link", "")

    link_markup = f'<a href="{link}" target="_blank" style="color:#22D3EE; font-weight:600; text-decoration:none; font-size:0.85rem;">🔗 Official Application Portal &rarr;</a>' if link and str(link).startswith("http") else '<span style="color:#64748B; font-size:0.85rem;">Portal verification required</span>'

    html_code = (
        f'<div class="univ-card-copilot">'
        f'<div class="univ-card-header">'
        f'<div>'
        f'<div style="font-weight:700; font-size:1.1rem; color:#FFFFFF;">💎 {name}</div>'
        f'<div style="font-size:0.85rem; color:#94A3B8;">🌍 {loc} &bull; ⏳ Deadline: {deadline}</div>'
        f'</div>'
        f'<div class="score-badge-circle" style="border-color:#22D3EE; background:radial-gradient(circle, rgba(34,211,238,0.2) 0%, transparent 100%);">'
        f'<span class="num" style="color:#22D3EE;">{score:.0f}%</span>'
        f'<span class="lbl" style="color:#22D3EE;">MATCH</span>'
        f'</div>'
        f'</div>'
        f'<div class="fit-breakdown-bar" style="margin:0.6rem 0;">'
        f'<div class="fit-progress-row">'
        f'<span>💰 Award Funding: <b>${amount}</b></span>'
        f'<span>📋 Intake: <b>{deadline}</b></span>'
        f'</div>'
        f'</div>'
        f'<p style="font-size:0.82rem; color:#94A3B8; margin: 0.5rem 0;">{desc[:200]}...</p>'
        f'<div>{link_markup}</div>'
        f'</div>'
    )
    st.markdown(html_code, unsafe_allow_html=True)

    is_saved = name in st.session_state.get("saved_scholarships", [])
    btn_label = "❤️ Saved" if is_saved else "🤍 Save Scholarship"
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
    """Renders the AI Agent activity status & RAG citations in a collapsible element."""
    with st.expander("⚡ Agent Activity & RAG Citations · Completed", expanded=False):
        c1, c2, c3 = st.columns(3)
        c1.metric("Intent Detected", agent_meta.get("detected_intent", "Query").replace("_", " ").title())
        c2.metric("Execution Latency", f"{agent_meta.get('latency_ms', 0):.0f} ms")
        c3.metric("RAG Citations", len(agent_meta.get("retrieved_documents", [])))

        if agent_meta.get("tool_execution_logs"):
            st.markdown("<div style='font-size:0.82rem; font-weight:700; margin-top:0.4rem;'>🛠️ Tools Orchestrated:</div>", unsafe_allow_html=True)
            for log in agent_meta.get("tool_execution_logs", []):
                st.caption(f"✓ `{log.get('tool')}` ({log.get('execution_ms')} ms)")

        if agent_meta.get("retrieved_documents"):
            st.markdown("<div style='font-size:0.82rem; font-weight:700; margin-top:0.5rem; color:#22D3EE;'>📚 Verified RAG Knowledge Chunks:</div>", unsafe_allow_html=True)
            for i, doc in enumerate(agent_meta.get("retrieved_documents")[:3], 1):
                doc_topic = doc.get('topic', 'Topic')
                doc_score = doc.get('similarity_score', 0)
                doc_src = doc.get('source_file', 'Dataset')
                doc_txt = doc.get('text', '')[:140]
                chunk_html = (
                    f'<div style="background:rgba(11, 16, 32, 0.7); border:1px solid rgba(255,255,255,0.06); padding:0.5rem 0.75rem; border-radius:6px; margin-top:0.35rem; font-size:0.8rem;">'
                    f'<b>Doc {i}: {doc_topic}</b> (Relevance: <code>{doc_score:.3f}</code> | Source: <code>{doc_src}</code>)<br>'
                    f'<span style="color:#94A3B8;">{doc_txt}...</span>'
                    f'</div>'
                )
                st.markdown(chunk_html, unsafe_allow_html=True)
