from typing import Dict, Any, List, Optional
from utils.profile import StudentProfile
from utils.recommendation_engine import (
    run_university_recommendations,
    run_country_recommendations,
    run_scholarship_recommendations
)
from utils.data_loader import get_master_university_df, get_recommendation_ready_df
from rag.retriever import RAGRetriever

_retriever = None

def get_rag_retriever() -> RAGRetriever:
    global _retriever
    if _retriever is None:
        _retriever = RAGRetriever()
    return _retriever

def search_universities_tool(query: str, country: Optional[str] = None, top_k: int = 5) -> Dict[str, Any]:
    """Search universities based on text keywords and optional country filter."""
    df = get_recommendation_ready_df()
    if df.empty:
        return {"error": "University dataset not available."}
    
    filtered = df
    if country:
        filtered = filtered[filtered["country"].str.contains(country, case=False, na=False)]
    if query:
        filtered = filtered[filtered["university"].str.contains(query, case=False, na=False) | 
                            filtered["program"].str.contains(query, case=False, na=False)]
    
    records = []
    for _, row in filtered.head(top_k).iterrows():
        records.append({
            "university": row.get("university"),
            "country": row.get("country"),
            "rank_2025": row.get("rank_2025"),
            "program": row.get("program"),
            "tuition_usd": row.get("tuition_numeric", row.get("tuition_usd")),
            "total_estimated_cost_usd": row.get("total_estimated_cost")
        })
    return {"status": "success", "count": len(records), "data": records}

def recommend_universities_tool(profile: StudentProfile, top_n: int = 5) -> Dict[str, Any]:
    """Multi-factor weighted university recommendation based on CGPA, budget, and location."""
    results = run_university_recommendations(profile, top_n=top_n)
    return {"status": "success", "count": len(results), "recommendations": results}

def recommend_countries_tool(profile: StudentProfile, top_n: int = 5) -> Dict[str, Any]:
    """Evaluate and recommend top destination countries for study abroad."""
    results = run_country_recommendations(profile, top_n=top_n)
    return {"status": "success", "count": len(results), "countries": results}

def search_scholarships_tool(keyword: str, country: Optional[str] = None, top_n: int = 5) -> Dict[str, Any]:
    """Search scholarships dataset by keyword and optional country filter."""
    retriever = get_rag_retriever()
    query = f"Scholarship {keyword} {country or ''}".strip()
    docs = retriever.retrieve_documents(query, top_k=top_n)
    return {"status": "success", "count": len(docs), "scholarships": docs}

def recommend_scholarships_tool(profile: StudentProfile, top_n: int = 5) -> Dict[str, Any]:
    """Recommends relevant scholarships matched to student profile."""
    results = run_scholarship_recommendations(profile, top_n=top_n)
    return {"status": "success", "count": len(results), "scholarships": results}

def calculate_total_cost_tool(university_name: str, country: Optional[str] = None) -> Dict[str, Any]:
    """Calculates comprehensive cost breakdown: tuition, rent, living, visa, and insurance."""
    df = get_master_university_df()
    match = df[df["university"].str.contains(university_name, case=False, na=False)]
    if match.empty:
        return {
            "status": "partial",
            "message": f"Exact item for '{university_name}' not found. Showing average cost benchmarks.",
            "average_annual_tuition_usd": 25000,
            "average_living_usd": 12000,
            "estimated_total_usd": 37000,
            "estimated_total_inr": 37000 * 83.5
        }
    row = match.iloc[0]
    tuition = float(row.get("tuition_usd", 25000)) if not pd.isna(row.get("tuition_usd")) else 25000.0
    rent = float(row.get("rent_usd", 1000)) * 12 if not pd.isna(row.get("rent_usd")) else 12000.0
    visa = float(row.get("visa_fee_usd", 400)) if not pd.isna(row.get("visa_fee_usd")) else 400.0
    insurance = float(row.get("insurance_usd", 1200)) if not pd.isna(row.get("insurance_usd")) else 1200.0
    total_usd = tuition + rent + visa + insurance
    
    return {
        "status": "success",
        "university": str(row.get("university")),
        "country": str(row.get("country")),
        "tuition_usd": tuition,
        "annual_rent_usd": rent,
        "visa_fee_usd": visa,
        "insurance_usd": insurance,
        "total_annual_cost_usd": total_usd,
        "total_annual_cost_inr": total_usd * 83.5
    }

