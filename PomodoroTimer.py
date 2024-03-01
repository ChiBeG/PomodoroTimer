import tkinter as tk
import ttkbootstrap as ttk
import threading
import time

class PomodoroTimer:
    def __init__(self):
        self.app = tk.Tk()
        self.app.title("Pomodoro Timer")
        self.app.geometry("500x500")
        self.style = ttk.Style(theme = "simplex")

        self.headerLabel = ttk.Label(self.app, text = "Pomodoro Timer")
        self.headerLabel.pack()


        self.timerFrame = ttk.Frame(self.app)
        self.timerFrame.pack(expand = True)


        self.minutes = ttk.StringVar('25')
        self.seconds = ttk.StringVar('0')

        self.minutesLabel = ttk.Label(self.timerFrame, textvariable = self.minutes)
        self.textMinutesLabel =  ttk.Label(self.timerFrame, text="minutos")
        self.secondsLabel = ttk.Label(self.timerFrame, textvariable = self.seconds)
        self.textSecondsLabel =  ttk.Label(self.timerFrame, text="segundos")

        self.minutesLabel.grid(column = 0, row = 0)
        self.textMinutesLabel.grid(column = 1, row = 0)
        self.secondsLabel.grid(column = 2, row = 0)
        self.textSecondsLabel.grid(column = 3, row = 0)

        
        self.buttonsFrame = ttk.Frame(self.app)

        self.startButton = ttk.Button(self.buttonsFrame, text = "Iniciar", bootstyle = "sucess-outline", command=self.start_thread)
        self.startButton.grid(column=0, row=0)
        self.startButton = ttk.Button(self.buttonsFrame, text = "Parar", bootstyle = "sucess-outline", command=self.stop)
        self.startButton.grid(column=1, row=0)

        self.buttonsFrame.pack()

        self.stop_loop = False
        self.app.mainloop()

    def start_thread(self):
        thread = threading.Thread(target=self.start)
        thread.start()
        
    def start(self):
        self.stop_loop = False
        fullSeconds = int(self.minutes.get())*60 + int(self.seconds.get())

        while fullSeconds > 0 and not self.stop_loop:
            fullSeconds -= 1

            curr_minutes, curr_seconds = divmod(fullSeconds, 60)
            self.minutes.set(curr_minutes)
            self.seconds.set(curr_seconds)
            self.app.update()
            time.sleep(1)

    def stop(self):
        self.stop_loop = True
        self.minutes.set(25)
        self.seconds.set(0)



        



PomodoroTimer()