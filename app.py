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
    render_profile_progress_bar,
    render_profile_card_inline,
    render_university_card_inline,
    render_scholarship_card_inline,
    render_agent_activity_tracer
)

# Set Streamlit Page Configuration
st.set_page_config(
    page_title="StudyAbroad AI — Conversational Agentic Advisor",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Inject Custom SaaS CSS
load_custom_css()

# Cache AI Agent & Knowledge Base
@st.cache_resource(show_spinner="Connecting AI Agent, Embeddings & FAISS Vector Index...")
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
    # First greeting from AI
    first_greeting = (
        "Hi! 👋 I'm **StudyAbroad AI**, your personal Study Abroad Advisor.\n\n"
        "I'll help you explore universities, scholarships, costs, and your application journey "
        "grounded in verified global datasets.\n\n"
        "Let's start with you. **What's your name?**"
    )
    st.session_state.messages = [
        {"role": "assistant", "content": first_greeting}
    ]

# --- SIDEBAR: Conversational Context & Saved Items ---
with st.sidebar:
    st.markdown("""
    <div style="display:flex; align-items:center; gap:0.75rem; margin-bottom:1.25rem;">
        <span style="font-size:2rem;">🎓</span>
        <div>
            <div style="font-weight:800; font-size:1.15rem; color:#FFFFFF;">StudyAbroad AI</div>
            <div style="font-size:0.75rem; color:#818CF8; font-weight:600;">CONVERSATIONAL AGENT</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("＋ New Conversation", use_container_width=True):
        st.session_state.messages = [
            {"role": "assistant", "content": "Hi! 👋 Let's start fresh. **What's your name?**"}
        ]
        st.session_state.student_profile = StudentProfile(
            name="", cgpa=0.0, budget=0.0, currency="INR", preferred_country="", preferred_field="", degree_level=""
        )
        st.session_state.onboarding_completed = False
        st.session_state.onboarding_expected_field = "name"
        st.toast("Started new conversation!", icon="✨")
        st.rerun()

    st.markdown("---")
    
    # Active Profile Snapshot
    p = st.session_state.student_profile
    completeness, _, _ = ConversationalOnboarding.get_profile_completeness(p)
    
    st.markdown(f"**👤 Profile Strength:** `{completeness}%`")
    if p.name:
        st.markdown(f"- **Student:** {p.name}")
    if p.cgpa > 0:
        st.markdown(f"- **Academic Score:** {p.cgpa} CGPA")
    if p.preferred_country:
        st.markdown(f"- **Target Country:** {p.preferred_country}")
    if p.preferred_field:
        st.markdown(f"- **Program / Field:** {p.preferred_field} ({p.degree_level or 'Master'})")
    if p.budget > 0:
        st.markdown(f"- **Budget:** ₹{p.budget_in_inr():,.0f} INR")

    st.markdown("---")
    
    # Saved Items in Sidebar
    st.markdown("**❤️ Your Saved Shortlist:**")
    if st.session_state.saved_universities:
        st.markdown("*Universities:*")
        for u in st.session_state.saved_universities:
            st.markdown(f"- 🎓 `{u}`")
    else:
        st.caption("No universities saved yet.")

    if st.session_state.saved_scholarships:
        st.markdown("*Scholarships:*")
        for s in st.session_state.saved_scholarships:
            st.markdown(f"- 🎁 `{s}`")

    st.markdown("---")
    st.markdown("<div style='font-size:0.75rem; color:#64748B;'>RAG + Agentic AI Engine &bull; FAISS 6,981 records</div>", unsafe_allow_html=True)


# --- TOP APP HEADER & PROGRESS ---
st.markdown("""
<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.8rem;">
    <div style="display:flex; align-items:center; gap:0.5rem;">
        <span style="font-size:1.4rem;">🎓</span>
        <span style="font-weight:800; font-size:1.25rem; color:#FFFFFF;">StudyAbroad AI</span>
    </div>
    <div class="ai-status-indicator">
        <span class="ai-pulse-dot"></span> AI Online
    </div>
</div>
""", unsafe_allow_html=True)

# Render Profile Progress
prof = st.session_state.student_profile
completeness_pct, next_missing_field, next_q_template = ConversationalOnboarding.get_profile_completeness(prof)
if completeness_pct > 0:
    render_profile_progress_bar(completeness_pct, prof)

# --- RENDER CHAT HISTORY ---
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="chat-bubble-user">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-bubble-ai">{msg["content"]}</div>', unsafe_allow_html=True)
        if "profile_card" in msg and msg["profile_card"]:
            render_profile_card_inline(msg["profile_card"])
        if "agent_meta" in msg and msg["agent_meta"]:
            meta = msg["agent_meta"]
            if meta.get("tool_results", {}).get("universities"):
                for u in meta["tool_results"]["universities"][:3]:
                    render_university_card_inline(u, key_prefix=f"hist_u_{u.get('university')[:8]}")
            if meta.get("tool_results", {}).get("scholarships"):
                for s in meta["tool_results"]["scholarships"][:2]:
                    render_scholarship_card_inline(s, key_prefix=f"hist_s_{s.get('scholarship_name')[:8]}")
            render_agent_activity_tracer(meta)

# --- DYNAMIC QUICK PROMPT CHIPS ---
quick_chips = []
if not st.session_state.onboarding_completed:
    if not prof.name:
        quick_chips = [("👋 I'm Nikhil", "My name is Nikhil"), ("🎓 7.43 CGPA, ₹35 Lakh budget for UK MSc CS", "I'm Nikhil, my CGPA is 7.43, I have ₹35 lakh budget and want MSc Computer Science in the UK.")]
    elif completeness_pct >= 80:
        quick_chips = [("✦ Analyze My Profile", "Analyze my profile and recommend universities, scholarships and next steps.")]
else:
    quick_chips = [
        ("🎓 More Universities", f"Find top universities in {prof.preferred_country} for {prof.preferred_field} within my budget."),
        ("💰 Find Scholarships", f"Recommend scholarships for {prof.preferred_field} in {prof.preferred_country}."),
        ("⚖️ Compare Universities", f"Compare the top recommended universities for me."),
        ("📋 Admission Requirements", f"What are the admission requirements and IELTS criteria for {prof.preferred_country}?"),
        ("🗺️ Build My Roadmap", "Create my complete study abroad application roadmap.")
    ]

selected_chip_text = None
if quick_chips:
    st.markdown("<div style='margin-top:0.4rem; margin-bottom:0.6rem;'>", unsafe_allow_html=True)
    chip_cols = st.columns(len(quick_chips))
    for idx, (chip_lbl, chip_val) in enumerate(quick_chips):
        if chip_cols[idx].button(chip_lbl, key=f"chip_{idx}", use_container_width=True):
            selected_chip_text = chip_val
    st.markdown("</div>", unsafe_allow_html=True)

# --- CHAT INPUT & EXECUTION LOGIC ---
user_query = st.chat_input("Ask anything about universities, scholarships, costs, or admission...")
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
        # Formulate intelligent progressive follow-up question
        formatted_q = next_q.format(
            name=updated_prof.name or "there",
            country=updated_prof.preferred_country or "your target destination",
            field=updated_prof.preferred_field or "your field"
        )
        time.sleep(0.3)
        st.markdown(f'<div class="chat-bubble-ai">{formatted_q}</div>', unsafe_allow_html=True)
        st.session_state.messages.append({"role": "assistant", "content": formatted_q})
        st.rerun()

    else:
        # Profile is either complete or user triggered a recommendation/action
        st.session_state.onboarding_completed = True

        with st.spinner("✦ AI Agent is analyzing your profile, querying FAISS vector store, and running tools..."):
            # If profile was just completed, show verified profile card
            is_first_full_analysis = (len([m for m in st.session_state.messages if "agent_meta" in m]) == 0)
            
            agent_result = agent.process_query(prompt_to_process, st.session_state.student_profile)
            response_text = agent_result["response"]

            st.markdown(f'<div class="chat-bubble-ai">{response_text}</div>', unsafe_allow_html=True)
            
            if is_first_full_analysis:
                render_profile_card_inline(updated_prof)

            # Render inline cards
            if agent_result.get("tool_results", {}).get("universities"):
                st.markdown("##### 🎓 Recommended Universities")
                for u in agent_result["tool_results"]["universities"][:3]:
                    render_university_card_inline(u, key_prefix=f"res_u_{u.get('university')[:8]}")

            if agent_result.get("tool_results", {}).get("scholarships"):
                st.markdown("##### 💰 Matching Scholarships")
                for s in agent_result["tool_results"]["scholarships"][:2]:
                    render_scholarship_card_inline(s, key_prefix=f"res_s_{s.get('scholarship_name')[:8]}")

            render_agent_activity_tracer(agent_result)

            # Save in chat history
            msg_data = {
                "role": "assistant",
                "content": response_text,
                "agent_meta": agent_result,
                "profile_card": updated_prof if is_first_full_analysis else None
            }
            st.session_state.messages.append(msg_data)
            st.session_state.student_profile = agent_result["updated_profile"]
            st.rerun()
