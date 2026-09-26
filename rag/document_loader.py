import json
import pandas as pd
from typing import List, Dict, Any
from utils.data_loader import (
    get_master_university_df,
    get_recommendation_ready_df,
    get_scholarship_intelligence_df,
    get_country_intelligence_df,
    get_academic_trends_df
)

def build_university_documents() -> List[Dict[str, Any]]:
    df = get_recommendation_ready_df()
    docs = []
    
    # Deduplicate universities if multiple program entries exist
    grouped = df.groupby(["university", "country"], as_index=False).first()
    
    for _, row in grouped.iterrows():
        univ = str(row.get("university", "Unknown University"))
        country = str(row.get("country", "Unknown Country"))
        city = str(row.get("city", "Unknown City"))
        rank_2025 = str(row.get("rank_2025", "N/A"))
        overall_score = str(row.get("overall_score", "N/A"))
        tuition = row.get("tuition_numeric", row.get("tuition_usd", "N/A"))
        living = row.get("living_cost_numeric", row.get("rent_usd", "N/A"))
        total_cost = row.get("total_estimated_cost", "N/A")
        program = str(row.get("program", "Various"))
        level = str(row.get("level", "Higher Education"))
        acad_rep = str(row.get("academic_reputation_score", "N/A"))
        emp_rep = str(row.get("employer_reputation_score", "N/A"))
        intl_students = str(row.get("international_students_score", "N/A"))
        
        content = (
            f"University: {univ}\n"
            f"Location: {city}, {country}\n"
            f"QS World University Rank 2025: {rank_2025} (Overall Score: {overall_score})\n"
            f"Sample Program: {program} ({level})\n"
            f"Estimated Annual Tuition (USD): ${tuition}\n"
            f"Estimated Annual Living/Rent Cost (USD): ${living}\n"
            f"Total Estimated Annual Cost (USD): ${total_cost}\n"
            f"Academic Reputation Score: {acad_rep}/100 | Employer Reputation Score: {emp_rep}/100\n"
            f"International Students Score: {intl_students}/100\n"
            f"Overview: {univ} is a premier educational institution located in {country}. "
            f"It offers globally accredited {level} programs including {program}, with QS 2025 ranking {rank_2025}."
        )
        
        doc_id = f"univ_{univ.lower().replace(' ', '_')}_{country.lower().replace(' ', '_')}"
        docs.append({
            "document_id": doc_id,
            "source_file": "Master Dataset/recommendation_ready_dataset.csv",
            "topic": f"University Profile: {univ}",
            "university": univ,
            "country": country,
            "document_type": "university_profile",
            "content": content
        })
    return docs

def build_scholarship_documents() -> List[Dict[str, Any]]:
    df = get_scholarship_intelligence_df()
    docs = []
    
    # Process top/sample scholarships up to 1500 to keep vector store lean and high-value
    sample_df = df.head(1500)
    
    for idx, row in sample_df.iterrows():
        name = str(row.get("scholarship_name", "International Scholarship"))
        amount = str(row.get("amount", "Varies / Partial to Full"))
        deadline = str(row.get("deadline", "Check official portal"))
        location = str(row.get("location", "Global"))
        years = str(row.get("years", "Undergraduate / Graduate"))
        desc = str(row.get("description", "No description provided."))
        link = str(row.get("link", ""))
        
        content = (
            f"Scholarship Name: {name}\n"
            f"Eligible Location / Country: {location}\n"
            f"Award Amount: ${amount}\n"
            f"Application Deadline: {deadline}\n"
            f"Target Academic Level: {years}\n"
            f"Official Link: {link}\n"
            f"Description & Eligibility: {desc}"
        )
        
        doc_id = f"scholarship_{idx}"
        docs.append({
            "document_id": doc_id,
            "source_file": "Master Dataset/scholarship_intelligence_dataset.csv",
            "topic": f"Scholarship: {name}",
            "university": "Various",
            "country": location,
            "document_type": "scholarship",
            "content": content
        })
    return docs

def build_country_guide_documents() -> List[Dict[str, Any]]:
    df = get_country_intelligence_df()
    docs = []
    
    for _, row in df.iterrows():
        country = str(row.get("country", "Unknown"))
        avg_cost = str(row.get("avg_estimated_cost", "N/A"))
        avg_rank = str(row.get("avg_ranking", "N/A"))
        univ_count = str(row.get("university_count", "N/A"))
        affordability = str(row.get("avg_affordability_score", "N/A"))
        category = str(row.get("recommendation_category", "Consider"))
        reason = str(row.get("recommendation_reason", "Fits international education criteria"))
        
        content = (
            f"Country Study Destination Guide: {country}\n"
            f"Recommendation Tier: {category}\n"
            f"Average Estimated Annual Cost (Tuition + Living): ${avg_cost} USD\n"
            f"Average University QS Rank: {avg_rank}\n"
            f"Recognized Higher Education Institutions Tracked: {univ_count}\n"
            f"Affordability Score: {affordability}/100\n"
            f"Key Advantage: {reason}\n"
            f"Admission & Visa Guidelines for {country}: International students require a student visa, "
            f"proof of financial funds, valid passport, English language proficiency test (IELTS/TOEFL/PTE), "
            f"and official academic transcripts."
        )
        
        doc_id = f"country_{country.lower().replace(' ', '_')}"
        docs.append({
            "document_id": doc_id,
            "source_file": "Master Dataset/country_intelligence_dataset.csv",
            "topic": f"Country Study Guide: {country}",
            "university": "General",
            "country": country,
            "document_type": "country_guide",
            "content": content
        })
    return docs

def load_all_structured_documents() -> List[Dict[str, Any]]:
    docs = []
    docs.extend(build_university_documents())
    docs.extend(build_scholarship_documents())
    docs.extend(build_country_guide_documents())
    return docs
