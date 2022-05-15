import random
import src.Enemy as Enemy
import src.Items as Items
import random
from colorama import Fore, Back, Style
import curses	
import time


class Room:	
	def __init__(self, name: str, global_position_x: int,
			 global_position_y: int, music: str, interior: list = [],
			 monsters: list = [], items: list = [], size: int = 9) -> None:
		self.name = name
		self.global_position_x = global_position_x  # X Coordinate Relative to Other Rooms
		self.global_position_y = global_position_y  # Y Coordintae Relative to Other Rooms
		self.music = music
		self.interior = [[0 for i in range(size)] for j in range(size)]
		self.monsters = monsters
		self.items = items
		self.size = size

	def show_description(self) -> None:
		TEXT_1 = '\nCurrent Room Description:'
		TEXT_2 = (f'Name: {self.name}\nPosition: {(self.global_position_x, self.global_position_y)}')
		print(Fore.YELLOW + TEXT_1, Style.RESET_ALL)
		print(Fore.BLUE + TEXT_2)
		
		print('Monsters: ', end = "")
		for monster in self.monsters:
			print(monster.name, end = ' ')
		if self.monsters:
			print('')
		else:
			print('There is no Monster in the Room')
		
		print('Items: ', end = "")
		for item in self.items:
			print(item.name, end = ' ')
		if self.items:
			print('\n', Style.RESET_ALL)
		else:
			print('There is no Items in the Room\n', Style.RESET_ALL)
		
	def generate_monsters(self, diff: str) -> None:
		if diff == 'E':
			monster_number = self.size // 2
			monster_weights = [6, 4, 7, 0, 5, 1, 2, 2, 3]
		elif diff == 'M':
			monster_number = self.size
			monster_weights = [5, 3, 6, 1, 4, 2, 3, 3, 3]
		elif diff == 'H':
			monster_number = self.size * 2
			monster_weights = [4, 2, 4, 2, 3, 3, 4, 4, 2]

		self.monsters = random.choices(
							Enemy.bestiary, 
							weights = monster_weights, 
							k = random.randint(2, monster_number))
	
	def generate_items(self) -> None:
		self.items = random.sample(Items.stock, random.randint(0, len(Items.stock)))
	
	def locate_monsters(self) -> None:	
		for monster in self.monsters:
			while True:
				i = random.randint(0, self.size - 1)
				j = random.randint(0, self.size - 1)
				if self.interior[i][j] == 0: 
					self.interior[i][j] = monster
					break 
		
	def locate_items(self) -> None:
		for item in self.items:	
			while True:
				i = random.randint(0, self.size - 1)
				j = random.randint(0, self.size - 1)
				if self.interior[i][j] == 0: 
					self.interior[i][j] = item
					break 
	
	def create_interior(self, diff: str) -> None:
		self.generate_monsters(diff)
		self.generate_items()
		self.locate_monsters()
		self.locate_items()

	def show_interior(self, room_position_x: int, room_position_y: int) -> None:	
		for i in range(self.size):
				for j in range(self.size):
					if isinstance(self.interior[i][j], Enemy.Monster):
						print(Fore.RED + f'{self.interior[i][j].name[0]}', 
							Style.RESET_ALL, end = '')
					elif isinstance(self.interior[i][j], Items.Item):	
						print(Fore.BLUE + f'{self.interior[i][j].name[0]}', 
							Style.RESET_ALL, end = '')
					elif i == room_position_y and j == room_position_x:
						print(Back.GREEN + f'M', Style.RESET_ALL, end = '')
					else:
						print(self.interior[i][j], end = ' ')
				print('')	
		print('')
	
	@classmethod
	def create_map(cls, map_size: int, difficulty: str) -> list: 	
		room1 = Room('Starting Room', 0, 0, "Music/Start/Survivors_Bivouac.mp3")
		file1 = open('Data/RoomNames.txt', "r")
		names = random.sample(file1.read().splitlines(), map_size)
		file1.close()
		file2 = open('Data/RoomMusic.txt', "r")
		music_list = random.choices(file2.read().splitlines(), k = map_size)
		file2.close()
		file3 = open('Data/BattleMusic.txt', "r") 
		battle_music = random.choices(file3.read().splitlines(), k = 1)
		file3.close()
		Map = []
		left_coord = int(-(map_size ** (1/2))/2)
		right_coord = int((map_size ** (1/2))/2) + 1

		coordinates_x = [i for i in range(left_coord, right_coord)]
		coordinates_y = [-i for i in range(left_coord, right_coord)]
		coordinates = []
		
		for i in coordinates_y:
			for j in coordinates_x:
				coordinates.append([j, i])

		for i in range(map_size):
			room_res = Room(
				names[i], coordinates[i][0], coordinates[i][1], 
				'Music/Rooms/'  + music_list[i])

			room_res.create_interior(difficulty)
			Map.append(room_res)
		
		start_room_index = int(len(Map)/2)
		Map[start_room_index] = room1
			
		return Map

	def show_map(
			Map: list, global_position_x: int, global_position_y: int, 
			room_position_x: int, room_position_y: int) -> None:
		if len(Map) == 9:
			size = Map[0].size
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

			row_len = int(len(Map) ** (1/2))
			for k in range(0, len(Map), row_len):
				for i in range(-1, size + 1):
					for e in range(row_len):
						for j in range(-1, size + 1):
							if ((j == -1 and i != -1) or (j == size and i != -1)):
								mypad.addstr("| ", MAGENDA)
							elif i == -1 or i == size:
								mypad.addstr("_ ", MAGENDA)
							elif isinstance(Map[k + e].interior[i][j], Enemy.Monster):
								mypad.addstr("1 ", RED)
							elif isinstance(Map[k + e].interior[i][j], Items.Item):
								mypad.addstr("1 ", BLUE)
							elif (Map[k + e].global_position_x == global_position_x and 
								  Map[k + e].global_position_y == global_position_y and 
								  i == room_position_y and j == room_position_x): 
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
			size = Map[0].size
			row_len = int(len(Map) ** (1/2))
			for k in range(0, len(Map), row_len):
				for i in range(-1, size + 1):
					for e in range(row_len):
						for j in range(-1, size + 1):
							if ((j == -1 and i != -1) or (j == size and i != -1)):
								print(Fore.MAGENTA + "|", Style.RESET_ALL, end = "")
							elif i == -1 or i == size:
								print(Fore.MAGENTA + "_", Style.RESET_ALL, end = "")
							elif isinstance(Map[k + e].interior[i][j], Enemy.Monster):
								print(Fore.RED + "1", Style.RESET_ALL, end = "")
							elif isinstance(Map[k + e].interior[i][j], Items.Item):
								print(Fore.BLUE + "1", Style.RESET_ALL, end = "")
							elif (Map[k + e].global_position_x == global_position_x and
							 	  Map[k + e].global_position_y == global_position_y and 
								  i == room_position_y and j == room_position_x): 
								print(Back.GREEN + 'M', Style.RESET_ALL, end = "")
							else:
								print("0", end = " ")
					print("")
			print('\n')
		

room1 = Room('Starting Room', 0, 0, "Music/Start/Survivors_Bivouac.mp3")

