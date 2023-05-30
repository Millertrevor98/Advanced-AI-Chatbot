import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import json
import random
import requests
from bs4 import BeautifulSoup


# OpenWeatherMap API key
API_KEY = "20980e620a4701dee0fafdf6c00e9122"

def get_chatbot_response(user_input):
    if "news" in user_input.lower():
        news = fetch_news()
        if news:
            return "Here are some latest news headlines:\n\n" + news
        else:
            return "Sorry, I couldn't fetch the news at the moment."
    elif "weather" in user_input.lower():
        weather = fetch_weather()
        if weather:
            return "Here is the current weather:\n\n" + weather
        else:
            return "Sorry, I couldn't fetch the weather at the moment."
    else:
        for intent in intents:
            for pattern in intent["patterns"]:
                if pattern in user_input.lower():
                    return random.choice(intent["responses"])
    return "I'm sorry, I didn't understand that."

def fetch_news():
    url = "https://www.bbc.com/news"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    headlines = soup.find_all("h3")

    if headlines:
        news = ""
        for headline in headlines:
            news += f"- {headline.text}\n"
        return news
    else:
        return None

def fetch_weather():
    api_key = "20980e620a4701dee0fafdf6c00e9122"  # Place your OpenWeatherMap API key here
    city = "New York"
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if data.get("weather") and data.get("main"):
        weather = f"Weather: {data['weather'][0]['main']}\n"
        temperature = f"Temperature: {data['main']['temp']}°C\n"
        humidity = f"Humidity: {data['main']['humidity']}%\n"
        return weather + temperature + humidity
    else:
        return None

def send_message():
    user_input = entry.get().strip()
    entry.delete(0, tk.END)

    if user_input.lower() == "quit":
        messagebox.showinfo("ChatBot", "Goodbye!")
        window.destroy()
        return

    response = get_chatbot_response(user_input)
    chat_log.insert(tk.END, "You: " + user_input + "\n")
    chat_log.insert(tk.END, "BroBot: " + response + "\n")
    chat_log.see(tk.END)

# Load intents from JSON file
with open("intents.json") as file:
    intents = json.load(file)

window = tk.Tk()
window.title("BroBot")
window.iconbitmap("favicon.ico")

# Set window size and position
window.geometry("650x500")
window.resizable(False, False)

# Set window background color
window.configure(bg="#2C5364")

# Load and resize the logo image
logo_image = Image.open("logo.png")
logo_image = logo_image.resize((150, 150))
logo_photo = ImageTk.PhotoImage(logo_image)

# Create a label widget for the logo
logo_label = tk.Label(window, image=logo_photo, bg="#2C5364")
logo_label.pack(pady=10)

# Create a frame for the chat log
chat_frame = tk.Frame(window, bg="#203A43", padx=10, pady=10)
chat_frame.pack(fill=tk.BOTH, expand=True)

# Create a scrollable text widget for the chat log
chat_log = tk.Text(chat_frame, bg="#0F2027", bd=0, height=2, width=90)
chat_log.configure(
    font=("Arial", 17),  # Set the font family and size
    fg="#ffffff",       # Set the text color
    padx=10,            # Set the padding on the X-axis
    pady=10             # Set the padding on the Y-axis
)
chat_log.pack(side=tk.LEFT, fill=tk.BOTH)


# Create a scroll bar for the chat log
scrollbar = tk.Scrollbar(chat_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Attach the scroll bar to the chat log
chat_log.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=chat_log.yview)

# Create a send button
send_button = tk.Button(window, text="Send", font=("Arial", 17), bg="#4285F4", fg="#000000", bd=0, command=send_message)
send_button.pack(fill=tk.BOTH, padx=10, pady=10)

def clear_placeholder(event):
    if entry.get() == placeholder_text:
        entry.delete(0, tk.END)

# Create an entry widget for user input
placeholder_text = "Type your question here"
entry = tk.Entry(window, font=("Arial", 17), bg="#203A43", bd=0)
entry.configure(
    fg="#ffffff"  # Set the text color
)
entry.insert(0, placeholder_text)
entry.bind("<FocusIn>", clear_placeholder)
entry.pack(fill=tk.BOTH, padx=10, pady=10)


# Set focus on the entry widget by default
entry.focus_set()

window.mainloop()
