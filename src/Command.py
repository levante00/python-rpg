from src.character import Hero, CannotLeave
from src.Room import Room
from src.Enemy import Monster
from src.Items import Item, Weapon, Armor
from colorama import Fore, Style
from abc import ABC, abstractmethod


class QuitGame(Exception):
    def __init__(self, message="In the End, It is all you can, coward...") -> None:
        self.message = message

    def __str__(self) -> str:
        return "User used Quit command"


class EmptyHistory(Exception):
    def __init__(self, message="Command History is Empty") -> None:
        self.message = message

    def __str__(self) -> str:
        return "User tried to get item from empty list in Invoker class"


class Handler(ABC):
    @abstractmethod
    def add_modifier(self, modifier):
        pass

    @abstractmethod
    def handle(self, request):
        pass


class AbstractHandler(Handler):
    def __init__(self, Map: list, admin: str, MC: Hero) -> None:
        self.MC = MC
        self.Map = Map
        self.admin = admin
        self.next_modifier = None

    def add_modifier(self, modifier) -> None:
        if self.next_modifier:
            self.next_modifier.add_modifier(modifier)
        else:
            self.next_modifier = modifier

    def handle(self, request) -> None:
        if self.next_modifier:
            self.next_modifier.handle(request)


class MoveInChain(AbstractHandler):
    def handle(self, request) -> None:
        if request == "N" or request == "S" or request == "E" or request == "W":
            self.MC.move(request, self.Map, self.admin)
            room_cell = self.MC.current_room.interior[self.MC.room_position_y][
                self.MC.room_position_x
            ]
            super().handle(room_cell)


class CheckCell(AbstractHandler):
    def handle(self, request) -> None:
        if isinstance(request, Monster):
            super().add_modifier(FoundMonster(self.Map, self.admin, self.MC))
        elif isinstance(request, Weapon):
            super().add_modifier(FoundWeapon(self.Map, self.admin, self.MC))
        elif isinstance(request, Armor):
            super().add_modifier(FoundArmor(self.Map, self.admin, self.MC))
        super().handle(request)


class FoundWeapon(AbstractHandler):
    def handle(self, request) -> None:
        WEAPON_TEXT = (
            ' To Pick It Enter "Pick", To Drop It Enter "Drop",'
            ' To See Weapon Description Enter "Description"\n'
        )
        print(
            Fore.YELLOW + f"You Found Weapon {request.name}," + WEAPON_TEXT,
            Style.RESET_ALL,
        )

        res = input()
        while res != "Drop":
            if res == "Pick":
                self.MC.pick_weapon(request)
                request = 0
                break
            elif res == "Description":
                request.show_status()
                res = input()
            else:
                print(Fore.RED + "Wrong Input, Try Again", Style.RESET_ALL)
                res = input()
        super().handle(request)


class FoundArmor(AbstractHandler):
    def handle(self, request) -> None:
        ARMOR_TEXT = (
            ' To Pick It Enter "Pick", To Drop It Enter "Drop",'
            ' To See Armor Description Enter "Description"\n'
        )
        print(
            Fore.YELLOW + f"You Found Armor {request.name}," + ARMOR_TEXT,
            Style.RESET_ALL,
        )

        res = input()
        while res != "Drop":
            if res == "Pick":
                self.MC.pick_armor(request)
                request = 0
                break
            elif res == "Description":
                request.show_status()
                res = input()
            else:
                print(Fore.RED + "Wrong Input, Try Again", Style.RESET_ALL)
                res = input()
        super().handle(request)


class FoundMonster(AbstractHandler):
    def handle(self, request) -> None:
        if isinstance(request, Monster):
            print(
                Fore.YELLOW + f"You Were Attaked by {request.name}\n", Style.RESET_ALL
            )
            self.MC.battle(request)
            super().handle(request)


class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass


class Move(Command):
    def __init__(
        self, direction: str, MC: Hero, Map: list, admin: str = "NO_RIGHTS"
    ) -> None:
        self.direction = direction
        self.MC = MC
        self.Map = Map
        self.admin = admin

        if self.direction == "N":
            self.reverse = "S"
        elif self.direction == "S":
            self.reverse = "N"
        elif self.direction == "E":
            self.reverse = "W"
        elif self.direction == "W":
            self.reverse = "E"

    def execute(self) -> None:
        chain_creator = AbstractHandler(self.Map, self.admin, self.MC)
        chain_creator.add_modifier(MoveInChain(self.Map, self.admin, self.MC))
        chain_creator.add_modifier(CheckCell(self.Map, self.admin, self.MC))
        chain_creator.handle(self.direction)

    def undo(self) -> None:
        self.MC.move(self.reverse, self.Map, "ADMIN_RIGHTS")


