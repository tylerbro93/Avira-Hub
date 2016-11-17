import pygame
from random import randint
from Tkinter import *
import copy
import subprocess

musicPlayList = []
playerState = "off"
playlistName = ""
loadingMusic = True
playlists = []
randomSongs = []
station_Names = []
station_Addresses = []
station_Name = ""
songPosition = 0
effects = []
pauseState = 0
accessMusicFrom = "local"

root = Tk()
topFrame = Frame(root, bg = "gray8")
leftFrame = Frame(topFrame, bg = "gray8")
scrollbar = Scrollbar(leftFrame, orient=VERTICAL)
availablePlaylistsField = Listbox(leftFrame, yscrollcommand=scrollbar.set, height = "5", bg = "gray35", highlightbackground="black", selectbackground= "cyan2")
availablePlaylistsField.pack(side = "left")
scrollbar.pack(side="left", fill=Y)
leftFrame.pack(side = "left")
rightFrame = Frame(topFrame, bg = "gray8", width = "200")
musicSourceFrame = Frame(topFrame, bg = "gray8")
musicFieldsFrame = Frame(root)
musicTextField = Label(musicFieldsFrame,font=("times",10,"bold"),width = "500", text = "Music Time",bg="gray8", fg="cyan")
visualEffectField = Label(musicFieldsFrame,relief = "solid", height = 10, highlightthickness = 2, highlightbackground="gray17",font=("times", 6),width = "500", text = "ENJOY>>>\n\n\n\n\n", bg="gray11", fg="cyan")
musicStateFrame = Frame(topFrame, bg = "gray8")

def playRadioStream(radioStationNumber):
    global pauseState
    subprocess.Popen("mpc play "+ str(radioStationNumber) +" &", shell=True)
    pauseState = 3

def loadFrom():
    global accessMusicFrom
    availablePlaylistsField.delete(0, END)
    if(accessMusicFrom == "local"):
        pygame.mixer.music.stop()
        readInRadioStations()
        accessMusicFrom = "remote"
        PlayFromButton.config(text = "Playlists")
    else:
        subprocess.Popen("mpc stop", shell=True)
        readInPlaylists()
        accessMusicFrom = "local"
        PlayFromButton.config(text = "Internet Radio")
        
PlayFromButton = Button(musicSourceFrame,width ="12", bg = "black", fg = "cyan2",text = "Internet Radio", font = ("times", 10),highlightbackground="gray17", command = loadFrom)        

def readInRadioStations():
    global playlists
    station_Addresses[:] = []
    station_Names[:] = []
    infile = open("Radio Stations/Stations.DataBank")
    line = infile.readline().strip()
    while(len(line)>0):
        name, address = line.split("[\]")
        station_Names.append(name)
        station_Addresses.append(address)
        subprocess.Popen("mpc add " + address, shell=True)
        availablePlaylistsField.insert(END, name)
        line = infile.readline().strip()
        print station_Names
    infile.close()
    
def readInPlaylists():
    global playlists
    playlists[:] = []
    infile = open("Music Playlist/playlists.DataBank")
    line = infile.readline().strip()
    while(len(line)>0):
        playlists.append(line)
        availablePlaylistsField.insert(END, line)
        line = infile.readline().strip()
    infile.close()

def playlistHasBeenSelected():
    global availablePlaylistsField
    global playlistName
    global accessMusicFrom
    try:
        items = map(int, availablePlaylistsField.curselection())
        item = items[0]
        if(accessMusicFrom == "local"):
            playlistName = playlists[item]
            loadPlaylistFromFile()
            randomSong()
        else:
            playRadioStream(item)
            musicTextField.config(text = station_Names[item])
            root.update()
    except:
        musicTextField.config(text = "Please select a playlist first")
        
