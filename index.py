#!/usr/bin/env python

from prettyprinter import pprint
from time import sleep

import light
import requests

print("\n✅ Ready to go.\n----")

URL = "https://h20-l.vercel.app/api"

def changeColor():
    identifier = input("Enter lamp ID: ")
    color = input("Enter lamp color: ") 
    brightness = input("Enter lamp brightness: ")

    r = requests.get(url=URL + "/update?id=" + identifier + "&color=" + color + "&brightness=" + brightness)
    pprint(r.text)


def viewLamps():
    r = requests.get(url=URL + "/view", timeout=5)
    return r.json()

def initLamp(id):
    requests.get(url=URL + "/create?id=" + id)

if __name__ == "__main__":
    id = input("Enter Lamp ID: ")
    initLamp(id)
    
    color = "white"
    brightness = "50"
    light.white()
       
    print("Scanning for changes...")
    try:
        while True:
            sleep(2)
            new_data = viewLamps()
            if new_data == None: continue
            
            lamp = new_data.get(id)
            if lamp == None:
                print("\nLamp not in databse; creating new one.")
                initLamp(id)
                continue
            
            changed = False

            if lamp.get("color") != None and lamp.get("color") != color:
                color = lamp.get("color")
                changed = True

            if lamp.get("brightness") != None and lamp.get("brightness") != brightness:
                brightness = lamp.get("brightness")
                changed = True

            
            print("#", end="", flush=True)
            
            if changed: 
                print("\nNew changes found:", id, color, brightness)

                if int(brightness) < 50:
                    light.turnOff()
                else:
                    if color == "red": light.red()
                    elif color == "green": light.green()
                    elif color == "blue": light.blue()
                    elif color == "yellow": light.yellow()
                    elif color == "cyan": light.lightBlue()
                    elif color == "purple": light.purple()
                    else: light.white()
            
    except Exception as e:
        light.turnOff()
        exit(print("\n", e, "\n"))
