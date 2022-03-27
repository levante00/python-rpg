from character import *
from Items import *
from Room import Room
import os
from pygame import mixer
from colorama import Fore, Back, Style

def Help():
	print(Fore.YELLOW + 'Move: Enter "N", "W", "E", "S" Keys to Move\nShowStatus: Enter "Status" to See Your Current Status\nRoomDescription: Enter "Room" to See Current Room Description\nDungeonMap: Enter "Map" to See All Dungeon Rooms\nWeaponStatus: Enter "Weapon" to See Your Weapon Characteristics\nArmorStatus: Enter "Armor" to See Your Armor Characteristics\nQuitGame: Enter "Quit"to Leave the Game', Style.RESET_ALL)
	print(Fore.YELLOW + 'After Calling "Map" Command You Will See Blocks With Cells And Each of Theme Will Contain 0 or Red 1 or Blue 1, Where Cells With 0 are Empty, Cells With Red 1 Contain Monster and Cells With Blue 1 Contain Armor or Weapon\n', Style.RESET_ALL)	

mixer.init()
mixer.music.load("Music/Spiders_Den.mp3")
mixer.music.set_volume(0.7)
mixer.music.play()

os.system('clear')

print(Fore.RED + '\033[1m' + 'Welcome to Dungeon and Mysteries Adventure Game\n'.center(os.get_terminal_size().columns), Style.RESET_ALL)

print(Fore.YELLOW + 'Create Your Character\n', Style.RESET_ALL)

MC = Hero.CreateHero() #MC = MainCharacter

print(Fore.YELLOW + '\nIf You Want to See the Commands List Enter "Help"\n', Style.RESET_ALL)

print(Fore.YELLOW + 'Enter "Start" to Start the Adventure\n', Style.RESET_ALL)

res = input()
while res == 'Help' or res != 'Start':
	if res != 'Start' and res != 'Help':
		print(Fore.RED + "Wrong Input, Try Again", Style.RESET_ALL)
		res = input()
	elif res == 'Help':
		Help()
		res = input()


os.system('clear')
print(Fore.RED + '\033[1m' + 'Welcome to Dungeon and Mysteries Adventure Game\n'.center(os.get_terminal_size().columns), Style.RESET_ALL)

Map = Room.CreateMap()	
while True:
	insert = input()
	if insert == 'Help':
		Help()
	elif insert == 'N' or insert == 'W' or insert == 'E' or insert == 'S':
		MC.Move(insert, Map)
	elif insert == 'Status':
		MC.ShowStatus()
	elif insert == 'Room':
		MC.CurrentRoom.ShowDescription()
	elif insert == 'Map':
		Room.ShowMap(Map)
	elif insert == 'Weapon':
		MC.Weapon.ShowStatus()
	elif insert == 'Armor':
		MC.Armor.ShowStatus()
	elif insert == 'Quit':	
		break
	else:
		print(Fore.RED + 'Wrong Input, Choose Command From Help', Style.RESET_ALL)


