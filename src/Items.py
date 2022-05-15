from colorama import Fore, Back, Style


class Item:
	"""The Game whole items class"""
	def __init__(self, name: str, description: str) -> None:
		self.name = name
		self.description = description

	def show_description(self) -> None:
		"""Prints Item objects attributes"""
		print(f'Name: {self.name}\nDescription: {self.description}')
	
	def show_stock() -> None:
		"""Prints all the Items list with their descriptions"""
		for item in stock:
			item.show_status()


class Armor(Item):
	"""SubClass of Items but with special attributes for defence"""
	def __init__(
			self, name: str, description: str, 
			profession_required: str, level_required: int, 
			agility: int, defense: int, intelligence: int) -> None:
		super().__init__(name, description)
		self.profession_required = profession_required
		self.level_required = level_required
		self.agility = agility
		self.defense = defense
		self.intelligence = intelligence

	def show_status(self) -> None:
		"""Prints Armor attributes"""
		ARMOR1_TEXT =  (f'Name: {self.name}\nProfession Required: {self.profession_required}\n'
					   f'Level Required: {self.level_required}\nAgility: {self.agility}\n'
					   f'Defense: {self.defense}\nIntelligence: {self.intelligence}\n')
		print(Fore.BLUE + ARMOR1_TEXT, Style.RESET_ALL)


class Weapon(Item):
	"""SubClass of Items but with special attributes for attack"""
	def __init__(
			self, name: str, description: str, profession_required: str, 
			level_required: int, attack: int, agility: int, intelligence: int) -> None:
		super().__init__(name, description)
		self.profession_required = profession_required
		self.level_required = level_required
		self.attack = attack
		self.agility = agility
		self.intelligence = intelligence

	def show_status(self) -> None:
		"""Prints Weapon Attributes"""
		WEAPON_TEXT = (f'Name: {self.name}\nProfession Required: {self.profession_required}\n'
					   f'Level Required: {self.level_required}\nAttack: {self.attack}\n'
					   f'Agility: {self.agility}\nIntelligence: {self.intelligence}\n')
		print(Fore.BLUE + WEAPON_TEXT, Style.RESET_ALL)
	


chainmail = Armor('ChainMail', 'the protective material that knights wear as part of a suit of armor', 'Knight', 1, 4, 6, 1)
ironarmor = Armor('IronArmor', 'Regular rookie armor', 'Knight', 2, 8, 10, 1)
knife = Weapon('Knife', 'Regular kitchen knife', 'Knight', 1, 10, 15, 0)
sword = Weapon('Sword', '100 inche long swod that was owned by old merchante', 'Knight', 1, 20, 30, 5)
arms = Weapon('Arms', '0', 'None', 0, 0, 0, 0)
shirt = Armor('Shirt', '0', 'None', 0, 0, 0, 0)
stock = [ironarmor, knife, chainmail, sword]
