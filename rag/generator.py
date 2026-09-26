import os
from typing import List, Dict, Any, Optional
from openai import OpenAI
from utils.config import OPENAI_API_KEY, OPENAI_BASE_URL, LLM_MODEL_NAME
from utils.profile import StudentProfile
from prompts.prompt_templates import SYSTEM_PROMPT, RAG_PROMPT_TEMPLATE

class RAGGenerator:
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or OPENAI_API_KEY
        self.model = model or LLM_MODEL_NAME
        self.client = OpenAI(api_key=self.api_key) if self.api_key else None

    def generate_response(
        self,
        query: str,
        retrieved_documents: List[Dict[str, Any]],
        profile: StudentProfile,
        tool_results_summary: Optional[str] = None
    ) -> str:
        """
        Generates a grounded answer using the LLM with prompt engineering and retrieved facts.
        Falls back to a structured deterministic synthesizer if no LLM API key is provided.
        """
        context_parts = []
        if tool_results_summary:
            context_parts.append(f"=== STRUCTURED SYSTEM RECOMMENDATIONS & DATA ===\n{tool_results_summary}")
            
        if retrieved_documents:
            retrieval_text = "\n".join([
                f"[{i+1}] ({d.get('topic', 'Topic')} | Source: {d.get('source_file', 'Dataset')} | Score: {d.get('similarity_score', 0):.2f})\n{d.get('text', d.get('content', ''))}"
                for i, d in enumerate(retrieved_documents)
            ])
            context_parts.append(f"=== RETRIEVED KNOWLEDGE DOCUMENTS ===\n{retrieval_text}")

        full_context = "\n\n".join(context_parts) if context_parts else "No specific documents retrieved."

        # Format prompt
        budget_str = f"₹{profile.budget:,.0f} {profile.currency}" if profile.currency == "INR" else f"${profile.budget:,.0f} {profile.currency}"
        user_prompt = RAG_PROMPT_TEMPLATE.format(
            context=full_context,
            name=profile.name,
            cgpa=profile.cgpa,
            budget_formatted=budget_str,
            preferred_country=profile.preferred_country,
            preferred_field=profile.preferred_field,
            degree_level=profile.degree_level,
            preferred_intake=profile.preferred_intake or "Upcoming Fall",
            query=query
        )

        if self.client and self.api_key:
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.2
                )
                return response.choices[0].message.content or ""
            except Exception as e:
                print(f"LLM generation error: {e}. Falling back to structured grounded response.")

        # Grounded Deterministic Fallback Generator
        return self._generate_fallback_response(query, retrieved_documents, profile, tool_results_summary)

    def _generate_fallback_response(
        self,
        query: str,
        retrieved_documents: List[Dict[str, Any]],
        profile: StudentProfile,
        tool_results_summary: Optional[str]
    ) -> str:
        """High-quality grounded fallback generator ensuring 100% offline functionality."""
        lines = []
        lines.append(f"## 🎓 StudyAbroad AI Advisory for {profile.name}\n")
        lines.append(f"**Target Program:** {profile.degree_level} in {profile.preferred_field} | **Country:** {profile.preferred_country} | **CGPA:** {profile.cgpa} | **Budget:** ₹{profile.budget_in_inr():,.0f} INR\n")
        
        if tool_results_summary:
            lines.append("### 📊 Personalized Analysis & Recommendations")
            lines.append(tool_results_summary)
            lines.append("")

        if retrieved_documents:
            lines.append("### 🔍 Verified Knowledge Base Insights")
            for i, doc in enumerate(retrieved_documents[:3], 1):
                topic = doc.get("topic", "Relevant Information")
                text = doc.get("text", doc.get("content", ""))
                # Format text cleanly
                snippet = text.strip()
                lines.append(f"**{i}. {topic}**")
                lines.append(f"> {snippet}\n")

        lines.append("### 🗺️ Recommended Action Plan")
        lines.append(f"1. **Shortlist Target Institutions:** Review top recommended universities in {profile.preferred_country} aligned with your budget.")
        lines.append("2. **Prepare Standardized Tests:** Register for IELTS / TOEFL (target 6.5 - 7.5 bands) or GRE if required.")
        lines.append("3. **Document Drafting:** Prepare 2-3 Letters of Recommendation (LORs), Statement of Purpose (SOP), and official transcripts.")
        lines.append("4. **Apply for Scholarships:** Submit scholarship applications early before deadlines.")
        lines.append("5. **Financial & Visa Verification:** Prepare bank statements and proof of liquid funds for student visa compliance.\n")

        lines.append("### 📚 Sources Consulted")
        sources = set([d.get("source_file", "Master Dataset") for d in retrieved_documents]) if retrieved_documents else ["Master University & Cost Dataset"]
        for s in sources:
            lines.append(f"- `{s}`")
            
        lines.append("\n> ⚠️ **Important Verification Note:** Recommendations are decision-support insights derived from verified dataset records. Fees, living expenses, scholarships, and visa criteria vary per intake and must be confirmed directly with official university admissions portals.")
        
        return "\n".join(lines)
