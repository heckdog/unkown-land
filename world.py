import random
import shop
import inventory
from time import sleep
from essentials import talk


worlds = {"Test World": 0, "Start Town": 1, "Topshelf": 2,}


def world_init(player):
    if "Ptonio" in player.metadata:
        worlds["Ptonio"] = 3


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


def menu(name, options=True):
    valid = True
    while valid:
        if options:
            choice = input("\n----{" + name.upper() + "}----\n"
                           "What would you like to do?\n"
                           "[I]nventory [S]hop E[X]it \n"
                           "[T]alk [O]ther" 
                           "\n>>>").lower().strip()
        else:
            choice = input("\n----{" + name.upper() + "}----\n"
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
        elif choice == "o" or choice == "other":
            return "other"


def test_world(player):
    print("hi, {}. you really dont wana be here. go away".format(player.name))


def start_world(player):
    print("You arrive at Start Town. A friendly local waves hello.")
    sleep(1)
    print("- Oi mate! Welcome to Start Town! We don't get many new folk here, stay a while!")
    sleep(1)
    dialog = ["I heard sometimes weapons land critical hits that do 3x damage!",
              "I wish I was a pegasus. What? You weren't supposed to hear that! Go away!",
              "A strange man came through here muttering about 'spaghetti code' and 'player and"
              " enemy objects' I think he's a bit coo-coo.",
              "I've heard that Fergus the Shopkeep here has the cheapest Health Potions around. In a 3 mile radius.",
              "Where did you say you're from? Some town by the name of player.town_name? What a strange place.",
              "A newbie's defence has only around a 1/10 shot of working. Better get some armour, huh?",
              "The quest system is so broken. It should be a list, damnit.",
              "What's with the guy that welcomes the new people here? \"ayo deadass wuz yo name nibba?\" Who speaks"
              " like that here? "]

    active = True
    while active:
        action = menu("Start Town", options=False)
        if action == "shop":
            print("You have arrived at the shop. You begin to look around...")
            sleep(1)
            shop.start_store(player)
        elif action == "inventory":
            inventory.use_item(player)
        elif action == "talk":
            print("- " + random.choice(dialog))
        elif action == "exit":
            active = False


def topshelf(player):
    print("You arrive at Topshelf. A local towers above you waves hello.")
    sleep(1)
    if "tall" not in player.traits:
        print("- Welcome, small one, to Topshelf, realm of the Longbois.")
    else:
        print("- Welcome to Topshelf, realm of the Longbois.")
    sleep(2)
    dialog = ["One must be considered quite tall to join the Longbois. Visit the evaluator if you wish to be judged.",
              "Jacob is the current leader of the Longbois. He's served us well.",
              "You may want to investigate the [O] path near the entrance of this world.\n It shows a directory of"
              " things harder to find in this town, had you not a directory.",
              "One fool wished to name our realm The Ceiling. I'm glad the great Dev denied that idea. The fool was "
              "smited.",
              "Think you're tall enough to join the Longbois? Perhaps you should visit the Evaluator."]

    active = True
    while active:
        action = menu("Topshelf")
        if action == "shop":
            print("You have arrived at the shop. You begin to look around...")
            sleep(1)
            shop.topshelf_store(player)
        elif action == "inventory":
            inventory.use_item(player)
        elif action == "talk":
            print("- " + random.choice(dialog))
        elif action == "exit":
            print("You climb back down to the surface.")
            active = False

        elif action == "other":
            o_check = True
            while o_check:
                print("----{TOPSHELF DIRECTORY}----\n")
                print("[1] The Evaluator's Hut\n"
                      "[2] Longboi Hall\n"
                      "[3] Bulletin Board\n")
                print("\nWhere would you like to go? ('cancel' to cancel)")
                choice = input(">>>")

                if choice == "1":
                    print("You head to the Evaluator's Hut...")
                    sleep(2)
                    if "tall" not in player.traits or "Longboi" not in player.traits:
                        talk("-[THE EVALUATOR] Well, what have we here?", 1.5)
                        # TODO: redo the print/sleeps with talk()s
                        print("- I assume you are looking to get evaluated, yes?")
                        sleep(1)
                        print("- Hmmm...")
                        sleep(1.5)
                        print("- Uh huh...")
                        sleep(1)
                        print("- Well, you seem to be quite short by Longboi standards.")
                        sleep(1)
                        print("- We require a certain height that you must achieve. I do admire"
                              " your determination, however...")
                        sleep(3)
                        print("- Tell you what, small one. I happen to know of a town nearby that has a special "
                              "something that could boost you a bit. I'll show you on this map...")
                        sleep(4)
                        player.metadata.append("Ptonio")
                        print("[!] You have learned about Ptonio!")
                        sleep(.5)
                        print("- Yes... Ptonio is a short ways away, but they have some potions."
                              " Try it out, you may find something good over there...")
                        o_check = False
                        sleep(3)
                    elif "Longboi" not in player.traits:
                        print("[INSERT EVALUATION]")
                        print("[!] You are now a Longboi!")
                        player.traits.append("Longboi")
                    else:
                        print("-[THE EVALUATOR] Why hello there fellow Longboi. I hope you enjoy "
                              "your stay here at Topshelf.")
                        sleep(3)
                elif choice == "2":
                    print("[UNDER CONSTRUCTION]")
                elif choice == "3":
                    print("No quests it seems...")
                    sleep(1)
                elif choice == "cancel":
                    o_check = False
                else:
                    print("'{}' isn't on the directory!")


def ptonio(player):
    dialog = ["Howdy, pardner!",
              "Business out here's interestin', ya know. We live on the edge of the law round here.",
              "Safe-tee pro-toe-calls? I ain't heard nothin' like that before 'round here.",
              "Any potion is legal if nobody catches you with em.",
              "Yeehaw!"]
    active = True
    while active:
        action = menu("Ptonio", options=False)
        if action == "shop":
            print("You have arrived at the shop. You begin to look around...")
            sleep(1)
            shop.ptonio_store(player)
        elif action == "inventory":
            inventory.use_item(player)
        elif action == "talk":
            print("- " + random.choice(dialog))
        elif action == "exit":
            active = False
