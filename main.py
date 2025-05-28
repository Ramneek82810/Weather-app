from tkinter import *
import tkinter as tk
import pytz
from geopy.geocoders import Nominatim
from datetime import datetime, timedelta
import requests
from PIL import Image,ImageTk
from tkinter import messagebox, ttk
from timezonefinder import TimezoneFinder

root=Tk()
root.title("Weather App 5")
root.geometry("800x470+300+200")
root.resizable(False,False)
root.config(bg='#202731')

def getWeather():
    city=textfield.get()
    geolocator=Nominatim(user_agent="new")
    location=geolocator.geocode(city)
    obj=TimezoneFinder()
    result=obj.timezone_at(lat=location.latitude, lng=location.longitude)
    timezone.config(text=result)
    
    long_lat.config(text=f"{round(location.latitude,4)}°N {round(location.longitude,4)}°E")
    
    home=pytz.timezone(result)
    local_time=datetime.now(home)
    current_time=local_time.strftime("%I:%M %p")
    clock.config(text=current_time)
    
    api_key="1e6bc535e6fc30ba79f63b0a2c3f4bd7"
    api=f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
    json_data=requests.get(api).json()
    print(json_data)
    
    #current weather from first forecast
    current=json_data['list'][0]
    temp=current['main']['temp']
    humidity=current['main']['humidity']
    pressure=current['main']['pressure']
    wind_speed=current['wind']['speed']
    description=current['weather'][0]['description']
    
    t.config(text=f"{temp}°C")
    h.config(text=f"{humidity}%")
    p.config(text=f"{pressure}hPa")
    w.config(text=f"{wind_speed}m/s") 
    d.config(text=f"{description}")
    
    #Daily forecast-pick 12:00PM entries
    daily_data=[]
    for entry in json_data['list']:
        if "12:00:00" in entry['dt_txt']:
            daily_data.append(entry)
    
    icons=[]
    temps=[]
    
    for i in range(5):
        if i>=len(daily_data):
            break
        icon_code=daily_data[i]['weather'][0]['icon']
        img=Image.open(f"icon/{icon_code}@2x.png").resize((50,50))
        icons.append(ImageTk.PhotoImage(img))
        temps.append((daily_data[i]['main']['temp_max'],daily_data[i]['main']['feels_like']))
    
    day_widget=[
        (firstimage,day1,day1temp),
        (secondimage,day2,day2temp),
        (thirdimage,day3,day3temp),
        (fourthimage,day4,day4temp),
        (fifthimage,day5,day5temp)
    ]
    
    for i,(img_label,day_label,temp_label) in enumerate(day_widget):
        if i>=len(icons):
            break
        img_label.config(image=icons[i])
        img_label.image=icons[i]
        temp_label.config(text=f"Day:{temps[i][0]}\nNight:{temps[i][1]}")
        future_date=datetime.now()+timedelta(days=i)
        day_label.config(text=future_date.strftime("%A"))
        
    
    
#icon
image_icon=PhotoImage(file="Images/logo.png")
root.iconphoto(False,image_icon)

Round_box=PhotoImage(file="Images/Rounded Rectangle 1.png")
Label(root,image=Round_box,bg="#202731").place(x=30,y=60)

#label
label1=Label(root,text="Temperature",font=("Helvetica",11),fg="#323661",bg="#aad1c8")
label1.place(x=50,y=120)

label2=Label(root,text="Humidity",font=("Helvetica",11),fg="#323661",bg="#aad1c8")
label2.place(x=50,y=140)

label3=Label(root,text="Pressure",font=("Helvetica",11),fg="#323661",bg="#aad1c8")
label3.place(x=50,y=160)

label4=Label(root,text="Wind Speed",font=("Helvetica",11),fg="#323661",bg="#aad1c8")
label4.place(x=50,y=180)

label5=Label(root,text="Description",font=("Helvetica",11),fg="#323661",bg="#aad1c8")
label5.place(x=50,y=200)

#search box
Search_image=PhotoImage(file="Images/Rounded Rectangle 3.png")
myimage=Label(root,image=Search_image,bg='#203731')
myimage.place(x=270,y=122)

weat_image=PhotoImage(file="Images/Layer 7.png")
weatherimage=Label(root,image=weat_image,bg="#333c4c")
weatherimage.place(x=270,y=122)

