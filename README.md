# Python Dungeon RPG

## Table of Contents
- [Python Dungeon RPG](#python-dungeon-rpg)
  - [Table of Contents](#table-of-contents)
  - [Gameplay](#gameplay)
  - [Installation (Linux)](#installation-linux)
  - [Running the Program](#running-the-program)
  - [Project Structure](#project-structure)
    - [Source Code Files](#source-code-files)
    - [Additional Resources](#additional-resources)
  - [UML Diagram](#uml-diagram)

## Gameplay

In this game, the player creates a character that must escape from a dungeon filled with various monsters and items. There are three available classes: **Archer**, **Mage**, and **Knight**—each with its own unique characteristics and items.

- **Monsters:** They will attack the hero when he gets close, attempting to kill him. 
- **Experience & Leveling Up:** The hero gains experience by defeating monsters, with stronger monsters providing more experience. Leveling up enhances the hero’s attributes, making it easier to face tougher enemies.
- **Dungeon:** The player can choose the size of the dungeon, which must be a square with an odd number of rooms. The standard dungeon consists of 25 interconnected rooms.
- **Objective:** The hero spawns in the center of the map and must clear a series of rooms to progress. After clearing the required rooms and escaping the dungeon, the player wins the game.


## Installation (Linux)

Follow these steps to install and run the game on a Linux system:

1. **Install Python 3.8**
    - Open Terminal and run the following commands:
    ```bash
    sudo apt-get update
    sudo apt-get install python3.8
    ```

2. **Install required modules (Colorama & Pygame)**
    - In the terminal, install the necessary Python libraries:
    ```bash
    sudo apt-get install python3-colorama
    sudo apt-get install python3-pygame
    ```

3. **Clone the repository**
    - Clone the project repository to your local machine:
    ```bash
    git clone https://github.com/levante00/python-rpg.git
    ```

## Running the Program

Once the installation is complete, run the program using the following steps:

1. Navigate to the project directory:
    ```bash
    cd python-rpg
    ```

2. Run the game by executing:
    ```bash
    python3 main.py
    ```

## Project Structure

### Source Code Files

- `src/Play.py`: Handles the game interface, user input, and the main game loop.
- `main.py`: Entry point for running the game. It calls the `Play.py` file.
- `/src`: Directory containing the main source code files.
  - `src/Command.py`: Implements the Command and Chain of Responsibility design patterns.
  - `src/Enemy.py`: Contains the Monster class.
  - `src/Items.py`: Contains the Item, Weapon, and Armor classes.
  - `src/character.py`: Implements the Hero class.
  - `src/Room.py`: Defines the Room class.

### Additional Resources

- `/Data`: Contains .txt files with room names, music titles for rooms and battle scenes.
- `/UML_Diagrams`: Includes UML diagrams in .jpg format.
- `/Music`: Directory with .mp3 music files for the game.
  - `/Music/Battle`: Music files played during battles.
  - `/Music/Ending`: Music files for win/lose scenarios.
  - `/Music/Rooms`: Music files for when the hero is inside a room.
  - `/Music/Start`: Music files played at the start of the game.

## UML Diagram
![Alt text]( UML_Diagrams/Class_Diagram.jpg "Class Diagram:")