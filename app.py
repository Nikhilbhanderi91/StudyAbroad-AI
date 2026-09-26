import os
import sys
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
from app.ui import render_custom_css, render_university_cards, render_scholarship_cards, render_agent_process

# Streamlit Page Setup
st.set_page_config(
    page_title="StudyAbroad AI — RAG & Agentic Advisor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
render_custom_css()

# Cache Knowledge Base & Agent
@st.cache_resource(show_spinner="Loading FAISS Vector Database & AI Models...")
def load_agent():
    if not FAISS_INDEX_PATH.exists():
        build_complete_knowledge_base(force_rebuild=False)
    return StudyAbroadAgent()

agent = load_agent()

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

if "student_profile" not in st.session_state:
    st.session_state.student_profile = StudentProfile(
        name="Nikhil",
        cgpa=7.43,
        budget=3500000.0,
        currency="INR",
        preferred_country="United Kingdom",
        preferred_field="Computer Science",
        degree_level="Master",
        ranking_priority="High",
        english_test_score="IELTS 7.0",
        work_experience="1 Year",
        preferred_intake="Fall 2025"
    )

# --- SIDEBAR: Student Profile & Settings ---
with st.sidebar:
    st.image("https://img.icons8.com/clouds/200/graduation-cap.png", width=100)
    st.title("👤 Student Profile")
    st.caption("Personalize your study abroad recommendations")
    
    with st.form("profile_form"):
        name = st.text_input("Full Name", value=st.session_state.student_profile.name)
        cgpa = st.number_input("Academic CGPA (out of 10)", min_value=0.0, max_value=10.0, value=float(st.session_state.student_profile.cgpa), step=0.01)
        
        c1, c2 = st.columns([2, 1])
        budget = c1.number_input("Total Budget", min_value=0.0, value=float(st.session_state.student_profile.budget), step=50000.0)
        currency = c2.selectbox("Currency", ["INR", "USD", "GBP", "EUR", "CAD", "AUD"], index=0)
        
        country = st.selectbox(
            "Preferred Country",
            ["United Kingdom", "United States", "Germany", "Australia", "Canada", "Ireland", "Singapore", "Netherlands", "France", "Switzerland"],
            index=0
        )
        
        field = st.text_input("Target Field / Major", value=st.session_state.student_profile.preferred_field)
        degree = st.selectbox("Degree Level", ["Master", "Bachelor", "PhD", "Diploma"], index=0)
        ranking_pri = st.selectbox("Ranking Priority", ["High", "Balanced", "Moderate"], index=0)
        ielts = st.text_input("English Test Score", value=st.session_state.student_profile.english_test_score or "IELTS 7.0")
        intake = st.selectbox("Target Intake", ["Fall 2025", "Spring 2026", "Fall 2026"], index=0)
        
        save_btn = st.form_submit_button("💾 Save Profile")
        if save_btn:
            st.session_state.student_profile = StudentProfile(
                name=name,
                cgpa=cgpa,
                budget=budget,
                currency=currency,
                preferred_country=country,
                preferred_field=field,
                degree_level=degree,
                ranking_priority=ranking_pri,
                english_test_score=ielts,
                preferred_intake=intake
            )
            st.success("Profile saved successfully!")

    st.divider()
    st.subheader("⚙️ System Control")
    if st.button("🔄 Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

    if st.button("🛠️ Rebuild Knowledge Base"):
        with st.spinner("Rebuilding FAISS Vector Store..."):
            build_complete_knowledge_base(force_rebuild=True)
            st.cache_resource.clear()
            st.success("Knowledge Base refreshed!")

# --- MAIN APP HEADER ---
st.markdown('<div class="main-header">🎓 StudyAbroad AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Your RAG-Powered Agentic Study Abroad Advisor — Powered by Knowledge Embeddings & Multi-Factor Intelligence</div>', unsafe_allow_html=True)

# Active Profile Summary Bar
prof = st.session_state.student_profile
col_p1, col_p2, col_p3, col_p4 = st.columns(4)
col_p1.metric("Student", prof.name)
col_p2.metric("Target Destination", prof.preferred_country)
col_p3.metric("Target Program", f"{prof.degree_level} in {prof.preferred_field}")
col_p4.metric("Budget", f"₹{prof.budget_in_inr():,.0f} INR")

st.markdown("---")

# Quick Action Chips
st.markdown("**⚡ Quick Consultation Starters:**")
qcols = st.columns(6)
quick_queries = [
    ("🎓 Top Universities", f"Find top universities in {prof.preferred_country} for {prof.preferred_field} within my budget."),
    ("💰 Check Total Costs", f"What are the detailed tuition, living, and total costs in {prof.preferred_country}?"),
    ("🎁 Find Scholarships", f"Recommend scholarships for {prof.preferred_field} in {prof.preferred_country}."),
    ("📋 Admission Basics", f"What are the admission requirements and IELTS criteria for {prof.preferred_country}?"),
    ("⚖️ Compare Unis", f"Compare universities in {prof.preferred_country} with global ranking and cost."),
    ("🗺️ Full Roadmap", f"I have {prof.cgpa} CGPA and ₹{prof.budget:,.0f} {prof.currency} budget. Create my complete study abroad plan and roadmap.")
]

clicked_query = None
for i, (label, query_text) in enumerate(quick_queries):
    if qcols[i].button(label, key=f"quick_btn_{i}"):
        clicked_query = query_text

# Render Historical Chat Messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "agent_meta" in msg:
            meta = msg["agent_meta"]
            if meta.get("tool_results", {}).get("universities"):
                render_university_cards(meta["tool_results"]["universities"])
            if meta.get("tool_results", {}).get("scholarships"):
                render_scholarship_cards(meta["tool_results"]["scholarships"])
            render_agent_process(meta)

# Handle Chat Input or Quick Action
user_input = st.chat_input("Ask anything about universities, scholarships, costs, or admission...")
prompt_to_run = clicked_query or user_input

if prompt_to_run:
    # Append User Message
    st.session_state.messages.append({"role": "user", "content": prompt_to_run})
    with st.chat_message("user"):
        st.markdown(prompt_to_run)

    # Agent Execution
    with st.chat_message("assistant"):
        with st.spinner("🤖 StudyAbroad AI is analyzing your profile, querying vector store, and running agent tools..."):
            agent_output = agent.process_query(prompt_to_run, st.session_state.student_profile)
            
            response_text = agent_output["response"]
            st.markdown(response_text)
            
            # Render structured cards
            if agent_output.get("tool_results", {}).get("universities"):
                render_university_cards(agent_output["tool_results"]["universities"])
            if agent_output.get("tool_results", {}).get("scholarships"):
                render_scholarship_cards(agent_output["tool_results"]["scholarships"])

            # Render Agent Process and Trace
            render_agent_process(agent_output)

            # Update session state
            st.session_state.messages.append({
                "role": "assistant",
                "content": response_text,
                "agent_meta": agent_output
            })
            
            # Update session profile if agent extracted new parameters
            st.session_state.student_profile = agent_output["updated_profile"]
