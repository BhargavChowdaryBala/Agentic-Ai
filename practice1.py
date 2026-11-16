import os
from groq import Groq

from dotenv import load_dotenv
load_dotenv() 

client=Groq(api_key=os.getenv("GROQ_API_KEY"))

system_prompt="""Think of you as a campus query router agent 
classify the {query} exactly any of three labels 'Academic','Exam','General'
Academic : course details,lecturer details , subjects 
Exam : Exam dates, hall tickets,results,revaluation
General : sports,bus timings , anything else
only give output as any one of these 3 labels"""

def acadamic_handler(query:str)->str:
    return f"[Acadamic office] noted your current query : {query} and our staff will contact you"\
            f"Redirecting you to course/lecturer desk ... "

def exam_handler(query:str)->str:
    return f"[Exam office] noted your current query : {query} and our staff will contact you"\
            f"Redirecting you to Exam dates/results/hall tickets  desk ... "

def general_handler(query:str)->str:
    return f"[General office] noted your current query : {query} and our staff will contact you"\
            f"Redirecting you to general campus information desk ... "

Intent_routes={
    "Academic":acadamic_handler,
    "Exam":exam_handler,
    "General":general_handler
}

def classify_content(query:str)->str:
    response=client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role":"system","content":system_prompt},
            {"role":"user","content":query}
        ],
        temperature=0.1
    )
    return response.choices[0].message.content.strip()
def run_agent(query:str)->str:
    print(f"[observe] query observed : {query}")
    intent=classify_content(query)
    print(f"[decide] decided intent is {intent}")
    handler=Intent_routes[intent]
    result=handler(query)
    print(f"[ACT] Tool response :{result}")
    return result
def main():
    print("Welcome to campus query agent")
    while True:
        query=input("Enter your query")
        if(query.lower()=="exit"):
            break
        run_agent(query)

if __name__=="__main__":
    main()
    