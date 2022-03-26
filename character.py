import random
import sys
from Items import *
from colorama import Fore, Back, Style
from Room import *
from Enemy import Monster
class Hero:
	
	ExpLimit = 10

	def __init__(self, Name: str, Age: int, Gender: str, Profession: str, Health: int, Attack: int, Agility: int, Defense: int, Intelligence: int, Weapon: Weapon, Armor: Armor, CurrentRoom: Room, Level: int = 1, Experience: int = 0, PositionX: int = 0, PositionY: int = 0):
		self.Name = Name
		self.Age = Age
		self.Gender = Gender
		self.Profession = Profession
		self.Level = Level
		self.Experience = Experience 
		self.PositionX = PositionX
		self.PositionY = PositionY
		self.CurrentRoom = CurrentRoom
		self.Weapon = Weapon
		self.Armor = Armor
		self.Health = Health
		self.Attack = Attack
		self.Agility = Agility
		self.Defense = Defense
		self.Intelligence = Intelligence

	def ShowStatus(self):
		print(f'Name: {self.Name}\nAge: {self.Age}\nGender: {self.Gender}\nProfession: {self.Profession}\nLevel: {self.Level}\nExperience: {self.Experience}\nRoom: {self.CurrentRoom.Name}\nPosition: {(self.PositionX, self.PositionY)}\nWeapon: {self.Weapon.Name}\nArmor: {self.Armor.Name}\nHealth: {self.Health}\nAttack: {self.Attack}\nAgility: {self.Agility}\nDefence: {self.Defense}\nInteligence: {self.Intelligence}')

	def ShowCurrentRoom(self):
		self.CurrentRoom.ShowDescription()

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
	
	def Move(self, direction, Map):
		if direction == 'N':
			self.PositionY += 1
			if (self.PositionX % 5 == 0 and self.PositionY % 5 == 0) and (self.PositionX + self.PositionY) % 2 != 0:
				for Room in Map:
					if self.CurrentRoom.GlobalPositionX == Room.GlobalPositionX and self.CurrentRoom.GlobalPositionY == Room.GlobalPositionY - 1: 
						self.CurrentRoom = Room
		elif direction == 'S':
			self.PositionY -= 1
			if (self.PositionX % 5 == 0 and self.PositionY % 5 == 0) and (self.PositionX + self.PositionY) % 2 != 0:
				for Room in Map:
					if self.CurrentRoom.GlobalPositionX == Room.GlobalPositionX and self.CurrentRoom.GlobalPositionY == Room.GlobalPositionY + 1: 
						self.CurrentRoom = Room
		elif direction == 'E':
			self.PositionX += 1
			if (self.PositionX % 5 == 0 and self.PositionY % 5 == 0) and (self.PositionX + self.PositionY) % 2 != 0:
				for Room in Map:
					if self.CurrentRoom.GlobalPositionX == Room.GlobalPositionX - 1 and self.CurrentRoom.GlobalPositionY == Room.GlobalPositionY: 
						self.CurrentRoom = Room
		elif direction == 'W':
			self.PositionX -= 1
			if (self.PositionX % 5 == 0 and self.PositionY % 5 == 0) and (self.PositionX + self.PositionY) % 2 != 0:
				for Room in Map:
					if self.CurrentRoom.GlobalPositionX == Room.GlobalPositionX + 1 and self.CurrentRoom.GlobalPositionY == Room.GlobalPositionY: 
						self.CurrentRoom = Room
		else:
			print("Wrong input, choose from (N)orth, (S)outh, (E)ast, (W)est")
		

	def CreateHero():
		Mage = [50, 10, 3, 3, 12]
		Archer = [70, 8, 12, 5, 3]
		Knight = [100, 12, 5, 12, 1]

		Name = input("Enter Your Name: ").strip()

		Age = input("Enter Your Age: ").strip()
		while Age.isdigit() != True:
			print(Fore.RED + "Wrong Input, Try Again", Style.RESET_ALL)
			Age = input("Enter Your Age: ").strip()

		Gender = input("Enter Your Gender[(M)ale/(F)emale]: ").strip()
		while Gender != 'M' and Gender != 'F':
			print(Fore.RED + "Wrong Input, Try Again", Style.RESET_ALL)
			Gender = input("Enter Your Gender[(M)ale/(F)emale]: ").strip()
		if Gender == 'M':
			Gender = 'Male'
		else:
			Gender = 'Female'


		Profession = input("Choose Character Profession[(M)age, (K)night, (A)rcher]: ").strip()
		while Profession != 'M' and Profession != 'K' and Profession != 'A':
			print(Fore.RED + "Wrong Input, Try Again", Style.RESET_ALL)
			Profession = input("Choose Character Profession[(M)age, (K)night, (A)rcher]: ").strip()

		if Profession == 'M':
			MC = Hero(Name, Age, Gender, 'Mage', Mage[0], Mage[1], Mage[2], Mage[3], Mage[4], Arms, Shirt)
		elif Profession == 'K':
 			MC = Hero(Name, Age, Gender, 'Knight', Knight[0], Knight[1], Knight[2], Knight[3], Knight[4], Arms, Shirt)
		elif Profession == 'A':
			MC = Hero(Name, Age, Gender, 'Archer', Archer[0], Archer[1], Archer[2], Archer[3], Archer[4], Arms, Shirt)
		else:
			raise ValueError

		print(Fore.BLUE + '\nYour Character Status: ', Style.RESET_ALL)
		MC.ShowStatus()
		return MC


Room1 = Room('Starting Room', 0, 0)
Levon = Hero('Levon', 18, 'male', 'Knight', 0, 0, 0, 0, 0, Arms, Shirt, Room1)
Levon.AttributeIncrease(10, 10, 10, 10, 5, 40)
Levon.PickWeapon(sword)
Levon.PickArmor(ironarmor)

Map = Room.CreateMap()

for komnata in Map:
	komnata.ShowDescription()

while True:
	Levon.Move(input(), Map)
	Levon.ShowStatus()

Levon.ShowStatus()
print("")

Orc = Monster('Orc', 'Human like being with big body and green skin', 3, 5, 1, 12, 3)
Orc.ShowStatus()
Orc.ShowDescription()
print("")

while True:
	print('You attaked Orc')
	Levon.DealDamage(Orc)	
	print('Orc attaked back')
	Orc.DealDamage(Levon)

Levon.ShowCurrentRoom()
