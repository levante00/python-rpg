import random
from colorama import Fore, Back, Style
class Monster():

	def __init__(self, Name: str, Description: str, Level: int, Health: int, Attack: int, Agility: int, Defense: int):
		self.Name = Name
		self.Description = Description
		self.Level = Level
		self.Health = Health
		self.Attack = Attack
		self.Agility = Agility
		self.Defense = Defense

	def ShowStatus(self):
		print(Fore.BLUE + f'Name: {self.Name}\nLevel: {self.Level}\nHealth: {self.Health}\nAttack: {self.Attack}\nAgility: {self.Agility}\nDefence: {self.Defense}', Style.RESET_ALL)

	def ShowDescription(self):
		print(self.Description)

	def ShowBestiary():
		print(Fore.YELLOW + '\nMonster List:', Style.RESET_ALL)
		for Monster in Bestiary:
			Monster.ShowStatus()
			Monster.ShowDescription()
			print('')

	def GainDamage(self, enemy, Damage):
		self.Health -= Damage
		GainExp = 5 * 2**(self.Level)  # Its the Formula of ExpLimit Series
		if self.Health <= 0:
			print(Fore.YELLOW + f'{self.Name} Died, You get {GainExp} Experience', Style.RESET_ALL)
			enemy.AttributeIncrease(0, 0, 0, 0, 0, GainExp)
			raise ValueError

	def DealDamage(self, enemy):
		if random.random() >= ((enemy.Agility/100)*0.5):  # Evasion Chance Depending on Agility     
			Damage = abs((random.randint(0, self.Attack + 1)) - (enemy.Defense%10))  # Damage Being Dealed to Enemy Depending on Hero Attack and Enemy Defence
			print(f'You Get a Direct Hit and Received {Damage} Damage')	 # This is for Hero to Know How Much Damage He Took
			enemy.AttributeDecrease(Damage, 0, 0, 0, 0)
		else:
			print('You Dodged the Attack')  # This is for Hero to Know that He Avoided the Attack


Goblin = Monster('Goblin', 'Goblins are small, weak humanoids with green skin and heigth beetween 3 and 3.5 feet', 5, 10, 3, 10, 2)
Orc = Monster('Orc', 'Orcs are brutal, violent humanoids with greyish or green skin and animalistic features', 20, 40, 12, 6, 10)
Slime = Monster('Slime', 'Slimes are gelatinous creatures that can come in many different colors and sizes, the most common appearance is green and about knee height', 7, 15, 5, 5, 3)
Giant = Monster('Giant', 'Giants are an extraordinarily large humanoid creatures, often with eldritch powers', 45, 150, 30, 3, 25)
Skeleton = Monster('Skeleton', 'Skeletons are the animated skeletal remains of once-living creatures, used as disposable troops by necromancers', 10, 20, 7, 6, 5)
Vampire = Monster('Vampire', 'Vampires are undead, nocturnal creatures that subsist on blood, they have superhuman powers and are sometimes able to shape-shift', 30, 100, 25, 30, 20)
Ghoul = Monster('Ghoul', 'Ghouls are carrion eating undead creatures that dwell in graveyards and other lonely places', 18, 30, 10, 15, 10)
Mummy = Monster('Mummy', 'Mummies are lumbering undead corpses wrapped in bandages, they are very resiliant to physical damage', 16, 35, 8, 5, 15)
Bear = Monster('Bear', 'Bears are large heavy mammalsthat have long shaggy hair, rudimentary tails and plantigrade feet', 12, 20, 19, 10, 10)
Bestiary = [Goblin, Orc, Slime, Giant, Skeleton, Vampire, Ghoul, Mummy, Bear]

