from colorama import Fore, Back, Style

class Item:

	def __init__(self, Name: str, Description: str):
		self.Name = Name
		self.Description = Description

	def ShowDescription(self):
		print(f'Name: {self.Name}\nDescription: {self.Description}')
	
	def ShowStock():
		for Item in Stock:
			Item.ShowStatus()


class Armor(Item):

	def __init__(self, Name: str, Description: str, ProfessionRequired: str, LevelRequired: int, Agility: int, Defense: int, Intelligence: int):
		super().__init__(Name, Description)
		self.ProfessionRequired = ProfessionRequired
		self.LevelRequired = LevelRequired
		self.Agility = Agility
		self.Defense = Defense
		self.Intelligence = Intelligence

	def ShowStatus(self):
		print(Fore.BLUE + f'Name: {self.Name}\nProfession Required: {self.ProfessionRequired}\nLevel Required: {self.LevelRequired}\nAgility: {self.Agility}\nDefense: {self.Defense}\nIntelligence: {self.Intelligence}\n', Style.RESET_ALL)


class Weapon(Item):

	def __init__(self, Name: str, Description: str, ProfessionRequired: str, LevelRequired: int, Attack: int, Agility: int, Intelligence: int):
		super().__init__(Name, Description)
		self.ProfessionRequired = ProfessionRequired
		self.LevelRequired = LevelRequired
		self.Attack = Attack
		self.Agility = Agility
		self.Intelligence = Intelligence

	def ShowStatus(self):
		print(Fore.BLUE + f'Name: {self.Name}\nProfession Required: {self.ProfessionRequired}\nLevel Required: {self.LevelRequired}\nAttack: {self.Attack}\nAgility: {self.Agility}\nIntelligence: {self.Intelligence}\n', Style.RESET_ALL)
	


chainmail = Armor('ChainMail', 'the protective material that knights wear as part of a suit of armor', 'Knight', 1, 4, 6, 1)
ironarmor = Armor('IronArmor', 'Regular rookie armor', 'Knight', 2, 8, 10, 1)
knife = Weapon('Knife', 'Regular kitchen knife', 'Knight', 1, 10, 15, 0)
sword = Weapon('Sword', '100 inche long swod that was owned by old merchante', 'Knight', 1, 20, 30, 5)
Arms = Weapon('Arms', '0', '0', 0, 0, 0, 0)
Shirt = Armor('Shirt', '0', '0', 0, 0, 0, 0)
Stock = [ironarmor, knife, chainmail, sword]
