#ShowMap() Variant of printing List in Curses by Storing
"""
LIST = []
RowLen = int(len(Map) ** (1/2))
for k in range(0, len(Map), RowLen):
	for i in range(-1, 11):
		for e in range(RowLen):
			for j in range(-1, 11):
				if ((j == -1 and i != -1) or (j == 10 and i != -1)):
					LIST.append("|")
				elif i == -1 or i == 10:
					LIST.append("_")
				elif isinstance(Map[k + e].Interior[i][j], Enemy.Monster):
					LIST.append("1")
				elif isinstance(Map[k + e].Interior[i][j], Items.Item):
					LIST.append("1")
				else:
					LIST.append("0")
		LIST.append("\n")

LIST = ' '.join(LIST)
stdscr = curses.initscr()

try:
	stdscr.addstr(0,0, LIST)
except curses.error:
	pass
stdscr.refresh()
time.sleep(3)
curses.endwin()
"""

#ShowMap() Regular Variant of printing Map
"""
RowLen = int(len(Map) ** (1/2))
for k in range(0, len(Map), RowLen):
	for i in range(-1, 11):
		for e in range(RowLen):
			for j in range(-1, 11):
				if ((j == -1 and i != -1) or (j == 10 and i != -1)):
					print(Fore.MAGENTA + "|", Style.RESET_ALL, end = "")
				elif i == -1 or i == 10:
					print(Fore.MAGENTA + "_", Style.RESET_ALL, end = "")
				elif isinstance(Map[k + e].Interior[i][j], Enemy.Monster):
					print(Fore.RED + "1", Style.RESET_ALL, end = "")
				elif isinstance(Map[k + e].Interior[i][j], Items.Item):
					print(Fore.BLUE + "1", Style.RESET_ALL, end = ""
				else:
					print("0", end = " ")
		print("")
"""

#ShowMap() Curses creating pad but not normally working scroll
"""
stdscr = curses.initscr()
curses.start_color()
curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)
RED = curses.color_pair(1)
BLUE = curses.color_pair(2)
MAGENDA = curses.color_pair(3)

curses.resizeterm(1000, 1000)
stdscr.refresh()
stdscr.clear()

mypad = curses.newpad(500, 500);
mypad.scrollok(True)
mypad_pos = 0

mypad_refresh = lambda: mypad.refresh(mypad_pos, 0, 2, 25, 499, 500)
mypad_refresh()

RowLen = int(len(Map) ** (1/2))
for k in range(0, len(Map), RowLen):
	for i in range(-1, 11):
		for e in range(RowLen):
			for j in range(-1, 11):
				if ((j == -1 and i != -1) or (j == 10 and i != -1)):
					mypad.addstr("| ", MAGENDA)
				elif i == -1 or i == 10:
					mypad.addstr("_ ", MAGENDA)
				elif isinstance(Map[k + e].Interior[i][j], Enemy.Monster):
					mypad.addstr("1 ", RED)
				elif isinstance(Map[k + e].Interior[i][j], Items.Item):
					mypad.addstr("1 ", BLUE)
				else:
					mypad.addstr("0 ")
		mypad.addstr("\n")

mypad_refresh()
running = True
while running:
ch = stdscr.getch()
	if chr(ch) == 'q':
		running = False
mypad_refresh()
mypad.clear()
curses.endwin()
"""
#Entering New Room Conditions in Global Coordinates
"""
if (self.PositionX % 5 == 0 and self.PositionY % 5 == 0) and (self.PositionX + self.PositionY) % 2 != 0:
"""
