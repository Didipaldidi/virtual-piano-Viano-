import numpy as np
import time
import cv2
from pygame import mixer
from tkinter import *
from tkinter import font
import tkinter.messagebox

class HomePage:
    def __init__(self):
        self.mwindow = Tk()
        self.mwindow.title("Viano")
        self.mwindow.geometry('500x500+100+100')
        self.w = 500
        self.h = 500
        self.homeframe = Frame(self.mwindow, width= self.w, height= self.h)
        self.homeframe.place(x = 0, y = 0)

        self.titleLabel = Label(self.homeframe, text = 'Welcom to Viano', font=(40))
        self.titleLabel.place(x = 170, y = 10)

        self.numOfChords = Label(self.homeframe, text= "Enter the number of chords you need(Max 5 chords):")
        self.numOfChords.place(x = 70, y = 50)

        self.chordNums = Entry(self.homeframe, width= 10) # Input needs to be between 1 - 5 to maintain the space between each chords that are displayed on the screen
        self.chordNums.place(x = 355, y = 50)

        self.chordConfirmButton = Button(self.homeframe, text= "confirm", command=self.chooseChords)
        self.chordConfirmButton.place(x = 190, y = 80)

        mainloop()
    
    def playPiano(self):
        piano = Piano(self.stringVar) # create a Piano class and send the number of chords the user wants

    def chooseChords(self):
        numOfChoords = int(self.chordNums.get())
        if ( numOfChoords > 5):
            print("Exceeding the maximum number of chords") # prevent error from diplaying to many chord
            return
        else:
            self.chordsLabel=[]
            self.chords = ['C','D','E','F','G','A','B']
            self.stringVar = []
            self.chordSpinbox = []

            # display all the available chords in a spinbox
            for i in range(0,numOfChoords):
                self.chordsLabel.append(Label(self.homeframe, text="chord " + str(i+1) + ":"))
                self.stringVar.append(StringVar())
            
            pad = 0
            for i in range(0,len(self.chordsLabel)):
                self.chordsLabel[i].place(x = pad * (self.h/len(self.chords) + 40), y = 110)
                self.chordSpinbox.append(Spinbox(self.homeframe, values= self.chords, width= 5, textvariable= self.stringVar[i]))
                self.chordSpinbox[i].place(x = pad * (self.h/len(self.chords) + 40), y = 140)
                pad += 1
            self.doneButton = Button(self.homeframe, text= "done", command=self.playPiano)
            self.doneButton.place(x = 190, y = 160)
            
