import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
load_dotenv(dotenv_path=Path(__file__).parent / ".env")
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "openai/gpt-oss-20b"
def research_agent(topic: str) -> str:
    print(f"\n[Research Agent] Gathering points on: {topic}")
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": (
                "You are a research agent. Given a topic, list 4-6 concise "
                "bullet points covering its key aspects. Output ONLY the "
                "bullet points, one per line, starting each with '- '."
            )},
            {"role": "user", "content": topic},
        ],
        temperature=0.3,
    )
    bullets = response.choices[0].message.content.strip()
    print(f"[Research Agent] Output:\n{bullets}")
    return bullets
def refiner_agent(bullets: str, topic: str) -> str:
    print(f"\n[Refiner Agent] Turning points into an explanation")
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": (
                "You are a refiner agent. Given a topic and a list of bullet "
                "points about it, write a short, well-structured explanation "
                "(3-5 sentences) in plain prose. Do not use bullet points in "
                "your output."
            )},
            {"role": "user", "content": f"Topic: {topic}\n\nPoints:\n{bullets}"},
        ],
        temperature=0.3,
    )
    explanation = response.choices[0].message.content.strip()
    print(f"[Refiner Agent] Output:\n{explanation}")
    return explanation
def run_pipeline(topic: str) -> str:
    print(f"\n[Observe] Topic: {topic}")

    bullets = research_agent(topic)
    final_explanation = refiner_agent(bullets, topic)

    print(f"\n[Act] Final delivered explanation:\n{final_explanation}")
    return final_explanation
def main():
    print("Multi-Agent Pipeline: Research Agent -> Refiner Agent")
    print("Type 'exit' to quit.\n")

    while True:
        topic = input("Enter a topic to explain: ")
        if topic.strip().lower() == "exit":
            print("Goodbye!")
            break
        run_pipeline(topic)
if __name__ == "__main__":
    main()
