import os
import sys
import time
from pathlib import Path

# Ensure project root is in python path
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
from utils.config import FAISS_INDEX_PATH
from utils.profile import StudentProfile
from build_knowledge_base import build_complete_knowledge_base
from agent.agent import StudyAbroadAgent
from agent.onboarding import ConversationalOnboarding
from app.ui import (
    load_custom_css,
    render_top_header,
    render_welcome_hero,
    render_quick_action_cards,
    render_profile_progress_bar,
    render_profile_card_inline,
    render_university_card_copilot,
    render_scholarship_card_copilot,
    render_agent_activity_tracer
)

# Set Streamlit Page Configuration
st.set_page_config(
    page_title="StudyAbroad AI — AI Copilot",
    page_icon="✦",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Load Ultra-Premium Design System
load_custom_css()

# Cache AI Agent & Vector Database
@st.cache_resource(show_spinner="Initializing AI Copilot & FAISS Vector Index...")
def load_agent():
    if not FAISS_INDEX_PATH.exists():
        build_complete_knowledge_base(force_rebuild=False)
    return StudyAbroadAgent()

agent = load_agent()

# --- INITIALIZE SESSION STATE ---
if "student_profile" not in st.session_state:
    st.session_state.student_profile = StudentProfile(
        name="",
        cgpa=0.0,
        budget=0.0,
        currency="INR",
        preferred_country="",
        preferred_field="",
        degree_level="",
        ranking_priority="High",
        english_test_score="",
        work_experience="",
        preferred_intake="Fall 2025"
    )

if "onboarding_expected_field" not in st.session_state:
    st.session_state.onboarding_expected_field = "name"

if "onboarding_completed" not in st.session_state:
    st.session_state.onboarding_completed = False

if "saved_universities" not in st.session_state:
    st.session_state.saved_universities = []

if "saved_scholarships" not in st.session_state:
    st.session_state.saved_scholarships = []

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- MINIMAL FUTURISTIC SIDEBAR ---
with st.sidebar:
    st.markdown("""
    <div style="display:flex; align-items:center; gap:0.6rem; margin-bottom:1rem;">
        <span style="font-size:1.6rem; color:#6366F1;">✦</span>
        <div style="font-family:'Space Grotesk',sans-serif; font-weight:800; font-size:1.1rem; color:#FFFFFF;">StudyAbroad AI</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("＋ New Conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.student_profile = StudentProfile(
            name="", cgpa=0.0, budget=0.0, currency="INR", preferred_country="", preferred_field="", degree_level=""
        )
        st.session_state.onboarding_completed = False
        st.session_state.onboarding_expected_field = "name"
        st.toast("Started fresh conversation!", icon="✨")
        st.rerun()

    st.markdown("---")
    
    # Active Profile Snapshot
    p = st.session_state.student_profile
    completeness, _, _ = ConversationalOnboarding.get_profile_completeness(p)
    
    st.markdown(f"**✦ Profile Strength:** `{completeness}%`")
    if p.name:
        st.markdown(f"- 👤 **Student:** {p.name}")
    if p.cgpa > 0:
        st.markdown(f"- 🎓 **Score:** {p.cgpa} CGPA")
    if p.preferred_country:
        st.markdown(f"- 📍 **Country:** {p.preferred_country}")
    if p.preferred_field:
        st.markdown(f"- 📚 **Field:** {p.preferred_field} ({p.degree_level or 'Master'})")
    if p.budget > 0:
        st.markdown(f"- 💰 **Budget:** ₹{p.budget_in_inr():,.0f} INR")

    st.markdown("---")
    
    # Saved Shortlist
    st.markdown("**⭐ Saved Shortlist:**")
    if st.session_state.saved_universities:
        for u in st.session_state.saved_universities:
            st.markdown(f"- 🎓 `{u}`")
    else:
        st.caption("No universities saved yet.")

    if st.session_state.saved_scholarships:
        for s in st.session_state.saved_scholarships:
            st.markdown(f"- 💎 `{s}`")

    st.markdown("---")
    st.markdown("<div style='font-size:0.72rem; color:#64748B;'>RAG + Agentic AI Engine &bull; FAISS 6,981 records</div>", unsafe_allow_html=True)

# --- TOP HEADER BAR ---
render_top_header()

# Render Profile Progress if active
prof = st.session_state.student_profile
completeness_pct, next_missing_field, next_q_template = ConversationalOnboarding.get_profile_completeness(prof)
if completeness_pct > 0 and not st.session_state.onboarding_completed:
    render_profile_progress_bar(completeness_pct, prof)

# --- WELCOME SCREEN (If no messages yet) ---
if len(st.session_state.messages) == 0:
    render_welcome_hero()
    render_quick_action_cards()

# --- RENDER CHAT HISTORY ---
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="chat-bubble-user">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-bubble-ai">
            <div class="ai-author-tag">✦ StudyAbroad AI Copilot</div>
            {msg["content"]}
        </div>
        """, unsafe_allow_html=True)
        
        if "profile_card" in msg and msg["profile_card"]:
            render_profile_card_inline(msg["profile_card"])
        if "agent_meta" in msg and msg["agent_meta"]:
            meta = msg["agent_meta"]
            if meta.get("tool_results", {}).get("universities"):
                for u in meta["tool_results"]["universities"][:3]:
                    render_university_card_copilot(u, key_prefix=f"hist_u_{u.get('university')[:8]}")
            if meta.get("tool_results", {}).get("scholarships"):
                for s in meta["tool_results"]["scholarships"][:2]:
                    render_scholarship_card_copilot(s, key_prefix=f"hist_s_{s.get('scholarship_name')[:8]}")
            render_agent_activity_tracer(meta)

# --- CONTEXTUAL SUGGESTION CHIPS ---
quick_chips = []
if len(st.session_state.messages) == 0:
    quick_chips = [
        ("✨ Start Conversation", "Hi! I want to start my study abroad journey."),
        ("🎓 7.43 CGPA, ₹35L budget, UK MSc CS", "I'm Nikhil, my CGPA is 7.43, I have ₹35 lakh budget and want MSc Computer Science in the UK.")
    ]
elif not st.session_state.onboarding_completed:
    if completeness_pct >= 80:
        quick_chips = [("✦ Analyze My Profile", "Analyze my profile and recommend universities, scholarships and next steps.")]
else:
    quick_chips = [
        ("🎓 Find Universities", f"Find universities in {prof.preferred_country} for {prof.preferred_field} within my budget."),
        ("💎 Find Scholarships", f"Recommend scholarships for {prof.preferred_field} in {prof.preferred_country}."),
        ("💰 Cost Breakdown", f"What is the complete tuition and living cost breakdown in {prof.preferred_country}?"),
        ("📋 Admission Guidelines", f"What are the admission requirements and IELTS criteria for {prof.preferred_country}?"),
        ("🗺️ Build My Roadmap", "Create my complete study abroad application roadmap.")
    ]

selected_chip_text = None
if quick_chips:
    st.markdown("<div style='margin-top:0.6rem; margin-bottom:0.6rem;'>", unsafe_allow_html=True)
    chip_cols = st.columns(len(quick_chips))
    for idx, (chip_lbl, chip_val) in enumerate(quick_chips):
        if chip_cols[idx].button(chip_lbl, key=f"chip_v2_{idx}", use_container_width=True):
            selected_chip_text = chip_val
    st.markdown("</div>", unsafe_allow_html=True)

# --- CHAT COMPOSER & EXECUTION LOGIC ---
user_query = st.chat_input("Ask anything: 'Find universities in UK under 35 lakhs', 'Compare Oxford vs Cambridge'...")
prompt_to_process = selected_chip_text or user_query

if prompt_to_process:
    # 1. Render User Message
    st.session_state.messages.append({"role": "user", "content": prompt_to_process})
    st.markdown(f'<div class="chat-bubble-user">{prompt_to_process}</div>', unsafe_allow_html=True)

    # 2. Extract entities and update student profile
    updated_prof = ConversationalOnboarding.extract_and_update(
        prompt_to_process,
        st.session_state.student_profile,
        st.session_state.onboarding_expected_field
    )
    st.session_state.student_profile = updated_prof

    pct, next_field, next_q = ConversationalOnboarding.get_profile_completeness(updated_prof)
    st.session_state.onboarding_expected_field = next_field

    # 3. Check if we should continue Onboarding Q&A or run the Full Agent + RAG
    if next_field is not None and not st.session_state.onboarding_completed and "analyze" not in prompt_to_process.lower() and "recommend" not in prompt_to_process.lower():
        formatted_q = next_q.format(
            name=updated_prof.name or "there",
            country=updated_prof.preferred_country or "your target destination",
            field=updated_prof.preferred_field or "your field"
        )
        time.sleep(0.3)
        st.session_state.messages.append({"role": "assistant", "content": formatted_q})
        st.rerun()

    else:
        # Profile is ready or user triggered an agent tool/action
        st.session_state.onboarding_completed = True

        with st.spinner("✦ AI Copilot is querying FAISS vector index and executing agent tools..."):
            is_first_full_analysis = (len([m for m in st.session_state.messages if "agent_meta" in m]) == 0)
            
            agent_result = agent.process_query(prompt_to_process, st.session_state.student_profile)
            response_text = agent_result["response"]

            st.session_state.messages.append({
                "role": "assistant",
                "content": response_text,
                "agent_meta": agent_result,
                "profile_card": updated_prof if is_first_full_analysis else None
            })
            st.session_state.student_profile = agent_result["updated_profile"]
            st.rerun()