class Piano:
    def __init__ (self,lsOfChords):

        mixer.init()
        ls = []
        for i  in lsOfChords:
            ls.append(i.get()) # copy the list of chords

        self.chordsSound = []
        self.chordPic = []
        self.loadSound(ls)
        self.loadImg(ls)

        self.setCamera(ls)

    def loadSound(self, lsOfChords):
        # load all the sound of chords the user wants
        for i in lsOfChords:
            if i == 'C':
                self.chordsSound.append(mixer.Sound('.\sound\C.mp3'))
            elif i == 'D':
                self.chordsSound.append(mixer.Sound('.\sound\D.mp3'))
            elif i == 'E':
                self.chordsSound.append(mixer.Sound('.\sound\E.mp3'))
            elif i == 'F':
                self.chordsSound.append(mixer.Sound('.\sound\F.mp3'))
            elif i == 'G':
                self.chordsSound.append(mixer.Sound('.\sound\G.mp3'))
            elif i == 'A':
                self.chordsSound.append(mixer.Sound('.\sound\A.mp3'))
            elif i == 'B':
                self.chordsSound.append(mixer.Sound('.\sound\B.mp3'))
        
    def loadImg(self, lsOfChords):
        # load all the image of chords the user wants
        for i in lsOfChords:
            if i == 'C':
                self.chordPic.append(cv2.resize(cv2.imread('.\img\Cmaj.png'),(100,100),interpolation=cv2.INTER_CUBIC))
            elif i =='D':
                self.chordPic.append(cv2.resize(cv2.imread('.\img\Dmaj.png'),(100,100),interpolation=cv2.INTER_CUBIC))
            elif i == 'E':
                self.chordPic.append(cv2.resize(cv2.imread('.\img\Emaj.png'),(100,100),interpolation=cv2.INTER_CUBIC))
            elif i == 'F':
                self.chordPic.append(cv2.resize(cv2.imread('.\img\Fmaj.png'),(100,100),interpolation=cv2.INTER_CUBIC))
            elif i == 'G':
                self.chordPic.append(cv2.resize(cv2.imread('.\img\Gmaj.png'),(100,100),interpolation=cv2.INTER_CUBIC))
            elif i == 'A':
                self.chordPic.append(cv2.resize(cv2.imread('.\img\Amaj.png'),(100,100),interpolation=cv2.INTER_CUBIC))
            elif i == 'B':
                self.chordPic.append(cv2.resize(cv2.imread('.\img\Bmaj.png'),(100,100),interpolation=cv2.INTER_CUBIC))

    def setCamera(self, lsOfChords):
        #Set HSV range for detecting black
        self.blackLower = (0, 0, 0)
        self.blackUpper = (180, 255, 30)

        #Obtain input from camera
        self.camera = cv2.VideoCapture(0)
        self.ret, self.frame = self.camera.read()
        self.H, self.W = self.frame.shape[:2]
        self.setRegion(lsOfChords)
    
    def setRegion(self,lsOfChords):

        while True:
            #Select the current frame
            self.ret, self.frame = self.camera.read()
            self.frame = cv2.flip(self.frame, 1)

            if not(self.ret):
                break
            
            self.createRegion(lsOfChords)        
            self.regions = []
            j = 0
            # setting and positionning the chord's detect region
            for i in range(0,len(self.lsregions),2):
                self.regions.append(np.copy(self.frame[self.lsregions[i][1]:self.lsregions[i+1][1], self.lsregions[i][0]: self.lsregions[i+1][0]]))
                self.frame[self.lsregions[i][1]:self.lsregions[i+1][1],self.lsregions[i][0]:self.lsregions[i+1][0]] = cv2.addWeighted(self.chordPic[j], 1, self.frame[self.lsregions[i][1]:self.lsregions[i+1][1],self.lsregions[i][0]:self.lsregions[i+1][0]], 1, 0)
                j += 1
            for i in range(0,len(lsOfChords)):
                if lsOfChords[i] == 'C':
                    mask = self.detect_in_region(self.regions[i], 'C')
                elif lsOfChords[i] == 'D':
                    mask = self.detect_in_region(self.regions[i], 'D')
                elif lsOfChords[i] == 'E':
                    mask = self.detect_in_region(self.regions[i], 'E')
                elif lsOfChords[i] == 'F':
                    mask = self.detect_in_region(self.regions[i], 'F')
                elif lsOfChords[i] == 'G':
                    mask = self.detect_in_region(self.regions[i], 'G')
                elif lsOfChords[i] == 'A':
                    mask = self.detect_in_region(self.regions[i], 'A')
                elif lsOfChords[i] == 'B':
                    mask = self.detect_in_region(self.regions[i], 'B')


            #Output project title
            cv2.putText(self.frame, 'Viano', (10,30), 2, 1, (20,20,20), 2)
                

            cv2.imshow('Output',self.frame)
            key = cv2.waitKey(1) & 0xFF
            # 'Q' to exit
            if key == ord("q"):
                self.closeCamera()
                break

    def createRegion(self, lsChords):
        self.lsregions = [] 
        padx = 0
        thickness = [100,100]
        self.kernel = np.ones((7,7), np.uint8)
        
        # creating the are of the detect region for a single chord
        for i in lsChords:
            box_center = [np.shape(self.frame)[1] * 2 // 8 + padx, np.shape(self.frame)[0] * 6 // 8]
            box_top = [box_center[0] - thickness[0] // 2, box_center[1] - thickness[1] // 2]
            box_btm = [box_center[0] + thickness[0] // 2, box_center[1] + thickness[1] // 2]
            self.lsregions.append(box_top)
            self.lsregions.append(box_btm)
            padx += 100

        time.sleep(0.01)

    def closeCamera(self):
        self.camera.release()
        cv2.destroyAllWindows()

    def detect_in_region(self, frame, chord):
        #Converting to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        #Creating mask
        mask = cv2.inRange(hsv, self.blackLower, self.blackUpper)

        #Calculating the number of black pixel
        detected = np.sum(mask)
        # Call the funtion to play the drum sounds
        self.play_sound(detected, chord)

        return mask

    def play_sound(self, detect, chord):
        #check if the detected black color is greater than the preset value
        thickness = [100,100]
        play = detect > thickness[0] * thickness[1] * 0.8
        #if it is detected play the corresponding chord sound
        if play and chord == 'C':
            self.chordsSound[0].play()
        elif play and chord == 'D':
            self.chordsSound[1].play()
        elif play and chord == 'E':
            self.chordsSound[2].play
        elif play and chord == 'F':
            self.chordsSound[3].play()
        elif play and chord == 'G':
            self.chordsSound[4].play
        elif play and chord == 'A':
            self.chordsSound[5].play()
        elif play and chord == 'B':
            self.chordsSound[6].play()
        
        time.sleep(0.01)


my_gui = HomePage()

