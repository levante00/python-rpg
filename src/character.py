from __future__ import annotations
import random
import sys
from src.Items import *
from colorama import Fore, Style
from src.Room import *
from src.Enemy import Monster, MonsterDeath
from src.ascii_art import AsciiArt
import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = (
    "hide"  # Its for The Print Which Pygame Automatically do After Being Imported
)
from pygame import mixer
import time


class CannotLeave(Exception):
    def __init__(
        self,
        index,
        message_1="You Can not Move to The Next Room Until You Do not Clear Current Room",
        message_2="You Can not Move This Way, There is a Wall",
    ) -> None:
        self.message_1 = message_1
        self.message_2 = message_2
        self.index = index

    def __str__(self) -> str:
        return "User used move command which caused leaving Map or Room arrays"


class Hero:
    """Class of the game characters"""

    exp_limit = 10

    def __init__(
        self,
        name: str,
        age: int,
        gender: str,
        profession: str,
        health: int,
        attack: int,
        agility: int,
        defense: int,
        intelligence: int,
        weapon: Weapon,
        armor: Armor,
        current_room: Room = room1,
        level: int = 1,
        experience: int = 0,
        position_x: int = 0,
        position_y: int = 0,
        room_position_x: int = 4,
        room_position_y: int = 4,
    ) -> None:
        self.name = name
        self.age = age
        self.gender = gender
        self.profession = profession
        self.level = level
        self.experience = experience
        self.position_x = position_x  # Hero X Cooridnate in Global Coordinates
        self.position_y = position_y  # Hero Y Coordinate in Global Coordinates
        self.current_room = current_room
        self.room_position_x = room_position_x  # Hero X Coordinate in The Current Room
        self.room_position_y = room_position_y  # Hero Y Coordinate in The Current Room
        self.weapon = weapon
        self.armor = armor
        self.health = health
        self.attack = attack
        self.agility = agility
        self.defense = defense
        self.intelligence = intelligence

    def show_status(self) -> None:
        """Prints Heroes attributes"""
        TEXT_1 = "\nYour Character Status: "
        TEXT_2 = (
            f"Name: {self.name}\nAge: {self.age}\n"
            f"Gender: {self.gender}\nProfession: {self.profession}\n"
            f"Level: {self.level}\nExperience: {self.experience}\n"
            f"Room: {self.current_room.name}\nPosition: {(self.position_x, self.position_y)}\n"
            f"Weapon: {self.weapon.name}\nArmor: {self.armor.name}\n"
            f"Health: {self.health}\nAttack: {self.attack}\n"
            f"Agility: {self.agility}\nDefence: {self.defense}\n"
            f"Inteligence: {self.intelligence}\n"
        )

        print(Fore.YELLOW + TEXT_1, Style.RESET_ALL)
        print(Fore.BLUE + TEXT_2, Style.RESET_ALL)

    def level_up(self) -> None:
        """Used after defeating the monster and gaining his EXP.
        Increases heroes attributes by given number"""
        EXP_LIMIT_MULTIPLAYER = 2
        while self.experience >= Hero.exp_limit:
            self.level += 1
            self.experience = self.experience - Hero.exp_limit
            Hero.exp_limit *= EXP_LIMIT_MULTIPLAYER
            self.attribute_increase(10, 1, 1, 1, 1, 0)

    def death(self) -> None:
        """End the game and closes the game loop if Heroes HP <= 0"""
        SLEEP_CONST = 6
        MUSIC_VOLUME = 0.9
        if self.health <= 0:
            AsciiArt.death_print()

            mixer.music.stop()
            mixer.music.load("Music/Ending/You_Died.mp3")
            mixer.music.set_volume(MUSIC_VOLUME)
            mixer.music.play()

            time.sleep(SLEEP_CONST)

            sys.exit()

    def win(self) -> None:
        SLEEP_CONST = 3
        MUSIC_VOLUME = 0.9
        AsciiArt.win_print()
        mixer.music.stop()
        mixer.music.load("Music/Ending/Win.mp3")
        mixer.music.set_volume(MUSIC_VOLUME)
        mixer.music.play()

        time.sleep(SLEEP_CONST)
        sys.exit()

    def attribute_increase(
        self,
        health: int,
        attack: int,
        agility: int,
        defense: int,
        intelligence: int,
        experience: int,
    ) -> None:

        self.health += health
        self.attack += attack
        self.agility += agility
        self.defense += defense
        self.intelligence += intelligence
        self.experience += experience
        self.level_up()

    def attribute_decrease(
        self, health: int, attack: int, agility: int, defense: int, intelligence: int
    ) -> None:

        self.health -= health
        self.attack -= attack
        self.agility -= agility
        self.defense -= defense
        self.intelligence -= intelligence
        self.death()

    def deal_damage(self, enemy: Monster) -> None:
        EVASION_DEV = 100
        EVASION_MULT = 0.5
        DEF_PERCENT = 10
        INT_PERCENT = 10

        # Evasion Chance Depending on Agility
        if random.random() >= ((enemy.agility / EVASION_DEV) * EVASION_MULT):
            if self.profession == "Knight":
                extra_damage = (self.defense) % (DEF_PERCENT)
            elif self.profession == "Mage":
                extra_damage = (self.intelligence) % (INT_PERCENT)
            elif self.profession == "Archer":
                extra_damage = self.agility

            # Damage Being Dealed to Enemy Depending on Hero Attack and Enemy Defence
            damage = abs((random.randint(0, self.attack)) - (enemy.defense % 10))
            enemy.gain_damage(self, damage)
            print(f"You Deal {damage} Damage to {enemy.name}")
        else:
            print(f"{enemy.name} Dogded the Attack")

    def pick_weapon(self, weapon: Weapon) -> None:
        REQ_LEVEL_TEXT = f"You do not have Required Level: {weapon.level_required}"
        REQ_PROF_TEXT = (
            f"You do not have Required Profession: {weapon.profession_required}"
        )

        if (
            self.level >= weapon.level_required
            and self.profession == weapon.profession_required
        ):
            if weapon.attack - self.weapon.attack > 0:
                self.attribute_increase(
                    0, weapon.attack - self.weapon.attack, 0, 0, 0, 0
                )
            else:
                self.attribute_decrease(0, self.weapon.attack - weapon.attack, 0, 0, 0)

            if weapon.agility - self.weapon.agility > 0:
                self.attribute_increase(
                    0, 0, weapon.agility - self.weapon.agility, 0, 0, 0
                )
            else:
                self.attribute_decrease(
                    0, 0, self.weapon.agility - weapon.agility, 0, 0
                )

            if weapon.intelligence - self.weapon.intelligence > 0:
                self.attribute_increase(
                    0, 0, 0, 0, weapon.intelligence - self.weapon.intelligence, 0
                )
            else:
                self.attribute_decrease(
                    0, 0, 0, 0, self.weapon.intelligence - weapon.intelligence
                )

            self.weapon = weapon
            self.show_status()
            # Removing Picked Weapon from Current Room Attribute
            self.current_room.items.remove(
                self.current_room.interior[self.room_position_y][self.room_position_x]
            )
            # Removing Picked Weapon from Map and Current Room Interior
            self.current_room.interior[self.room_position_y][self.room_position_x] = 0
        else:
            if self.level < weapon.level_required:
                print(Fore.RED + REQ_LEVEL_TEXT, Style.RESET_ALL)
            else:
                print(Fore.RED + REQ_PROF_TEXT, Style.RESET_ALL)

    def pick_armor(self, armor: Armor) -> None:
        REQ_LEVEL_TEXT = f"You do not have Required Level: {armor.level_required}"
        REQ_PROF_TEXT = (
            f"You do not have Required Profession: {armor.profession_required}"
        )

        if (
            self.level >= armor.level_required
            and self.profession == armor.profession_required
        ):
            if armor.agility - self.armor.agility > 0:
                self.attribute_increase(
                    0, 0, armor.agility - self.armor.agility, 0, 0, 0
                )
            else:
                self.attribute_decrease(0, 0, self.armor.agility - armor.agility, 0, 0)

            if armor.defense - self.armor.defense > 0:
                self.attribute_increase(
                    0, 0, 0, armor.defense - self.armor.defense, 0, 0
                )
            else:
                self.attribute_decrease(0, 0, 0, armor.defense - self.armor.defense, 0)

            if armor.intelligence - self.armor.intelligence > 0:
                self.attribute_increase(
                    0, 0, 0, 0, armor.intelligence - self.armor.intelligence, 0
                )
            else:
                self.attribute_decrease(
                    0, 0, 0, 0, self.armor.intelligence - armor.intelligence
                )
            self.armor = armor
            self.show_status()
            # Removing Picked Armor from Current Room Attribute
            self.current_room.items.remove(
                self.current_room.interior[self.room_position_y][self.room_position_x]
            )
            # Removing Picked Weapon from Map and Current Room Interior
            self.current_room.interior[self.room_position_y][self.room_position_x] = 0
        else:
            if self.level < armor.level_required:
                print(Fore.RED + REQ_LEVEL_TEXT, Style.RESET_ALL)
            else:
                print(Fore.RED + REQ_PROF_TEXT, Style.RESET_ALL)

    def battle(self, enemy: Monster) -> None:
        MUSIC_VOLUME = 0.7
        NEXT_ATTACK_TIME = 0.5
        attack_res = 0
        file3 = open("Data/BattleMusic.txt", "r")
        BattleMusic = random.choices(file3.read().splitlines(), k=1)
        file3.close()
        mixer.music.stop()
        mixer.music.load("Music/Battle/" + BattleMusic[0])
        mixer.music.set_volume(MUSIC_VOLUME)
        mixer.music.play()
        while True:
            if attack_res % 2 == 0:
                print(
                    Fore.YELLOW + 'It is Your Turn to Attack, Enter "A" to Attack',
                    Style.RESET_ALL,
                )
                res = input()
                while res != "A":
                    print(
                        Fore.RED + 'Wrong Input, Enter "A" to Attack', Style.RESET_ALL
                    )
                    res = input()
                try:
                    self.deal_damage(enemy)
                except MonsterDeath as error:
                    print(Fore.YELLOW + error.message, Style.RESET_ALL)
                    # Removing Death Monster from Current Room Attribute
                    self.current_room.monsters.remove(
                        self.current_room.interior[self.room_position_y][
                            self.room_position_x
                        ]
                    )
                    # Removing Death Monster from Map and Current Room Interior
                    self.current_room.interior[self.room_position_y][
                        self.room_position_x
                    ] = 0
                    self.current_room.show_interior(
                        self.room_position_x, self.room_position_y
                    )
                    break
                attack_res += 1
            else:
                print(
                    Fore.YELLOW + f"It is {enemy.name} Turn to Attack", Style.RESET_ALL
                )
                time.sleep(NEXT_ATTACK_TIME)
                enemy.deal_damage(self)
                attack_res += 1
        mixer.music.stop()
        mixer.music.load(self.current_room.music)
        mixer.music.set_volume(MUSIC_VOLUME)
        mixer.music.play()

    def move(self, direction: str, Map: list, admin: str = "NO_RIGHTS") -> None:
        NEW_ROOM_TEXT = "You Entered New Room"
        WRONG_INPUT_TEXT = "Wrong input, choose from (N)orth, (S)outh, (E)ast, (W)est"
        MUSIC_VOLUME = 0.7
        SLEEP_CONST_1 = 0.2
        SLEEP_CONST_2 = 3

        if direction == "N":
            self.position_y += 1
            # If Hero is Next to The Door Change The Room
            if (
                self.room_position_x == self.current_room.size // 2
                and self.room_position_y == 0
            ):
                if self.current_room.monsters != [] and admin == "NO_RIGHTS":
                    self.position_y -= 1
                    raise CannotLeave(1)
                elif (
                    self.current_room.global_position_y == int(len(Map) ** (1 / 2)) // 2
                ):
                    self.win()
                else:
                    for room in Map:
                        if (
                            self.current_room.global_position_x
                            == room.global_position_x
                            and self.current_room.global_position_y
                            == room.global_position_y - 1
                        ):

                            self.current_room = room
                            print(Fore.YELLOW + NEW_ROOM_TEXT, Style.RESET_ALL)
                            self.current_room.show_description()
                            self.room_position_y = self.current_room.size - 1
                            self.room_position_x = self.current_room.size // 2
                            self.current_room.show_interior(
                                self.room_position_x, self.room_position_y
                            )
                            mixer.music.stop()
                            mixer.music.load(self.current_room.music)
                            mixer.music.set_volume(MUSIC_VOLUME)
                            mixer.music.play()
                            break
            else:
                if self.room_position_y == 0:
                    self.position_y -= 1
                    raise CannotLeave(2)
                else:
                    self.room_position_y -= 1

        elif direction == "S":
            self.position_y -= 1
            # If Hero is Next to The Door Change The Room
            if (
                self.room_position_x == self.current_room.size // 2
                and self.room_position_y == self.current_room.size - 1
            ):
                if self.current_room.monsters != [] and admin == "NO_RIGHTS":
                    self.position_y += 1
                    raise CannotLeave(1)
                elif self.current_room.global_position_y == -(
                    int(len(Map) ** (1 / 2)) // 2
                ):
                    self.win()
                else:
                    for room in Map:
                        if (
                            self.current_room.global_position_x
                            == room.global_position_x
                            and self.current_room.global_position_y
                            == room.global_position_y + 1
                        ):

                            self.current_room = room
                            print(Fore.YELLOW + NEW_ROOM_TEXT, Style.RESET_ALL)
                            self.current_room.show_description()
                            self.room_position_y = 0
                            self.room_position_x = self.current_room.size // 2
                            self.current_room.show_interior(
                                self.room_position_x, self.room_position_y
                            )
                            mixer.music.stop()
                            mixer.music.load(self.current_room.music)
                            mixer.music.set_volume(MUSIC_VOLUME)
                            mixer.music.play()
                            break
            else:
                if self.room_position_y == self.current_room.size - 1:
                    self.position_y += 1
                    raise CannotLeave(2)
                else:
                    self.room_position_y += 1

        elif direction == "E":
            self.position_x += 1
            # If Hero is Next to The Door Change The Room
            if (
                self.room_position_x == self.current_room.size - 1
                and self.room_position_y == self.current_room.size // 2
            ):
                if self.current_room.monsters != [] and admin == "NO_RIGHTS":
                    self.position_x -= 1
                    raise CannotLeave(1)
                elif (
                    self.current_room.global_position_x == int(len(Map) ** (1 / 2)) // 2
                ):
                    self.win()
                else:
                    for room in Map:
                        if (
                            self.current_room.global_position_x
                            == room.global_position_x - 1
                            and self.current_room.global_position_y
                            == room.global_position_y
                        ):

                            self.current_room = room
                            print(Fore.YELLOW + NEW_ROOM_TEXT, Style.RESET_ALL)
                            self.current_room.show_description()
                            self.room_position_y = self.current_room.size // 2
                            self.room_position_x = 0
                            self.current_room.show_interior(
                                self.room_position_x, self.room_position_y
                            )
                            mixer.music.stop()
                            mixer.music.load(self.current_room.music)
                            mixer.music.set_volume(MUSIC_VOLUME)
                            mixer.music.play()
                            break
            else:
                if self.room_position_x == self.current_room.size - 1:
                    self.position_x -= 1
                    raise CannotLeave(2)
                else:
                    self.room_position_x += 1

        elif direction == "W":
            self.position_x -= 1
            # If Hero is Next to The Door Change The Room
            if (
                self.room_position_x == 0
                and self.room_position_y == self.current_room.size // 2
            ):
                if self.current_room.monsters != [] and admin == "NO_RIGHTS":
                    self.position_x += 1
                    raise CannotLeave(1)
                elif self.current_room.global_position_x == -(
                    int(len(Map) ** (1 / 2)) // 2
                ):
                    self.win()
                else:
                    for room in Map:
                        if (
                            self.current_room.global_position_x
                            == room.global_position_x + 1
                            and self.current_room.global_position_y
                            == room.global_position_y
                        ):

                            self.current_room = room
                            print(Fore.YELLOW + NEW_ROOM_TEXT, Style.RESET_ALL)
                            self.current_room.show_description()
                            self.room_position_y = self.current_room.size // 2
                            self.room_position_x = self.current_room.size - 1
                            self.current_room.show_interior(
                                self.room_position_x, self.room_position_y
                            )
                            mixer.music.stop()
                            mixer.music.load(self.current_room.music)
                            mixer.music.set_volume(MUSIC_VOLUME)
                            mixer.music.play()
                            break
            else:
                if self.room_position_x == 0:
                    self.position_x += 1
                    raise CannotLeave(2)
                else:
                    self.room_position_x -= 1
        else:
            print(Fore.RED + WRONG_INPUT_TEXT, Style.RESET_ALL)

    @classmethod
    def create_hero(self, name: str, gender: str, profession: str, age: int) -> Hero:
        """Used for creating Hero class character at the start of the game"""
        # HEALTH, ATTACK, AGILITY, DEFENSE, INTELLIGENCE
        MAGE = [50, 10, 3, 3, 12]
        ARCHER = [70, 8, 12, 5, 3]
        KNIGHT = [100, 12, 5, 12, 1]

        if profession == "M":
            MC = Hero(
                name,
                age,
                gender,
                "Mage",
                MAGE[0],
                MAGE[1],
                MAGE[2],
                MAGE[3],
                MAGE[4],
                arms,
                shirt,
            )
        elif profession == "K":
            MC = Hero(
                name,
                age,
                gender,
                "Knight",
                KNIGHT[0],
                KNIGHT[1],
                KNIGHT[2],
                KNIGHT[3],
                KNIGHT[4],
                arms,
                shirt,
            )
        elif profession == "A":
            MC = Hero(
                name,
                age,
                gender,
                "Archer",
                ARCHER[0],
                ARCHER[1],
                ARCHER[2],
                ARCHER[3],
                ARCHER[4],
                arms,
                shirt,
            )

        return MC
