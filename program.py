# from threading import Timer
# from collections import namedtuple
from time import sleep
import quests
import data
import shop
import inventory
import os
from essentials import *
import world

# latest update: added ryan as a boss
# still need to add burnt popcorn


# naming convention as follows:
# RELEASE.BIGUPDATE.Small (BUILD)
build = data.load_version()
print("Version 0.9.0 (Build {})".format(build))

# uncomment this during development to increase build number. comment for full release
data.save_version(build)

"""
def test():
  print("whats poppin")

t = Timer(5.0, test)
t.start()
print("does it continue tho")
"""


#  we are no longer using namedtuples they gay
# Player = namedtuple("Player", "name weapon quest health max_health defence completed")


# The Player Class
class Player:
    def __init__(self, name, weapon, quest, health, defence, crit_chance=10):
        self.name = name
        self.weapon = weapon
        self.quest = quest
        self.health = health
        self.max_health = health
        self.defence = defence
        self.completed = []
        self.xp = 0
        self.level = 1
        self.inventory = {"Test Item": 100, "bread": 3}  # TODO The actual v.1.0 release should remove this
        self.money = 0

        self.crit_chance = crit_chance
        self.debugEnabled = False
        self.traits = []  # this will hold traits that, if had, activate special things. ex: having "cute" could
        #                   dull an enemy's senses or something. maybe lower attack
        self.metadata = []


    def debug(self):
        self.quest = input("Set new Quest: ")
        self.money += int(input("Set Money: "))
        self.health = 9999
        self.max_health = 9999
        self.level = int(input("Set level: "))
        self.xp = int(input("Set XP:"))
        choice = input("New Item? ")
        amount = int(input("New Value? "))
        self.metadata.append(input("Metadata?").strip())
        self.inventory.update({choice: amount})
        self.debugEnabled = True

    def xp_check(self):
        original = self.level
        level_up = 80 * self.level + (100 * .05 * self.level)
        hp_gain = 0
        while self.xp >= level_up:
            self.level += 1
            hp_gain += int(10 + .1*self.level)
            level_up = 80 * self.level + (100 * .05 * self.level)
        self.max_health += hp_gain
        self.health += 5
        if self.level != original:
            print("Level up! You are at level {}. Gained {} HP from leveling!".format(self.level, hp_gain))
            print("{} XP away from next level.".format(level_up - self.xp))


# broken thing below
# quest_dict = {"Clap the Dragon": quests.clap_the_dragon(player), "Mess with Turtles": quests.battle_turtles(player,5 )}
# TODO: optimize how quests are run, bc the current system is not sustainable for long term


def main():
    print_header()
    # player = start_choice()
    player = start()
    if not player:
        player = start_choice()
    info(player)
    sleep(1)
    active = True

    while active:
        option = menu()
        # Quest Option
        if option == "quest":
            if player.quest:  # check that a quest exists
                confirm = input("Start quest?: {} (y/n) \n>>>".format(player.quest))
                if confirm.find("y") != -1:
                    # TODO: make a good system for this, cuz 2 lines of extra elifs per quest cant be great
                    # if player.quest == "Clap the Dragon":
                    #     quests.clap_the_dragon(player)
                    if player.quest == "Dab on Turtles":
                        quests.battle_turtles(player, 3)
                    elif player.quest == "Beat up the Developer":
                        quests.beat_the_dev(player)
                    elif player.quest == "Mess with Goblins":
                        quests.mess_with_goblins(player)
                    elif player.quest == "Ryan's Battle":  # test battle - only accessable via debug mode
                        quests.ryans_battle(player)
                    elif player.quest == "Defeat Ryan":
                        quests.defeat_ryan(player)
                    elif player.quest == "Defeat the Outlaws":
                        quests.defeat_outlaws(player)
                    else:
                        print("You don't have a quest!")
                else:
                    print("ok then be that way man all this work i do to launch quests and u be that way ok cool")
            else:
                print("You don't have a quest! Go find one before trying to start! There may be some in town...")

        # Inventory Option
        elif option == "inventory":
            inventory.use_item(player)

        # Shop Option
        elif option == "shop":
            shop.shop(player)

        # Player Info
        elif option == "player":
            info(player)

        # Debug mode
        elif option == "debug":
            player.debug()

        # World Option
        elif option == "world":
            world.world_init(player)
            selection = world.select_world()
            if selection == "Test World":
                world.test_world(player)
            elif selection == "Start Town":
                world.start_world(player)
            elif selection == "Topshelf":
                world.topshelf(player)
            elif selection == "Ptonio" and "Ptonio" in player.metadata:
                world.ptonio(player)

        # Save the game!
        elif option == "save":
            data.save(player)
            data.save_settings(settings)
            print("[!] Saved game!")

        # I NEED HELP!!!
        elif option == "help":
            game_help()

        # Set some tings
        elif option == "settings":
            change_settings()

        # Exit Option
        elif option == "exit":
            # print("See ya later!")
            data.save(player)
            data.save_settings(settings)
            active = False
            # break


def print_header():
    print("--------------------------------------")
    print("|        The adventure of uh         |")
    print("|             UNKOWNLAND             |")
    print("|   another quality text based rpg   |")
    print("--------------------------------------")


