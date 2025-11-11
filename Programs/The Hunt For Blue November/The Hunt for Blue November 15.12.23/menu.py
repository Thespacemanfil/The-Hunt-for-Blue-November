import random, sys, time, pygame as pg
from main_loop import initialise
from colorama import Fore, Back, Style

pg.mixer.Sound('das_boot.mp3').play()

def text(message):
    for char in message:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(random.randint(1,325)/10000)

def menu():
    text(Fore.BLUE + open("Title.txt").read())
    choice = ""
    while choice != "exit":
        choice = input("\nControls, start, exit\n").lower()
        if choice == "controls": text(open("Controls.txt").read())
        elif choice == "start": initialise()
    sys.exit()

menu()
