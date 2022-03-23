class Hero:
	
	ExpLimit = 10

	def __init__(self, Name: str, Age: int, Gender: str, Proffession: str, Level: int, Experience: int, Health: int, Attack: int, Agility: int, Defense: int, Intelligence: int):
		self.Name = Name
		self.Age = Age
		self.Gender = Gender
		self.Proffession = Proffession
		self.Level = 1
		self.Experience = 0
		self.Health = Health
		self.Attack = Attack
		self.Agility = Agility
		self.Defense = Defense
		self.Intelligence = Intelligence

	def ShowStatus(self):
		print(f'Name:{self.Name}\nAge:{self.Age}\nGender:{self.Gender}\nLevel:{self.Level}\nExperience:{self.Experience}\nHealth:{self.Health}\nAttack:{self.Attack}\nAgility:{self.Agility}\nDefence:{self.Defense}\nInteligence:{self.Intelligence}')

	def LevelUp(self):
		while self.Experience >= Hero.ExpLimit:
			self.Level += 1
			self.Experience = self.Experience - Hero.ExpLimit
			Hero.ExpLimit *= 2

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




Levon = Hero('Levon', 18, 'male', 0, 0, 0, 0, 0, 0 , 0, 0)
Levon.ShowStatus()
print("")
Levon.AttributeIncrease(10, 10, 10, 10, 5, 40)
print("")
Levon.ShowStatus()
print("")

Orc = Monster('Orc', 'Human like being with big body and green skin',30, 100, 30, 10, 25)
Orc.ShowStatus()
Orc.ShowDescription()
