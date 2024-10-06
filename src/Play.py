from src.character import Hero
from src.Room import Room
import src.Command as Commands
import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = (
    "hide"  # Its for The Print Which Pygame Automatically do After Being Imported
)
from pygame import mixer
from colorama import Fore, Back, Style


class StartGame:
    def __init__(self) -> None:
        mixer.init()
        self.start_screen()
        self.prepare_screen()
        self.game_loop()

    def input_map_size(self) -> None:
        self.map_size = input("Choose Dungeon Size[(9), (25), (49), (81)]: ").strip()

        if self.map_size.isdigit():
            self.map_size = int(self.map_size)
        while (
            self.map_size != 9
            and self.map_size != 25
            and self.map_size != 49
            and self.map_size != 81
        ):
            print(Fore.RED + "Wrong Input, Try Again", Style.RESET_ALL)
            self.map_size = input(
                "Choose Dungeon Size[(9), (25), (49), (81)]: "
            ).strip()
            if self.map_size.isdigit():
                self.map_size = int(self.map_size)

    def input_difficulty(self) -> None:
        self.difficulty = input("Choose Difficulty[(E)asy, (M)edium, (H)ard]: ").strip()

        while (
            self.difficulty != "E" and self.difficulty != "M" and self.difficulty != "H"
        ):
            print(Fore.RED + "Wrong Input, Try Again", Style.RESET_ALL)
            self.difficulty = input(
                "Choose Difficulty[(E)asy, (M)edium, (H)ard]: "
            ).strip()

    def set_music(self, volume: float, path: str) -> None:
        mixer.music.load(path)
        mixer.music.set_volume(volume)
        mixer.music.play()

    def create_character(self) -> None:
        print(Fore.YELLOW + "Create Your Character\n", Style.RESET_ALL)
        name = input("Enter Your Name: ").strip()

        age = input("Enter Your Age: ").strip()
        while age.isdigit() != True:
            print(Fore.RED + "Wrong Input, Try Again", Style.RESET_ALL)
            age = input("Enter Your Age: ").strip()

        gender = input("Enter Your Gender[(M)ale/(F)emale]: ").strip()
        while gender != "M" and gender != "F":
            print(Fore.RED + "Wrong Input, Try Again", Style.RESET_ALL)
            gender = input("Enter Your Gender[(M)ale/(F)emale]: ").strip()
        if gender == "M":
            gender = "Male"
        else:
            gender = "Female"

        profession = input(
            "Choose Character Profession[(M)age, (K)night, (A)rcher]: "
        ).strip()
        while profession != "M" and profession != "K" and profession != "A":
            print(Fore.RED + "Wrong Input, Try Again", Style.RESET_ALL)
            profession = input(
                "Choose Character Profession[(M)age, (K)night, (A)rcher]: "
            ).strip()

        self.MC = Hero.create_hero(name, gender, profession, age)  # MC = MainCharacter

    def start_screen(self) -> None:
        MUSIC_VOLUME = 0.7
        PATH = "Music/Start/Mysterious_Grotto.mp3"
        START_TEXT = "\033[1m" + "Welcome to Dungeon and Mysteries Adventure Game\n"

        os.system("clear")  # Clear The Screen
        self.set_music(MUSIC_VOLUME, PATH)

        print(
            Fore.RED + START_TEXT.center(os.get_terminal_size().columns),
            Style.RESET_ALL,
        )

        self.create_character()

        print(Fore.YELLOW + "\nCreate Dungeon\n", Style.RESET_ALL)
        self.input_map_size()
        self.input_difficulty()

        self.MC.show_status()

        print(
            Fore.YELLOW + 'If You Want to See the Commands List Enter "Help"\n',
            Style.RESET_ALL,
        )

        print(Fore.YELLOW + 'Enter "Start" to Start the Adventure\n', Style.RESET_ALL)

        self.Map = Room.create_map(self.map_size, self.difficulty)

        self.receiver = Commands.CommandExecuter(self.MC, self.Map)

        res = input()
        while res == "Help" or res != "Start":
            if res != "Start" and res != "Help":
                print(Fore.RED + "Wrong Input, Try Again", Style.RESET_ALL)
                res = input()
            elif res == "Help":
                self.receiver.check_command(res)
                res = input()

    def prepare_screen(self) -> None:
        MUSIC_VOLUME = 0.7
        PATH = "Music/Start/Survivors_Bivouac.mp3"
        START_TEXT = "\033[1m" + "Welcome to Dungeon and Mysteries Adventure Game\n"

        os.system("clear")
        print(
            Fore.RED + START_TEXT.center(os.get_terminal_size().columns),
            Style.RESET_ALL,
        )

        mixer.music.stop()
        self.set_music(MUSIC_VOLUME, PATH)

    def game_loop(self) -> None:
        try:
            while True:
                insert = input()
                self.receiver.check_command(insert)
        except Commands.QuitGame as error:
            print(Fore.RED + error.message, Style.RESET_ALL)


if __name__ == "__main__":
    StartGame()
