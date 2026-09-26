import time
from utils.profile import StudentProfile
from agent.agent import StudyAbroadAgent

def evaluate_agent_workflows():
    print("==================================================")
    print("🤖 EVALUATION: AGENT INTENT & TOOL ROUTING")
    print("==================================================")

    test_cases = [
        {
            "query": "I have 7.43 CGPA, ₹35 lakh budget and want MSc Computer Science in UK. Find suitable universities and scholarships and tell me what I should do next.",
            "expected_intent": "full_study_abroad_plan",
            "expected_tools": ["recommend_universities", "recommend_scholarships", "create_application_roadmap"]
        },
        {
            "query": "Find scholarships for MSc Computer Science in the UK",
            "expected_intent": "scholarship_search",
            "expected_tools": ["search_scholarships", "recommend_scholarships"]
        },
        {
            "query": "What is the cost of studying in Oxford vs Cambridge?",
            "expected_intent": "university_comparison",
            "expected_tools": ["compare_universities"]
        },
        {
            "query": "What are the admission requirements and IELTS criteria?",
            "expected_intent": "admission_information",
            "expected_tools": ["get_admission_information"]
        }
    ]

    agent = StudyAbroadAgent()
    passed = 0

    for idx, tc in enumerate(test_cases, 1):
        profile = StudentProfile()
        out = agent.process_query(tc["query"], profile)
        
        executed = set(out["tools_executed"])
        expected = set(tc["expected_tools"])
        matched = expected.intersection(executed)
        success = len(matched) > 0
        if success:
            passed += 1

        print(f"\n[Test Case {idx}]")
        print(f"Query: \"{tc['query']}\"")
        print(f"Detected Intent: {out['detected_intent']}")
        print(f"Tools Executed: {out['tools_executed']}")
        print(f"Latency: {out['latency_ms']} ms")
        print(f"Tool Selection Match: {'✅ PASSED' if success else '❌ FAILED'}")

    accuracy = (passed / len(test_cases)) * 100
    print(f"\n==================================================")
    print(f"🎯 AGENT EVALUATION ACCURACY: {accuracy:.1f}%")
    print("==================================================")

if __name__ == "__main__":
    evaluate_agent_workflows()