def compare_universities_tool(univ1: str, univ2: str) -> Dict[str, Any]:
    """Provides side-by-side comparative metrics for two universities."""
    df = get_recommendation_ready_df()
    u1_df = df[df["university"].str.contains(univ1, case=False, na=False)]
    u2_df = df[df["university"].str.contains(univ2, case=False, na=False)]
    
    r1 = u1_df.iloc[0].to_dict() if not u1_df.empty else {"university": univ1, "error": "Not found in dataset"}
    r2 = u2_df.iloc[0].to_dict() if not u2_df.empty else {"university": univ2, "error": "Not found in dataset"}
    
    return {
        "status": "success",
        "comparison": [
            {
                "university": r1.get("university", univ1),
                "country": r1.get("country", "N/A"),
                "rank_2025": str(r1.get("rank_2025", "N/A")),
                "total_estimated_cost_usd": r1.get("total_estimated_cost", "N/A"),
                "academic_score": r1.get("academic_reputation_score", "N/A"),
                "overall_score": r1.get("overall_score", "N/A")
            },
            {
                "university": r2.get("university", univ2),
                "country": r2.get("country", "N/A"),
                "rank_2025": str(r2.get("rank_2025", "N/A")),
                "total_estimated_cost_usd": r2.get("total_estimated_cost", "N/A"),
                "academic_score": r2.get("academic_reputation_score", "N/A"),
                "overall_score": r2.get("overall_score", "N/A")
            }
        ]
    }

def get_admission_information_tool(country: str, program: Optional[str] = None) -> Dict[str, Any]:
    """Retrieves admission guidelines and standard requirements for target country."""
    retriever = get_rag_retriever()
    query = f"Admission requirements eligibility exams visa guidelines for {country} {program or ''}"
    docs = retriever.retrieve_documents(query, top_k=3)
    return {"status": "success", "country": country, "knowledge_chunks": docs}

def create_application_roadmap_tool(profile: StudentProfile) -> Dict[str, Any]:
    """Generates an action-oriented study abroad application roadmap."""
    intake = profile.preferred_intake or "Fall 2025"
    roadmap = [
        {"step": 1, "phase": "Profile & Budget Assessment", "description": f"Evaluate GPA ({profile.cgpa}) and allocate financial budget (₹{profile.budget_in_inr():,.0f} INR)."},
        {"step": 2, "phase": "Target Country Selection", "description": f"Focus research on {profile.preferred_country} based on visa policies and job opportunities."},
        {"step": 3, "phase": "University Shortlisting", "description": f"Shortlist 3 Dream, 3 Target, and 2 Safe universities for {profile.degree_level} in {profile.preferred_field}."},
        {"step": 4, "phase": "Standardized Tests", "description": "Prepare and take IELTS/TOEFL (target 7.0+) or GRE if required by target institutions."},
        {"step": 5, "phase": "Scholarship Exploration", "description": "Identify external and university merit scholarships with upcoming deadlines."},
        {"step": 6, "phase": "Document Compilation", "description": "Request official transcripts, prepare 3 Letters of Recommendation (LORs), and draft a strong Statement of Purpose (SOP)."},
        {"step": 7, "phase": "Application Submission", "description": f"Submit online applications via university portals for {intake} priority round."},
        {"step": 8, "phase": "Interview & Offer Acceptance", "description": "Attend university interviews (if applicable) and confirm offer letter with deposit."},
        {"step": 9, "phase": "Financial Documentation", "description": "Organize loan sanction letters, bank balances, and sponsorship affidavits for visa proof."},
        {"step": 10, "phase": "Student Visa Application", "description": f"Book visa appointment at embassy/VFS for {profile.preferred_country}."},
        {"step": 11, "phase": "Pre-Departure Briefing", "description": "Book flights, secure student housing/dormitories, and arrange international health insurance."}
    ]
    return {"status": "success", "student": profile.name, "target_intake": intake, "roadmap": roadmap}

def retrieve_documents_tool(query: str, top_k: int = 5) -> Dict[str, Any]:
    """Semantic vector search across RAG Knowledge Base."""
    retriever = get_rag_retriever()
    docs = retriever.retrieve_documents(query, top_k=top_k)
    return {"status": "success", "count": len(docs), "documents": docs}
