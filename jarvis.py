import pyttsx3  # pip install pyttsx3
import datetime
import speech_recognition as sr  # pip install SpeechRecognition
import pyaudio
import wikipedia  # pip install wikipedia
import smtplib  # for sending emails
import webbrowser as wb  # for opening chrome

engine = pyttsx3.init()

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def get_time():
    current_time = datetime.datetime.now().strftime("%I:%M:%S %p")
    speak(f"The current time is {current_time}")

def get_date():
    year = datetime.datetime.now().year
    month = datetime.datetime.now().strftime("%B")
    day = datetime.datetime.now().day
    speak(f"The date is {day} {month} {year}")

def wish_me():
    speak("Welcome back, Ms. Jindam!")
    speak("The current time is")
    get_time()
    speak("The current date is")
    get_date()
    hour = datetime.datetime.now().hour
    if 6 <= hour < 12:
        speak("Good Morning, Ms. Jindam")
    elif 12 <= hour < 18:
        speak("Good Afternoon, Ms. Jindam")
    elif 18 <= hour < 24:
        speak("Good Evening, Ms. Jindam")
    else:
        speak("Good Night, Ms. Jindam")
    speak("Stark at your service. Please tell me how I can help you.")

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
    except Exception as e:
        print(e)
        speak("Say that again, please...")
        return "None"
    
    return query.lower()

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    # Note: You should use environment variables or a config file for storing credentials securely
    server.login('your_email@gmail.com', 'your_password')
    server.sendmail('your_email@gmail.com', to, content)
    server.close()

if __name__ == "__main__":
    wish_me()
    while True:
        query = take_command()
        
        if 'time' in query:
            get_time()
        elif 'date' in query:
            get_date()
        elif 'thank you' in query or 'thanks' in query:
            speak("You're welcome!")
        elif 'wikipedia' in query:
            speak("Searching for you...")
            query = query.replace("wikipedia", "")
            result = wikipedia.summary(query, sentences=2)
            print(result)
            speak(result)
        elif 'send email' in query:
            try:
                speak("What should I send?")
                content = take_command()
                to = 'recipient_email@gmail.com'
                sendEmail(to, content)
                speak("Email has been successfully sent")
            except Exception as e:
                print(e)
                speak("Sorry, I was unable to send the email")
        elif 'search in chrome' in query:
            speak("What should I search?")
            chromepath = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'  # Ensure this path is correct
            search = take_command().lower()
            wb.get(chromepath).open_new_tab(f'{search}.com')
        elif 'exit' in query or 'bye' in query:
            speak("Goodbye, Ms. Jindam!")
            break
