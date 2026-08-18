import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
load_dotenv(dotenv_path=Path(__file__).parent / ".env")
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
SYSTEM_PROMPT = (

    "You are an intent classifier for a campus query router agent. "
    "Classify the user's query into exactly one of these three labels: "
    "Academic, Exam, or General. "
    "Academic = course content, subjects, faculty, registration. "
    "Exam = exam dates, hall tickets, results, revaluation. "
    "General = hostel, fees, library, campus facilities, anything else. "
    "Respond with ONLY the single label word, nothing else."
)
def academic_handler(query: str) -> str:
    return f"[Academic Office] Noted your academic query: '{query}'. " \
           f"Redirecting to the syllabus/course-registration desk."
def exam_handler(query: str) -> str:
    return f"[Exam Cell] Noted your exam-related query: '{query}'. " \
           f"Redirecting to the examination timetable/hall-ticket desk."

def general_handler(query: str) -> str:
    return f"[General Helpdesk] Noted your query: '{query}'. " \
           f"Redirecting to the general campus information desk."

INTENT_ROUTES = {
    "Academic": academic_handler,
    "Exam": exam_handler,
    "General": general_handler,
}
def classify_intent(query: str) -> str:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query},
        ],
        temperature=0,
    )
    label = response.choices[0].message.content.strip()

    if label not in INTENT_ROUTES:
        print(f"  (Warning: unexpected label '{label}', defaulting to General)")
        label = "General"

    return label
def run_agent(query: str) -> str:
    print(f"\n[Observe] Query: {query}")
    intent = classify_intent(query)
    print(f"[Decide] Classified intent: {intent}")
    handler = INTENT_ROUTES[intent]
    result = handler(query)
    print(f"[Act] Tool response: {result}")
    return result
def main():
    print(" Welcome to Campus Query Router Agent")
    print("Type 'exit' to quit.\n")
    while True:
        query = input("Ask something about campus: ")
        if query.strip().lower() == "exit":
            print("Goodbye!")
            break
        run_agent(query)
if __name__ == "__main__":
    main()