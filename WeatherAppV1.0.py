# Import modules

import tkinter as tk
import requests
from tkinter import messagebox
from PIL import Image, ImageTk
import ttkbootstrap

def get_weather(city):
    API_key ="18c5b092953ac7f70c30ca7abfd57b81"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city},&appid={API_key}"
    res = requests.get(url)

    if res.status_code == 404:
        messagebox.showerror("Error", "City not found")
        return None

    #parse JSON to get weather information
    weather = res.json()
    icon_id = weather['weather'][0]['icon']
    temperature = weather['main']['temp'] - 273.15
    description = weather['weather'][0]['description']
    city = weather['name']
    country = weather['sys']['country']

#get weather icons from OpenWeatherAPI
    icon_url = f"https://openweathermap.org/img/wn/{icon_id}@2x.png"
    return (icon_url, temperature, description, city, country)


#Search for weather in a given City
def search():
    city = city_entry.get()
    result = get_weather(city)
    if result is None:
        return
    # If found then return icon_url, tempature, decription, city, county as results
    icon_url, temperature, description, city, country = result
    location_label.configure(text=f"{city}, {country}")

    #get Icon from URL and update Label
    image = Image.open(requests.get(icon_url, stream=True).raw)
    icon = ImageTk.PhotoImage(image)
    icon_label.configure(image=icon)
    icon_label.image = icon

    #Update tempatures
    temperature_label.configure(text=f"Temperature: {temperature:.2f}°C")
    description_label.configure(text=f"Description: {description}")

root = ttkbootstrap.Window(themename="morph")
root.title("Weather App")
root.geometry("800x800")

    #Allows you to enter the City Name
city_entry = ttkbootstrap.Entry(root, font="Terminal, 24")
city_entry.pack(pady=10)

    #Creates Search Button
search_button = ttkbootstrap.Button(root, text="Search", command=search, bootstyle="warning")
search_button.pack(pady=10)

    #Shows City/Country Name
location_label = tk.Label(root, font="Terminal, 32")
location_label.pack(pady=20)

    #Shows Weather Icon
icon_label = tk.Label(root)
icon_label.pack()

    #Shows Local Tempature
temperature_label = tk.Label(root, font="terminal, 24")
temperature_label.pack()

    #Discribes Local Weather
description_label = tk.Label(root, font="terminal, 24")
description_label.pack()

root.mainloop()
