import tkinter as tk
from tkinter import PhotoImage
import ttkbootstrap as ttk
import threading
import time
from playsound import playsound
import json


class PomodoroTimer:
    def __init__(self):

        self.app = tk.Tk()
        self.app.title("Pomodoro Timer")
        self.app.geometry("700x300")
        self.app.tk.call('wm', 'iconphoto', self.app._w, PhotoImage(file = "resources/timer-icon.png"))
        self.style = ttk.Style(theme = "cyborg")

        try:
            with open("settings.json", "r") as openfile:
                jsonObject = json.load(openfile)
                self.focusTime = jsonObject["focusTime"]
                self.restTime = jsonObject["restTime"]
                self.longrestTime = jsonObject["longrestTime"]
    
        except FileNotFoundError:
                self.focusTime = 25
                self.restTime = 5
                self.longrestTime = 15
                
        
        self.tabs = ttk.Notebook(self.app, bootstyle = "success")
        self.tabs.pack(fill="both", expand=True)
        
        self.focusTab = ttk.Frame(self.tabs)
        self.restTab = ttk.Frame(self.tabs)
        self.longrestTab = ttk.Frame(self.tabs)

        self.tabs.add(self.focusTab, text="Foco")
        self.tabs.add(self.restTab, text="Descanso")
        self.tabs.add(self.longrestTab, text="Descanso Longo")

        self.focusLabel = ttk.Label(self.focusTab, text=f"{self.focusTime:02d}:00", font=("Open Sans", 50))
        self.focusLabel.pack(expand=True)        
        
        self.restLabel = ttk.Label(self.restTab, text=f"{self.restTime:02d}:00", font=("Open Sans", 50))
        self.restLabel.pack(expand=True)

        self.longrestLabel = ttk.Label(self.longrestTab, text=f"{self.longrestTime:02d}:00", font=("Open Sans", 50))
        self.longrestLabel.pack(expand=True)

        self.cycles = 0
        self.cyclesCounter = ttk.Label(self.app, text=f"Ciclos: {self.cycles}")
        self.cyclesCounter.pack(pady=10)
        
        self.buttonsFrame = ttk.Frame(self.app)

        self.startButton = ttk.Button(self.buttonsFrame, text = "Iniciar", bootstyle = "success", command=self.start_thread)
        self.startButton.grid(column=0, row=0, padx=3)
        self.stopButton = ttk.Button(self.buttonsFrame, text = "Parar", bootstyle = "success", command=self.stop)
        self.stopButton.grid(column=1, row=0, padx=3)
        self.skipButton = ttk.Button(self.buttonsFrame, text = "Pular", bootstyle = "success", command=self.skip)
        self.skipButton.grid(column=2, row=0, padx=3)
        self.settingsButton = ttk.Button(self.buttonsFrame, text = "Configurar", bootstyle = "success", command = self.openSettings)
        self.settingsButton.grid(column=3, row=0, padx=3)

        self.buttonsFrame.pack(pady=10)

        
        self.skipped = False
        self.stopped = False

        
        
        self.app.mainloop()

    def start_thread(self):
        thread = threading.Thread(target=self.start())
        thread.start()
        
    def start(self):
        self.stopped = False
        self.skipped = False
        selectedTab = self.tabs.index(self.tabs.select())


        if selectedTab == 0:
            fullSeconds = 60 * self.focusTime
            while fullSeconds > 0 and not self.stopped:
                minutes, seconds = divmod(fullSeconds, 60)
                minutes = int(minutes)
                seconds = int(seconds)
                self.focusLabel.config(text=f"{minutes:02d}:{seconds:02d}")
                self.app.update()
                time.sleep(0.1)
                fullSeconds -= 0.1
            playsound("resources/alarm.wav")
            if not self.stopped or self.skipped:
                self.cycles += 1
                self.cyclesCounter.config(text=f"Ciclos: {self.cycles}")
                if self.cycles % 4 == 0:
                    self.tabs.select(2)
                else:
                    self.tabs.select(1)
                self.focusLabel.config(text=f"{self.focusTime:02d}:00")
        
        elif selectedTab == 1:
            fullSeconds = 60 * self.restTime
            while fullSeconds > 0 and not self.stopped:
                minutes, seconds = divmod(fullSeconds, 60)
                minutes = int(minutes)
                seconds = int(seconds)
                self.restLabel.config(text=f"{minutes:02d}:{seconds:02d}")
                self.app.update()
                time.sleep(0.1)
                fullSeconds -= 0.1
            playsound("resources/alarm.wav")
            if not self.stopped or self.skipped:
                self.tabs.select(0)
            self.restLabel.config(text=f"{self.restTime:02d}:00")

        elif selectedTab == 2:
            fullSeconds = 60 * self.longrestTime
            while fullSeconds > 0 and not self.stopped:
                minutes, seconds = divmod(fullSeconds, 60)
                minutes = int(minutes)
                seconds = int(seconds)
                self.longrestLabel.config(text=f"{minutes:02d}:{seconds:02d}")
                self.app.update()
                time.sleep(0.1)
                fullSeconds -= 0.1
            playsound("resources/alarm.wav")
            if not self.stopped or self.skipped:
                self.tabs.select(0)
            self.longrestLabel.config(text=f"{self.longrestTime:02d}:00")



    def stop(self):
        self.stopped = True
        self.skipped = False
        self.cycles = 0
        self.focusLabel.config(text=f"{self.focusTime:02d}:00")
        self.restLabel.config(text=f"{self.restTime:02d}:00")
        self.longrestLabel.config(text=f"{self.longrestTime:02d}:00")
        self.cyclesCounter.config(text=f"Ciclos: {self.cycles}")

    def skip(self):
        selectedTab = self.tabs.index(self.tabs.select())
        if selectedTab == 0:
            self.focusLabel.config(text=f"{self.focusTime:02d}:00")
        elif selectedTab == 1:
            self.restLabel.config(text=f"{self.restTime:02d}:00")
        elif selectedTab == 2:
            self.longrestLabel.config(text=f"{self.longrestTime:02d}:00")

        self.stopped = True
        self.skipped = True

    def openSettings(self):
        settings = tk.Toplevel()
        settings.title("Configurações")
        settings.geometry("500x170")

        inputFrame = ttk.Frame(settings)
        inputFrame.pack(pady = 10)

        
        new_focusTime = ttk.StringVar(value=self.focusTime)
        new_restTime = ttk.StringVar(value=self.restTime)
        new_longrestTime = ttk.StringVar(value=self.longrestTime)
        
        focusLabel = ttk.Label(inputFrame, text = "Minutos de foco")
        focusInput = ttk.Entry(inputFrame, textvariable = new_focusTime, width=10, justify= "center", bootstyle = "success")
        restLabel = ttk.Label(inputFrame, text = "Minutos de descanso")
        restInput = ttk.Entry(inputFrame, textvariable = new_restTime, width=10, justify= "center", bootstyle = "success")
        longrestLabel = ttk.Label(inputFrame, text = "Descanso longo")
        longrestInput = ttk.Entry(inputFrame, textvariable = new_longrestTime, width=10, justify= "center", bootstyle = "success")

        focusLabel.grid(column=0, row=0, padx=7)
        focusInput.grid(column=0, row=1, padx=7)
        restLabel.grid(column=1, row=0, padx=7)
        restInput.grid(column=1, row=1)
        longrestLabel.grid(column=2, row=0, padx=7)
        longrestInput.grid(column=2, row=1, padx=7)

        saveButton = ttk.Button(settings, text = "Salvar", bootstyle = "success-outline", command = lambda: self.changeTimes(int(new_focusTime.get()), int(new_restTime.get()), int(new_longrestTime.get())))
        saveButton.pack(pady=30)

    
    def changeTimes (self, new_focusTime, new_restTime, new_longrestTime):
        self.focusTime = new_focusTime
        self.restTime = new_restTime
        self.longrestTime = new_longrestTime
        dictionary = {
            "focusTime": self.focusTime,
            "restTime": self.restTime,
            "longrestTime": self.longrestTime
        }
        jsonObject = json.dumps(dictionary, indent=3)
        with open ("settings.json", "w+") as outfile: 
            outfile.write(jsonObject)
        self.focusLabel.config(text=f"{self.focusTime:02d}:00")
        self.restLabel.config(text=f"{self.restTime:02d}:00")
        self.longrestLabel.config(text=f"{self.longrestTime:02d}:00")
        self.app.update()
    

PomodoroTimer()