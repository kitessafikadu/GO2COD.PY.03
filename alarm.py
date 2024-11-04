from threading import Thread
from tkinter.ttk import *
from tkinter import *
from PIL import ImageTk, Image  
from pygame import mixer  
from datetime import datetime, timedelta
from time import sleep
import os

bg_color = '#ffffff'
co1 = "#566FC6"  
light_blue = "#ADD8E6"  
co2 = "#000000"  

window = Tk()
window.title("Alarm Clock")
window.iconbitmap("D:/Projects/PYTHON/GO2COD/alarm_icon.ico")
window.geometry('375x175')
window.configure(bg=bg_color)

frame_line = Frame(window, width=400, height=5, bg=co1)
frame_line.grid(row=0, column=0)

frame_body = Frame(window, width=400, height=290, bg=bg_color)
frame_body.grid(row=1, column=0)

img = Image.open('icon1.png')
img = img.resize((100, 100), Image.LANCZOS)
img = ImageTk.PhotoImage(img)

app_image = Label(frame_body, height=100, image=img, bg=bg_color)
app_image.place(x=10, y=10)

name = Label(frame_body, text="Alarm", height=1, font=('Ivy 18 bold'), bg=bg_color, fg=light_blue)
name.place(x=125, y=10)

hour_dropdown = Combobox(frame_body, width=2, font=('Arial 15'))
hour_dropdown['values'] = tuple(f"{i:02d}" for i in range(1, 13))
hour_dropdown.current(0)
hour_dropdown.place(x=130, y=58)

minute_dropdown = Combobox(frame_body, width=2, font=('Arial 15'))
minute_dropdown['values'] = tuple(f"{i:02d}" for i in range(60))
minute_dropdown.current(0)
minute_dropdown.place(x=180, y=58)

second_dropdown = Combobox(frame_body, width=2, font=('Arial 15'))
second_dropdown['values'] = tuple(f"{i:02d}" for i in range(60))
second_dropdown.current(0)
second_dropdown.place(x=230, y=58)

period_dropdown = Combobox(frame_body, width=3, font=('Arial 15'))
period_dropdown['values'] = ("AM", "PM")
period_dropdown.current(0)
period_dropdown.place(x=280, y=58)

time_left_label = Label(frame_body, text="", font=('Ivy 12 bold'), bg=bg_color, fg=co1)
time_left_label.place(x=125, y=90)

selected = IntVar()

def activate_alarm():
    Thread(target=countdown).start()  

def deactivate_alarm():
    mixer.music.stop()
    selected.set(0)
    time_left_label.config(text="")  

rad1 = Radiobutton(frame_body, font=('Arial 10 bold'), value=1, text="Activate", bg=bg_color, fg="green", command=activate_alarm, variable=selected)
rad1.place(x=125, y=120)

rad2 = Radiobutton(frame_body, font=('Arial 10 bold'), value=2, text="Deactivate", bg=bg_color, fg="red", command=deactivate_alarm, variable=selected)
rad2.place(x=210, y=120)

mixer.init()
alarm_sound_path = 'alarm_sound.mp3'  
def sound_alarm():
    try:
        if os.path.exists(alarm_sound_path):
            mixer.music.load(alarm_sound_path)  
            mixer.music.set_volume(1)  
            mixer.music.play(-1)  
        else:
            print(f"Error: Sound file '{alarm_sound_path}' not found.")
    except Exception as e:
        print("Error playing sound:", e)

def countdown():
    while selected.get() == 1:
        now = datetime.now()
        
        alarm_hour = int(hour_dropdown.get()) % 12 + (12 if period_dropdown.get() == "PM" else 0)
        alarm_minute = int(minute_dropdown.get())
        alarm_second = int(second_dropdown.get())
        
        alarm_time = now.replace(hour=alarm_hour, minute=alarm_minute, second=alarm_second, microsecond=0)

        time_left = alarm_time - now

        if time_left.total_seconds() > 0:
            hours, remainder = divmod(time_left.total_seconds(), 3600)
            minutes, seconds = divmod(remainder, 60)
            time_left_label.config(text=f"Alarm in {int(hours):02}:{int(minutes):02}:{int(seconds):02}")
        else:
            time_left_label.config(text="Alarm ringing!")
            sound_alarm()  
            break 

        sleep(1)

window.mainloop()
