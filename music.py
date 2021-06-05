
import pygame
import tkinter as tkr
from tkinter.filedialog import askdirectory
from threading import Thread as process
import os
from tkinter import *
#from threading import Thread
import threading
import time
# state 0 = loop， state 1 = normal state, state 2 = random play
previous = pygame.USEREVENT + 2
nxt = pygame.USEREVENT + 3
noop = pygame.USEREVENT
state = 1
def play_time(song):
    current_time = pygame.mixer.music.get_pos() / 1000
    # convert to time format
    converted_current_time = time.strftime('%H:%M:%S', time.gmtime(current_time))
    status_bar.config(text=converted_current_time)
    status_bar.after(1000, play_time)
    song_name = pygame.mixer.Sound(song)
    
def play():
    global state
    current_track = 0
    NEXT = pygame.USEREVENT + 1
    tracks_number = len(song_list)
    print(current_track)
    print(song_list)
    if current_track == 0 :
            pygame.mixer.music.load(play_list.get(tkr.ACTIVE))
            var.set(play_list.get(tkr.ACTIVE))
    else:
        pygame.mixer.music.load(song_list[current_track])

    pygame.mixer.music.play()
    print(play_list.get(tkr.ACTIVE))
    position = 0 
    for song in song_list:
        if play_list.get(tkr.ACTIVE) == song:
            current_track = position
        else:
            position += 1 
    # send event NEXT every time tracks ends
    print("The current track is :", current_track)
    pygame.mixer.music.set_endevent(NEXT) 

    running = True
    while running:
        
        for event in pygame.event.get():
            play_time()
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == NEXT:
                state = 1
                
                # get next track (modulo number of tracks)
                current_track = (current_track + 1) % tracks_number
                print("Play:", song_list[current_track])
                pygame.mixer.music.load(song_list[current_track])
                var.set(song_list[current_track])
                pygame.mixer.music.play()
                
            elif event.type == previous:

                current_track = (current_track - 1) % tracks_number

                print("Play:", song_list[current_track])

                pygame.mixer.music.load(song_list[current_track])
                var.set(song_list[current_track])
                if state == 1:
                    pygame.mixer.music.play()
                else:
                    pygame.mixer.music.play(-1,0.0)

            elif event.type == nxt:

                current_track = (current_track + 1) % tracks_number

                print("Play:", song_list[current_track])
                pygame.mixer.music.load(song_list[current_track])
                var.set(song_list[current_track])
                if state == 1:
                    pygame.mixer.music.play()
                else:
                    pygame.mixer.music.play(-1,0.0)

            elif event.type == noop:
                state = 0
                pygame.mixer.music.load(play_list.get(tkr.ACTIVE))
                pygame.mixer.music.play(-1,0.0)
    pygame.quit()


def next():
    global state
    pygame.mixer.music.set_endevent(nxt) 
    pygame.mixer.music.stop()
    
    

def pause():
    pygame.mixer.music.pause()


def unpause():
    pygame.mixer.music.unpause()


def loop():
    global state
    pygame.mixer.music.set_endevent(noop) 


def pre():
    global state
    pygame.mixer.music.set_endevent(previous) 
    pygame.mixer.music.stop()



music_player = tkr.Tk()
music_player.title("Music Player")


directory = askdirectory()
os.chdir(directory) #it permits to chenge the current dir
song_list = os.listdir() #it returns the list of files song
height = str(500+len(song_list)*10)
music_player.geometry("500x"+height) # initialize the height and width for the user interface

# background color and the text style of the play list
play_list = tkr.Listbox(music_player, font="Helvetica 12 bold", bg="yellow", selectmode=tkr.SINGLE)
# insert every song files into the bottom of the current song files.(like a queue)
# for the purpose of showing the song's name. 
for item in song_list:
    pos = len(song_list)-1
    play_list.insert(pos, item)
    

pygame.init()
pygame.mixer.init()



#music_thread = threading.Thread(target=play,daemon=True)
# using lambda to recreate a new thread whenever user click the button, avoid error [thread start only once]
Button1 = tkr.Button(music_player, width=5, height=3, font="Helvetica 12 bold", text="PLAY", command=lambda: process (target = play, daemon = True).start (), bg="blue", fg="white")
#Button 2 kill the main program.
Button2 = tkr.Button(music_player, width=5, height=3, font="Helvetica 12 bold", text="STOP", command= music_player.destroy, bg="red", fg="white")
# pause the song
Button3 = tkr.Button(music_player, width=5, height=3, font="Helvetica 12 bold", text="PAUSE", command=pause, bg="purple", fg="white")
# unpause
Button4 = tkr.Button(music_player, width=5, height=3, font="Helvetica 12 bold", text="UNPAUSE", command=unpause, bg="orange", fg="white")
# loop the single song
Button5 = tkr.Button(music_player, width=5, height=3, font="Helvetica 12 bold", text="LOOP", command=loop, bg="green", fg="white")
# play the next song
Button6 = tkr.Button(music_player, width=5, height=3, font="Helvetica 12 bold", text="NEXT", command=next, bg="blue", fg="white")
# play the previous song
Button7 = tkr.Button(music_player, width=5, height=3, font="Helvetica 12 bold", text="PRVE", command=pre, bg="black", fg="white")

status_bar = Label(music_player, text='',bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill="x",side=BOTTOM, ipady=2)
var = tkr.StringVar()

song_title = tkr.Label(music_player, font="Helvetica 12 bold", textvariable= var)
song_title.pack()
Button1.pack(fill="x")
Button2.pack(fill="x")
Button3.pack(fill="x")
Button4.pack(fill="x")
Button5.pack(fill="x")
Button6.pack(fill="x")
Button7.pack(fill="x")
play_list.pack(fill="both", expand="yes")
music_player.mainloop()
