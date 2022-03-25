import random
import sys
from Items import Weapon
from Items import Armor

class Hero:
	
	ExpLimit = 10

	def __init__(self, Name: str, Age: int, Gender: str, Profession: str, Health: int, Attack: int, Agility: int, Defense: int, Intelligence: int, Weapon: Weapon, Armor: Armor, Level: int = 1, Experience: int = 0, PositionX: int = 0, PositionY: int = 0):
		self.Name = Name
		self.Age = Age
		self.Gender = Gender
		self.Profession = Profession
		self.Level = Level
		self.Experience = Experience 
		self.PositionX = PositionX
		self.PositionY = PositionY
		self.Weapon = Weapon
		self.Armor = Armor
		self.Health = Health
		self.Attack = Attack
		self.Agility = Agility
		self.Defense = Defense
		self.Intelligence = Intelligence

	def ShowStatus(self):
		print(f'Name:{self.Name}\nAge:{self.Age}\nGender:{self.Gender}\nProfession:{self.Profession}\nLevel:{self.Level}\nExperience:{self.Experience}\nPosition:{(self.PositionX, self.PositionY)}\nWeapon:{self.Weapon.Name}\nArmor:{self.Armor.Name}\nHealth:{self.Health}\nAttack:{self.Attack}\nAgility:{self.Agility}\nDefence:{self.Defense}\nInteligence:{self.Intelligence}')

	def LevelUp(self):
		while self.Experience >= Hero.ExpLimit:
			self.Level += 1
			self.Experience = self.Experience - Hero.ExpLimit
			Hero.ExpLimit *= 2
	
	def Death(self):
		if self.Health <=0:
			print("YOU DIED")	
			sys.exit()
			
	def AttributeIncrease(self, Health: int, Attack: int, Agility: int, Defense: int, Intelligence: int, Experience: int):
		self.Health += Health
		self.Attack += Attack
		self.Agility += Agility
		self.Defense += Defense
		self.Intelligence += Intelligence
		self.Experience += Experience
		self.LevelUp()
	
	def AttributeDecrease(self, Health: int, Attack: int, Agility: int, Defense: int, Intelligence: int):
		self.Health -= Health
		self.Attack -= Attack
		self.Agility -= Agility
		self.Defense -= Defense
		self.Intelligence -= Intelligence
		self.Death()

	def DealDamage(self, enemy):
		if random.random() >= ((enemy.Agility/100)*0.5): #evasion depending on agility
			if self.Profession == 'Knight':
				ExtraDamage = self.Defense % 10		
			elif self.Profession == 'Mage':
				ExtraDamage = self.Intelligence % 10
			elif self.Profession == 'Archer':
				ExtraDamage = self.Agility	
			Damage = abs((random.randint(0, self.Attack)) - (enemy.Defense%10)) # damage dealing to enemy depending on hero attack and enemy defence
			enemy.GainDamage(self, Damage)
	
	def PickWeapon(self, Weapon):
		if self.Level >= Weapon.LevelRequired and self.Profession == Weapon.ProfessionRequired:
			if Weapon.Attack - self.Weapon.Attack > 0:
				self.AttributeIncrease(0, Weapon.Attack - self.Weapon.Attack, 0, 0, 0, 0)
			else:
				self.AttributeDecrease(0, self.Weapon.Attack - Weapon.Attack, 0, 0, 0)

			if Weapon.Agility - self.Weapon.Agility > 0:
				self.AttributeIncrease(0, 0, Weapon.Agility - self.Weapon.Agility, 0, 0, 0)
			else:
				self.AttributeDecrease(0, 0, self.Weapon.Agility - Weapon.Agility, 0, 0)
		
			if Weapon.Intelligence - self.Weapon.Intelligence > 0:
				self.AttributeIncrease(0, 0, 0, 0, Weapon.Intelligence - self.Weapon.Intelligence, 0)
			else:
				self.AttributeDecrease(0, 0, 0, 0, self.Weapon.Intelligence - Weapon.Intelligence)
			self.Weapon = Weapon
		else:
			if self.Level < Weapon.LevelRequired:
				print(f'You do not have Required Level: {Weapon.LevelRequired}')
			else:
				print(f'You do not have Required Profession: {Weapon.ProfessionRequired}')
	
	def PickArmor(self, Armor):
		if self.Level >= Armor.LevelRequired and self.Profession == Armor.ProfessionRequired:
			if Armor.Agility - self.Armor.Agility > 0:
				self.AttributeIncrease(0, 0, Armor.Agility - self.Armor.Agility, 0, 0, 0)
			else:
				self.AttributeDecrease(0, 0, self.Armor.Agility - Armor.Agility, 0, 0)
			
			if Armor.Defense - self.Armor.Defense > 0:
				self.AttributeIncrease(0, 0, 0, Armor.Defense - self.Armor.Defense, 0, 0)
			else:
				self.AttributeDecrease(0, 0, 0, Armor.Defense - self.Armor.Defense, 0)
		
			if Armor.Intelligence - self.Armor.Intelligence > 0:
				self.AttributeIncrease(0, 0, 0, 0, Armor.Intelligence - self.Armor.Intelligence, 0)
			else:
				self.AttributeDecrease(0, 0, 0, 0, self.Armor.Intelligence - Armor.Intelligence)
			self.Armor = Armor
		else:
			if self.Level < Armor.LevelRequired:
				print(f'You do not have Required Level: {Armor.LevelRequired}')
			else:
				print(f'You do not have Required Profession: {Armor.ProfessionRequired}')
	
	def Move(self, direction: str):
		if direction == 'N':
			self.PositionY += 1
		elif direction == 'S':
			self.PositionY -= 1
		elif direction == 'E':
			self.PositionX += 1
		elif direction == 'W':
			self.PositionY -= 1
		else:
			raise ValueError
