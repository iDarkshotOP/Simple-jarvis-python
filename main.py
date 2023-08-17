import pyttsx3
import datetime
import speech_recognition as sr
import time
from playsound import playsound
import random
import wikipedia
import webbrowser as wb

CLEAR = "\033[2J"
CLEAR_AND_RETURN = "\033[H"

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()
    
def wish_me():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 14:
        speak("Good Afternoon!")
    else:
        speak("Good Evening")
    speak("Welcome Back, sir. I trust you're having a productive day.")

def takecmd():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("I'm Listening..........")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print('Recognizing......')
        query = r.recognize_google(audio, language='en-IN')
        print(f"User Said: '{query}' \n")
        return query.lower()
    except Exception as e:
        print("Repeat That AGAIN! ")
        return "None"

def get_alarm_time():
    speak("How many minutes to wait?")
    minutes_text = takecmd()
    minutes = extract_number(minutes_text)

    speak("How many seconds to wait?")
    seconds_text = takecmd()
    seconds = extract_number(seconds_text)

    total_seconds = minutes * 60 + seconds
    return total_seconds

def extract_number(text):
    words = text.split()
    for word in words:
        if word.isdigit():
            return int(word)
    return 0

def search_wikipedia(query):
    speak('Searching Wikipedia ......... ')
    results = wikipedia.summary(query, sentences=2)
    speak('According to Wikipedia')
    with open(f"prompt - {random.randint(999999, 9999999)}.txt", 'a') as f:
        f.write(results)
    speak(results)

if __name__ == "__main__":
    while True:
        query = takecmd()

        if 'set an alarm' in query:
            total_seconds = get_alarm_time()

            def alarm(seconds):
                time_elapsed = 0
                print(CLEAR)
                while time_elapsed < seconds:
                    time.sleep(1)
                    time_elapsed += 1
                    time_left = seconds - time_elapsed
                    minutes_left = time_left // 60
                    seconds_left = time_left % 60
                    print(f"{CLEAR_AND_RETURN}ALARM WILL SOUND IN: {minutes_left:02d}:{seconds_left:02d}")
                playsound('alarm.mp3')

            alarm(total_seconds)
        elif 'wikipedia' in query or 'who is' in query:
            query = query.replace('wikipedia', '')
            search_wikipedia(query)
        elif 'open google' in query:
            wb.open('www.google.com')
        elif 'open youtube' in query:
            wb.open('www.youtube.com')
        elif 'open instagram' in query:
            wb.open('www.instagram.com')
        elif 'open whatsapp' in query:
            wb.open('web.whatsapp.com')