import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import sys
import pyjokes
import pyautogui
import ctypes
import subprocess
import requests
import psutil
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QTimer, QTime, QDate, Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from alphaUi import Ui_jarvisUi
from location import weather
import wolframalpha
try:
    apps = wolframalpha.Client('K7G63E-THP7KXWJUW')
except Exception:
    print("some features are not working")


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
#print(voices[0].id)
engine.setProperty('voice',voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")
    elif hour>=12 and hour<18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")

    speak("I am Alpha Sir. Please tell me how I may help you")

def cpu():
    usage = str(psutil.cpu_percent())
    speak("CPU is at" + usage)

    battery = psutil.sensors_battery()
    speak("battery is at")
    speak(battery.percent)


def news():
    main_url = 'http://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey=86e45722f0864265885d0643cf212e49'

    main_page = requests.get(main_url).json()
    #print(main_page)
    articles = main_page["articles"]
    #print(articles)
    head = []
    day=["frist","second","third","fourth","fifth"]
    for ar in articles:
        head.append(ar["title"])
    for i in range (len(day)):
        print(f"today's {day[i]} news is:", head[i])
        speak(f"today {day[i]} news is: {head[i]}")



class MainThread(QThread):
    def __init__(self):
        super(MainThread,self).__init__()

    def run(self):
        self.TaskExecution()

    def takeCommand(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening........")
            r.pause_threshold = 1
            audio = r.listen(source, )

        try:
            print("Recognizing.....")
            self.query = r.recognize_google(audio, )
            print("user said:", self.query)

        except Exception as e:
            print("Say that again please...")
            speak("Say that again please")
            return "none"
        return self.query


    def TaskExecution(self):
         wishMe()
         while True:
             self.query = self.takeCommand().lower()

             if 'wikipedia' in self.query:
                 speak('Searching wikipedia....')
                 self.query = self.query.replace("wikipedia", "")
                 results = wikipedia.summary(self.query, sentences=2)
                 speak("According to wikipedia")
                 speak(results)
                 #print(result)

             elif 'who are you' in self.query:
                 speak("I am Alpha sir")

             elif 'how are you' in self.query:
                 speak("I am fine, Thank you")


             elif 'open notepad' in self.query:
                 npath = "C:\\Windows\\SysWOW64\\notepad.exe"
                 os.startfile(npath)

             elif'open command prompt'in self.query:
                 os.system("start cmd")

             elif 'open youtube' in self.query:
                    webbrowser.open("www.youtube.com")

             elif 'open google' in self.query:
                webbrowser.open("www.google.com")


             elif 'open stack overflow' in self.query:
                 webbrowser.open("www.stackoverflow.com")


             elif 'play music' in self.query:
                 music_dir = 'D:\music'
                 songs = os.listdir(music_dir)
                 os.startfile(os.path.join(music_dir, songs[1]))

             elif 'joke' in self.query:
                 speak(pyjokes.get_joke())

             elif 'the time' in self.query:
                 strTime = datetime.datetime.now().strftime("%H:,%M:,%S")
                 speak(f"Sir, the time is {strTime}")

             elif 'shutdown' in self.query:
                 speak("do you really want to shutdown the system sir")
                 reply = self.takeCommand().lower()
                 if 'yes' in reply:
                     os.system('shutdown /s /t 1')
                 else:
                     speak("As you wish, Sir!")

             elif "restart" in self.query:
                 speak("do you really want to restart the system sir")
                 reply = self.takeCommand().lower()
                 if 'yes' in reply:
                     subprocess.call(["shutdown", "/r"])
                 else:
                     speak("As you wish, Sir!")


             elif 'switch window' in self.query:#error
                 pyautogui.keyDown('alt')
                 pyautogui.press('tab')
                 pyautogui.press('tab')
                 pyautogui.keyUp('alt')

             elif 'lock window' in self.query:
                 speak("locking the device")
                 ctypes.windll.user32.LockWorkStation()

             elif 'temperature' in self.query:
                 try:
                     res = apps.query(self.query)
                     print(next(res.results).text)
                     speak(next(res.results).text)
                 except:
                     print("internet connection not working")

             elif 'calculate' in self.query:
                 speak("what should I calculate?")
                 gh = self.takeCommand().lower()
                 res = apps.query(gh)
                 speak("results is ")
                 speak(next(res.results).text)

             elif 'news' in self.query:
                 speak("please wait sir, fetching the latest news")
                 news()

             elif 'weather' in self.query:
                 weather()

             elif 'cpu' in self.query:
                 cpu()


             elif 'tell me' in self.query or 'who is' in self.query or 'what is' in self.query or 'which is' in self.query:
                 self.query = self.query
                 speak('Searching...')
                 try:
                     try:
                         res = apps.query(self.query)
                         results = next(res.results).text
                         speak('Got it.')
                         speak('WOLFRAM-ALPHA says - ')
                         speak(results)
                     except:
                         results = wikipedia.summary(self.query, sentences=2)
                         speak('Got it.')
                         speak('WIKIPEDIA says - ')
                         speak(results)
                 except:
                     webbrowser.open('www.google.com')

             elif 'no thanks' in self.query:
                 speak('thanks for using me sir, have a nice day.')
                 sys.exit()

             speak('Sir, do you have any other work')


startExecution = MainThread()


class Main(QMainWindow):
    def __init__(self):
            super().__init__()
            self.ui = Ui_jarvisUi()
            self.ui.setupUi(self)
            self.ui.pushButton.clicked.connect(self.startTask)
            self.ui.pushButton_2.clicked.connect(self.close)

    def startTask(self):
            self.ui.movie = QtGui.QMovie("C:/Users/Ojas/PycharmProjects/pythonprogram/images/24ce143fafec7bd6-.gif")
            self.ui.label.setMovie(self.ui.movie)
            self.ui.movie.start()
            self.ui.movie = QtGui.QMovie("C:/Users/Ojas/PycharmProjects/pythonprogram/images/20210102_130653.gif")
            self.ui.label_2.setMovie(self.ui.movie)
            self.ui.movie.start()
            self.ui.movie = QtGui.QMovie("C:/Users/Ojas/PycharmProjects/pythonprogram/images/20210102_133356.gif")
            self.ui.label_3.setMovie(self.ui.movie)
            self.ui.movie.start()
            timer = QTimer(self)
            timer.timeout.connect(self.showTime)
            timer.start(5000)
            startExecution.start()

    def showTime(self):
        current_time = QTime.currentTime()
        current_Date = QDate.currentDate()
        label_time = current_time.toString("hh:mm:ss")
        label_date = current_Date.toString(Qt.ISODate)
        self.ui.textBrowser.setText(label_date)
        self.ui.textBrowser_2.setText(label_time)


app = QApplication(sys.argv)
jarvis = Main()
jarvis.show()
exit(app.exec_())




