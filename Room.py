import random
import character
import Items



class Room:
	def __init__(self, Name: str, GlobalPositionX: int, GlobalPositionY: int, Description: str, Interior: list, Monsters: list = character.Bestiary, Items: list = character.Objects):
		self.Name = Name
		self.GlobalPositionX = GlobalPositionX
		self.GlobalPositionY = GlobalPositionY
		self.Description = Description
		self.Interior = [[0 for i in range(10)] for j in range(10)]
		self.Monsters = random.sample(Monsters, random.randint(0, len(Monsters)))
		self.Items = random.sample(Items, random.randint(0, len(Items)))

		
	def ShowDescription(self):
		print(f'Name:{self.Name}\nPosition:{(self.GlobalPositionX, self.GlobalPositionY)}\nDescription: {self.Description}')
		for Monster in self.Monsters:
			print(Monster.Name, end = ' ')
		print('')
		for Item in self.Items:
			print(Item.Name, end = ' ')
		print('')
		for i in range(10):
			for j in range(10):
				if self.Interior[i][j] != 0:
					print(self.Interior[i][j].Name, end = '      ')
				else:
					print(self.Interior[i][j], end = '      ')
	
				
			print('')	

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
	
#Room1 = Room('Pillar', 0, 0, 'Big room with very strange looking walls', 0)
#Room1.LocateMonsters()
#Room1.LocateItems()
#Room1.ShowDescription()

