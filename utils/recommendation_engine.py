import math
import pandas as pd
from typing import Dict, Any, List, Optional
from utils.data_loader import (
    get_recommendation_ready_df,
    get_country_intelligence_df,
    get_scholarship_intelligence_df
)
from utils.profile import StudentProfile

def normalize_university_name(name: str) -> str:
    """Standardizes university names for consistent matching."""
    if not isinstance(name, str):
        return ""
    cleaned = name.lower().strip()
    replacements = ["the ", "university of ", " university", " institute of technology", " college"]
    for r in replacements:
        cleaned = cleaned.replace(r, " ")
    return " ".join(cleaned.split())

def calculate_budget_score(university_cost: float, student_budget: float) -> float:
    """Calculates budget fit score based on total estimated cost vs budget."""
    if pd.isna(university_cost) or university_cost <= 0:
        return 50.0
    if student_budget <= 0:
        return 50.0
    
    ratio = university_cost / student_budget
    if ratio <= 0.8:
        return 100.0
    elif ratio <= 1.0:
        return 90.0
    elif ratio <= 1.2:
        return 70.0
    elif ratio <= 1.5:
        return 45.0
    else:
        return 20.0

def calculate_ranking_score(rank_val: Any) -> float:
    """Normalizes ranking value to 0-100 score."""
    try:
        if pd.isna(rank_val):
            return 50.0
        r_str = str(rank_val).replace("=", "").replace("+", "").strip()
        if "-" in r_str:
            r_str = r_str.split("-")[0]
        rank_num = float(r_str)
        if rank_num <= 50:
            return 100.0
        elif rank_num <= 100:
            return 90.0
        elif rank_num <= 250:
            return 80.0
        elif rank_num <= 500:
            return 65.0
        elif rank_num <= 1000:
            return 45.0
        else:
            return 30.0
    except Exception:
        return 50.0

def get_recommendation_category(score: float) -> str:
    if score >= 85:
        return "Top Recommendation (Strong Match)"
    elif score >= 75:
        return "Recommended Match"
    elif score >= 60:
        return "Competitive / Target Match"
    else:
        return "Reach / Alternative"

def run_university_recommendations(profile: StudentProfile, top_n: int = 5) -> List[Dict[str, Any]]:
    """
    Executes the multi-factor weighted university recommendation algorithm.
    """
    df = get_recommendation_ready_df().copy()
    if df.empty:
        return []

    budget_usd = profile.budget_in_usd()
    target_country = profile.preferred_country.strip().lower()
    target_field = profile.preferred_field.strip().lower()

    results = []
    # Deduplicate rows by university
    grouped = df.groupby("university", as_index=False).first()

    for _, row in grouped.iterrows():
        univ = str(row.get("university", "Unknown"))
        country = str(row.get("country", ""))
        rank = row.get("rank_2025", row.get("ranking_numeric", "N/A"))
        cost_usd = row.get("total_estimated_cost", row.get("tuition_numeric", 30000))
        try:
            cost_usd = float(cost_usd)
        except Exception:
            cost_usd = 30000.0

        # Sub-scores
        r_score = calculate_ranking_score(rank)
        b_score = calculate_budget_score(cost_usd, budget_usd)
        
        c_score = 100.0 if target_country in country.lower() or country.lower() in target_country else 40.0
        prog = str(row.get("program", "")).lower()
        f_score = 95.0 if target_field in prog or prog in target_field else 60.0
        data_comp = float(row.get("data_completeness_score", 80.0)) if not pd.isna(row.get("data_completeness_score")) else 80.0

        # Weights: Ranking (0.25), Budget (0.30), Country (0.25), Field (0.10), Data Confidence (0.10)
        final_score = (
            (r_score * 0.25) +
            (b_score * 0.30) +
            (c_score * 0.25) +
            (f_score * 0.10) +
            (data_comp * 0.10)
        )

        category = get_recommendation_category(final_score)
        
        reasons = []
        if c_score == 100.0:
            reasons.append(f"Located in preferred country ({country})")
        if b_score >= 80.0:
            reasons.append(f"Well within estimated budget (${cost_usd:,.0f} USD/yr)")
        elif b_score <= 45.0:
            reasons.append(f"Higher cost bracket (${cost_usd:,.0f} USD/yr)")
        if r_score >= 80.0:
            reasons.append(f"High QS Global Standing (Rank #{rank})")

        reason_str = " | ".join(reasons) if reasons else "Good overall academic fit"

        results.append({
            "university": univ,
            "country": country,
            "rank_2025": str(rank),
            "estimated_annual_cost_usd": cost_usd,
            "estimated_annual_cost_inr": cost_usd * 83.5,
            "recommendation_score": round(final_score, 2),
            "category": category,
            "reason": reason_str,
            "program": str(row.get("program", target_field))
        })

    results.sort(key=lambda x: x["recommendation_score"], reverse=True)
    return results[:top_n]

