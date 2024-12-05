import streamlit as st
import speech_recognition as sr
import pyttsx3
import datetime
import requests
from pytube import Search
import webbrowser

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty("rate", 150)
voices = engine.getProperty("voices")
for voice in voices:
    if "female" in voice.name.lower():
        engine.setProperty("voice", voice.id)
        break

def say(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def get_weather(city):
    """Fetch and announce live weather information for the given city."""
    api_key = "c234ae7e76b9846b047a3677c80eca07"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        if data["cod"] == 200:
            weather = data["weather"][0]["description"]
            temp = data["main"]["temp"]
            result = f"The weather in {city} is {weather} with a temperature of {temp}\u00b0C."
            say(result)
            return result
        else:
            say("Sorry, I couldn't fetch the weather information. Please check the city name and try again.")
            return "Invalid city name."
    except Exception as e:
        say("There was an error fetching the weather data. Please try again later.")
        return "Error fetching weather data."

def play_music(song):
    """Play music or videos from YouTube."""
    try:
        say("Searching for the song on YouTube...")
        search = Search(song)
        video = search.results[0]  # Get the first search result
        webbrowser.open(video.watch_url)  # Open the video in the web browser
        result = f"Playing {song} on YouTube."
        say(result)
        return result
    except Exception as e:
        say("Sorry, I couldn't fetch the song. Please try again.")
        return "Error playing music."

# Streamlit App
def main():
    st.title("Jarvis - Your Voice Assistant")

    # Sidebar for user options
    st.sidebar.header("Options")
    option = st.sidebar.selectbox("Choose an action:", ["Welcome", "Check Time", "Get Weather", "Play Music"])

    if option == "Welcome":
        st.write("Hey! I'm Jarvis. How can I assist you today?")

    elif option == "Check Time":
        now = datetime.datetime.now().strftime("%H:%M")
        st.write(f"The current time is: {now}")
        say(f"The time is {now}")

    elif option == "Get Weather":
        city = st.text_input("Enter the city name:")
        if st.button("Get Weather"):
            if city:
                result = get_weather(city)
                st.write(result)

    elif option == "Play Music":
        song = st.text_input("Enter the song name:")
        if st.button("Play Music"):
            if song:
                result = play_music(song)
                st.write(result)

if __name__ == "__main__":
    main()
