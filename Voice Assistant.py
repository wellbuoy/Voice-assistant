# Import necessary modules
import speech_recognition as sr
import pyttsx3
import smtplib
import ssl
import requests
import webbrowser

# Initialize speech recognizer
recognizer = sr.Recognizer()

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Function to speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to recognize speech
def recognize_speech():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-US')
        print(f"User said: {query}")
        return query.lower()
    except Exception as e:
        print(e)
        return ""

# Function to send email
def send_email(receiver_email, subject, body):
    sender_email = "your_email_address"
    password = "your_email_password"

    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"

    message = f"Subject: {subject}\n\n{body}"

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

# Function to fetch weather updates
def get_weather(city):

    # your openweathermap api key
    api_key = "5071e6e27a20771f1ae38649a39d8701"

    # the url for the weather
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

    response = requests.get(url)
    data = response.json()
    if data['cod'] == 200:
        weather_desc = data['weather'][0]['description']
        temp_kelvin = data['main']['temp']
        temp_celsius = temp_kelvin - 273.15

        # tell the user about the city temperature
        return f"The weather in {city} is {weather_desc} with a temperature of {temp_celsius:.2f}°C."
    
    # return error message when the weather data could not be fetched
    else:
        return "Sorry, couldn't fetch weather data."

# Function to search on Google
def search_google(query):
    search_url = f"https://www.google.com/search?q={query}"
    webbrowser.open(search_url)

# Function to play music on YouTube
def play_music():
    speak("Sure, what music would you like to play?")
    music_query = recognize_speech()
    search_query = f"{music_query} music"
    search_url = f"https://www.youtube.com/results?search_query={search_query}"
    webbrowser.open(search_url)

# Main function
def main():
    # Introduction and instructions
    speak("""Hello! I am your voice assistant.
          Please say 'google' to search anything on Google.
          Say 'send email' to send emails.
          Say 'play music' to play a song.
          Say 'weather' to check the weather.
          Say 'exit' to close the voice assistant.""")
    
    # Voice assistant operations loop
    while True:
        query = recognize_speech()

        # Google search command
        if "google" in query:
            speak("What would you like to search on Google?")
            search_query = recognize_speech()
            search_google(search_query)

        # Send email command
        elif "send email" in query:
            try:
                # Email composition
                speak("What is the receiver's email address?")
                receiver_email = recognize_speech()

                speak("What is the subject of the email?")
                subject = recognize_speech()

                speak("What should I say in the email?")
                body = recognize_speech()

                send_email(receiver_email, subject, body)

                speak("Email has been sent successfully.")

            except Exception as e:
                print(e)
                speak("Sorry, I am unable to send the email.")

        # Check the weather command
        elif "weather" in query:
            speak("Sure, which city's weather do you want to know?")
            city = recognize_speech()
            weather_info = get_weather(city)
            speak(weather_info)

        # Play music command
        elif "play music" in query:
            play_music()

        # Exit command
        elif "exit" in query:
            speak("Goodbye, and have a nice day!")
            break
        
        # Unrecognized command
        else:
            speak("Sorry, I didn't get that.")

if __name__ == "__main__":
    main()
