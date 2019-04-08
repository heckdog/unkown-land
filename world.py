import random
import shop
import inventory
from time import sleep
from essentials import talk, choose


worlds = {"Start Town": 1, "Topshelf": 2,}


# checks for new lands
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
    talk("hi, {}. you really dont wana be here. go away".format(player.name), 1)


def start_world(player):
    talk("You arrive at Start Town. A friendly local waves hello.", 1)
    talk("- Oi mate! Welcome to Start Town! We don't get many new folk here, stay a while!", 1)

    if not player.quest:  # just for the dialog below. removes None from dialog.
        player.quest = "do nothing"

    dialog = ["I heard sometimes weapons land critical hits that do 3x damage!",
              "I wish I was a pegasus. What? You weren't supposed to hear that! Go away!",
              "A strange man came through here muttering about 'spaghetti code' and 'player and"
              " enemy objects' I think he's a bit coo-coo.",
              "I've heard that Fergus the Shopkeep here has the cheapest Health Potions around. In a 3 mile radius.",
              "Where did you say you're from? Some town by the name of player.town_name? What a strange place.",
              "A newbie's defence has only around a 1/10 shot of working. Better get some armour, huh?",
              "The quest system is so redundant. It should be a list, damn it.",
              "What's with the guy that welcomes the new people here? \"ayo deadass wuz yo name nibba?\" Who speaks"
              " like that here? ",
              "The battle system of UNKOWNLAND has zero resemblance to Undertale. What are you talking about?",
              "(insert tutorial dialog here)",
              "There is a great figure known as \"The Dev\" that supposedly created this world. Intriguing.",
              "Isn't it kind of strange that all the signs in every town look ----{LIKE THIS}----?",
              "If you attack the leader of a party in battle (that is, [1]), the one right behind them gets "
              "too frightened to attack! It's totally NOT a bug!",
              "It's quite empty here, don't you think? At least there is much to discuss.",
              "What is your quest, anyways? Is it really just to {}? Seems like there's more to it than that.".format(player.quest),
              "I'd love to move somewhere warmer like Ptonio. Unfortunately, I can't find it on a map. Perhaps "
              "someone in Topshelf could help me. You can't really miss Topshelf, its straight Northeast and up.",
              "nibba",
              "I hear rumors about a powerful force known as UNKOWN, for it is not known. What could it be?"
              ]

    if player.quest == "do nothing":
        player.quest = None

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
            talk("- " + random.choice(dialog) + "\n", 2)
        elif action == "exit":
            active = False


def topshelf(player):
    print("You arrive at Topshelf. A local towers above and you waves hello.")
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
            talk("- " + random.choice(dialog) + "\n", 3)
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

                        talk("- I assume you are looking to get evaluated, yes?", 2)
                        talk("- Hmmm...", 1.75)
                        talk("- Uh huh...", 2)
                        talk("- Well, you seem to be quite short by Longboi standards.", 1)
                        talk("- We require a certain height that you must achieve. I do admire"
                             " your determination, however...", 4)
                        talk("- Tell you what, small one. I happen to know of a town nearby that has a special "
                             "something that could boost you a bit. I'll show you on this map...", 4)
                        player.metadata.append("Ptonio")
                        print("[!] You have learned about Ptonio!")
                        sleep(1.5)
                        talk("- Yes... Ptonio is a short ways away, but they have some potions."
                             " Try it out, you may find something good over there...", 3.5)
                        o_check = False
                    elif "Longboi" not in player.traits:
                        # TODO: longboi evaluation
                        talk("-[THE EVALUATOR] Why, look at that!", 1.5)
                        talk("- That right there is some fine Longboi material. Let me just have a glance at your other stats.", 3)
                        talk("- Hmm...", 2)
                        talk("- Uh huh...", 2.5)
                        talk("- Yep, yep...", 3)
                        talk("Well {}, you did it. I hereby declare you a Longboi. Welcome to Topshelf.".format(player.name), 4)
                        print("[!] You are now a Longboi!")
                        sleep(.5)
                        player.traits.append("Longboi")
                    else:
                        talk("-[THE EVALUATOR] Why hello there fellow Longboi. I hope you enjoy "
                             "your stay here at Topshelf.", 3)

                elif choice == "2":
                    print("[UNDER CONSTRUCTION]")

                elif choice == "3":
                    if not player.quest:
                        # Quest Lore: Quest ID <-- goes to program.py, which sends it to quests.py
                        bulletin = {
                            "SEEKING PEST EXPERT TO EXTERMINATE LONGWORMS INFESTING FIELD. PAY: 500G.": "do Pest Control",
                            "Wanted: Hemlick, Ptonian Outlaw. Owes me money. 600G Reward.": "Teach Hemlick a Lesson"
                        }

                        talk("You go up to the bulletin...", 1.5)

                        # Add quest lore to a list to cycle it + index it
                        quest_list = []
                        for quest in bulletin:
                            if bulletin[quest] not in player.completed:  # check to see if player has done quest before
                                quest_list.append(quest)

                        # Quest Choice
                        chosen = False
                        while not chosen:
                            for quest in quest_list:
                                print("\n")
                                print(quest)
                                choice = ""
                                while choice != "y" and choice != "n" and choice != "cancel":  # auto exits if good answer
                                    choice = input("Choose this Quest? (y/n/cancel)").strip().lower()
                                if choice == "cancel" or choice == "x":
                                    o_check = False  # leave "other" loop
                                    chosen = True  # exit bulletin loop
                                elif choice == "y":
                                    talk("[!] Accepted quest to {}!".format(bulletin[quest]))  # set quest to ID
                                    player.quest = bulletin[quest]
                                    chosen = True
                                    o_check = False
                                elif choice == "n":
                                    print("Next...")
                                    sleep(.75)

                    else:
                        talk("[!] You already have a quest!")

                elif choice == "cancel":
                    o_check = False
                else:
                    print("'{}' isn't on the directory!")


