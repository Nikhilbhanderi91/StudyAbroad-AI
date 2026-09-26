# 🎬 StudyAbroad AI — Video Recording & Demo Workflow Playbook

> **Project Name:** StudyAbroad AI — RAG-Based Agentic AI Personalized Study Abroad Advisor  
> **Presenter:** Nikhil Bhanderi  
> **Target Audience:** University Evaluators, Academic Mentors & Viva Examination Panel  
> **Estimated Video Duration:** 6 – 8 Minutes  

---

## 📋 PRE-RECORDING CHECKLIST

Before pressing record, verify each item:

- [ ] **Application Running:** Executed `streamlit run app.py` (accessible at `http://localhost:8501`).
- [ ] **Clean Browser State:** Closed all unnecessary tabs, bookmarks bar hidden, full-screen mode enabled (`Cmd + Shift + F` or `F11`).
- [ ] **Clean Chat History:** Clicked **"＋ New Conversation"** in sidebar to start with the futuristic welcome hero.
- [ ] **Audio & Resolution:** Microphone volume tested; display zoom set to 100% or 110% for optimal readability.
- [ ] **Notifications Disabled:** Mac "Do Not Disturb" / Focus Mode turned ON.
- [ ] **API Keys & Secrets:** Ensured `.env` and terminal windows with credentials are not exposed on screen.
- [ ] **Demo Profile Memorized:**
  - **Name:** Nikhil Bhanderi
  - **Academic Score:** 7.43 CGPA
  - **Degree Target:** Master's (MSc)
  - **Field:** Computer Science
  - **Budget:** ₹35,00,000 INR (~$42,000 USD)
  - **Target Country:** United Kingdom

---

## ⏱️ VIDEO TIMELINE AT A GLANCE

| Stage | Section | Target Duration | Key Concept Demonstrated |
|---|---|---|---|
| **01** | Project Introduction & Problem Statement | 0:00 – 0:45 (45s) | Problem & Generative AI Overview |
| **02** | UI/UX & Conversational AI Onboarding | 0:45 – 1:45 (60s) | Natural Language Profile Extraction |
| **03** | University Recommendations & Match Scoring | 1:45 – 2:45 (60s) | Multi-Factor Decision Engine |
| **04** | RAG (Retrieval-Augmented Generation) Demo | 2:45 – 3:45 (60s) | FAISS Dense Vector Retrieval |
| **05** | Agentic AI Tool Orchestration Demo | 3:45 – 4:45 (60s) | Autonomous Intent & Tool Calling |
| **06** | Scholarships, Costs & Roadmap Generation | 4:45 – 6:00 (75s) | Integrated Study Abroad Intelligence |
| **07** | Technical Architecture & System Status | 6:00 – 6:45 (45s) | System Design & Performance |
| **08** | Conclusion & Viva Wrap-up | 6:45 – 7:15 (30s) | Final Value Summary |

---

## 🎥 STEP-BY-STEP RECORDING GUIDE

---

### STEP 01 — PROJECT INTRODUCTION
- **Screen Action:** Show the clean top hero of StudyAbroad AI with the pulsing neon AI Orb and the tagline: *"Your AI Copilot for Studying Abroad."*
- **What to Say:**
  > *"Hello everyone. Welcome to the demonstration of **StudyAbroad AI** — a personalized Study Abroad Advisor powered by **Retrieval-Augmented Generation (RAG)**, **Agentic AI Tool Calling**, and multi-factor recommendation algorithms.*
  >
  > *Selecting an international university is a complex challenge where students must balance academic eligibility, tuition fees, cost of living, and scholarship deadlines. Traditional chatbots often hallucinate unverified numbers. StudyAbroad AI solves this by combining verified structured datasets, dense vector search via FAISS, and an autonomous Agentic decision layer inside a single conversational copilot."*
- **Viewer Sees:** Sleek dark Obsidian interface (`#070A12`), glowing AI Orb, status badge (`● AI Online • RAG Ready`).
- **Concept:** Problem Definition & Proposed Generative AI Solution.
- **Recording Tip:** Keep your cursor still over the logo for 2 seconds before scrolling.

---

### STEP 02 — CONVERSATIONAL ONBOARDING & PROFILE EXTRACTION
- **Screen Action:** Click the quick prompt chip or type in the chat input:
  ```text
  "I'm Nikhil, my CGPA is 7.43, I have around 35 lakh budget and want MSc Computer Science in the UK."
  ```
  Press enter and watch the AI seamlessly extract the attributes and update the progress bar.
