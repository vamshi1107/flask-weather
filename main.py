from flask import Flask,render_template,request
import requests
from bs4 import BeautifulSoup
import html5lib
import math

app=Flask(__name__,template_folder="templates")

@app.route("/", methods=['GET', 'POST'])
def ind():
    con = requests.get("https://www.google.com/search?q=hgh").content
    soup = BeautifulSoup(con, "html5lib")
    lc=soup.find("span", {"id": "xxxXMc"})
    if lc!=None:
        location= lc.text.split(",")[0]
    else:
        location="india"
    if request.method=="POST":
        city=request.form['city']
        if city != None:
           name = city
        else:
           name=location
    else:
        name=location
    w= weather(name)
    found=False
    if len(w.keys()) > 0:
        found=True
    else:
        found=False
    return render_template("index.html",weather=w,found=found)

def weather(name):
    c = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={name}&appid=5814201029ba001e12185ab57c6ddd8e").json()
    if c["cod"]!="404":
       t = c["main"]["temp"] - 273.0
       c["main"]["temp"] = round(t, 1)
       c["main"]["temp"] = round(t, 1)
       c["l_time"]=time(name)
    else:
        c={}
    return c

def time(city):
    url = f"https://www.google.com/search?q=time+in+{city}"
    tc = requests.get(url).content
    ts = BeautifulSoup(tc, "html5lib")
    tt = ts.find("div", {"class": "BNeawe iBp4i AP7Wnd"})
    if tt != None:
        time = tt.text
    else:
        time = "12:00"
    return time

@app.route("/time")
def getTime():
    city=request.args["city"]
    url = f"https://www.google.com/search?q=time+in+{city}"
    tc = requests.get(url).content
    ts = BeautifulSoup(tc, "html5lib")
    tt=ts.find("div", {"class": "BNeawe iBp4i AP7Wnd"})
    if tt !="" :
       time = tt.text
    else:
        time="12:00"
    return time


if __name__ == '__main__':
    app.run()