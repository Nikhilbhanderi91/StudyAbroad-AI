import os
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

class StudentProfile(BaseModel):
    name: str = Field(default="Nikhil", description="Student's name")
    cgpa: float = Field(default=7.43, ge=0.0, le=10.0, description="Academic CGPA (out of 10.0 or converted)")
    budget: float = Field(default=3500000.0, ge=0.0, description="Total budget amount")
    currency: str = Field(default="INR", description="Currency of the budget (INR, USD, GBP, EUR, etc.)")
    preferred_country: str = Field(default="United Kingdom", description="Target destination country")
    preferred_field: str = Field(default="Computer Science", description="Target study program/field")
    degree_level: str = Field(default="Master", description="Target degree level (Bachelor, Master, PhD)")
    ranking_priority: str = Field(default="High", description="Priority given to ranking (High, Medium, Balanced, Low)")
    english_test_score: Optional[str] = Field(default="IELTS 7.0", description="IELTS, TOEFL, or PTE test score")
    work_experience: Optional[str] = Field(default="1 Year", description="Relevant industry/research experience")
    preferred_intake: Optional[str] = Field(default="Fall 2025", description="Target admission intake session")

    def budget_in_inr(self) -> float:
        from utils.config import EXCHANGE_RATES
        rate = EXCHANGE_RATES.get(self.currency.upper(), 1.0)
        return self.budget * rate

    def budget_in_usd(self) -> float:
        from utils.config import EXCHANGE_RATES
        rate_inr = self.budget_in_inr()
        usd_rate = EXCHANGE_RATES.get("USD", 83.5)
        return rate_inr / usd_rate

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump()
