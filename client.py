import socket
from threading import Thread
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from playsound import playsound
import pygame
from pygame import mixer
import os
import time
import ftplib
from ftplib import FTP
import ntpath
from pathlib import Path

song_counter = 0
result_counter = 0
textarea = None
filePathLabel = None
PORT  = 8080
IP_ADDRESS = '127.0.0.1'
SERVER = None
BUFFER_SIZE = 4096
selected_song = None
searchQuery = None
lst = None

def setup():
    global SERVER
    global PORT
    global IP_ADDRESS
    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.connect((IP_ADDRESS, PORT))
    openChatWindow()

def get_songs():
    global song_counter
    listbox.delete(0, END)
    for file in os.listdir('shared_files'):
        filename = os.fsdecode(file)
        listbox.insert(song_counter, filename)
        song_counter = song_counter + 1

def play():
    global selected_song
    selected_song = listbox.get(ANCHOR)
    pygame
    mixer.init()
    mixer.music.load('shared_files/'+selected_song)
    mixer.music.play()
    if(selected_song != ""):
        infoLabel.configure(text = "Now Playing: " + selected_song)
    else:
        infoLabel.configure(text = "")

def stop():
    global selected_song
    pygame
    mixer.init()
    mixer.music.load('shared_files/'+selected_song)
    mixer.music.pause()
    infoLabel.configure(text = "")


def browseFiles():  
    global textarea
    global filePathLabel
    global song_counter

    try:
        filename = filedialog.askopenfilename()
        HOSTNAME = "127.0.0.2"
        USERNAME = "root"
        PASSWORD = "toor"

        ftp_server = FTP(HOSTNAME, USERNAME, PASSWORD)
        ftp_server.encoding = "utf-8"
        ftp_server.cwd('shared_files')
        fname = ntpath.basename(filename)  
        with open (filename, 'rb') as f:
            ftp_server.storbinary(f"stor {fname}", f)
        ftp_server.dir()
        ftp_server.quit()
        get_songs()
    except FileNotFoundError:
        print("File does not exist")

def check_input(event):    
    global lst
    lst = os.listdir('shared_files')
    value = event.widget.get()

    if value == '':
        combo_box['values'] = lst
    else:
        data = []
        for item in lst:
            if value.lower() in item.lower():
                data.append(item)

        combo_box['values'] = data

def download():
    global song_to_download
    song_to_download = listbox.get(ANCHOR)
    infoLabel.configure(text="Dowloading "+ song_to_download)
    HOSTNAME = "127.0.0.1"
    USERNAME = "root"
    PASSWORD = "toor"

    home = str(Path.home())
    download_path = home+"/Desktop"
    ftp_server = ftplib.FTP(HOSTNAME, USERNAME, PASSWORD)
    ftp_server.encoding = "utf-8"
    ftp_server.cwd('shared_files')
    local_filename = os.path.join(download_path, song_to_download)
    file = open(local_filename, 'wb')
    ftp_server.retrbinary('RETR '+ song_to_download, file.write)
    ftp_server.dir()
    file.close()
    ftp_server.quit()
    infoLabel.configure(text = "Download Complete")
    time.sleep(1)
    if(str(selected_song) != ""):
        infoLabel.configure(text = "Now Playing "+str(selected_song))
    else:
        infoLabel.configure(text="")
                    
def openChatWindow():
    global infoLabel
    global listbox
    global searchQuery
    global combo_box
    window=Tk()
    window.title('LAN Music Sharing')
    window.geometry("500x350")
    window.configure(bg = '#ccffee')
    
    photo = PhotoImage(file = "pause.png")
    photoimage = photo.subsample(7, 7)

    photo2 = PhotoImage(file = "play.png")
    photoimage2 = photo2.subsample(13, 13)
    
    photo4 = PhotoImage(file = "stop.png")
    photoimage4 = photo4.subsample(15, 16)

    selectlabel = Label(window, text= "Select a Song:", bg = '#ccffee', font = ("Calibri",15))
    selectlabel.place(x=2, y=1)

    searchlabel = Label(window, text= "Or Search:", bg = '#ccffee', font = ("Calibri",15))
    searchlabel.place(x=300, y=1)

    listbox = Listbox(window,height=10, width=39, activestyle = 'dotbox', bg = '#ccffee', borderwidth=2, font = ("Calibri", 10))
    listbox.place(x=10,y=30)

    scrollbar1 = Scrollbar(listbox)
    scrollbar1.place(relheight=1, relx = 1)
    scrollbar1.config(command=listbox.yview)

    playButton = Button(window, text="Play", bd= 1, bg= "#ddffee", font = ("Calibri",10), image = photoimage2, compound = LEFT, command = play)
    playButton.pack(side = TOP)
    playButton.place(x=30,y=220)

    Pause = Button(window, text= "Pause", bd=1, bg="#ddffee", font = ("Calibri", 10), image = photoimage, compound = LEFT, command = stop)
    Pause.pack(side = TOP)
    Pause.place(x=120, y=220)
    
    Stop = Button(window, text= "Stop", bd=1, bg="#ddffee", font = ("Calibri", 10), image = photoimage4, compound = LEFT)
    Stop.pack(side = TOP)
    Stop.place(x=210, y=220)
  
    Upload =Button(window, text="Upload", width=10, bd = 1, bg ='#ddffee', font = ("Calibri", 10),command = browseFiles)
    Upload.place(x=30, y=280)

    Download =Button(window, text="Download", width=10, bd = 1, bg ='#ddffee', font = ("Calibri", 10), command=download)
    Download.place(x=200, y=280)

    infoLabel = Label(window, text="", fg = "blue", font = ("Calibri", 8))
    infoLabel.place(x=50, y = 320)

    
    combo_box = ttk.Combobox(window)
    combo_box['values'] = lst
    combo_box.bind('<KeyRelease>', check_input)
    combo_box.pack()
    combo_box.place(x= 300, y =30)

    get_songs()
    window.mainloop()

setup()