textfield=tk.Entry(root,justify="center",width=15,font=("poppins",25,"bold"),bg="#333c4c",border=0,fg="white")
textfield.place(x=370,y=130)

Search_icon=PhotoImage(file="Images/Layer 6.png")
myimage_icon=Button(root,image=Search_icon,borderwidth=0,cursor="hand2",bg="#333c4c",command=getWeather)
myimage_icon.place(x=640,y=135)

#bottom box
frame=Frame(root,width=900,height=180,bg="#7094d4")
frame.pack(side=BOTTOM)

#boxes
firstbox=PhotoImage(file="Images/Rounded Rectangle 2.png")
secondbox=PhotoImage(file="Images/Rounded Rectangle 2 copy.png")

Label(frame,image=firstbox,bg="#7094d4").place(x=30,y=20)
Label(frame,image=secondbox,bg="#7094d4").place(x=300,y=30)
Label(frame,image=secondbox,bg="#7094d4").place(x=400,y=30)
Label(frame,image=secondbox,bg="#7094d4").place(x=500,y=30)
Label(frame,image=secondbox,bg="#7094d4").place(x=600,y=30)

#clock
clock=Label(root,font=("Helvetica",20),bg="#202731",fg="white")
clock.place(x=30,y=20)

#timezone
timezone=Label(root,font=("Helvetica",20),bg="#202731",fg="white")
timezone.place(x=500,y=20)

long_lat=Label(root,font=("Helvetica",20),bg="#202731",fg="white")
long_lat.place(x=500,y=50)

#thpwd
t=Label(root,font=("Helvetica",9),bg="#333c4c",fg="white")
t.place(x=150,y=120)

h=Label(root,font=("Helvetica",9),bg="#333c4c",fg="white")
h.place(x=150,y=140)

p=Label(root,font=("Helvetica",9),bg="#333c4c",fg="white")
p.place(x=150,y=160)

w=Label(root,font=("Helvetica",9),bg="#333c4c",fg="white")
w.place(x=150,y=180)

d=Label(root,font=("Helvetica",9),bg="#333c4c",fg="white")
d.place(x=150,y=200)

#first cell
firstframe=Frame(root,width=170,height=115,bg="#eeefea")
firstframe.place(x=65,y=325)

firstimage=Label(firstframe,bg="#eeefea")
firstimage.place(x=7,y=20)

day1=Label(firstframe,bg="#eeefea",fg="#000")
day1.place(x=10,y=5)

day1temp=Label(firstframe,bg="#eeefea",fg="#000")
day1temp.place(x=2,y=70)

#second cell
secondframe=Frame(root,width=70,height=115,bg="#eeefea")
secondframe.place(x=305,y=325)

secondimage=Label(secondframe,bg="#eeefea")
secondimage.place(x=7,y=20)

day2=Label(secondframe,bg="#eeefea",fg="#000")
day2.place(x=10,y=5)

day2temp=Label(secondframe,bg="#eeefea",fg="#000")
day2temp.place(x=2,y=70)

#third cell
thirdframe=Frame(root,width=70,height=115,bg="#eeefea")
thirdframe.place(x=405,y=325)

thirdimage=Label(thirdframe,bg="#eeefea")
thirdimage.place(x=7,y=20)

day3=Label(thirdframe,bg="#eeefea",fg="#000")
day3.place(x=10,y=5)

day3temp=Label(thirdframe,bg="#eeefea",fg="#000")
day3temp.place(x=2,y=70)

#fourth cell
fourthframe=Frame(root,width=70,height=115,bg="#eeefea")
fourthframe.place(x=505,y=325)

fourthimage=Label(fourthframe,bg="#eeefea")
fourthimage.place(x=7,y=20)

day4=Label(fourthframe,bg="#eeefea",fg="#000")
day4.place(x=10,y=5)

day4temp=Label(fourthframe,bg="#eeefea",fg="#000")
day4temp.place(x=2,y=70)

#fifth cell
fifthframe=Frame(root,width=70,height=115,bg="#eeefea")
fifthframe.place(x=605,y=325)

fifthimage=Label(fifthframe,bg="#eeefea")
fifthimage.place(x=7,y=20)

day5=Label(fifthframe,bg="#eeefea")
day5.place(x=10,y=5)

day5temp=Label(fifthframe,bg="#eeefea",fg="#000")
day5temp.place(x=2,y=70)

root.mainloop()