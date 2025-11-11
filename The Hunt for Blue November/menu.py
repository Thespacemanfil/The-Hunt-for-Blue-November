import sys, pygame as pg
from main_loop import initialise
from colorama import Fore

print(Fore.BLUE + open("Title.txt").read())

pg.mixer.Sound('sound/das_boot.mp3').play()
def menu():
    choice = ""
    while choice != "exit":
        choice = input("\nControls, start, exit\n").lower()
        if choice == "controls": print("\n" + open("Controls.txt").read())
        elif choice == "start": initialise()
        else: menu()
    sys.exit()

menu()
