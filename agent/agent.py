import time
from typing import Dict, Any, List, Optional
from utils.profile import StudentProfile
from agent.intent import IntentDetector
from agent.tool_registry import execute_tool
from rag.generator import RAGGenerator
from rag.retriever import RAGRetriever

class StudyAbroadAgent:
    """
    Agentic AI Controller for StudyAbroad AI.
    Coordinates intent detection, dynamic tool orchestration, vector RAG retrieval, and grounded generation.
    """

    def __init__(self, api_key: Optional[str] = None):
        self.intent_detector = IntentDetector()
        self.retriever = RAGRetriever()
        self.generator = RAGGenerator(api_key=api_key)

    def process_query(self, user_query: str, current_profile: StudentProfile) -> Dict[str, Any]:
        start_time = time.time()
        
        # 1. Intent Detection & Profile Extraction
        routing_decision = self.intent_detector.detect_intent_and_tools(user_query)
        detected_intent = routing_decision["intent"]
        tools_to_run = routing_decision["tools"]
        extracted_info = routing_decision.get("extracted_profile", {})

        # Merge extracted natural language profile attributes into active profile
        active_profile = current_profile.model_copy()
        if "cgpa" in extracted_info and extracted_info["cgpa"]:
            active_profile.cgpa = extracted_info["cgpa"]
        if "budget" in extracted_info and extracted_info["budget"]:
            active_profile.budget = extracted_info["budget"]
        if "currency" in extracted_info and extracted_info["currency"]:
            active_profile.currency = extracted_info["currency"]
        if "preferred_country" in extracted_info and extracted_info["preferred_country"]:
            active_profile.preferred_country = extracted_info["preferred_country"]
        if "preferred_field" in extracted_info and extracted_info["preferred_field"]:
            active_profile.preferred_field = extracted_info["preferred_field"]
        if "degree_level" in extracted_info and extracted_info["degree_level"]:
            active_profile.degree_level = extracted_info["degree_level"]

        # 2. Dynamic Tool Calling
        tool_results = {}
        tool_execution_logs = []
        structured_summaries = []

        for tool_name in tools_to_run:
            t0 = time.time()
            res = {}
            if tool_name == "recommend_universities":
                res = execute_tool("recommend_universities", profile=active_profile, top_n=5)
                tool_results["universities"] = res.get("recommendations", [])
                if res.get("recommendations"):
                    lines = [f"- **{u['university']}** ({u['country']}) | Rank: #{u['rank_2025']} | Score: {u['recommendation_score']}/100 | Annual Cost: ${u['estimated_annual_cost_usd']:,.0f} USD (₹{u['estimated_annual_cost_inr']:,.0f} INR)\n  *Reason:* {u['reason']}" for u in res["recommendations"][:4]]
                    structured_summaries.append("🎓 **Top Recommended Universities:**\n" + "\n".join(lines))

            elif tool_name == "recommend_countries":
                res = execute_tool("recommend_countries", profile=active_profile, top_n=4)
                tool_results["countries"] = res.get("countries", [])
                if res.get("countries"):
                    lines = [f"- **{c['country']}** (Score: {c['suitability_score']}/100) — Avg Cost: ${c['average_annual_cost_usd']:,.0f} USD/yr | Avg QS Rank: {c['average_qs_ranking']}" for c in res["countries"]]
                    structured_summaries.append("🌍 **Recommended Study Abroad Countries:**\n" + "\n".join(lines))

            elif tool_name == "recommend_scholarships":
                res = execute_tool("recommend_scholarships", profile=active_profile, top_n=4)
                tool_results["scholarships"] = res.get("scholarships", [])
                if res.get("scholarships"):
                    lines = [f"- **{s['scholarship_name']}** | Location: {s['location']} | Award: ${s['amount']} | Deadline: {s['deadline']}" for s in res["scholarships"][:3]]
                    structured_summaries.append("💰 **Matching Scholarships:**\n" + "\n".join(lines))

            elif tool_name == "search_scholarships":
                res = execute_tool("search_scholarships", keyword=active_profile.preferred_field, country=active_profile.preferred_country, top_n=3)
                tool_results["search_scholarships"] = res

            elif tool_name == "create_application_roadmap":
                res = execute_tool("create_application_roadmap", profile=active_profile)
                tool_results["roadmap"] = res.get("roadmap", [])
                if res.get("roadmap"):
                    lines = [f"**Step {item['step']}: {item['phase']}** — {item['description']}" for item in res["roadmap"][:6]]
                    structured_summaries.append("🗺️ **Action Roadmap Timeline:**\n" + "\n".join(lines))

            elif tool_name == "calculate_total_cost":
                res = execute_tool("calculate_total_cost", university_name=active_profile.preferred_country, country=active_profile.preferred_country)
                tool_results["cost_breakdown"] = res

            elif tool_name == "compare_universities":
                res = execute_tool("compare_universities", univ1="Oxford", univ2="Cambridge")
                tool_results["comparison"] = res

            elif tool_name == "get_admission_information":
                res = execute_tool("get_admission_information", country=active_profile.preferred_country, program=active_profile.preferred_field)
                tool_results["admission"] = res

            tool_duration = round((time.time() - t0) * 1000, 2)
            tool_execution_logs.append({
                "tool": tool_name,
                "status": "success" if "error" not in res else "error",
                "execution_ms": tool_duration
            })

        # 3. RAG Semantic Retrieval
        retrieval_query = f"{user_query} {active_profile.preferred_country} {active_profile.preferred_field} {active_profile.degree_level}"
        retrieved_docs = self.retriever.retrieve_documents(retrieval_query, top_k=4)

        # 4. LLM Generation
        tool_summary_str = "\n\n".join(structured_summaries)
        final_answer = self.generator.generate_response(
            query=user_query,
            retrieved_documents=retrieved_docs,
            profile=active_profile,
            tool_results_summary=tool_summary_str
        )

        total_time_ms = round((time.time() - start_time) * 1000, 2)

        return {
            "query": user_query,
            "detected_intent": detected_intent,
            "tools_executed": tools_to_run,
            "tool_execution_logs": tool_execution_logs,
            "updated_profile": active_profile,
            "tool_results": tool_results,
            "retrieved_documents": retrieved_docs,
            "response": final_answer,
            "latency_ms": total_time_ms
        }
