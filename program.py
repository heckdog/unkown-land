# from threading import Timer
# from collections import namedtuple
from time import sleep
import quests
import data
import shop
import os
from essentials import add_commas

# naming convention as follows:
# RELEASE.BIGUPDATE.Run (BUILD)
build = data.load_version()
print("Version 0.3.1 ({})".format(build))
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
    def __init__(self, name, weapon, quest, health, defence):
        self.name = name
        self.weapon = weapon
        self.quest = quest
        self.health = health
        self.max_health = health
        self.defence = defence
        self.completed = 0
        self.xp = 0
        self.level = 1
        self.inventory = {"Test Item": 100, "bread": 1231}
        self.money = 0


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
    sleep(2)
    active = True

    while active:
        option = menu()
        # Quest Option
        if option == "quest":
            if player.quest:  # check that a quest exists
                confirm = input("Start quest?: {} (y/n) \n>>>".format(player.quest))
                if confirm.find("y") != -1:
                    # TODO: make a good system for this, cuz 2 lines of extra elifs per quest cant be great
                    print("[!]Warning: This version of Quest is in beta. Proceed with caution.")
                    if player.quest == "Clap the Dragon":
                        quests.clap_the_dragon(player)
                    elif player.quest == "Dab on Turtles":
                        quests.battle_turtles(player, 5)
                else:
                    print("ok then")
            else:
                print("ok maybe next time")

        # Inventory Option
        elif option == "inventory":
            print("\n----{INVENTORY}----")
            if not player.inventory:  # if nothing exists in the inventory
                print("[*] Nothing!")
            else:
                for item in player.inventory:
                    print("[*] {} ({})".format(item, add_commas(player.inventory[item])))

        # Shop Option
        elif option == "shop":
            shop.shop(player)
        # Exit Option
        elif option == "exit":
            print("See ya later!")
            data.save(player)
            active = False
            #break


def print_header():
    print("--------------------------------------")
    print("|        The adventure of uh         |")
    print("|             UNKOWNLAND             |")
    print("|   another quality text based rpg   |")
    print("--------------------------------------")


# TODO: rewrite this with better options/dialogue
def start_choice():

    # TODO: if the name is on the list of users, load that and skip this dialogue
    name = input("-Wuz yo name, nibba? \n>>>").strip()
    print("-Ah, so it is {}. Sounds pretty dumb but ok".format(name))
    sleep(2)
    print("-These gay ass turtles be dabbin on all the land. deadass get him b")
    answer = input("yes or no \n>>>").lower()
    if answer.find("ye") != -1:
        print("-finna clap these nibbas cheeks")

    else:
        print("-well thats gay but youre doing it anyways slave")

    sleep(2)
    weapon_choice = input("-anyways you need a weapon b. whatchu want a sword or a mf rpg \n>>>").lower().strip()
    if weapon_choice == "sword":
        print("-you have fun with that but ok")
        weapon = "Sword"
    elif weapon_choice == "mf rpg" or weapon_choice == "rpg":
        print("-hell yeah")
        weapon = "RPG"
    else:
        print("-that's not a weapon so you goin barehanded. try actually choosing something next game tho.")
        weapon = "Fists"

    quest = "Dab on Turtles"

    return Player(name, weapon, quest, 100, 10)  # the last 2 numbers are health, defence


def damage(player, dmg):
    player.health -= dmg
    print("{} took {} damage! HP: {}/{}".format(player.name, damage, player.health, player.max_health))


def menu():
    valid = True
    while valid:
        choice = input("\n----{MENU}----\n"
                       "What would you like to do?\n"
                       "[Q]uest [I]nventory [S]hop E[X]it\n"
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
        elif choice.find("i") != -1:
            return "inventory"


def start():
    print("\n----{MAIN MENU}----\n"
          "[N]ew Game\n"
          "[L]oad Profile")
    ask = input(">>>")
    if ask.lower() == "l" or ask.lower() == "load":
        print("Type your username:")
        ask_name = input(">>>").strip()
        filepath = data.get_full_path(ask_name)
        if os.path.exists(filepath):
            loaded = data.load(ask_name)
            if not loaded:  # if loading throws an error
                return None
            return loaded
        print("Save file not found: '{}' \nStarting New Game...".format(ask_name))
    else:
        return None


def info(player):
    print("\n----{INFO}----")
    print("You are {}, wielder of the {}.".format(player.name, player.weapon))
    print("Your current task is to {}".format(player.quest))
    print("You have {}/{} HP and {}G".format(player.health, player.max_health, add_commas(player.money)))
    print("LEVEL {} ({} XP)".format(player.level, player.xp))


if __name__ == "__main__":
    main()