- **What to Say:**
  > *"Instead of forcing students to fill out long, rigid forms, StudyAbroad AI begins conversationally. Here, I'll provide my profile in natural language: 7.43 CGPA, 35 Lakh budget, targeting MSc Computer Science in the UK.*
  >
  > *Notice how the system immediately parses my academic score, converts my currency to INR, captures my target country, and updates the profile strength to 100% while rendering an inline verified profile summary card."*
- **Viewer Sees:**
  - User chat bubble.
  - Profile strength progress bar animating to 100%.
  - Glowing **✦ VERIFIED STUDY ABROAD PROFILE** card displaying Name, CGPA (7.43), Budget (₹35.0L), Country (UK), and Field (Computer Science).
- **Concept:** Natural Language Entity Extraction & Progressive State Tracking.
- **Recording Tip:** Highlight the 6-parameter profile grid briefly before proceeding to the recommendation.

---

### STEP 03 — UNIVERSITY RECOMMENDATION & MATCH SCORING
- **Screen Action:** Show the AI response containing the university recommendation cards. Click **"🤍 Save University"** on the top match (*Imperial College London* or *University of Manchester*).
- **What to Say:**
  > *"The system immediately triggers our multi-factor recommendation engine. It scores universities by evaluating QS world rankings, budget compatibility, country preferences, and program alignment.*
  >
  > *Each card presents an interactive circular match score badge — for example, 91% Match — along with QS global ranking, annual tuition and living expenses in both USD and Lakh INR, and an explainable AI Fit Rationale. Students can save universities directly to their shortlist in the sidebar."*
- **Viewer Sees:**
  - Dynamic university cards with green circular match badges (`91% MATCH`).
  - Progress meters comparing academic & budget compatibility.
  - Toast notification when saving: *"Saved to your Journey! ❤️"*.
- **Concept:** Multi-Factor Weighted Scoring & Explainable AI.
- **Recording Tip:** Hover over the circular match score badge to show the micro-animation.

---

### STEP 04 — RAG (RETRIEVAL-AUGMENTED GENERATION) DEMONSTRATION
- **Screen Action:** Type a factual question into the chat:
  ```text
  "What are the admission requirements and estimated living costs for UK universities?"
  ```
  Wait 1.5 seconds for the response, then expand the **"⚡ Agent Activity & RAG Citations"** drop-down.
- **What to Say:**
  > *"Now let's examine the RAG pipeline. When I ask about admission requirements and living costs, the system does not simply guess. It converts my query into a dense embedding using `all-MiniLM-L6-v2` and searches our local **FAISS vector store** containing over 6,980 indexed dataset chunks.*
  >
  > *Expanding the RAG Citations section, we can see the exact source documents retrieved with their cosine similarity relevance scores — such as the Master University Dataset and Country Intelligence guide. This guarantees 100% factual grounding and eliminates hallucinations."*
- **Viewer Sees:**
  - Structured grounded answer detailing IELTS band requirements (6.5–7.5), academic transcripts, and SOP requirements.
  - Expanded **RAG Knowledge Chunks** showing `Doc 1: Country Study Guide: United Kingdom (Relevance: 0.862)`.
  - Important official verification disclaimer.
- **Concept:** RAG Vector Search, Dense Embeddings & Anti-Hallucination Grounding.
- **Recording Tip:** Pause for 3 seconds on the expanded citation box so the evaluator can clearly read the relevance scores and source file paths.

---

### STEP 05 — AGENTIC AI & TOOL ORCHESTRATION DEMO
- **Screen Action:** Click the quick prompt chip or type:
  ```text
  "Find scholarships for MSc Computer Science in the UK"
  ```
  Show the AI dynamic tool routing under **"⚡ Agent Activity"**.
- **What to Say:**
  > *"This brings us to the Agentic AI capability. When I request scholarships, the autonomous agent analyzes the user's intent, inspects the active profile, and decides which specific tools to orchestrate.*
  >
  > *Rather than executing every script indiscriminately, the agent dynamically calls `search_scholarships` and `recommend_scholarships` from our tool registry, retrieves the relevant financial aid records, and presents them in real-time."*
- **Viewer Sees:**
  - Intent classification: `Scholarship Search`.
  - Tool execution logs: `✓ search_scholarships (12ms)`, `✓ recommend_scholarships (18ms)`.
  - Execution latency metric: `< 300 ms`.