def run_country_recommendations(profile: StudentProfile, top_n: int = 5) -> List[Dict[str, Any]]:
    """
    Executes country suitability scoring based on budget, average QS rank, and user preference.
    """
    df = get_country_intelligence_df().copy()
    if df.empty:
        return []

    budget_usd = profile.budget_in_usd()
    target_country = profile.preferred_country.strip().lower()

    results = []
    for _, row in df.iterrows():
        country = str(row.get("country", "Unknown"))
        avg_cost = float(row.get("avg_estimated_cost", 25000.0))
        avg_rank = row.get("avg_ranking", "N/A")
        univ_count = int(row.get("university_count", 1))
        
        # Scoring
        b_score = calculate_budget_score(avg_cost, budget_usd)
        pref_score = 100.0 if target_country in country.lower() or country.lower() in target_country else 50.0
        rank_score = calculate_ranking_score(avg_rank)
        
        # Weighted composite score
        composite_score = (b_score * 0.35) + (pref_score * 0.35) + (rank_score * 0.20) + (min(univ_count * 5, 100) * 0.10)

        results.append({
            "country": country,
            "average_annual_cost_usd": avg_cost,
            "average_qs_ranking": str(avg_rank),
            "universities_tracked": univ_count,
            "suitability_score": round(composite_score, 2),
            "category": "Highly Recommended" if composite_score >= 80 else "Recommended" if composite_score >= 65 else "Consider",
            "reason": f"Budget fit score: {b_score:.0f}/100 with {univ_count} universities tracked"
        })

    results.sort(key=lambda x: x["suitability_score"], reverse=True)
    return results[:top_n]

def run_scholarship_recommendations(profile: StudentProfile, top_n: int = 5) -> List[Dict[str, Any]]:
    """
    Recommends scholarships based on field match, location, and award amounts.
    """
    df = get_scholarship_intelligence_df().copy()
    if df.empty:
        return []

    target_field = profile.preferred_field.strip().lower()
    target_country = profile.preferred_country.strip().lower()

    scored = []
    for _, row in df.iterrows():
        name = str(row.get("scholarship_name", "Scholarship"))
        desc = str(row.get("description", "")).lower()
        loc = str(row.get("location", "")).lower()
        amount_val = row.get("scholarship_amount_numeric", row.get("amount", 1000))
        deadline = str(row.get("deadline", "Check Portal"))
        link = str(row.get("link", ""))
        
        field_match = 100.0 if target_field in desc or target_field in name.lower() else 40.0
        country_match = 100.0 if target_country in loc or "global" in loc or "no geographic" in loc else 50.0
        
        total_score = (field_match * 0.5) + (country_match * 0.5)
        
        scored.append({
            "scholarship_name": name,
            "amount": amount_val,
            "deadline": deadline,
            "location": str(row.get("location", "Global")),
            "match_score": round(total_score, 2),
            "link": link,
            "description": desc[:200] + ("..." if len(desc) > 200 else "")
        })

    scored.sort(key=lambda x: x["match_score"], reverse=True)
    return scored[:top_n]