# TODO: it could still be better
def start_choice():
    sleep(2)
    name = input("-[???] wuz yo name, nibba? \n>>>").strip()
    if name.lower().find("steve") == -1:
        talk("- oh, it's {}. sounds pretty stupid but ok".format(name),2)
    else:
        talk("- aight, yo name's {}. cool name".format(name),2)  # haha cuz he name steve
    talk("-[steve] oh by the way, the name's steve. yeah. lowercase. got a problem? no? ok.",3)
    talk("- so let's get to business. you're gonna need to learn to fight so ima let you throw some punches", 4)

    player = Player(name, "Fists", None, 100, 10)
    quests.tutorial_mission(player)

    talk("- anyways you need a weapon b. i've got this broken sword if you want. here nibba.", 2.5)
    player.weapon = "Rusty Sword"
    print("[!] Equipped Rusty Sword!")
    sleep(.25)
    talk("- now go dab on them turtle nerds. they need a good beatin.", 2)
    talk("- and once you're done with that, go visit a town or something. start town and topshelf are pretty aight", 5)

    player.quest = "Dab on Turtles"

    return player  # the last 2 numbers are health, defence


# I dont think the below gets used anywhere here, only in battle.py
def damage(player, dmg):
    player.health -= dmg
    print("{} took {} damage! HP: {}/{}".format(player.name, damage, player.health, player.max_health))


def menu():
    valid = True
    while valid:
        choice = input("\n----{MENU}----\n"
                       "What would you like to do?\n"
                       "[Q]uest [I]nventory [S]hop \n"
                       "[P]layer [W]orld E[X]it\n"
                       "[SAVE] [HELP] [SETTINGS]\n"
                       ">>>").lower().strip()
        if choice.find("q") != -1:
            return "quest"
        elif choice == "exit" or choice == "x":
            sure = input("Confirm Quit? (y/n)").lower()
            if sure.find("y") != -1:
                print("Ok, see ya next time bruv.")
                return "exit"
        elif choice == "s" or choice == "shop" or choice == "store":
            return "shop"
        elif choice == "player" or choice == "p":
            return "player"
        elif choice == "world" or choice == "w":
            return "world"
        elif choice == "save":
            return "save"
        elif choice == "help":
            return "help"
        elif choice == "settings":
            return "settings"
        elif choice == "debug mode":
            return "debug"
        elif choice.find("i") != -1:
            return "inventory"


def start():
    active = True
    while active:
        print("\n----{START MENU}----\n"
              "[N]ew Game\n"
              "[L]oad Profile")
        ask = input(">>>").lower()
        if ask == "l" or ask == "load":
            saves = data.get_saves()
            for save in saves:
                print("[-] {}".format(save))
            print("Type your username:")
            ask_name = input(">>>").strip()
            filepath = data.get_full_path(ask_name)
            if os.path.exists(filepath):
                loaded = data.load(ask_name)
                if not loaded:  # if loading throws an error
                    return None
                return loaded
            else:
                print("'{}' is not a save file. Did you spell it correctly? Caps matter ya know.".format(ask_name))
        elif ask == "n" or ask == "new" or ask == "new game":
            print("Starting New Game!")
            return None
        else:
            print("'{}' not recognized. Try again.".format(ask))


def info(player):
    print("\n----{INFO}----")
    print("You are {}, wielder of the {}.".format(player.name, player.weapon))
    if player.quest:
        print("Your current task is to {}".format(player.quest))
    else:
        print("You have no current task.")
    print("You have {}/{} HP and {}G".format(player.health, player.max_health, add_commas(player.money)))
    print("LEVEL {} ({} XP)".format(player.level, player.xp))
    print("------------\n")
    sleep(1)


def game_help():
    print("\n\n----{HELP}----")
    print("* Menus always follow the ----{TITLE}---- format to alert you to the menu's start.")
    print("* Anything you can type in a situation, like keys or keywords, are in [BRACKETS]")
    print("* Dialog starts with a '-[NAME]' so you can see who's talking.")
    print("-[HELP GUY] Hello!")
    print("- Also, any other dialog by the same person is shortened to a dash.")
    print("-[HELP GUY 2] But other people can join conversations!")
    print("[!] Personal Alerts show up with a [!] identifier.")
    input("\nPress [ENTER] to continue...")
    print("\n\n----{HELP}----")
    print("* Quests are under the [Q] tab, where you can launch quests from the main menu.")
    print("* Shops and other stuff is found in [W]orlds. Different places have different goods!")
    print("* They can also give you new quests! Check town directories, they may have quest bulletins"
          "\nor people to talk to!")
    print("* Use [I]nventory to use items! Some items can only be used within battles.")
    print("* Finally, be sure to [SAVE] often!")
    input("\nPress [ENTER] to continue...")


def change_settings():
    global settings
    check = True
    print("\nDo you want timed dialog or when you press [ENTER]? (timed/enter)")
    while check:
        ask = input(">>>").lower().strip()
        if ask == "timed":
            settings.enter_dialog = False
            check = False
        elif ask == "enter":
            settings.enter_dialog = True
            check = False
    print("Settings changed! Be sure to [SAVE] to keep changes!")


if __name__ == "__main__":
    main()
