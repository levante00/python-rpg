from character import *
from Items import *
from Room import Room
import os
from pygame import mixer
from colorama import Fore, Back, Style

def Help():
	print(Fore.CYAN + 'Move: Enter "N", "W", "E", "S" Keys to Move\nShowStatus: Enter "Status" to See Your Current Status\nRoomStatus: Enter "Room" to See Current Room Description\nQuitGame: Enter "Quit"to Leave the Game', Style.RESET_ALL)
	

mixer.init()
mixer.music.load("Music/Spiders_Den.mp3")
mixer.music.set_volume(0.7)
mixer.music.play()

os.system('clear')

print(Fore.RED + '\033[1m' + 'Welcome to Dungeon and Mysteries Adventure Game\n'.center(os.get_terminal_size().columns), Style.RESET_ALL)

print(Fore.YELLOW + 'Create Your Character\n', Style.RESET_ALL)

MC = Hero.CreateHero() #MC = MainCharacter

print(Fore.YELLOW + '\nIf You Want to See the Commands List Enter "Help"\n', Style.RESET_ALL)

print(Fore.YELLOW + 'Enter "Start" to start the adventure\n', Style.RESET_ALL)

res = input()

if res == 'Help':
	Help()
	res = input()

if res == 'Start':
	os.system('clear')
	
	print(Fore.RED + '\033[1m' + 'Welcome to Dungeon and Mysteries Adventure Game\n'.center(os.get_terminal_size().columns), Style.RESET_ALL)
		
	while True:
		insert = input()
		
		if insert == 'Help':
			Help()
		elif insert == 'N' or insert == 'W' or insert == 'E' or insert == 'S':
			MC.Move(insert)
		elif insert == 'Room':
			print("PRIVWEFSD") 
		elif insert == 'Quit':	
			break
		