class Help(Command):
    def __init__(self) -> None:
        self.text_1 = (
            '\nMove: Enter "N", "W", "E", "S" Keys to Move\n'
            'ShowStatus: Enter "Status" to See Your Current Status\n'
            'RoomDescription: Enter "R" to See Current Room Description\n'
            'DungeonMap: Enter "Map" to See All Dungeon Rooms\n'
            'WeaponStatus: Enter "Weapon" to See Your Weapon Characteristics\n'
            'ArmorStatus: Enter "Armor" to See Your Armor Characteristics\n'
            'ShowBestiary: Enter "Bestiary" to See All Monsters List\n'
            'ShowStock: Enter "Stock" to See All Items List\n'
            'QuitGame: Enter "Quit"to Leave the Game\n'
            'UndoMove: Enter "U" to Undo Last Command'
        )

        self.text_2 = (
            'After Calling "Map" Command You Will See Blocks With Cells\nEach of Theme'
            " Will Contain 0 or Red 1 or Blue 1, \nWhere Cells With 0 are Empty,"
            " Cells With Red 1 Contain Monster,\nCells With Blue 1 Contain Armor or Weapon\n"
        )

    def execute(self) -> None:
        print(Fore.YELLOW + self.text_1)
        print(self.text_2, Style.RESET_ALL)


class ShowStatus(Command):
    def __init__(self, MC: Hero) -> None:
        self.MC = MC

    def execute(self) -> None:
        self.MC.show_status()


class ShowRoom(Command):
    def __init__(self, MC: Hero) -> None:
        self.MC = MC

    def execute(self) -> None:
        self.MC.current_room.show_description()
        self.MC.current_room.show_interior(
            self.MC.room_position_x, self.MC.room_position_y
        )


class ShowMap(Command):
    def __init__(self, MC: Hero, Map: list) -> None:
        self.MC = MC
        self.Map = Map

    def execute(self) -> None:
        Room.show_map(
            self.Map,
            self.MC.current_room.global_position_x,
            self.MC.current_room.global_position_y,
            self.MC.room_position_x,
            self.MC.room_position_y,
        )


class ShowWeapon(Command):
    def __init__(self, MC: Hero) -> None:
        self.MC = MC

    def execute(self) -> None:
        print(Fore.YELLOW + "\nYour Weapon Description:", Style.RESET_ALL)
        self.MC.weapon.show_status()


class ShowArmor(Command):
    def __init__(self, MC: Hero) -> None:
        self.MC = MC

    def execute(self) -> None:
        print(Fore.YELLOW + "\nYour Armor Description:", Style.RESET_ALL)
        self.MC.armor.show_status()


class ShowBestiary(Command):
    def execute(self) -> None:
        Monster.show_bestiary()


class ShowStock(Command):
    def execute(self) -> None:
        Item.show_stock()


class Quit(Command):
    def execute(self) -> Exception:
        raise QuitGame


class Wrong(Command):
    def execute(self) -> None:
        print(Fore.RED + "Wrong Input, Choose Command From Help", Style.RESET_ALL)


class Invoker:
    _current_command = None

    def __init__(self) -> None:
        self._history = []

    def add_command(self, command: Command) -> None:
        self._history.append(command)

    def remove_command(self) -> Command:
        if self._history != []:
            return self._history.pop()
        else:
            raise EmptyHistory

    def set_command(self, command: Command) -> None:
        self._current_command = command
        if isinstance(command, Move):
            self.add_command(command)

    def perform_command(self) -> None:
        if isinstance(self._current_command, Command):
            self._current_command.execute()

    def undo_command(self) -> None:
        res_com = self.remove_command()
        res_com.undo()


class CommandExecuter:
    def __init__(self, MC: Hero, Map: list) -> None:
        self.MC = MC
        self.Map = Map
        self.invoker = Invoker()

    def check_command(self, insert: str) -> None:
        if insert == "Help":
            self.invoker.set_command(Help())
            self.invoker.perform_command()
        elif insert == "N" or insert == "W" or insert == "E" or insert == "S":
            try:
                self.invoker.set_command(Move(insert, self.MC, self.Map))
                self.invoker.perform_command()
            except CannotLeave as error:
                if error.args[0] == 1:
                    print(Fore.RED + error.message_1, Style.RESET_ALL)
                else:
                    print(Fore.RED + error.message_2, Style.RESET_ALL)
                self.invoker.remove_command()
        elif insert == "Status":
            self.invoker.set_command(ShowStatus(self.MC))
            self.invoker.perform_command()
        elif insert == "R":
            self.invoker.set_command(ShowRoom(self.MC))
            self.invoker.perform_command()
        elif insert == "Map":
            self.invoker.set_command(ShowMap(self.MC, self.Map))
            self.invoker.perform_command()
        elif insert == "Weapon":
            self.invoker.set_command(ShowWeapon(self.MC))
            self.invoker.perform_command()
        elif insert == "Armor":
            self.invoker.set_command(ShowArmor(self.MC))
            self.invoker.perform_command()
        elif insert == "Bestiary":
            self.invoker.set_command(ShowBestiary())
            self.invoker.perform_command()
        elif insert == "Stock":
            self.invoker.set_command(ShowStock())
            self.invoker.perform_command()
        elif insert == "Quit":
            self.invoker.set_command(Quit())
            self.invoker.perform_command()
        elif insert == "U":
            try:
                self.invoker.undo_command()
            except EmptyHistory as error:
                print(Fore.RED + error.message, Style.RESET_ALL)
        elif insert == "":
            pass
        else:
            self.invoker.set_command(Wrong())
            self.invoker.perform_command()
