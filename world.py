import random
import shop
import inventory
from time import sleep

worlds = {"Test World": 0, "Start Town": 1, "Topshelf": 2,}


def select_world():
    active = True
    while active:
        print("\n----{WORLD}----\nWhich world would you like to go to?")
        for world in worlds:
            print("[{}] {}".format(worlds[world], world))
        choice = input(">>>").strip()
        try:
            for world in worlds:
                if world.lower() == choice.lower():
                    return world
                elif choice == str(worlds[world]):
                    return world
        except KeyError:
            print("That... isn't a world. Now lets try this again. (If it was, note a KeyError in bug report.")
        except:
            print("Something went wrong.")
            return None


def menu(options=True):
    valid = True
    while valid:
        if options:
            choice = input("\n----{WORLD MENU}----\n"
                           "What would you like to do?\n"
                           "[I]nventory [S]hop E[X]it [T]alk\n"
                           "[O]ther"
                           "\n>>>").lower().strip()
        else:
            choice = input("\n----{WORLD MENU}----\n"
                           "What would you like to do?\n"
                           "[I]nventory [S]hop E[X]it [T]alk"
                           "\n>>>").lower().strip()
        if choice == "s" or choice == "shop" or choice == "store":
            return "shop"
        elif choice == "talk" or choice == "t":
            return "talk"
        elif choice == "exit" or choice == "x":
            return "exit"
        elif choice.find("i") != -1:
            return "inventory"


def test_world(player):
    print("hi, {}. you really dont wana be here. go away".format(player.name))


def start_world(player):
    print("You arrive at Start Town. A friendly local waves hello.")
    sleep(1)
    print("-Oi mate! Welcome to Start Town! We don't get many new folk here, stay a while!")
    sleep(1)
    dialog = ["I heard sometimes weapons land critical hits that do 3x damage!",
              "I wish I was a pegasus. What? You weren't supposed to hear that! Go away!",
              "A strange man came through here muttering about 'spaghetti code' and 'player and enemy objects' I think he's a bit coo-coo.",
              "I've heard that Fergus the Shopkeep here has the cheapest Health Potions around. In a 3 mile radius.",
              "Where did you say you're from? Some town by the name of player.town_name? What a strange place.",
              "A newbie's defence has only around a 1/10 shot of working. Better get some armour, huh?",
              "The quest system is so broken. It should be a list, damnit.",
              "What's with the guy that welcomes the new people here? \"ayo deadass wuz yo name nibba?\" Who speaks like that here? "]

    active = True
    while active:
        action = menu(options=False)
        if action == "shop":
            print("You have arrived at the shop. You begin to look around...")
            sleep(1)
            shop.start_store(player)
        elif action == "inventory":
            inventory.use_item(player)
        elif action == "talk":
            print("-" + random.choice(dialog))
        elif action == "exit":
            active = False


def topshelf(player):
    print("You arrive at Topshelf. A local towers above you waves hello.")
    sleep(1)
    print("-Welcome, small one, to the realm of the Longbois. Welcome, to Topshelf.")
    sleep(2)
    dialog = ["One must be considered quite tall to join the Longbois. Visit the evaluator if you wish to be judged.",
    "Jacob is the current leader of the Longbois. He's served us well.",
    "You may want to investigate the [O] path near the entrance of this world.\n It shows a directory of things harder to find in this town, had you not a directory.",
    "One fool wished to name our realm The Ceiling. I'm glad the great Dev denied\n that idea. The fool was smited."]

    active = True
    while active:
        action = menu()
        if action == "shop":
            print("You have arrived at the shop. You begin to look around...")
            sleep(1)
            shop.start_store(player)
        elif action == "inventory":
            inventory.use_item(player)
        elif action == "talk":
            print("-" + random.choice(dialog))
        elif action == "exit":
            active = False