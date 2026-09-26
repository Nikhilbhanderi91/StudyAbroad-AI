# 🎓 StudyAbroad AI — Viva Voce & Presentation Guide

### 1. What is RAG and why is it used in StudyAbroad AI?
**Answer:** Retrieval-Augmented Generation (RAG) is a technique that retrieves verified context documents from an external vector store (like FAISS) and passes them to the LLM prompt before generating an answer. In StudyAbroad AI, it is used to ground facts (tuition fees, rankings, scholarship links) to eliminate LLM hallucinations.

---

### 2. What is Agentic AI and how does it differ from a standard chatbot?
**Answer:** A standard chatbot simply predicts the next token from text. An **Agentic AI system** perceives user intent, reasons about necessary sub-tasks, dynamically chooses and calls specific tools (e.g. `calculate_total_cost`, `recommend_scholarships`), gathers intermediate outputs, and synthesizes a final structured action plan.

---

### 3. Why did we choose `all-MiniLM-L6-v2` for embeddings?
**Answer:** `all-MiniLM-L6-v2` maps sentences to a 384-dimensional dense vector space. It delivers state-of-the-art semantic search accuracy while remaining lightweight, fast (<5ms on CPU), and optimal for local Mac/Colab deployment.

---

### 4. What is the role of the FAISS Vector Database?
**Answer:** FAISS (Facebook AI Similarity Search) provides high-performance vector indexing. In our project, we use `IndexFlatIP` with normalized vectors to execute rapid Cosine Similarity nearest-neighbor lookups over 6,981 indexed knowledge records.

---

### 5. What are the Traditional AI vs Generative AI components in this project?
**Answer:**
* **Traditional AI / NLP:** TF-IDF Cosine Similarity, RapidFuzz entity matching, multi-criteria weighted scoring algorithm.
* **Generative AI:** Dense Sentence Transformer embeddings, FAISS vector retrieval, LLM Prompt Engineering, Agentic Tool Calling, and grounded generation.

---

### 6. How is user profile information extracted from natural language?
**Answer:** The `IntentDetector` uses regex and pattern-matching NLP parsers to extract attributes like `cgpa: 7.43`, `budget: 3500000 INR`, `country: UK`, and `field: Computer Science` directly from chat messages and updates the active session profile automatically.
