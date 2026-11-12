import os
import json
import requests
from dotenv import load_dotenv
from groq import Groq
 
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY is not set in the .env file.")
 
client = Groq(api_key=api_key)
MODEL = "openai/gpt-oss-120b"
 
def ask_llm(system_prompt, user_text):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": system_prompt},
                  {"role": "user", "content": user_text}],
        temperature=0
    )
    return response.choices[0].message.content.strip()
 
def extract_city(query):
    return ask_llm("Extract only the city name from the query. "
                   "Return just the city name.", query)
 
def get_weather(city):
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"
    geo = requests.get(geo_url, params={"name": city, "count": 1},
                       timeout=10)
    geo.raise_for_status()
    results = geo.json().get("results")
    if not results:
        raise ValueError(f"City '{city}' not found.")
    place = results[0]
 
    wx_url = "https://api.open-meteo.com/v1/forecast"
    wx = requests.get(wx_url, params={
        "latitude": place["latitude"],
        "longitude": place["longitude"],
        "current_weather": True}, timeout=10)
    wx.raise_for_status()
    return place["name"], wx.json()
 
def run_agent(query):
    city = extract_city(query)
    print(f"\nExtracted City: {city}")
    if input("Call the weather API? (y/n): ").strip().lower() != "y":
        print("API call cancelled by the user.")
        return
 
    name, data = get_weather(city)
    current = data["current_weather"]
 
    print("\n--- Raw Output ---")
    print(json.dumps(current, indent=2))
 
    explanation = ask_llm(
        "Explain this weather data to a student in 2 simple sentences. "
        "Temperature is in Celsius and wind speed is in km/h.",
        f"City: {name}\nData: {json.dumps(current)}")
    print("\n--- Explanation ---")
    print(explanation)
 
def main():
    print("\n" + "-" * 50)
    print("       Web-Lookup Agent (Weather)")
    print("-" * 50)
    print("\nType 'exit' to stop the agent.")
    while True:
        query = input("\nAsk your question: ")
        if query.lower() == "exit":
            print("Agent stopped.")
            break
        if not query.strip():
            print("Please enter a question.")
            continue
        try:
            run_agent(query)
        except requests.RequestException as e:
            print(f"Network Error: {e}")
        except Exception as e:
            print(f"Error: {e}")
 
if __name__ == "__main__":
    main()
