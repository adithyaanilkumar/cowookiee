import requests
import pytz
from datetime import date,datetime
import json
from deta import App
from fastapi import FastAPI

app = App(FastAPI())

def sendTGMessage(message:str)->None:
    url = f'https://api.telegram.org/bot1760938714:AAH-B9bpd0ZUZlNxdU6LuKXR-5HwrH8vz04/sendMessage'
    msg_data = {'chat_id':"-517874387",'text':message,"parse_mode":"Markdown"}
    resp = requests.post(url, msg_data).json()
    #print(resp)
    print("Message Not Send" if resp['ok'] is False else "👉    Message Sent")

@app.get("/")
def http():
    return "Hello Deta, I am running with HTTP"

@app.lib.cron()
def getCowinData(event):
    tz = pytz.timezone("Asia/Calcutta")
    time= datetime.now(tz).strftime('%H:%M:%S')
    today = date.today().strftime("%d-%m-%Y")
    data = requests.get(f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=307&date={today}").json()
    nos_centers = len(data['centers'])
    avl_centers = 0
    avl_center_list =[]
    for centers in data['centers']:
        for sessions in centers["sessions"]:
            if sessions["available_capacity"] >0:
                avl_centers+=1
                string = centers["name"] +" "+ str(centers["pincode"]) + " - avl: " + str(sessions["available_capacity"]) + " on " + sessions["date"] + "\n\n----\n"
                avl_center_list.append(string)
    count = len(avl_center_list)
    listToStr = " ".join(map(str, avl_center_list))
    if(count>0):
        message = f"{count} Available in ERNAKULAM on {today} at {time} \n\n ---\n\n {listToStr}"
        sendTGMessage(message)

