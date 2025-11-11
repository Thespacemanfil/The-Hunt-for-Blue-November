import os, sys
from main_loop import initialise

print(open("Title.txt").read())

def menu():
    if input("Press Enter to continue...\n") == "":
        initialise()

menu()
