from langchain.agents import create_agent
from dotenv import load_dotenv

load_dotenv()


from langchain.tools import tool 
import pyautogui as pg
from time import sleep 

@tool('sendmessage' , description="This tool is To send Messages in whatsapp. Using pyautogui accept two Parameters name , message ")
def sendmessage(name , message):

    CONTACTS = {
        "siva":"9381644896",
        "sunil":"8290788851"
    }





    number = CONTACTS[name]
    if number is None:
         print("Not valid")
    else:
        pg.press("win")
        sleep(0.5)
        pg.write("whatsapp" , interval=0.2)
        sleep(1)
        pg.press("enter")
        sleep(5)
        pg.hotkey("win" , "up")

        sleep(5)

        pg.press("tab")
        sleep(1)
        pg.press("tab")
        sleep(1)

        pg.press("tab")
        sleep(1)
        pg.press("tab")
        sleep(1)

        pg.write(f"{number}" , interval=0.2)
        sleep(1)
        pg.press("enter")
        sleep(0.5)
        pg.write(f"{message}" , interval=0.2)
        sleep(1)
        pg.press("enter")


agent = create_agent(
    model="groq:openai/gpt-oss-20b",
    tools=[sendmessage],
    system_prompt="You are a helpful assistant",
)


result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "Send a message to sunil that i m saying i m leaving hall politly "
            }
        ]
    }
)

print(result["messages"][-1].content_blocks)