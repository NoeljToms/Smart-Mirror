from tkinter import*
import locale
import threading
import time
import requests
import json
import traceback
import feedparser

from contextlib import contextmanager
from PIL import Image, ImageTk


icon_lookup={
    'clear-day': "Sun.png",  
    'wind': "Wind.png",
    'cloudy': "Cloud.png",  
    'partly-cloudy-day': "PartlySunny.png",  
    'rain': "Rain.png",  
    'snow': "Snow.png", 
    'snow-thin': "Snow.png",  
    'fog': "Haze.png", 
    'clear-night': "Moon.png", 
    'partly-cloudy-night': "PartlyMoon.png",  
    'thunderstorm': "Storm.png",  
    'tornado': "Tornado.png",    
    'hail': "Hail.png"  

}

xlarge_text_size = 94
large_text_size = 48
medium_text_size = 28
small_text_size = 18



def exit(event):
    root.destroy()

def fullscrn(event):
    root.attributes("-fullscreen", True)
    root.overrideredirect(1)

def bckspace(event):
    root.attributes("-fullscreen",False)
    root.geometry("800x500")
    root.overrideredirect(0)
def Clock():
    time2=time.strftime("%I:%M:%S %p")
    widget.config(text=time2)
    widget.after(200, Clock)

def Date():
    date=time.strftime("%b %d %Y")
    date_label["text"]=date
    date_label.after(200,Date)

def Day_Week():
    dayofweek=time.strftime("%A")
    day_label.config(text=dayofweek)
    day_label.after(200,Day_Week)

def Weather():
    r=requests.get("https://api.darksky.net/forecast/8c24755f5fb2bb362a64602867008935/43.7315,-79.7626")
    json_object=r.json()
    tempK=int(json_object["currently"]["temperature"])
    tempC=int((tempK-32)/(9/5))
    weather_label.config(text=tempC)
    weather_label.after(300000,Weather)
    currently=json_object["currently"]["summary"]
    currentlyLbl["text"]=currently
    currentlyLbl.after(300000,Weather)


def Icon():
    r=requests.get("https://api.darksky.net/forecast/8c24755f5fb2bb362a64602867008935/43.7315,-79.7626")
    json_object=json.loads(r.text)
    icon_id=json_object["currently"]["icon"]
    icon2=None
    if icon_id in icon_lookup:
        icon2 = icon_lookup[icon_id]
    
    image=Image.open(icon2)
    image=image.resize((100,100),Image.ANTIALIAS)
    image=image.convert('RGB')
    photo=ImageTk.PhotoImage(image)
    icon_label.config(image=photo)
    icon_label.image=photo
    icon_label.after(300000, Icon)

class News(Frame):
    def __init__(self,master,*args, **kwargs):
        Frame.__init__(self,master,*args, **kwargs)
        self.config(bg="black")
        self.title='News'
        self.newsLbl=Label(self,text=self.title,font=('Helvetica',medium_text_size),fg="white",bg="black")
        self.newsLbl.pack(side=TOP,anchor=W)
        self.headlinesContainer=Frame(self,bg="black")
        self.headlinesContainer.pack(side=TOP)
        self.get_headlines()

    def get_headlines(self):
        feed=feedparser.parse("https://news.google.com/news?ned=ca&output=rss")
        for post in feed.entries[1:6]:
            headline=NewsHeadline(self.headlinesContainer,post.title)
            headline.pack(side=TOP, anchor=W)
        self.after(900000,self.get_headlines)

class NewsHeadline(Frame):
    def __init__(self,master,event_name=''):
        Frame.__init__(self,master,bg="black")

        image = Image.open("Newspaper.png")
        image = image.resize((25, 25), Image.ANTIALIAS)
        image = image.convert('RGB')
        photo = ImageTk.PhotoImage(image)
        
        self.iconLbl = Label(self, bg='black', image=photo)
        self.iconLbl.image = photo
        self.iconLbl.pack(side=LEFT, anchor=N)

        self.eventName=event_name
        self.eventNameLbl=Label(self,text=self.eventName,fg='white',bg="black",font=('Helvetica', small_text_size))
        self.eventNameLbl.pack(side=LEFT, anchor=N)





root = Tk()
#BACKGROUND
root.configure(bg="black")

#ORGANIZATION
tempFrame=Frame(root,bg="black")
tempFrame.pack(side=TOP,fill=BOTH)
tapFrame=Frame(tempFrame,bg="black")
tapFrame.pack(side=LEFT,anchor=NW)
topFrame=Frame(tempFrame,bg="black")
topFrame.pack(side=RIGHT,anchor=NE)
degreeFrame=Frame(tapFrame,bg="black")
degreeFrame.pack(side=TOP, anchor=W)
bottomFrame=Frame(root,bg="black")
bottomFrame.pack(side=BOTTOM,fill=BOTH)


#WEATHER
weather_label=Label(degreeFrame,font=("helvitic",xlarge_text_size,"bold"),bg="black",fg="white",)
weather_label.pack(side=LEFT,anchor=N)
Celscius=Label(degreeFrame,font=("helvitic",xlarge_text_size,"bold"),bg="black",fg="white",text="°C")
Celscius.pack(side=LEFT,anchor=N)
currentlyLbl = Label(tapFrame, font=('Helvetica', medium_text_size), fg="white", bg="black")
currentlyLbl.pack(side=TOP, anchor=W,)
Weather()

#CLOCK WIDGET
widget=Label(topFrame,font=("helvitic",large_text_size,"bold",),bg="black",fg="white")                                       
widget.pack(side=TOP,anchor=E)
Clock()

#DAY OF THE WEEK
day_label=Label(topFrame,font=("helvitic",small_text_size,"bold"),bg="black",fg="white")
day_label.pack(side=TOP,anchor=E)
Day_Week()

#DATE
date_label=Label(topFrame,font=("helvitic",small_text_size,"bold"),bg="black",fg="white")
date_label.pack(side=TOP,anchor=E)
Date()

#WEATHER ICON
icon_label=Label(degreeFrame,font=("helvitic",50,"bold"),bg="black",fg="white",)
icon_label.pack(side=TOP,anchor=W)
Icon()

#NEWS
news=News(bottomFrame)
news.pack(side=LEFT, anchor=S,)



#FULLSCREEN AND EXIT
root.bind("<Delete>",exit)
root.bind("<Return>",fullscrn)
root.bind("<Escape>",bckspace)





root.mainloop()
