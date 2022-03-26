import random
import Enemy
import Items
import random
from colorama import Fore, Back, Style
import curses
import time

class Room:
	def __init__(self, Name: str, GlobalPositionX: int, GlobalPositionY: int, Interior: list = [], Monsters: list = [], Items: list = []):
		self.Name = Name
		self.GlobalPositionX = GlobalPositionX
		self.GlobalPositionY = GlobalPositionY
		self.Interior = [[0 for i in range(10)] for j in range(10)]
		self.Monsters = Monsters
		self.Items = Items

	def ShowDescription(self):
		print(f'Name: {self.Name}\nPosition: {(self.GlobalPositionX, self.GlobalPositionY)}')
		
		print('Monsters: ', end = "")
		for Monster in self.Monsters:
			print(Monster.Name, end = ' ')
		if self.Monsters:
			print('')
		else:
			print('There Is No Monster in the Room')
		
		print('Items: ', end = "")
		for Item in self.Items:
			print(Item.Name, end = ' ')
		if self.Items:
			print('')
		else:
			print('There is no Items in the Room')
		
	def GenerateMonsters(self):
		self.Monsters = random.sample(Enemy.Bestiary, random.randint(0, len(Enemy.Bestiary)))
	
	def GenerateItems(self):
		self.Items = random.sample(Items.Stock, random.randint(0, len(Items.Stock)))
	
	def LocateMonsters(self):	
		for Monster in self.Monsters:
			while True:
				i = random.randint(0, 9)
				j = random.randint(0, 9)
				if self.Interior[i][j] == 0: 
					self.Interior[i][j] = Monster
					break 
		
	def LocateItems(self):
		for Item in self.Items:	
			while True:
				i = random.randint(0, 9)
				j = random.randint(0, 9)
				if self.Interior[i][j] == 0: 
					self.Interior[i][j] = Item
					break 
	
	def CreateInterior(self):
		self.GenerateMonsters()
		self.GenerateItems()
		self.LocateMonsters()
		self.LocateItems()


	def ShowInterior(self):				
		for i in range(0, 10):
				for j in range(0, 10):
					if self.Interior[i][j] != 0:
						print(self.Interior[i][j].Name, end = ' ')
					else:
						print(self.Interior[i][j], end = ' ')
				print('')	


	def CreateMap():
		Room1 = Room('Starting Room', 0, 0)
		Names = random.sample(open('Data/RoomNames.txt').read().split('\n'), 25)
		Map = []

#		CoordinateX = random.sample([-2, -1, 0, 1, 2], 5)
#		CoordinateY = random.sample([-2, -1, 0, 1, 2], 5)
		CoordinateX = [-2, -1, 0, 1, 2]
		CoordinateY = [-2, -1, 0, 1, 2]
		Coordinates = []
		
		for i in CoordinateX:
			for j in CoordinateY:
				Coordinates.append([i, j])
		
		for i in range(25):
			Room_res = Room(Names[i], Coordinates[i][0], Coordinates[i][1])
			Room_res.CreateInterior()
			Map.append(Room_res)
		
		StartRoomIndex = int(len(Map)/2)
		Map[StartRoomIndex] = Room1
			
		return Map

		

	def ShowMap(self, Map):
		RowLen = int(len(Map) ** (1/2))
		for k in range(0, len(Map), RowLen):
			for i in range(-1, 11):
				for e in range(RowLen):
					for j in range(-1, 11):
						if ((j == -1 and i != -1) or (j == 10 and i != -1)):
							print(Fore.MAGENTA + "|", Style.RESET_ALL, end = "")
						elif i == -1 or i == 10:
							print(Fore.MAGENTA + "_", Style.RESET_ALL, end = "")
						elif isinstance(Map[k + e].Interior[i][j], Enemy.Monster):
							print(Fore.RED + "1", Style.RESET_ALL, end = "")
						elif isinstance(Map[k + e].Interior[i][j], Items.Item):
							print(Fore.BLUE + "1", Style.RESET_ALL, end = "")
						else:
							print("0", end = " ")
				print("")
			
"""
Map = Room.CreateMap()

for Room in Map:
#	print(Room.GlobalPositionX, Room.GlobalPositionY)
	Room.ShowDescription()
	Room.ShowInterior()

Room.ShowMap(Map)

"""


