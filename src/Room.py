import random
import src.Enemy as Enemy
import src.Items as Items
import random
from colorama import Fore, Back, Style
import curses	
import time


class Room:
	
	def __init__(self, Name: str, GlobalPositionX: int, GlobalPositionY: int, Music: str, Interior: list = [], Monsters: list = [], Items: list = [], Size: int = 9):
		self.Name = Name
		self.GlobalPositionX = GlobalPositionX  # X Coordinate Relative to Other Rooms
		self.GlobalPositionY = GlobalPositionY  # Y Coordintae Relative to Other Rooms
		self.Music = Music
		self.Interior = [[0 for i in range(Size)] for j in range(Size)]
		self.Monsters = Monsters
		self.Items = Items
		self.Size = Size

	def ShowDescription(self):
		print(Fore.YELLOW + '\nCurrent Room Description:', Style.RESET_ALL)
		print(Fore.BLUE + f'Name: {self.Name}\nPosition: {(self.GlobalPositionX, self.GlobalPositionY)}')
		
		print('Monsters: ', end = "")
		for Monster in self.Monsters:
			print(Monster.Name, end = ' ')
		if self.Monsters:
			print('')
		else:
			print('There is no Monster in the Room')
		
		print('Items: ', end = "")
		for Item in self.Items:
			print(Item.Name, end = ' ')
		if self.Items:
			print('\n', Style.RESET_ALL)
		else:
			print('There is no Items in the Room\n', Style.RESET_ALL)
		
	def GenerateMonsters(self):
		self.Monsters = random.choices(Enemy.Bestiary, weights = [6, 4, 7, 1, 5, 2, 4, 4, 5], k = random.randint(2, self.Size))
	
	def GenerateItems(self):
		self.Items = random.sample(Items.Stock, random.randint(0, len(Items.Stock)))
	
	def LocateMonsters(self):	
		for Monster in self.Monsters:
			while True:
				i = random.randint(0, self.Size - 1)
				j = random.randint(0, self.Size - 1)
				if self.Interior[i][j] == 0: 
					self.Interior[i][j] = Monster
					break 
		
	def LocateItems(self):
		for Item in self.Items:	
			while True:
				i = random.randint(0, self.Size - 1)
				j = random.randint(0, self.Size - 1)
				if self.Interior[i][j] == 0: 
					self.Interior[i][j] = Item
					break 
	
	def CreateInterior(self):
		self.GenerateMonsters()
		self.GenerateItems()
		self.LocateMonsters()
		self.LocateItems()

	def ShowInterior(self, RoomPositionX: int, RoomPositionY: int):	
		for i in range(self.Size):
				for j in range(self.Size):
					if isinstance(self.Interior[i][j], Enemy.Monster):
						print(Fore.RED + f'{self.Interior[i][j].Name[0]}', Style.RESET_ALL, end = '')
					elif isinstance(self.Interior[i][j], Items.Item):	
						print(Fore.BLUE + f'{self.Interior[i][j].Name[0]}', Style.RESET_ALL, end = '')
					elif i == RoomPositionY and j == RoomPositionX:
						print(Back.GREEN + f'M', Style.RESET_ALL, end = '')
					else:
						print(self.Interior[i][j], end = ' ')
				print('')	
		print('')
	
	def CreateMap():
		RoomNumber = 81  # Has to be Square of Odd Number Bigger Then 1
		Room1 = Room('Starting Room', 0, 0, "Music/Start/Survivors_Bivouac.mp3")
		file1 = open('Data/RoomNames.txt', "r")
		Names = random.sample(file1.read().splitlines(), RoomNumber)
		file1.close()
		file2 = open('Data/RoomMusic.txt', "r")
		MusicList = random.choices(file2.read().splitlines(), k = RoomNumber)
		file2.close()
		file3 = open('Data/BattleMusic.txt', "r") 
		BattleMusic = random.choices(file3.read().splitlines(), k = 1)
		file3.close()
		Map = []
		CoordinateX = [i for i in range(int(-(RoomNumber ** (1/2))/2), (int((RoomNumber ** (1/2))/2) + 1))]
		CoordinateY = [-i for i in range(int(-(RoomNumber ** (1/2))/2), (int((RoomNumber ** (1/2))/2) + 1))]
		Coordinates = []
		
		for i in CoordinateY:
			for j in CoordinateX:
				Coordinates.append([j, i])

		for i in range(RoomNumber):
			Room_res = Room(Names[i], Coordinates[i][0], Coordinates[i][1], 'Music/Rooms/'  + MusicList[i])
			Room_res.CreateInterior()
			Map.append(Room_res)
		
		StartRoomIndex = int(len(Map)/2)
		Map[StartRoomIndex] = Room1
			
		return Map

	def ShowMap(Map: list, GlobalPositionX: int, GlobalPositionY: int, RoomPositionX: int, RoomPositionY: int):
		if len(Map) == 9:
			Size = Map[0].Size
			stdscr = curses.initscr()
			curses.noecho()
			stdscr.keypad(True)

			curses.start_color()	
			curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
			curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
			curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)
			curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_GREEN)
			RED = curses.color_pair(1)
			BLUE = curses.color_pair(2)
			MAGENDA = curses.color_pair(3)
			BACK_GREEN = curses.color_pair(4)
			curses.resizeterm(300, 300)
	
			mypad = curses.newpad(200, 200)
			mypad.clear()
			mypad.refresh(0, 0, 1, 62, 100, 150)

			RowLen = int(len(Map) ** (1/2))
			for k in range(0, len(Map), RowLen):
				for i in range(-1, Size + 1):
					for e in range(RowLen):
						for j in range(-1, Size + 1):
							if ((j == -1 and i != -1) or (j == Size and i != -1)):
								mypad.addstr("| ", MAGENDA)
							elif i == -1 or i == Size:
								mypad.addstr("_ ", MAGENDA)
							elif isinstance(Map[k + e].Interior[i][j], Enemy.Monster):
								mypad.addstr("1 ", RED)
							elif isinstance(Map[k + e].Interior[i][j], Items.Item):
								mypad.addstr("1 ", BLUE)
							elif Map[k + e].GlobalPositionX == GlobalPositionX and Map[k + e].GlobalPositionY == GlobalPositionY and i == RoomPositionY and j == RoomPositionX: 
								mypad.addstr('M ', BACK_GREEN)
							else:
								mypad.addstr("0 ")
					mypad.addstr("\n")

			mypad.addstr(37, 0, "Press Any Key to Close...")
			mypad.refresh(0, 0, 1, 62, 100, 150)
			
			stdscr.getkey(38, 87)
			stdscr.getkey(38, 87)
			stdscr.getkey(38, 87)
