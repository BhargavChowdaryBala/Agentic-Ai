def weather():
    print('calling weather API')

def cal():
    print('calling caliculator API')

while True:
    query = input('enter query : ')
    print('observe')
    print('decide')
    print('act')
    if "weather" in query:
        print("intent = weather")
        weather()
    if "add" in query:
            print("intent = addition")
            cal()
    if "exit" in query:
        print("Exiting ....")
        break







