# virtual-piano

This is a python project that is inspired by **Navendu-Pottekkat(2020) virtual-drums (https://github.com/navendu-pottekkat/virtual-drums)**, however I modified the projec, turing it into a program that allows the user to play a number of piano chords virtually.

## Requirements For Initial Setup:
- Install openCV, Tkinter, Numpy, and Pygame libraries



## How it works:
When this program is run it will display a window that allows the user to enter an integer for how many chords.

![The selection page](https://user-images.githubusercontent.com/64215294/229029747-89bae02a-3a96-4d80-8a9f-7cd794508da4.jpg)

For now the maximum number of chords possible to display on a screen is 5. After the user choose what chords that they need. The user can press the "done" button, then the program will pop up a small windo and turn on the camera to start a live recoding. The user can see the recoding through that window as well as the region of all the chords that the user has choosen. 

![The camera page](https://user-images.githubusercontent.com/64215294/229029795-8d6daef7-c916-4086-8ab0-dc88688b9207.jpg)

In this program if a black color object enters a region associated to a chord, then the sound of that chord will be played. To exit the recording press "Q".
