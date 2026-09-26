import re
from typing import Dict, Any, List, Optional
from utils.profile import StudentProfile

INTENT_MAPPING = {
    "university_search": ["recommend_universities", "search_universities"],
    "country_recommendation": ["recommend_countries"],
    "scholarship_search": ["search_scholarships", "recommend_scholarships"],
    "admission_information": ["get_admission_information", "retrieve_documents"],
    "cost_calculation": ["calculate_total_cost"],
    "university_comparison": ["compare_universities"],
    "application_roadmap": ["create_application_roadmap"],
    "full_study_abroad_plan": ["recommend_countries", "recommend_universities", "recommend_scholarships", "create_application_roadmap", "retrieve_documents"],
    "general_study_abroad_question": ["retrieve_documents"]
}

class IntentDetector:
    """
    Hybrid Intent Detector combining pattern regex extraction with semantic keyword parsing.
    """

    def detect_intent_and_tools(self, query: str) -> Dict[str, Any]:
        q = query.lower()
        tools = []
        intent = "general_study_abroad_question"

        # Check for full plan
        if any(w in q for w in ["full plan", "complete plan", "study abroad plan", "roadmap and scholarship", "guide me completely", "what should i do next"]):
            intent = "full_study_abroad_plan"
            tools = ["recommend_countries", "recommend_universities", "recommend_scholarships", "create_application_roadmap", "retrieve_documents"]
        # Comparison
        elif any(w in q for w in ["compare", " vs ", "versus", "difference between"]):
            intent = "university_comparison"
            tools = ["compare_universities", "retrieve_documents"]
        # Roadmap / Steps
        elif any(w in q for w in ["roadmap", "timeline", "milestones", "steps to apply", "application process", "when to apply"]):
            intent = "application_roadmap"
            tools = ["create_application_roadmap"]
        # Cost / Budget / Fees
        elif any(w in q for w in ["cost", "fee", "tuition", "budget", "expenses", "living cost", "afford", "expensive", "cheap"]):
            intent = "cost_calculation"
            tools = ["calculate_total_cost", "recommend_universities"]
        # Scholarships / Funding
        elif any(w in q for w in ["scholarship", "funding", "grant", "financial aid", "fellowship"]):
            intent = "scholarship_search"
            tools = ["search_scholarships", "recommend_scholarships"]
        # Admission / Requirements / Eligibility / IELTS
        elif any(w in q for w in ["admission", "requirement", "eligibility", "criteria", "ielts", "toefl", "gre", "gpa required", "cgpa"]):
            intent = "admission_information"
            tools = ["get_admission_information", "retrieve_documents"]
        # Countries
        elif any(w in q for w in ["country", "countries", "destination", "where should i go"]):
            intent = "country_recommendation"
            tools = ["recommend_countries"]
        # Universities
        elif any(w in q for w in ["university", "universities", "college", "colleges", "institutions", "top unis"]):
            intent = "university_search"
            tools = ["recommend_universities", "search_universities"]
        else:
            intent = "general_study_abroad_question"
            tools = ["retrieve_documents"]

        # If question mentions universities AND scholarships
        if "scholarship" in q and ("university" in q or "universities" in q or "msc" in q or "bachelor" in q):
            if "recommend_scholarships" not in tools:
                tools.append("recommend_scholarships")
            if "recommend_universities" not in tools:
                tools.append("recommend_universities")
            intent = "university_and_scholarship_search"

        return {
            "intent": intent,
            "tools": tools,
            "extracted_profile": self.extract_profile_from_nl(query)
        }

    def extract_profile_from_nl(self, text: str) -> Dict[str, Any]:
        """
        Extracts student attributes (CGPA, Budget, Country, Field, Degree) from natural language text.
        """
        extracted = {}

        # 1. CGPA extraction (e.g. 7.43 CGPA, GPA 3.5, 8.2 gpa)
        cgpa_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:cgpa|gpa)', text, re.IGNORECASE)
        if not cgpa_match:
            cgpa_match = re.search(r'(?:cgpa|gpa)\s*(?:of|is|:)?\s*(\d+(?:\.\d+)?)', text, re.IGNORECASE)
        if cgpa_match:
            try:
                extracted["cgpa"] = float(cgpa_match.group(1))
            except ValueError:
                pass

        # 2. Budget extraction (e.g. ₹35 lakh, 3500000, $40k, 25 lakhs, 35 lacs)
        lakh_match = re.search(r'(?:₹|rs\.?|inr)?\s*(\d+(?:\.\d+)?)\s*(?:lakh|lakhs|lac|lacs)', text, re.IGNORECASE)
        if lakh_match:
            try:
                extracted["budget"] = float(lakh_match.group(1)) * 100000
                extracted["currency"] = "INR"
            except ValueError:
                pass
        else:
            usd_match = re.search(r'\$\s*(\d+(?:,\d+)*(?:\.\d+)?)\s*(?:k|thousand)?', text, re.IGNORECASE)
            if usd_match:
                val_str = usd_match.group(1).replace(",", "")
                try:
                    num = float(val_str)
                    if "k" in text.lower():
                        num *= 1000
                    extracted["budget"] = num
                    extracted["currency"] = "USD"
                except ValueError:
                    pass

        # 3. Country extraction
        countries = ["uk", "united kingdom", "usa", "united states", "germany", "australia", "canada", "ireland", "singapore", "netherlands", "france", "switzerland", "sweden", "italy", "new zealand"]
        for c in countries:
            if re.search(rf'\b{c}\b', text, re.IGNORECASE):
                extracted["preferred_country"] = "United Kingdom" if c == "uk" else "United States" if c == "usa" else c.title()
                break

        # 4. Field extraction
        fields = {
            "computer science": ["computer science", "cs", "software", "ai", "machine learning", "data science"],
            "data science": ["data science", "analytics", "business analytics"],
            "business & management": ["mba", "business", "finance", "management", "marketing"],
            "mechanical engineering": ["mechanical engineering", "mechanical"],
            "biotechnology": ["biotechnology", "bioinformatics", "biomedical"]
        }
        for f_name, synonyms in fields.items():
            for syn in synonyms:
                if re.search(rf'\b{syn}\b', text, re.IGNORECASE):
                    extracted["preferred_field"] = f_name.title()
                    break
            if "preferred_field" in extracted:
                break

        # 5. Degree level
        if re.search(r'\b(msc|ms|master|masters|postgraduate|pg)\b', text, re.IGNORECASE):
            extracted["degree_level"] = "Master"
        elif re.search(r'\b(bsc|btech|bachelor|bachelors|undergraduate|ug)\b', text, re.IGNORECASE):
            extracted["degree_level"] = "Bachelor"
        elif re.search(r'\b(phd|doctorate)\b', text, re.IGNORECASE):
            extracted["degree_level"] = "PhD"

        return extracted
