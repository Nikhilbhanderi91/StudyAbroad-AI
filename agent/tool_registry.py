from typing import Dict, Any, Callable
from tools.agent_tools import (
    search_universities_tool,
    recommend_universities_tool,
    recommend_countries_tool,
    search_scholarships_tool,
    recommend_scholarships_tool,
    calculate_total_cost_tool,
    compare_universities_tool,
    get_admission_information_tool,
    create_application_roadmap_tool,
    retrieve_documents_tool
)

TOOL_REGISTRY: Dict[str, Dict[str, Any]] = {
    "search_universities": {
        "function": search_universities_tool,
        "description": "Searches for universities by name, field, or location."
    },
    "recommend_universities": {
        "function": recommend_universities_tool,
        "description": "Calculates multi-criteria ranked university recommendations."
    },
    "recommend_countries": {
        "function": recommend_countries_tool,
        "description": "Evaluates countries by budget, QS ranks, and user preference."
    },
    "search_scholarships": {
        "function": search_scholarships_tool,
        "description": "Searches scholarships by topic, field, or country."
    },
    "recommend_scholarships": {
        "function": recommend_scholarships_tool,
        "description": "Matches scholarships to student academic and geographic profile."
    },
    "calculate_total_cost": {
        "function": calculate_total_cost_tool,
        "description": "Calculates detailed tuition, rent, living, visa, and insurance costs."
    },
    "compare_universities": {
        "function": compare_universities_tool,
        "description": "Compares ranking, cost, and reputation across multiple universities."
    },
    "get_admission_information": {
        "function": get_admission_information_tool,
        "description": "Retrieves admission guidelines, test scores, and visa basics."
    },
    "create_application_roadmap": {
        "function": create_application_roadmap_tool,
        "description": "Generates a structured timeline and milestone roadmap."
    },
    "retrieve_documents": {
        "function": retrieve_documents_tool,
        "description": "RAG semantic vector retrieval over entire knowledge corpus."
    }
}

def execute_tool(tool_name: str, **kwargs) -> Dict[str, Any]:
    """Executes registered tool with safe error handling."""
    if tool_name not in TOOL_REGISTRY:
        return {"error": f"Tool '{tool_name}' not found in registry."}
    
    fn = TOOL_REGISTRY[tool_name]["function"]
    try:
        return fn(**kwargs)
    except Exception as e:
        return {"error": f"Tool execution failed for '{tool_name}': {str(e)}"}
