import speech_recognition as sr
import pyttsx3 # text to speech conversion
import datetime
import wikipedia
import webbrowser
import os
import time
import subprocess # log off or restart pc
from ecapture import ecapture as ec # capture img from camera
import wolframalpha #
import json
import requests
import smtplib
from selenium import webdriver
import regex as re
from selenium.webdriver.common.keys import Keys


# o for male, 1 for female
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice','voices[0].id')

def speak(text):
    engine.say(text)
    engine.runAndWait()

def wishMe():
    hour = datetime.datetime.now().hour
    if hour >= 0 and hour < 12:
        speak("Hey, Good Morning!")
        print("Hey, Good Morning!")
    elif hour >= 12 and hour <= 18:
        speak("Hey, Good Afternoon!")
        print("Hey, Good Afternoon!")
    else:
        speak("Hey, Good Evening!")
        print("Hey, Good Evening!")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

        try:
            statement = r.recognize_google(audio, language='en-in')
            print(f"you said:{statement}\n")
        except Exception as e:
            speak("Couldn't catch you, can you please repeat?")
            return "None"
        return statement
print("Opening EA Assistant")
speak("Opening EA Assistant")
wishMe()

if __name__ == '__main__':
    while True:
        speak("How can I help you ?")
        statement = takeCommand().lower()
        if statement == 0:
            continue

        # Stoppping Virtual Assistant
        if "good bye" in statement or "ok bye" in statement or "stop" in statement:
            speak("Turning off EA Assistant")
            print("Turning off EA Assistant")
            break
        # Answering with wiki articles
        if "wikipedia" in statement:
            speak("searching wikipedia")
            statement = statement.replace("wikipedia", "")
            results = wikipedia.summary(statement, sentences=3)
            speak("According to wikipedia")
            print(results)
            speak(results)
        # web searching
        elif "search" in statement:
            statement = statement.replace("search", "")
            webbrowser.open_new_tab(statement)
            time.sleep(5)
        # Opening from browser
        elif "open youtube" in statement:
            webbrowser.open_new_tab("http://www.youtube.com")
            speak("youtube is opened")
            time.sleep(5)
        elif "open google" in statement:
            webbrowser.open_new_tab("http://www.google.com")
            speak("google is opened")
            time.sleep(5)
        elif "open gmail" in statement:
            webbrowser.open_new_tab("http://www.gmail.com")
            speak("gmail is opened")
            time.sleep(5)
        # time
        elif "time" in statement:
            now = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"It is {now}")
        # Fetch news
        elif "news" in statement:
            news = webbrowser.open_new_tab("https://medium.com/")
            speak("Tech and Data Science Headlines from Medium")
            time.sleep(5)
        # camera
        elif "camera" in statement or "photo" in statement:
            ec.capture(0, "virtual_cam", "img.jpg")
        # Geography
        elif "ask" in statement:
            speak("I can answer harder # QUESTION: ")
            question = takeCommand()
            app_id =  "X725RY-86RJ7H48LX"
            client = wolframalpha.Client('R2K75H-7ELALHR35X')
            res = client.query(question)
            answer = next(res.results).text
            speak(answer)
            print(answer)
        elif "who are you" in statement:
            speak("I am a virtual Assistant")
        elif "who made you" in statement:
            speak("Made by EA Elvin")

        # weather app api
        elif "weather" in statement:
            api_key = "9d46554e7960c225059b751947fb329e"
            base_url="api.openweathermap.org/data/2.5/weather?"
            speak("Which city?")
            city_name = takeCommand()
            complete_url=base_url+"appid="+api_key+"&q="+city_name
            response = requests.get(complete_url)
            x=response.json()
            if x["cod"]!="404":
                y=x["main"]
                current_temperature = y["temp"]
                current_humidiy = y["humidity"]
                z = x["weather"]
                weather_description = z[0]["description"]
                speak(" Temperature in kelvin unit is " +
                      str(current_temperature) +
                      "\n humidity in percentage is " +
                      str(current_humidiy) +
                      "\n description  " +
                      str(weather_description))
        # shut down pc
        elif "shut down" in statement:
            speak("OK, pc is shutting down all apps")
            subprocess.call(["shutdown", "/l"])
        # mail
        elif 'email' in statement:
            speak('What is the subject?')
            time.sleep(3)
            subject = takeCommand()
            speak('What should I say?')
            time.sleep(3)
            message = takeCommand()
            content = 'Subject: {}\n\n{}'.format(subject, message)
            mail = smtplib.SMTP('smtp.gmail.com', 587)
            #identify to server
            mail.ehlo()
            #encrypt session
            mail.starttls()
            #login
            mail.login('agammedzadee@gmail.com', 'elvinelvin1997')
            #send message
            mail.sendmail('FROM', 'TO', content)
            #end mail connection
            mail.close()

            talk('Email sent.')

        # telling you a joke
        elif "tell me a joke" in statement:
            responeData = requests.get("http://api.icndb.com/jokes/random/?escape=javascript")
            joke = str(responeData.json()['value']['joke'])
            print (joke)
            speak(joke)

        elif "google" in statement:
            reg_ex = re.search('open google and search (.*)', statement)
            search_for = statement.split("search",1)[1]
            url = 'https://www.google.com/'
            if reg_ex:
                subgoogle = reg_ex.group(1)
                url = url + 'r/' + subgoogle
            speak('Okay!')
            # **************************************************************************************************
            driver = webdriver.Firefox(executable_path='/path/to/geckodriver') #depends which web browser you are using
            driver.get('http://www.google.com')
            search = driver.find_element_by_name('q') # finds search
            search.send_keys(str(search_for)) #sends search keys
            search.send_keys(Keys.RETURN) #hits enter
time.sleep(3)
