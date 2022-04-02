import random
import sys
from Items import *
from colorama import Fore, Back, Style
from Room import *
from Enemy import Monster
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"  # Its for The Print Which Pygame Automatically do After Being Imported
from pygame import mixer
import time
class Hero:
	
	ExpLimit = 10

	def __init__(self, Name: str, Age: int, Gender: str, Profession: str, Health: int, Attack: int, Agility: int, Defense: int, Intelligence: int, Weapon: Weapon, Armor: Armor, CurrentRoom: Room = Room1, Level: int = 1, Experience: int = 0, PositionX: int = 0, PositionY: int = 0, RoomPositionX: int = 4, RoomPositionY: int = 4):
		self.Name = Name
		self.Age = Age
		self.Gender = Gender
		self.Profession = Profession
		self.Level = Level
		self.Experience = Experience 
		self.PositionX = PositionX  # Hero X Cooridnate in Global Coordinates
		self.PositionY = PositionY  # Hero Y Coordinate in Global Coordinates
		self.CurrentRoom = CurrentRoom		
		self.RoomPositionX = RoomPositionX  # Hero X Coordinate in The Current Room
		self.RoomPositionY = RoomPositionY  # Hero Y Coordinate in The Current Room
		self.Weapon = Weapon
		self.Armor = Armor
		self.Health = Health
		self.Attack = Attack
		self.Agility = Agility
		self.Defense = Defense
		self.Intelligence = Intelligence

	def ShowStatus(self):
		print(Fore.YELLOW + '\nYour Character Status: ', Style.RESET_ALL)
		print(Fore.BLUE + f'Name: {self.Name}\nAge: {self.Age}\nGender: {self.Gender}\nProfession: {self.Profession}\nLevel: {self.Level}\nExperience: {self.Experience}\nRoom: {self.CurrentRoom.Name}\nPosition: {(self.PositionX, self.PositionY)}\nWeapon: {self.Weapon.Name}\nArmor: {self.Armor.Name}\nHealth: {self.Health}\nAttack: {self.Attack}\nAgility: {self.Agility}\nDefence: {self.Defense}\nInteligence: {self.Intelligence}\n', Style.RESET_ALL)

	def LevelUp(self):
		while self.Experience >= Hero.ExpLimit:
			self.Level += 1
			self.Experience = self.Experience - Hero.ExpLimit
			Hero.ExpLimit *= 2  # Every Time After Leveling Up Experience Limit for Next Level Doubles
			self.AttributeIncrease(10, 1, 1, 1, 1, 0)
			
	def Death(self):
		if self.Health <= 0:
			print(Fore.RED + "YOU DIED", Style.RESET_ALL)	
			sys.exit()  # Closing The Program After The Hero Death
			
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
		if random.random() >= ((enemy.Agility/100)*0.5):  # Evasion Chance Depending on Agility
			if self.Profession == 'Knight':	
				ExtraDamage = self.Defense % 10			
			elif self.Profession == 'Mage':	
				ExtraDamage = self.Intelligence % 10
			elif self.Profession == 'Archer':	
				ExtraDamage = self.Agility	
			Damage = abs((random.randint(0, self.Attack)) - (enemy.Defense%10)) # Damage Being Dealed to Enemy Depending on Hero Attack and Enemy Defence
			enemy.GainDamage(self, Damage)
			print(f'You Deal {Damage} Damage to {enemy.Name}')
		else:
			print(f'{enemy.Name} Dogded the Attack')
	
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
			self.ShowStatus()
			self.CurrentRoom.Items.remove(self.CurrentRoom.Interior[self.RoomPositionY][self.RoomPositionX])  # Removing Picked Weapon from Current Room Attribute
			self.CurrentRoom.Interior[self.RoomPositionY][self.RoomPositionX] = 0  # Removing Picked Weapon from Map and Current Room Interior
		else:
			if self.Level < Weapon.LevelRequired:
				print(Fore.RED + f'You do not have Required Level: {Weapon.LevelRequired}', Style.RESET_ALL)
			else:
				print(Fore.RED + f'You do not have Required Profession: {Weapon.ProfessionRequired}', Style.RESET_ALL)
	
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
			self.ShowStatus()
			self.CurrentRoom.Items.remove(self.CurrentRoom.Interior[self.RoomPositionY][self.RoomPositionX])  # Removing Picked Armor from Current Room Attribute
			self.CurrentRoom.Interior[self.RoomPositionY][self.RoomPositionX] = 0  # Removing Picked Weapon from Map and Current Room Interior
		else:
			if self.Level < Armor.LevelRequired:
				print(Fore.RED + f'You do not have Required Level: {Armor.LevelRequired}', Style.RESET_ALL)
			else:
				print(Fore.RED + f'You do not have Required Profession: {Armor.ProfessionRequired}', Style.RESET_ALL)

	def Battle(self, enemy):
		file3 = open('Data/BattleMusic.txt', "r") 
		BattleMusic = random.choices(file3.read().splitlines(), k = 1)
		file3.close()
		mixer.music.stop()
		mixer.music.load('Music/Battle/' + BattleMusic[0])
		mixer.music.set_volume(0.7)
		mixer.music.play()
		while True:
			if random.randint(0, 1) == 1:  # Randomly Choosing Whose Turn to Attack is it
				print(Fore.YELLOW + 'It is Your Turn to Attack, Enter "A" to Attack', Style.RESET_ALL)
				res = input()
				while res != "A":
					print(Fore.RED + 'Wrong Input, Enter "A" to Attack', Style.RESET_ALL)
					res = input()
				try:
					self.DealDamage(enemy)
				except ValueError:  # Exeption is Being Risen When Monster Dies // See Enemy.py
					self.CurrentRoom.Monsters.remove(self.CurrentRoom.Interior[self.RoomPositionY][self.RoomPositionX])  # Removing Death Monster from Current Room Attribute
					self.CurrentRoom.Interior[self.RoomPositionY][self.RoomPositionX] = 0  # Removing Death Monster from Map and Current Room Interior
					self.CurrentRoom.ShowInterior(self.RoomPositionX, self.RoomPositionY)
					break
			else:
				print(Fore.YELLOW + f'It is {enemy.Name} Turn to Attack', Style.RESET_ALL)
				time.sleep(0.5)
				enemy.DealDamage(self)	
		mixer.music.stop()
		mixer.music.load(self.CurrentRoom.Music)
		mixer.music.set_volume(0.7)
		mixer.music.play()	

	def Move(self, direction, Map):
		if direction == 'N':
			self.PositionY += 1
			if self.RoomPositionX == self.CurrentRoom.Size // 2 and self.RoomPositionY == 0:  # If Hero is Next to The Door Change The Room
				if self.CurrentRoom.GlobalPositionY == 2:
					print(Fore.GREEN + "YOU WON THE GAME", Style.RESET_ALL)
					sys.exit()
				elif self.CurrentRoom.Monsters != []:
					print(Fore.RED + 'You Can not Move to The Next Room Until You Do not Clear Current Room', Style.RESET_ALL)
					self.PositionY -= 1
				else:	
					for Room in Map:
						if self.CurrentRoom.GlobalPositionX == Room.GlobalPositionX and self.CurrentRoom.GlobalPositionY == Room.GlobalPositionY - 1: 
							self.CurrentRoom = Room
							print(Fore.YELLOW + f'You Entered New Room', Style.RESET_ALL)
							self.CurrentRoom.ShowDescription()
							self.RoomPositionY = self.CurrentRoom.Size - 1
							self.RoomPositionX = self.CurrentRoom.Size // 2
							self.CurrentRoom.ShowInterior(self.RoomPositionX, self.RoomPositionY)
							mixer.music.stop()
							mixer.music.load(self.CurrentRoom.Music)
							mixer.music.set_volume(0.7)
							mixer.music.play()
							break
			else:
				if self.RoomPositionY == 0:
					print(Fore.RED + 'You Can not Move This Way, There is a Wall', Style.RESET_ALL)
					self.PositionY -= 1
				else:
					self.RoomPositionY -= 1

		elif direction == 'S':
			self.PositionY -= 1
			if self.RoomPositionX  == self.CurrentRoom.Size // 2 and self.RoomPositionY == self.CurrentRoom.Size - 1:  # If Hero is Next to The Door Change The Room
				if self.CurrentRoom.GlobalPositionY == -2:
					print(Fore.GREEN + "YOU WON THE GAME", Style.RESET_ALL)
					sys.exit()
				elif self.CurrentRoom.Monsters != []:
					print(Fore.RED + 'You Can not Move to The Next Room Until You Do not Clear Current Room', Style.RESET_ALL)
					self.PositionY += 1
				else:
					for Room in Map:
						if self.CurrentRoom.GlobalPositionX == Room.GlobalPositionX and self.CurrentRoom.GlobalPositionY == Room.GlobalPositionY + 1: 
							self.CurrentRoom = Room
							print(Fore.YELLOW + f'You Entered New Room', Style.RESET_ALL)
							self.CurrentRoom.ShowDescription()
							self.RoomPositionY = 0
							self.RoomPositionX = self.CurrentRoom.Size // 2
							self.CurrentRoom.ShowInterior(self.RoomPositionX, self.RoomPositionY)	
							mixer.music.stop()
							mixer.music.load(self.CurrentRoom.Music)
							mixer.music.set_volume(0.7)
							mixer.music.play()
							break
			else:
				if self.RoomPositionY == self.CurrentRoom.Size - 1:
					print(Fore.RED + 'You Can not Move This Way, There is a Wall', Style.RESET_ALL)
					self.PositionY += 1
				else:
					self.RoomPositionY += 1

		elif direction == 'E':
			self.PositionX += 1
			if self.RoomPositionX == self.CurrentRoom.Size - 1 and self.RoomPositionY == self.CurrentRoom.Size // 2:  # If Hero is Next to The Door Change The Room
				if self.CurrentRoom.GlobalPositionX == 2:
					print(Fore.GREEN + "YOU WON THE GAME", Style.RESET_ALL)
					sys.exit()
				elif self.CurrentRoom.Monsters != []:
					print(Fore.RED + 'You Can not Move to The Next Room Until You Do not Clear Current Room', Style.RESET_ALL)
					self.PositionX -= 1
				else:
					for Room in Map:
						if self.CurrentRoom.GlobalPositionX == Room.GlobalPositionX - 1 and self.CurrentRoom.GlobalPositionY == Room.GlobalPositionY: 
							self.CurrentRoom = Room
							print(Fore.YELLOW + f'You Entered New Room', Style.RESET_ALL)
							self.CurrentRoom.ShowDescription()
							self.RoomPositionY = self.CurrentRoom.Size // 2
							self.RoomPositionX = 0
							self.CurrentRoom.ShowInterior(self.RoomPositionX, self.RoomPositionY)
							mixer.music.stop()
							mixer.music.load(self.CurrentRoom.Music)
							mixer.music.set_volume(0.7)
							mixer.music.play()
							break
			else:
				if self.RoomPositionX == self.CurrentRoom.Size - 1:
					print(Fore.RED + 'You Can not Move This Way, There is a Wall', Style.RESET_ALL)
					self.PositionX -= 1
				else:
					self.RoomPositionX += 1

		elif direction == 'W':
			self.PositionX -= 1
			if self.RoomPositionX == 0 and self.RoomPositionY == self.CurrentRoom.Size // 2:  # If Hero is Next to The Door Change The Room
				if self.CurrentRoom.GlobalPositionX == -2:
					print(Fore.GREEN + "YOU WON THE GAME", Style.RESET_ALL)
					sys.exit()
				elif self.CurrentRoom.Monsters != []:
					print(Fore.RED + 'You Can not Move to The Next Room Until You Do not Clear Current Room', Style.RESET_ALL)
					self.PositionX += 1
				else:
					for Room in Map:
						if self.CurrentRoom.GlobalPositionX == Room.GlobalPositionX + 1 and self.CurrentRoom.GlobalPositionY == Room.GlobalPositionY: 
							self.CurrentRoom = Room
							print(Fore.YELLOW + f'You Entered New Room', Style.RESET_ALL)
							self.CurrentRoom.ShowDescription()
							self.RoomPositionY = self.CurrentRoom.Size // 2
							self.RoomPositionX = self.CurrentRoom.Size - 1
							self.CurrentRoom.ShowInterior(self.RoomPositionX, self.RoomPositionY)
							mixer.music.stop()
							mixer.music.load(self.CurrentRoom.Music)
							mixer.music.set_volume(0.7)
							mixer.music.play()
							break
			else:
				if self.RoomPositionX == 0:
					print(Fore.RED + 'You Can not Move This Way, There is a Wall', Style.RESET_ALL)
					self.PositionX += 1
				else:
					self.RoomPositionX -= 1
		else:
			print(Fore.RED + 'Wrong input, choose from (N)orth, (S)outh, (E)ast, (W)est', Style.RESET_ALL)
		
		RoomCell =  self.CurrentRoom.Interior[self.RoomPositionY][self.RoomPositionX]  # Current Location in The Room

		if isinstance(RoomCell, Monster):
			print(Fore.YELLOW + f'You Were Attaked by {RoomCell.Name}\n', Style.RESET_ALL)
			self.Battle(RoomCell)
			 			
		elif isinstance(RoomCell, Weapon):
			print(Fore.YELLOW + f'You Found Weapon {RoomCell.Name}, To Pick It Enter "Pick", To Drop It Enter "Drop", To See Weapon Description Enter "Description"\n', Style.RESET_ALL)
			res = input()
			while res != 'Drop':
				if res == 'Pick':
					self.PickWeapon(RoomCell)
					RoomCell = 0		
					break
				elif res == 'Description':
					RoomCell.ShowStatus()
				else:
					print(Fore.RED + "Wrong Input, Try Again", Style.RESET_ALL)
				res = input()
			
		elif isinstance(RoomCell, Armor):
			print(Fore.YELLOW + f'You Found Armor {RoomCell.Name}, To Pick It Enter "Pick", To Drop It Enter "Drop", To See Armor Description Enter "Description"\n', Style.RESET_ALL)
			res = input()
			while res != 'Drop':
				if res == 'Pick':
					self.PickArmor(RoomCell)
					RoomCell = 0		
					break
				elif res == 'Description':
					RoomCell.ShowStatus()
				else:
					print(Fore.RED + "Wrong Input, Try Again", Style.RESET_ALL)
				res = input()
				
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

		MC.ShowStatus()
		return MC

