import streamlit as st
import pandas as pd
from typing import Dict, Any, List

def render_custom_css():
    st.markdown("""
    <style>
    /* Modern SaaS Styling */
    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 0.8rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .card-title {
        font-weight: 700;
        font-size: 1.1rem;
        color: #1E293B;
    }
    .tag-badge {
        display: inline-block;
        background-color: #DBEAFE;
        color: #1E40AF;
        padding: 0.2rem 0.6rem;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-right: 0.4rem;
    }
    .tag-score {
        display: inline-block;
        background-color: #DCFCE7;
        color: #166534;
        padding: 0.2rem 0.6rem;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 700;
    }
    .source-box {
        font-size: 0.85rem;
        background: #F1F5F9;
        border-left: 3px solid #3B82F6;
        padding: 0.6rem;
        border-radius: 4px;
        margin-top: 0.4rem;
    }
    </style>
    """, unsafe_allow_html=True)

def render_university_cards(universities: List[Dict[str, Any]]):
    if not universities:
        return
    st.markdown("#### 🎓 Recommended Universities")
    cols = st.columns(min(len(universities), 2))
    for i, u in enumerate(universities[:4]):
        with cols[i % 2]:
            st.markdown(f"""
            <div class="metric-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span class="card-title">{u.get('university')}</span>
                    <span class="tag-score">{u.get('recommendation_score')}/100</span>
                </div>
                <div style="margin: 0.4rem 0;">
                    <span class="tag-badge">📍 {u.get('country')}</span>
                    <span class="tag-badge">🏆 QS Rank #{u.get('rank_2025')}</span>
                    <span class="tag-badge">💵 ${u.get('estimated_annual_cost_usd', 0):,.0f} USD</span>
                </div>
                <p style="font-size:0.85rem; color:#475569; margin-top:0.4rem;"><b>Reason:</b> {u.get('reason')}</p>
            </div>
            """, unsafe_allow_html=True)

def render_scholarship_cards(scholarships: List[Dict[str, Any]]):
    if not scholarships:
        return
    st.markdown("#### 💰 Available Scholarships")
    for s in scholarships[:3]:
        link_html = f"<a href='{s.get('link')}' target='_blank' style='color:#2563EB;'>🔗 Official Application Link</a>" if s.get('link') else "<em>Check portal</em>"
        st.markdown(f"""
        <div class="metric-card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span class="card-title">🎁 {s.get('scholarship_name')}</span>
                <span class="tag-score">Match: {s.get('match_score')}%</span>
            </div>
            <div style="margin: 0.3rem 0;">
                <span class="tag-badge">🌍 {s.get('location')}</span>
                <span class="tag-badge">💵 ${s.get('amount')}</span>
                <span class="tag-badge">⏳ Deadline: {s.get('deadline')}</span>
            </div>
            <p style="font-size:0.85rem; color:#475569; margin-bottom:0.2rem;">{s.get('description')}</p>
            <div style="font-size:0.85rem;">{link_html}</div>
        </div>
        """, unsafe_allow_html=True)

def render_agent_process(agent_meta: Dict[str, Any]):
    with st.expander("🔍 Agentic AI Execution & Retrieval Details", expanded=False):
        c1, c2, c3 = st.columns(3)
        c1.metric("Detected Intent", agent_meta.get("detected_intent", "N/A"))
        c2.metric("Execution Latency", f"{agent_meta.get('latency_ms', 0):.0f} ms")
        c3.metric("RAG Chunks Retrieved", len(agent_meta.get("retrieved_documents", [])))
        
        st.markdown("**Tools Executed:**")
        for log in agent_meta.get("tool_execution_logs", []):
            st.markdown(f"- `{log.get('tool')}` — Status: `{log.get('status')}` ({log.get('execution_ms')} ms)")

        if agent_meta.get("retrieved_documents"):
            st.markdown("**Top Retrieved RAG Knowledge Documents:**")
            for i, doc in enumerate(agent_meta.get("retrieved_documents")[:3], 1):
                st.markdown(f"""
                <div class="source-box">
                    <b>Doc {i}: {doc.get('topic')}</b> (Score: {doc.get('similarity_score', 0):.3f} | Source: <code>{doc.get('source_file')}</code>)<br>
                    <span style="color:#64748B;">{doc.get('text', '')[:180]}...</span>
                </div>
                """, unsafe_allow_html=True)
