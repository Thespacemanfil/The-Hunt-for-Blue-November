import os, sys, pygame as pg
from main_loop import initialise
from colorama import Fore, Back, Style
#print(Fore.RED + 'some red text')
#print(Back.GREEN + 'and with a green background')
#print(Style.DIM + 'and in dim text')
#print(Style.RESET_ALL)
#print('back to normal now')
# Get the directory where the script is running from
current_path = sys.path[0]
# Change the working directory to the directory of the script
os.chdir(current_path)

print(Fore.BLUE + open("Title.txt").read())

pg.mixer.Sound('das_boot.mp3').play()

def menu():
    choice = ""
    while choice != "exit":
        choice = input("\nControls, start, exit\n").lower()
        if choice == "controls": print("\n" + open("Controls.txt").read())
        elif choice == "start": initialise()
    sys.exit()

menu()