def ptonio(player):
    talk("Howdy there! Welcome to Ptonio, home of UNKOWNLAND's finest potion breweries!",3)
    dialog = ["Howdy, pardner!",
              "Business out here's interestin', ya know. We live on the edge of the law round here.",
              "Safe-tee pro-toe-calls? I ain't heard nothin' like that before 'round here.",
              "Any potion is legal if nobody catches you with em.",
              "Yeehaw!"]
    active = True
    while active:
        action = menu("Ptonio")
        if action == "shop":
            print("You have arrived at the shop. You begin to look around...")
            sleep(1)
            shop.ptonio_store(player)
        elif action == "inventory":
            inventory.use_item(player)
        elif action == "talk":
            talk("- " + random.choice(dialog), 3)
        elif action == "exit":
            active = False
        elif action == "other":
            o_check = True
            while o_check:
                print("\n----{PTONIO DIRECTORY}----\n")
                print("[1] Strange Alley\n"
                      "[2] Ptonio Dump\n"
                      "[3] Bulletin Board\n")
                print("\nWhere would you like to go? ('cancel' to cancel)")
                choice = input(">>>").strip()

                if choice == "1":
                    talk("You enter the strange alley...", 3)
                    # TODO: verifiy the below
                    if "metMel" not in player.metadata:
                        if "knowMelName" not in player.metadata:
                            talk("-[?] Eh? Who are you?", 2)
                            talk("- I sense you are new round here, aren't ya?", 2.5)
                            talk("- What brings you down here? Nobody ever comes down the alley...", 3)
                            talk("- You must be seekin some sort of potion, ain't that right?", 2.5)
                            talk("-[MEL] Well, alright. Folks round here call me Mel. I sell, uh, questionable potions.", 4)
                            player.metadata.append("knowMelName")
                            talk("- Apparently the Longbois didn't prefer that I allow just anyone to be tall, so\n"
                                 "  they attempted to shut me down", 6)
                            talk("- But I managed. And here we are", 2)
                        else:
                            talk("-[MEL] Eh? Who's that?", 1.5)
                            talk("- Oh. I've seen you before. Come on in.", 3)
                        talk("- So, what're you lookin for?")
                        sleep(.5)

                        choice = ""
                        while choice != "1" and choice != "2":
                            choice = input("[1] A tall potion?\n"
                                           "[2] Nothing, just seeing what you have.\n"
                                           ">>>")
                            if choice == "1":
                                choice = input("- I don't produce that one anymore. If it's that you're lookin for, "
                                               "you best leave.\n"
                                               "[1] What if I did something for ya?\n"
                                               "[2] Ok, bye.\n"
                                               ">>>")
                                if choice == "2":
                                    o_check = False
                                elif choice == "1":
                                    player.metadata.append("metMel")
                                    talk("- Well, you COULD clear out some pests for me.", 2)
                                    talk("- The outlaws are gettin a real mess. If you can clear em out, we can talk.", 3)
                                    if player.quest:
                                        if "MelQuestBacklog" not in player.metadata:
                                            player.metadata.append("MelQuestBacklog")
                                            print("[!] Already have quest! Come back after it's done.")
                                        else:
                                            print("[!] Come back without a quest!")
                                    else:
                                        player.quest = "Defeat the Outlaws"
                            elif choice == "2":
                                talk("- Oh, ok. Here you are, take a look.", 2)
                                shop.early_mel_shop(player)
                            else:
                                print("-[DEV] you done broke something you buffoon! ")
                                o_check = False
                    else:
                        talk("-[MEL] Oooh, is that {}? Yes, come in...".format(player.name), 1.5)
                        if "MelQuestBacklog" in player.metadata:
                            print("Start quest? Defeat the Outlaws (y/n)")
                            choice = input(">>>").strip().lower()
                            if choice == "y":
                                player.quest = "Defeat the Outlaws"
                                o_check = False
                            elif choice == "n":
                                o_check = False
                        else:
                            shop.mel_shop(player)

                elif choice == "2":
                    check = True
                    choice = choose("Search the dump?", ["yes", "no"])
                    if choice == "y" or choice == "yes":
                        # litterally the only animation in this entire game
                        print("Searching.", end="")
                        for i in range(3):
                            sleep(.5)
                            print(".", end="")
                        print(".")

                        luck = random.randint(1,100)
                        if luck < 20:
                            hurt_dialog = {"[!] You cut yourself on loose glass shards! -5HP": 5,
                                           "[!] You step on a rusty iron spike. -20HP": 20,
                                           "[!] You fall off a loose pile of garbage 5 feet up. -10HP": 10,
                                           "[!] You trip, and a rat laughs. -1HP just out of embarrassment.": 1,
                                           "[!] An old rigged trap goes off with your finger in it. -15HP": 15}
                            hurt = random.choice(list(hurt_dialog))
                            print(hurt)
                            player.health -= hurt_dialog[hurt]  # i may have mixed something up here
                            talk("[!] HP: ({}/{})".format(player.health, player.max_health), 3)
                        else:
                            print("No luck today...")
                    else:
                        o_check = False

                elif choice == "3":
                    talk("No missions right now... damn.", 3)
                    o_check = False
                elif choice.lower() == "cancel":
                    o_check = False


