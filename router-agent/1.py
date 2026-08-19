import pyautogui as pg
from time import sleep


CONTACTS = {
     "siva":"9381644896",
     "sunil":"8290788851"
}


def sendmessage(name , message):

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

def call():
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
    
        pg.write("9381644896" , interval=0.2)
        sleep(1)
        pg.press("enter")
        sleep(2)
        for i in range(11):
            pg.press("tab")
            sleep(1)
        pg.press("enter  ")
sendmessage('sunil' , "Message Gen by Ai ")