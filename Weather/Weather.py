import tkinter as tk
import requests
import time
def get_weather():
    city = textField.get()
    api = "https://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=06c921750b9a82d8f5d1294e1586276f"
    
    try:
        json_data = requests.get(api).json()

        if 'weather' in json_data:
            condition = json_data['weather'][0]['main']
            temp_celsius = int(json_data['main']['temp'] - 273.15)
            temp_fahrenheit = int((temp_celsius * 9/5) + 32)
            min_temp = int(json_data['main']['temp_min'] - 273.15)
            max_temp = int(json_data['main']['temp_max'] - 273.15)
            pressure = json_data['main']['pressure']
            humidity = json_data['main']['humidity']
            wind = json_data['wind']['speed']
            sunrise = time.strftime('%I:%M:%S', time.gmtime(json_data['sys']['sunrise'] - 21600))
            sunset = time.strftime('%I:%M:%S', time.gmtime(json_data['sys']['sunset'] - 21600))

            final_info = condition + "\n" + f"{temp_celsius}°C / {temp_fahrenheit}°F"
            final_data = "\n" + "Min Temp: " + f"{min_temp}˚C / {int((min_temp * 9/5) + 32)}˚F" + "\n" + "Max Temp: " + f"{max_temp}˚C / {int((max_temp * 9/5) + 32)}˚F" + "\n" + "Pressure: " + str(
                pressure) + "\n" + "Humidity: " + str(humidity) + "\n" + "Wind Speed: " + str(wind) + "\n" + "Sunrise: " + sunrise + "\n" + "Sunset: " + sunset
            label1.config(text=final_info, fg="white", bg="blue")
            label2.config(text=final_data, fg="white", bg="green")
        else:
            label1.config(text="Weather data not found for " + city, fg="purple", bg="white",font =("Helvetica",20,"bold"))
            label2.config(text="", fg="white", bg="white")
            
    except Exception as e:
        label1.config(text="An error occurred: " + str(e), fg="red", bg="white")
        label2.config(text="", fg="white", bg="white")

def toggle_temp_unit():
    current_text = toggle_button["text"]
    if current_text == "Celsius":
        toggle_button["text"] = "Fahrenheit"
    else:
        toggle_button["text"] = "Celsius"
    get_weather()

def submit_weather():
    get_weather()

def clear_weather():
    textField.delete(0, "end")
    label1.config(text="")
    label2.config(text="")

canvas = tk.Tk()
canvas.title("Weather App")

screen_width = canvas.winfo_screenwidth()
screen_height = canvas.winfo_screenheight()

x = (screen_width / 2) - (600 / 2) 
y = (screen_height / 2) - (500 / 2)
canvas.geometry(f"600x500+{int(x)}+{int(y)}")

textField = tk.Entry(canvas, justify="center", width=20, font=("Arial", 35, "bold"))
textField.pack(pady=20)
textField.focus()
textField.bind("<Return>", lambda event=None: get_weather())

label1 = tk.Label(canvas, font=("Helvetica", 35, "bold"))
label1.pack()
label2 = tk.Label(canvas, font=("Helvetica", 15, "bold"))
label2.pack()

submit_button = tk.Button(canvas, text="Submit", command=submit_weather)
submit_button.pack()

clear_button = tk.Button(canvas, text="Clear", command=clear_weather)
clear_button.pack()

canvas.configure(bg="lightyellow")
canvas.mainloop()