- **Concept:** Autonomous Intent Classification & Dynamic Tool Calling.
- **Recording Tip:** Point out that execution latency is measured and displayed live.

---

### STEP 06 — SCHOLARSHIPS, COSTS & APPLICATION ROADMAP
- **Screen Action:** Scroll down to display the matching **Scholarship Cards** and then type:
  ```text
  "Create my complete study abroad application roadmap"
  ```
  Show the generated 12-step milestone plan.
- **What to Say:**
  > *"Here are the matching scholarship cards, complete with award amounts, intake deadlines, and direct official application links.*
  >
  > *Next, I'll request a complete application roadmap. The agent synthesizes our 12-stage milestone pipeline — guiding the student through GPA assessment, English standardized tests (IELTS/TOEFL), LOR and SOP drafting, priority intake submissions, visa financial proofs (28-day liquid funds), and pre-departure preparation."*
- **Viewer Sees:**
  - Cyan-glowing scholarship cards with verified application portal links.
  - Step-by-step numbered roadmap formatted with bold milestone phases.
- **Concept:** End-to-End Decision Support & Personalized Milestone Planning.
- **Recording Tip:** Show that the roadmap matches the student's specific target intake (Fall 2025).

---

### STEP 07 — TECHNICAL ARCHITECTURE & PERFORMANCE
- **Screen Action:** Open the sidebar, show the saved shortlist, and summarize the system architecture diagram.
- **What to Say:**
  > *"Let's review the end-to-end technical architecture:*
  > 1. *Frontend:* Streamlit conversational UI with custom CSS design tokens.
  > 2. *Agent Layer:* Pydantic profile validation, regex & pattern intent routing, and dynamic tool dispatcher.
  > 3. *RAG & Vector Store:* 6,981 documents indexed in FAISS (`IndexFlatIP`) using 384-dimensional Sentence Transformers.
  > 4. *Traditional AI Engine:* RapidFuzz entity normalization and multi-criteria weighted scoring formulas.
  > 5. *Evaluation Suite:* Verified **100% HitRate@5** on retrieval and **100% Intent Routing Accuracy** across automated benchmark tests."*
- **Viewer Sees:** Clean sidebar with saved universities and scholarships, system status metrics.
- **Concept:** System Architecture, Evaluation Metrics & Provenance.
- **Recording Tip:** Mention the evaluation scripts in the repository (`evaluate_rag.py` and `evaluate_agent.py`).

---

### STEP 08 — CONCLUSION & VIVA WRAP-UP
- **Screen Action:** Scroll back to the top of the chat showing the clean header and summary.
- **What to Say:**
  > *"In summary, StudyAbroad AI demonstrates how modern Generative AI can be combined with deterministic decision systems. By uniting Conversational AI, RAG factual grounding, and Agentic Tool Calling into one unified interface, we provide students with an intelligent, reliable, and personalized guide for their global education journey.*
  >
  > *Thank you for your time. I am now ready for any questions."*
- **Viewer Sees:** Full-screen polished app view.
- **Concept:** Final Wrap-Up & Value Delivery.

---

## 🛡️ BACKUP DEMO PLAN (CONTINGENCY)

In case of any unexpected event during recording:

| Scenario | Immediate Action |
|---|---|
| **Slow Internet / Offline Mode** | StudyAbroad AI includes built-in grounded deterministic fallback generators. The app works **100% offline** without needing external API connectivity. |
| **Accidental Bad Input** | Click **"＋ New Conversation"** in the sidebar to instantly restart the session state in 0.5s. |
| **Port Conflict on 8501** | Run `streamlit run app.py --server.port 8502`. |
| **Terminal Crash** | Re-run `source .venv/bin/activate && streamlit run app.py` and refresh browser. |

---

## 🎤 QUICK VIVA CHEAT SHEET

If asked during your demonstration:

1. **Why FAISS and not ChromaDB/Pinecone?**  
   *Answer:* FAISS `IndexFlatIP` provides exact Cosine Inner-Product similarity directly in memory on macOS with zero external server dependencies and sub-3ms retrieval latency over 6,981 documents.
2. **How do you prevent hallucinations?**  
   *Answer:* The LLM prompt is grounded strictly in top-k FAISS retrieved context blocks with exact dataset citations, backed by a strict fallback when evidence is missing.
3. **What is the Agentic component?**  
   *Answer:* The `IntentDetector` and `tool_registry` inspect user queries, classify intent, extract missing profile entities, and dynamically orchestrate tools rather than executing every function indiscriminately.
