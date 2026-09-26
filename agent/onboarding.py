import re
from typing import Dict, Any, Optional, Tuple
from utils.profile import StudentProfile

class ConversationalOnboarding:
    """
    Manages conversational profile discovery and progressive state tracking.
    """

    QUESTIONS = [
        ("name", "Hi! 👋 I'm **StudyAbroad AI**, your personal Study Abroad Advisor.\n\nI'll help you explore universities, scholarships, costs, and your application journey grounded in verified global datasets.\n\nTo get started, **what's your name?**"),
        ("cgpa", "Nice to meet you, {name}! 🎓\n\nWhat is your **current CGPA or academic percentage** (e.g., *7.43 CGPA* or *80%*)?"),
        ("preferred_field", "Got it! What **field of study or major** are you planning to pursue (e.g., *Computer Science, Data Science, MBA, Mechanical Engineering*)?"),
        ("degree_level", "Great. Which **degree level** are you targeting (e.g., *Master's (MSc), Bachelor's (BSc), PhD*)?"),
        ("preferred_country", "Which **destination country or countries** are you considering (e.g., *United Kingdom, Germany, USA, Australia, Canada*)?"),
        ("budget", "What is your **approximate total study-abroad budget** (e.g., *₹35 Lakh INR*, *$40,000 USD*)?"),
        ("english_test_score", "Have you taken or planned an **English proficiency test** like IELTS, TOEFL, or PTE (e.g., *IELTS 7.0*, *Planning soon*)? (Optional)")
    ]

    @classmethod
    def get_profile_completeness(cls, profile: StudentProfile) -> Tuple[int, Optional[str], Optional[str]]:
        """
        Calculates completion percentage (0-100%) and returns the next missing field key & question.
        """
        # Core essential fields required for complete analysis
        essential_fields = ["name", "cgpa", "preferred_field", "degree_level", "preferred_country", "budget"]
        filled = 0
        next_field = None
        next_question_template = None

        for field_key, q_text in cls.QUESTIONS:
            val = getattr(profile, field_key, None)
            is_valid = False
            if field_key == "name" and val and val != "Student" and len(val.strip()) > 1:
                is_valid = True
            elif field_key == "cgpa" and val and val > 0:
                is_valid = True
            elif field_key in ["preferred_field", "preferred_country", "degree_level"] and val and len(str(val).strip()) > 1:
                is_valid = True
            elif field_key == "budget" and val and val > 0:
                is_valid = True
            elif field_key == "english_test_score" and val:
                is_valid = True

            if is_valid:
                filled += 1
            elif next_field is None and field_key in essential_fields:
                next_field = field_key
                next_question_template = q_text

        completeness_pct = min(int((filled / len(essential_fields)) * 100), 100)
        return completeness_pct, next_field, next_question_template

    @classmethod
    def extract_and_update(cls, text: str, profile: StudentProfile, current_expected_field: Optional[str] = None) -> StudentProfile:
        """
        Extracts entities from user chat message and updates the student profile.
        """
        updated = profile.model_copy()
        t = text.strip()

        # If we were specifically expecting a name
        if current_expected_field == "name" and (not updated.name or updated.name in ["Student", "Nikhil"]):
            # Clean possible greeting phrases
            clean_name = re.sub(r'^(?:hi|hello|hey|my name is|i am|i\'m)\s+', '', t, flags=re.IGNORECASE).strip()
            clean_name = clean_name.split(".")[0].split(",")[0].title()
            if len(clean_name) > 1 and len(clean_name.split()) <= 4:
                updated.name = clean_name

        # Extract CGPA / GPA
        cgpa_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:cgpa|gpa|percentage|%)', t, re.IGNORECASE)
        if not cgpa_match and current_expected_field == "cgpa":
            cgpa_match = re.search(r'^(\d+(?:\.\d+)?)$', t)
        if cgpa_match:
            try:
                val = float(cgpa_match.group(1))
                if val > 10.0 and val <= 100.0:  # percentage converted to 10-scale
                    val = round(val / 10.0, 2)
                if 0.0 < val <= 10.0:
                    updated.cgpa = val
            except ValueError:
                pass

        # Extract Budget & Currency
        lakh_match = re.search(r'(?:₹|rs\.?|inr)?\s*(\d+(?:\.\d+)?)\s*(?:lakh|lakhs|lac|lacs)', t, re.IGNORECASE)
        if lakh_match:
            try:
                updated.budget = float(lakh_match.group(1)) * 100000
                updated.currency = "INR"
            except ValueError:
                pass
        else:
            usd_match = re.search(r'\$\s*(\d+(?:,\d+)*(?:\.\d+)?)\s*(?:k|thousand)?', t, re.IGNORECASE)
            if usd_match:
                val_str = usd_match.group(1).replace(",", "")
                try:
                    num = float(val_str)
                    if "k" in t.lower():
                        num *= 1000
                    updated.budget = num
                    updated.currency = "USD"
                except ValueError:
                    pass
            elif current_expected_field == "budget":
                # Check pure numbers like 3500000 or 35
                num_match = re.search(r'^(\d+(?:,\d+)*(?:\.\d+)?)$', t.replace(",", ""))
                if num_match:
                    num = float(num_match.group(1))
                    if num < 200:  # Assume lakhs
                        num = num * 100000
                    updated.budget = num
                    updated.currency = "INR"

        # Extract Field of study
        fields_map = {
            "Computer Science": ["computer science", "cs", "software", "artificial intelligence", "ai", "machine learning", "ml"],
            "Data Science": ["data science", "data analytics", "analytics", "business analytics"],
            "Business & Management": ["mba", "business administration", "management", "marketing", "finance"],
            "Mechanical Engineering": ["mechanical engineering", "mechanical"],
            "Electrical Engineering": ["electrical engineering", "electronics", "ece"],
            "Biotechnology": ["biotechnology", "biomedical", "bioinformatics"]
        }
        for std_field, keywords in fields_map.items():
            if any(re.search(rf'\b{re.escape(k)}\b', t, re.IGNORECASE) for k in keywords):
                updated.preferred_field = std_field
                break
        if current_expected_field == "preferred_field" and not any(k in t.lower() for k in ["hi", "hello", "yes", "no"]):
            if len(t) < 50:
                updated.preferred_field = t.title()

        # Extract Degree level
        if re.search(r'\b(msc|ms|master|masters|postgraduate|pg)\b', t, re.IGNORECASE):
            updated.degree_level = "Master"
        elif re.search(r'\b(bsc|btech|bachelor|bachelors|undergraduate|ug)\b', t, re.IGNORECASE):
            updated.degree_level = "Bachelor"
        elif re.search(r'\b(phd|doctorate)\b', t, re.IGNORECASE):
            updated.degree_level = "PhD"

        # Extract Countries
        countries_list = ["United Kingdom", "United States", "Germany", "Australia", "Canada", "Ireland", "Singapore", "Netherlands", "France", "Switzerland", "Sweden", "Italy", "New Zealand"]
        for c in countries_list:
            alias = "uk" if c == "United Kingdom" else "usa" if c == "United States" else c.lower()
            if re.search(rf'\b{re.escape(alias)}\b', t, re.IGNORECASE) or re.search(rf'\b{re.escape(c)}\b', t, re.IGNORECASE):
                updated.preferred_country = c
                break

        # Extract IELTS / English score
        ielts_match = re.search(r'\b(ielts|toefl|pte)\s*(\d+(?:\.\d+)?)\b', t, re.IGNORECASE)
        if ielts_match:
            updated.english_test_score = f"{ielts_match.group(1).upper()} {ielts_match.group(2)}"

        return updated
