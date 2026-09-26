# 🎓 StudyAbroad AI — RAG-Based Agentic AI Personalized Study Abroad Advisor

StudyAbroad AI is a Generative AI & Decision-Support System that assists prospective international students in discovering university programs, evaluating cost breakdowns, finding scholarships, and generating personalized study abroad roadmaps.

The platform integrates **Retrieval-Augmented Generation (RAG)** over structured educational datasets with **Agentic AI Tool Calling**, powered by **Sentence Transformers**, **FAISS Vector Indexing**, and a **Streamlit Web Interface**.

---

## 🌟 Architecture & Highlights

```
                                  USER (Streamlit UI)
                                         │
                                         ▼
                                   AGENT ENGINE
                           (Intent Detection & Planning)
                                         │
               ┌─────────────────────────┼─────────────────────────┐
               ▼                         ▼                         ▼
          RAG RETRIEVER             DATA TOOLS               PROFILE & MEMORY
       (SentenceTransformer +     (Univ, Scholarship,       (Session State &
         FAISS Vector Store)      Country, Cost Tools)      Natural Language Parsing)
               │                         │                         │
               └─────────────────────────┼─────────────────────────┘
                                         │
                                         ▼
                                     LLM ENGINE
                           (Grounded Prompt + Evidence)
                                         │
                                         ▼
                        PERSONALIZED ADVISORY + CITATIONS
```

### Key Capabilities
1. **RAG Vector Search:** Semantic similarity search over **6,981 indexed knowledge records** using `all-MiniLM-L6-v2` embeddings and FAISS Inner-Product indexing.
2. **Agentic Tool Calling:** Dynamically maps user queries to structured tools (`recommend_universities`, `recommend_scholarships`, `calculate_total_cost`, `compare_universities`, `create_application_roadmap`).
3. **Multi-Factor Recommendation Engine:** Weighted scoring taking into account Academic Standing (Ranking), Budget Feasibility, Country Preferences, Degree Match, and Data Completeness.
4. **Natural Language Profile Extraction:** Automatically identifies and parses student attributes (e.g. `7.43 CGPA`, `₹35 lakh budget`) from chat queries.
5. **Interactive UI:** Real-time chat with rich visual university and scholarship cards, execution trace metrics, and customizable sidebar profile controls.

---

## 🚀 Quickstart Guide

### 1. Prerequisites & Virtual Environment
```bash
cd "/Users/nikhilbhanderi/Documents/StudyAbroad AI"

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration (Optional LLM Key)
Copy `.env.example` to `.env` and optionally provide your OpenAI API key for online LLM synthesis (the system includes high-quality grounded deterministic fallbacks when operating offline):
```bash
cp .env.example .env
```

### 3. Build Vector Knowledge Base (One-Time)
```bash
python build_knowledge_base.py
```

### 4. Launch Streamlit Application
```bash
streamlit run app.py
```

---

## 🧪 Evaluation & Benchmarks

Run the automated test suite to verify RAG retrieval accuracy and Agentic routing:
```bash
PYTHONPATH=. python3 evaluation/evaluate_rag.py
PYTHONPATH=. python3 evaluation/evaluate_agent.py
```
- **RAG HitRate@5:** `100.0%`
- **Agent Intent Routing Accuracy:** `100.0%`

---

## 📁 Repository Structure

```
StudyAbroad AI/
├── dataset/                         # Raw CSV datasets
├── Master Dataset/                  # Cleaned & recommendation-ready datasets
├── Output/                          # Guidance reports
├── knowledge_base/                  # Structured RAG corpus
├── vector_store/                    # Serialized FAISS index & metadata
├── prompts/                         # Grounded prompt templates
├── rag/                             # RAG chunker, embeddings, vector store, retriever & generator
├── agent/                           # Intent classifier, tool registry, and agent orchestrator
├── tools/                           # Modular tool functions
├── app/                             # UI components & CSS styling
├── evaluation/                      # RAG & Agent evaluation scripts
├── utils/                           # Config, data loader, profile & recommendation engine
├── app.py                           # Main Streamlit Application
├── build_knowledge_base.py          # Vector store builder script
└── requirements.txt                 # Project dependencies
```
