import random
from Items import Weapon
from Items import Armor

class Hero:
	
	ExpLimit = 10

	def __init__(self, Name: str, Age: int, Gender: str, Profession: str, Level: int, Experience: int, Health: int, Attack: int, Agility: int, Defense: int, Intelligence: int, Weapon: Weapon, Armor: Armor):
		self.Name = Name
		self.Age = Age
		self.Gender = Gender
		self.Profession = Profession
		self.Level = 1
		self.Experience = 0
		self.Health = Health
		self.Attack = Attack
		self.Agility = Agility
		self.Defense = Defense
		self.Intelligence = Intelligence
		self.Weapon = Weapon
		self.Armor = Armor

	def ShowStatus(self):
		print(f'Name:{self.Name}\nAge:{self.Age}\nGender:{self.Gender}\nProfession:{self.Profession}\nLevel:{self.Level}\nExperience:{self.Experience}\nWeapon:{self.Weapon.Name}\nArmor:{self.Armor.Name}\nHealth:{self.Health}\nAttack:{self.Attack}\nAgility:{self.Agility}\nDefence:{self.Defense}\nInteligence:{self.Intelligence}')

	def LevelUp(self):
		while self.Experience >= Hero.ExpLimit:
			self.Level += 1
			self.Experience = self.Experience - Hero.ExpLimit
			Hero.ExpLimit *= 2

	def Death(self):
		if self.Health <=0:
			print("GAME OVER")

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
			Damage = abs((random.randint(0, self.Attack + 1)) - (enemy.Defense%10)) # damage dealing to enemy depending on hero attack and enemy defence
			enemy.AttributeDecrease(Damage, 0, 0, 0)
	
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
	


class Monster():
	
	def __init__(self, Type: str, Description: str, Level: int, Health: int, Attack: int, Agility: int, Defense: int):
		self.Type = Type
		self.Description = Description
		self.Level = Level
		self.Health = Health
		self.Attack = Attack
		self.Agility = Agility
		self.Defense = Defense

	def ShowStatus(self):
		print(f'Type:{self.Type}\nLevel:{self.Level}\nHealth:{self.Health}\nAttack:{self.Attack}\nAgility:{self.Agility}\nDefence:{self.Defense}')

	def ShowDescription(self):
		print(self.Description)
	
	def Death(self):
		if self.Health <= 0:
			print(f'{self.Type} Died')	

	def AttributeDecrease(self, Health: int, Attack: int, Agility: int, Defense: int):
		self.Health -= Health
		self.Attack -= Attack
		self.Agility -= Agility
		self.Defense -= Defense
		self.Death()

	def DealDamage(self, enemy):
		if random.random() >= ((enemy.Agility/100)*0.5): #evasion depending on agility		
			Damage = abs((random.randint(0, self.Attack + 1)) - (enemy.Defense%10)) # damage dealing to enemy depending on hero attack and enemy defence
			enemy.AttributeDecrease(Damage, 0, 0, 0, 0)



	
chainmail = Armor('ChainMail', 'the protective material that knights wear as part of a suit of armor', 'Knight', 1, 4, 6, 1)
ironarmor = Armor('IronArmor', 'Regular rookie armor', 'Knight', 2, 8, 10, 1)
knife = Weapon('Knife', 'Regular kitchen knife', 'Knight', 1, 10, 15, 0)
sword = Weapon('Sword', '100 inche long swod that was owned by old merchante', 'Knight', 1, 20, 30, 5)
NULL_W = Weapon('0', '0', '0', 0, 0, 0, 0)
NULL_A = Armor('0', '0', '0', 0, 0, 0, 0)

Levon = Hero('Levon', 18, 'male', 'Knight', 0, 0, 0, 0, 0 , 0, 0, NULL_W, NULL_A)
Levon.AttributeIncrease(10, 10, 10, 10, 5, 40)
Levon.ShowStatus()
print("")
Levon.PickWeapon(sword)
Levon.ShowStatus()
print("")
Levon.PickWeapon(knife)
Levon.ShowStatus()
print("")
Levon.PickArmor(ironarmor)
Levon.ShowStatus()
print("")




Orc = Monster('Orc', 'Human like being with big body and green skin', 1, 5, 1, 12, 3)
Orc.ShowStatus()
Orc.ShowDescription()
print("")

print("Orc attacks Hero")
Orc.DealDamage(Levon)
Levon.ShowStatus()
print("")

print("Hero attacks Orc")
Levon.DealDamage(Orc)
Orc.ShowStatus()



