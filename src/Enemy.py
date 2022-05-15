import random
from colorama import Fore, Back, Style

class MonsterDeath(Exception):
	def __init__(self, name: str = "None", exp: int = 0) -> None:
		self.name = name
		self.exp = exp
		self.message = f'{self.name} Died, You get {self.exp} Experience'

	def __str__(self) -> str:
		return 'Heores dealed damage exceeded Monsters health'



class Monster():
	"""Class used for creating Monsters to locate in Dangeon"""
	def __init__(
		self, name: str, description: str, level: int, 
		health: int, attack: int, agility: int, defense: int) -> None:

		self.name = name
		self.description = description
		self.level = level
		self.health = health
		self.attack = attack
		self.agility = agility
		self.defense = defense

	def show_status(self) -> None:
		"""Prints Monsters all attributes"""
		TEXT = (f'Name: {self.name}\nLevel: {self.level}\nHealth: {self.health}\n'
				f'Attack: {self.attack}\nAgility: {self.agility}\nDefence: {self.defense}') 
		
		print(Fore.BLUE + TEXT, Style.RESET_ALL)

	def show_description(self) -> None:
		print(self.description)

	def show_bestiary() -> None:
		"""Print all the Monsters list in the game with
		their characteristics and descriptions"""
		print(Fore.YELLOW + '\nMonster List:', Style.RESET_ALL)
		for monster in bestiary:
			monster.show_status()
			monster.show_description()
			print('')

	def gain_damage(self, enemy: "Hero", damage: int) -> None:
		"""Based on Heroes damage lowers Monsters HP"""
		self.health -= damage
		gain_exp = 5 * 2**(self.level)  # Its the Formula of ExpLimit Series
		if self.health <= 0:
			enemy.attribute_increase(0, 0, 0, 0, 0, gain_exp)
			raise MonsterDeath(self.name, gain_exp)

	def deal_damage(self, enemy: "Hero") -> None:
		"""Used to lower Heroes HP based on Monster Attack and Hero Defence.
		Also on Hero can evade the attack if his agility is high"""
		if random.random() >= ((enemy.agility/100)*0.5):  # Evasion Chance Depending on Agility     
			damage = abs((random.randint(0, self.attack + 1)) - (enemy.defense%10))  
			print(f'You Get a Direct Hit and Received {damage} Damage')	 
			enemy.attribute_decrease(damage, 0, 0, 0, 0)
		else:
			print('You Dodged the Attack')


Goblin = Monster('Goblin', 'Goblins are small, weak humanoids with green skin and heigth beetween 3 and 3.5 feet', 5, 10, 3, 10, 2)
Orc = Monster('Orc', 'Orcs are brutal, violent humanoids with greyish or green skin and animalistic features', 20, 40, 12, 6, 10)
Slime = Monster('Slime', 'Slimes are gelatinous creatures that can come in many different colors and sizes, the most common appearance is green and about knee height', 7, 15, 5, 5, 3)
Giant = Monster('Giant', 'Giants are an extraordinarily large humanoid creatures, often with eldritch powers', 45, 150, 30, 3, 25)
Skeleton = Monster('Skeleton', 'Skeletons are the animated skeletal remains of once-living creatures, used as disposable troops by necromancers', 10, 20, 7, 6, 5)
Vampire = Monster('Vampire', 'Vampires are undead, nocturnal creatures that subsist on blood, they have superhuman powers and are sometimes able to shape-shift', 30, 100, 25, 30, 20)
Ghoul = Monster('Ghoul', 'Ghouls are carrion eating undead creatures that dwell in graveyards and other lonely places', 18, 30, 10, 15, 10)
Mummy = Monster('Mummy', 'Mummies are lumbering undead corpses wrapped in bandages, they are very resiliant to physical damage', 16, 35, 8, 5, 15)
Bear = Monster('Bear', 'Bears are large heavy mammalsthat have long shaggy hair, rudimentary tails and plantigrade feet', 12, 20, 19, 10, 10)
bestiary = [Goblin, Orc, Slime, Giant, Skeleton, Vampire, Ghoul, Mummy, Bear]