#			print("Wrong input, choose from (N)orth, (S)outh, (E)ast, (W)est")


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
		print(f'Name:{self.Name}\nLevel:{self.Level}\nHealth:{self.Health}\nAttack:{self.Attack}\nAgility:{self.Agility}\nDefence:{self.Defense}')

	def ShowDescription(self):
		print(self.Description)
	
	def GainDamage(self, enemy, Damage):
		self.Health -= Damage
		GainExp = 5 * 2**(self.Level) #Its the formula of ExpLimit series
		if self.Health <= 0: 
			print(f'{self.Name} Died, You get {GainExp} Experience')
			enemy.AttributeIncrease(0, 0, 0, 0, 0, GainExp)
			raise ValueError
		
	def DealDamage(self, enemy):
		if random.random() >= ((enemy.Agility/100)*0.5): #evasion depending on agility			
			Damage = abs((random.randint(0, self.Attack + 1)) - (enemy.Defense%10)) # damage dealing to enemy depending on hero attack and enemy defence
			enemy.AttributeDecrease(Damage, 0, 0, 0, 0)

"""
Goblin = Monster('Goblin', 'Goblins are small, weak humanoids with green skin and heigth beetween 3 and 3.5 feet', 5, 10, 3, 10, 2)
Orc = Monster('Orc', 'Orcs are brutal, violent humanoids with greyish or green skin and animalistic features', 20, 40, 12, 6, 10)
Slime = Monster('Slime', 'Slimes are gelatinous creatures that can come in many different colors and sizes, the most common appearance is green and about knee height', 7, 15, 5, 5, 3)
Giant = Monster('Giant', 'Giants are an extraordinarily large humanoid creatures, often with eldritch powers', 45, 150, 30, 3, 25)
Skeleton = Monster('Skeleton', 'Skeletons are the animated skeletal remains of once-living creatures, used as disposable troops by necromancers', 10, 20, 7, 6, 5)
Vampire = Monster('Vampire', 'Vampires are undead, nocturnal creatures that subsist on blood, they have superhuman powers and are sometimes able to shape-shift', 30, 100, 25, 30, 20)
Ghoul = Monster('Ghoul', 'Ghouls are carrion eating undead creatures that dwell in graveyards and other lonely places', 18, 30, 10, 15, 10)
Mummy = Monster('Mummy', 'Mummies are lumbering undead corpses wrapped in bandages, they are very resiliant to physical damage', 16, 35, 8, 5, 15)
Bear = Monster('Bear', 'Bears are large heavy mammalsthat have long shaggy hair, rudimentary tails and plantigrade feet', 12, 20, 19, 10, 10)

chainmail = Armor('ChainMail', 'the protective material that knights wear as part of a suit of armor', 'Knight', 1, 4, 6, 1)
ironarmor = Armor('IronArmor', 'Regular rookie armor', 'Knight', 2, 8, 10, 1)
knife = Weapon('Knife', 'Regular kitchen knife', 'Knight', 1, 10, 15, 0)
sword = Weapon('Sword', '100 inche long swod that was owned by old merchante', 'Knight', 1, 20, 30, 5)
NULL_W = Weapon('0', '0', '0', 0, 0, 0, 0)
NULL_A = Armor('0', '0', '0', 0, 0, 0, 0)


Bestiary = [Goblin, Orc, Slime, Giant, Skeleton, Vampire, Ghoul, Mummy, Bear]
Objects = [ironarmor, knife, chainmail, sword]


Levon = Hero('Levon', 18, 'male', 'Knight', 0, 0, 0, 0, 0, NULL_W, NULL_A)
Levon.AttributeIncrease(10, 10, 10, 10, 5, 40)
Levon.PickWeapon(sword)
Levon.PickArmor(ironarmor)
while True:
	try: 
		Levon.Move(input())
		#Levon.ShowStatus()
	except ValueError:
		print("Wrong input, choose from (N)orth, (S)outh, (E)ast, (W)est")
	break

Levon.ShowStatus()
print("")

Orc = Monster('Orc', 'Human like being with big body and green skin', 3, 5, 1, 12, 3)
Orc.ShowStatus()
Orc.ShowDescription()
print("")

while True:
	print('You attaked Orc')
	try:
		Levon.DealDamage(Orc)
	except ValueError:
		break
	
	print('Orc attaked back')
	Orc.DealDamage(Levon)
"""