def loadPlaylistFromFile():
    global musicPlayList
    global playlistName
    infile = open("Music Playlist/"+ playlistName + ".txt")
    line = infile.readline().strip()
    while(len(line)>0):
        musicPlayList.append(line)
        line = infile.readline().strip()
    infile.close()
        
def randomSong():
    global musicPlayList
    global randomSongs
    global loadingMusic
    randomSongs[:] = []
    songsListHolder = copy.deepcopy(musicPlayList)
    for song in songsListHolder:
        positionInPlayList = randint(0, len(songsListHolder)-1)
        musicFileName = songsListHolder[positionInPlayList]
        randomSongs.append(musicFileName)
    playNextSong()
    loadingMusic = False
    
def changeSongTitleColor():
    colorOptions = ["green", "red", "blue", "yellow"]
    foreground = colorOptions[randint(0, len(colorOptions)-1)]
    musicTextField.config(fg = foreground)
    
def playNextSong():
    global songPosition
    global randomSongs
    global pauseState
    musicFileName = randomSongs[songPosition]
    pygame.mixer.music.load("Music/" + musicFileName)
    pygame.mixer.music.play(0)
    musicName, fileType = musicFileName.split(".")
    musicTextField.config(text = musicName)
    songPosition = songPosition + 1
    pauseState = 2
  
def pauseOrPlaySong():
    global pauseState
    if(pauseState == 1):
        pauseState = 2
        pygame.mixer.music.unpause()
        pauseButton.config(text = "Pause")
    elif(pauseState == 2):
        pauseState = 1
        pygame.mixer.music.pause()
        pauseButton.config(text = "Play")
    elif(pauseState == 3):
        subprocess.Popen("mpc pause", shell=True)
        pauseState = 0

pauseButton = Button(musicStateFrame, width = "5", bg = "black", fg = "cyan2",text = "Pause", font = ("times", 10),highlightbackground="gray17", command = pauseOrPlaySong)

def setEffects():
    effectsInView = "*" * 52 + "\n"
    for i in range(0, 5):
        effectsInView += "*\n"
    visualEffectField.config(text = effectsInView)

def musicPlayer():
    global songPosition
    global randomSongs
    global accessMusicFrom
    changeSongTitleColor()
    SONG_END = pygame.USEREVENT + 1
    pygame.mixer.music.set_endevent(SONG_END)
    
    if(loadingMusic != True):
        setEffects()
        if(accessMusicFrom == "local"):
            for event in pygame.event.get():
                    if event.type == SONG_END:
                        if(songPosition != len(randomSongs)):
                            playNextSong()
                        else:
                            songPosition = 0
                            randomSong()
    musicTextField.after(1000, musicPlayer)

def shutdownMusicPlayer():
    root.destroy()
    
def main():
    global topFrame
    pygame.init()
    root.title("Music Player by tylerbro93")
    readInPlaylists()
   
    musicTextField.pack(side = "bottom")
    visualEffectField.pack(side = "bottom", anchor = "w")
    musicFieldsFrame.pack(side = "bottom")
    PlayFromButton.pack(side = "bottom")
    selectButton = Button(musicSourceFrame, width = "12", bg = "gray3", fg = "cyan2",text = "Load Playlist", font = ("times", 10),highlightbackground="gray17", command = playlistHasBeenSelected)
    selectButton.pack(side = "top")
    exitButton = Button(musicStateFrame, width = "5", bg = "gray3", fg = "cyan2",text = "Exit", font = ("times", 10),highlightbackground="gray17", command = shutdownMusicPlayer)
    exitButton.pack(side = "bottom")
    pauseButton.pack(side = "top")
    musicSourceFrame.pack(side = "left")
    musicStateFrame.pack(side = "left")
    rightFrame.pack(side = "right")
    topFrame.pack(side = "top")
    root.geometry("500x300")
    root.config(background = "gray8")
    musicPlayer()
    root.mainloop()
    pygame.mixer.music.stop()
    subprocess.Popen("pkill ffplay", shell=True)
main()
    