def unkown_realm(player):
    print("You arrive at a deep, daunting cave. You enter...")
    sleep(1)
    if "UNKOWN" in player.inventory:
        print("-[?] !")
    else:
        print("-[?] ...?")
    talk("", 2)
    dialog = ["...",
              "&&&Y!",
              "§§§d2hhdCBhcmUgeW91IGRvaW5nPw==♣",
              "ÖÉ╞ÑÑÑÑ««▐▐▐",
              "EEEEEEEEEEEEEEEEEEEEEEEEEEEE",
              "&&***********&%%%%",
              "aGV5IHlvdSdyZSBub3Qgc3VwcG9zZWQgdG8gcmVhZCB0aGlzIHlldA==",
              "ON2G64BANF2CAIBA"]

    active = True
    while active:
        action = menu("UNKOWNREALM", options=False)
        if action == "shop":
            print("There is no shop...")
        elif action == "inventory":
            inventory.use_item(player)
        elif action == "talk":
            print("- " + random.choice(dialog))
        elif action == "exit":
            print("You leave. Things feel much more real again.")
            active = False

        elif action == "other":
            o_check = True
            while o_check:
                print("----{UNKOWNLAND DIRECTORY}----\n")
                #TODO: fill this in
                # print("[1] The Evaluator's Hut\n"
                #       "[2] Longboi Hall\n"
                #       "[3] Bulletin Board\n")
                print("\nWhere would you like to go? ('cancel' to cancel)")
                choice = input(">>>")

