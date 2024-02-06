import os
import openai
from dotenv import load_dotenv
import time
import speech_recognition as sr
import pyttsx3
import numpy as np



load_dotenv()
openai.api_key = ""

model = 'gpt-3.5-turbo'
r = sr.Recognizer()
engine = pyttsx3.init()
voice = engine.getProperty('voices')[1]
engine.setProperty('voice', voice.id)
name = "YOUR NAME HERE"
greetings = [f"whats up master {name}",
             "yeah?",
             "Well, hello there, Master of Puns and Jokes - how's it going today?",
             f"Ahoy there, Captain {name}! How's the ship sailing?",
             f"Bonjour, Monsieur {name}! Comment ça va? Wait, why the hell am I speaking French?"]


def listen_for_wake_word(source):
    print("Listening for 'Hey pesant'...")

    while True:
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            if "hey pesant" in text.lower():
                print("Wake word detected.")
                engine.say(np.random.choice(greetings))
                engine.runAndWait()
                listen_and_respond(source)
                break
        except sr.UnknownValueError:
            pass


# Listen for input and respond with OpenAI API
def listen_and_respond(source):
    print("Listening...")

    while True:
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            print(f"You said: {text}")
            if not text:
                continue

            # Send input to OpenAI API
            response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                                    messages=[{"role": "user", "content": f"{text}"}])
            response_text = response.choices[0].message.content
            print(f"OpenAI response: {response_text}")

            # Speak the response
            engine.say(response_text)
            engine.runAndWait()

            if not audio:
                listen_for_wake_word(source)
        except sr.UnknownValueError:
            time.sleep(2)
            print("Silence found, shutting up, listening...")
            listen_for_wake_word(source)
            break

        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            engine.say(f"Could not request results; {e}")
            engine.runAndWait()
            listen_for_wake_word(source)
            break


# Use the default microphone as the audio source
with sr.Microphone() as source:
    listen_for_wake_word(source)