#			stdscr.clear()
#			stdscr.refresh()		
			stdscr.keypad(False)
			curses.endwin()
			print("")

		elif len(Map) >= 25:
			Size = Map[0].Size
			RowLen = int(len(Map) ** (1/2))
			for k in range(0, len(Map), RowLen):
				for i in range(-1, Size + 1):
					for e in range(RowLen):
						for j in range(-1, Size + 1):
							if ((j == -1 and i != -1) or (j == Size and i != -1)):
								print(Fore.MAGENTA + "|", Style.RESET_ALL, end = "")
							elif i == -1 or i == Size:
								print(Fore.MAGENTA + "_", Style.RESET_ALL, end = "")
							elif isinstance(Map[k + e].Interior[i][j], Enemy.Monster):
								print(Fore.RED + "1", Style.RESET_ALL, end = "")
							elif isinstance(Map[k + e].Interior[i][j], Items.Item):
								print(Fore.BLUE + "1", Style.RESET_ALL, end = "")
							elif Map[k + e].GlobalPositionX == GlobalPositionX and Map[k + e].GlobalPositionY == GlobalPositionY and i == RoomPositionY and j == RoomPositionX: 
								print(Back.GREEN + 'M', Style.RESET_ALL, end = "")
							else:
								print("0", end = " ")
					print("")
			print('\n')
		

Room1 = Room('Starting Room', 0, 0, "Music/Start/Survivors_Bivouac.mp3")

