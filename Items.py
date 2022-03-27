class Item:

	def __init__(self, Name: str, Description: str):
		self.Name = Name
		self.Description = Description

	def ShowDescription(self):
		print(f'Name: {self.Name}\nDescription: {self.Description}')


class Armor(Item):

	def __init__(self, Name: str, Description: str, ProfessionRequired: str, LevelRequired: int, Agility: int, Defense: int, Intelligence: int):
		super().__init__(Name, Description)
		self.ProfessionRequired = ProfessionRequired
		self.LevelRequired = LevelRequired
		self.Agility = Agility
		self.Defense = Defense
		self.Intelligence = Intelligence

	def ShowStatus(self):
		print(f'Name: {self.Name}\nProfession Required: {self.ProfessionRequired}\nLevel Required: {self.LevelRequired}\nAgility: {self.Agility}\nDefense: {self.Defense}\nIntelligence: {self.Intelligence}')

	def ShowDescription(self):
		print(self.Description)


class Weapon(Item):

	def __init__(self, Name: str, Description: str, ProfessionRequired: str, LevelRequired: int, Attack: int, Agility: int, Intelligence: int):
		super().__init__(Name, Description)
		self.ProfessionRequired = ProfessionRequired
		self.LevelRequired = LevelRequired
		self.Attack = Attack
		self.Agility = Agility
		self.Intelligence = Intelligence

	def ShowStatus(self):
		print(f'Name: {self.Name}\nProfession Required: {self.ProfessionRequired}\nLevel Required: {self.LevelRequired}\nAttack: {self.Attack}\nAgility: {self.Agility}\nIntelligence: {self.Intelligence}')

	def ShowDescription(self):
		print(self.Description)


chainmail = Armor('ChainMail', 'the protective material that knights wear as part of a suit of armor', 'Knight', 1, 4, 6, 1)
ironarmor = Armor('IronArmor', 'Regular rookie armor', 'Knight', 2, 8, 10, 1)
knife = Weapon('Knife', 'Regular kitchen knife', 'Knight', 1, 10, 15, 0)
sword = Weapon('Sword', '100 inche long swod that was owned by old merchante', 'Knight', 1, 20, 30, 5)
Arms = Weapon('Arms', '0', '0', 0, 0, 0, 0)
Shirt = Armor('Shirt', '0', '0', 0, 0, 0, 0)
Stock = [ironarmor, knife, chainmail, sword]



'''
Table = Item('Table', 'Oak Table, looks like it was destroyed by some creature')
Table.ShowDescription()
print("")

chainmail = Armor('ChainMail', 'the protective material that knights wear as part of a suit of armor', 'Knight', 30, 20, 100, 10)
chainmail.ShowStatus()
chainmail.ShowDescription()
print("")

knife = Weapon('Knife', 'Regular kitchen knife', 'None', 1, 10, 15, 0)
knife.ShowStatus()
knife.ShowDescription()
print("")
'''
