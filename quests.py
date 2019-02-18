from random import randint
import random
from time import sleep
from essentials import weapons
import inventory
import data


# below is deprecated
# Enemy = namedtuple("Enemy", "name health max_health damage")


class Enemy:
    def __init__(self, name, health, damage, xp, doing_plus=[], is_boss=False, item_trigger=None):
        self.name = name
        self.health = health
        self.max_health = health
        self.damage = damage
        self.xp = int(xp)  # its an int to prevent other calculations from being floats idk why

        self.item_trigger = item_trigger

        self.doing = ["stands dreamily.",
                      "dances furiously.",
                      "stands in your way.",
                      "looks ripe.",
                      "smells bad.",
                      "stands there... menacingly.",
                      "called yo mama fat.",
                      "eats pant.",
                      "ran out of text ideas.",
                      "fails to throw trash into the trashcan."
                      ]

        if is_boss:
            self.doing = []

        for i in range(5):  # makes the other text more rare. change to lower to make special text appear more often.
            self.doing.append("stands in your way.")

        for thing in doing_plus:
            self.doing.append(thing)

        self.has_special = False

    def gain(self, player):
        xp_gain = self.xp + int((randint(0, self.xp) / 2))  # Give player Enemy XP + up to 0.5x more
        money_gain = xp_gain * randint(2, 3) + randint(1, 10)  # pseudo-random money based on enemy xp.
        print("You have successfully defeated the {}! Gained {} XP and {}G".format(self.name, xp_gain, money_gain))
        player.xp += xp_gain
        player.money += money_gain

    def special(self, player):
        print("\n----{SPECIAL}----\n")
        print("There's nothing you can do!")


class Boss(Enemy):
    def __init__(self, name, health, damage, xp, doing_plus=[]):
        Enemy.__init__(self, name, health, damage, xp, doing_plus, is_boss=True)  # its dumb but it works


class EvilTurtle(Enemy):
    has_special = True

    # THIS IS HOW TO CALL OTHER STATS FROM ENEMY CLASS
    def __init__(self, name):
        Enemy.__init__(self, "EvilTurtle", 30, 5, 10, ["rolls around in its shell.",
                                                       "fails to dab."])
        self.name = name

    def special(self, player):
        print("\n----{SPECIAL}----")
        print("[DAB] [DEFAULT DANCE]")
        choice = input(">>>").strip().lower()
        if choice == "dab" or choice == "d":
            print("ooh my god you just dabbed on that turtle")
            chance = randint(1, 10)
            if chance > 7:  # just a random chance of dab back
                print("BUT IT DABS BACK OH MY GOD!!!!!")
                damage(player, int(player.health / 4))  # TODO: if something ever breaks, its this int
            else:
                self.health = -9999
        elif choice == "default dance" or choice == "dance" or choice == "dd":
            print("The Turtle is unfazed by your smooth moves!")
            damage(player, 5)
        else:
            print("I'm just gonna assume you're good cuz '{}' aint a choice my guy.".format(choice))


class Dragon(Boss):
    has_special = True

    def special(self, player):
        print("\n----{SPECIAL}----")
        print("[Clap] [Talk]")
        choice = input(">>>").lower().strip()
        if choice == "c" or choice == "clap":
            print("OOF you done CLAPPED that dragon. He lost half his HP!")
            damage(self, int(self.health / 2))
        elif choice == "t" or choice == "talk":  # TODO: add more talking options, dialog choices
            print("You talk to the dragon...")
            sleep(1)
            print("-huh? you wanna talk to me b?")
            sleep(2)
            if "knows Bob" in player.traits:
                print("-yo, you know my nibba bob! aight man thats cool. i'll leave ya alone. tell em ya won.")
                self.health = 0
                self.doing = ["is ready to talk to bob."]
            else:
                print("-welp, nice chat but im s'posed to beat yo ass so...")
                self.doing.append("thinks about that chat you just had.")


class Ryan(Boss):
    has_special = True

    def __init__(self):
        self.name = "Ryan, Consumer of the Cosmos"
        self.damage = 1
        self.health = 10000000
        self.xp = 15000
        Boss.__init__(self, "Ryan, Consumer of the Cosmos", 10000000, 1, 15000, ["craves the finest burnt popcorn.",
                                                                                 "prepares for a feast.",
                                                                                 "revs up his Beyblade."])

    def special(self, player):
        if "Burnt Popcorn" in player.inventory:
            print("-what is that delectable smell?")


def battle(player, enemies):
    print("\n---{BATTLE START}---")
    try:
        if player.health > 0:
            print("Battle Load successful.")
        else:
            print("ur dead lmao")
    except TypeError:
        print("Battle system currently down, sorry. Go nag the dev about it (For error reporting, its a 'TypeError')")
        print("also... you really shouldn't even be able to see this. go away")
        return "Broke"

    while player.health > 0:

        # check for the whole enemy team being dead.
        for enemy in enemies:
            dead = 0
            if enemy.health <= 0:
                dead += 1
            if dead == len(enemies):
                return "Won"

        status = random.choice(enemy.doing)

        if len(enemies) == 1:
            choice = input("\n{} {} What do? "
                           "\n[A]ttack [I]nventory [S]pecial [E]scape\n>>>".format(enemy.name, status)).lower().strip()
        else:
            names = []
            for enemy in enemies:
                names.append(enemy.name)
            status = status.replace("s ", " ")  # a grammar thing
            choice = input(("\n{} {} What do? "
                            "\n[A]ttack [I]nventory [S]pecial [E]scape\n>>>".format(arrange(names),
                                                                                    status))).lower().strip()

        # Attacking
        if choice == "a" or choice == "attack":

            print("\nAttack who? (type 'cancel' to cancel attack)")
            target = select(enemies)
            # Player Turn
            dam = weapons[player.weapon]  # returns attack stats
            dam += randint(0, dam)
            # random crits
            for i in range(3):
                if randint(0, 100) <= player.crit_chance:  # a ten percent chance
                    dam += randint(dam * 2, dam * 3)
                    print("CRITICAL HIT!")
            damage(target, dam)
            sleep(1)
            if target.health < 0:  # if you killed an enemy
                print("{} died!".format(target.name))

            print()  # spacer
            # Enemy Turn
            for enemy in enemies:
                if enemy.health <= 0:
                    enemy.gain(player)
                    enemies.remove(enemy)
                else:
                    print(enemy.name + " attacked!")
                    damage(player, enemy.damage + randint(0, enemy.damage))
                    sleep(1)
                    print()  # just a spacer
                if len(enemies) == 0:
                    player.xp_check()
                    return "Won"

        # Inventory
        elif choice == "i" or choice == "inventory":
            item = inventory.use_item(player, battle=True)
            for enemy in enemies:
                if item == enemy.item_trigger and player.debugEnabled:
                    print("ITEM TRIGGER!")

        # Special
        elif choice == "s" or choice == "special":
            print("Perform Special on who?")
            target = select(enemies)
            target.special(player)
            # if enemy.health <= 0:  # if enemy dead
            #     break  # break just makes it go to win sequence

            # TODO: perhaps in the future make this script an Enemy class default?
            for enemy in enemies:
                if enemy.health <= 0:
                    enemy.gain(player)
                    enemies.remove(enemy)
                else:
                    print(enemy.name + " attacked!")
                    damage(player, enemy.damage + randint(0, enemy.damage))
                    sleep(1)
                    print()  # just a spacer
                if len(enemies) == 0:
                    player.xp_check()
                    return "Won"

        # Escape
        elif choice == "e" or choice == "escape":
            escape_number = randint(1, 100)
            if escape_number < 50:
                print("You escaped from the {}".format(enemy.name))
                return "Escaped"
            else:
                print("You couldn't escape!")
                for enemy in enemies:
                    print("{} attacked!".format(enemy.name))
                    damage(player, enemy.damage)
                    print()

        # Unknown Command
        else:
            print("'{}' not recognized, please try again.".format(choice))

    # End sequence
    # Todo: work with multi xp gain
    if not enemies:
        player.xp_check()
        sleep(1.5)
        return "Won"
    elif player.health <= 0:
        print("You lost. You lose 25% of your money.")
        player.health = 1
        player.money = player.money * .75
        return "Lost"
    else:
        print("Unknown Error: You shouldn't be able to see this text unless the laws of math suddenly changed.")
        return None


def damage(player, dmg):
    hp = player.health
    hp += -dmg
    player.health = hp
    print("{} took {} damage! HP: {}/{}".format(player.name, dmg, player.health, player.max_health))


# WARNING: only use with DIFFERENTLY NAMED ENEMIES or you will get mixed results.
def arrange(names):
    arranged = names[0]
    check = arranged

    # check for single
    if len(names) == 1:
        return arranged

    # check for multiple of the same
    for name in names:
        if name == check:
            is_multiple = True
        else:
            is_multiple = False
            break

    if is_multiple:
        return "{} {}s".format(len(names), arranged)  # eg: 10 goblins

    # if none of the above
    for name in names[1:]:
        name_index = names.index(name)  # name_index and length are for debug purposes
        length = len(names[1:])
        if name_index == length:  # if it's the last name
            # check that names isn't over 2
            if len(names) > 2:  # if it isnt, do proper grammar
                arranged = "{}, and {}".format(arranged, name)
            else:  # if it is in fact 2 names, arrange without comma
                arranged = "{} and {}".format(arranged, name)
            return arranged
        arranged = "{}, {}".format(arranged, name)  # if not the last name, add a comma
    return arranged


def select(enemies):
    check = True
    while check:
        for e in enemies:
            print("[{}] {} ({}/{}HP)".format(enemies.index(e) + 1, e.name, e.health, e.max_health))

        target = input(">>>").strip()

        try:
            if target.lower() == "cancel":
                print("yo idk this shouldnt be happening idk whats going on")
            elif int(target) <= len(enemies) and int(target) >= 0:  # check if its within 0-len of targets
                target = enemies[int(target) - 1]
                check = False
            else:
                print("'{}' isn't valid. Type the number, not the name...").format(target)
        except TypeError:
            print("'{}' isn't valid. Type the number, not the name.").format(target)
    return target


# def clap_the_dragon(player):
#     # THIS QUEST IS FAR FROM WORKING
#     if player.quest == "Clap the Dragon":
#         dragon = Dragon("Dragon", 5000, 20, 233)
#         status = battle(player, dragon)
#         if status == "Won":
#             player.quest = None
#             player.completed.append("Clap the Dragon")
#             player.xp += 300


def battle_turtles(player, turtles):
    number = 0
    evil_turtles = []
    for turtle in range(turtles):
        number += 1
        evil_turtles.append(EvilTurtle("Evil Turtle {}".format(number)))
    status = battle(player, evil_turtles)
    if status == "Lost":
        print("You have lost to {} turtles. Kinda sad really.".format(turtles))
        sleep(2)
        return False
    if status == "Escaped":
        return False
    print("You beat all {} of the turtles! Good Job!".format(turtles))
    player.quest = None
    player.completed.append("Dab on Turtles")
    player.xp += 100
    sleep(2)
    return True


def mess_with_goblins(player):
    original_money = player.money
    number = 0
    while player.money <= (original_money + 400):
        number += 1
        goblin = Enemy("Goblin #{}".format(number), 100, 15,
                       50)  # change the last value to make this chalenge harder or easier
        status = battle(player, [goblin])
        if status == "Lost":
            print("Aw you lost to goblins boohoo. I've given you a bandaid tho so ur not dead yet.")
            player.health = 20
            return False
        if status == "Escaped":
            return False
    print("You beat {} Goblins! Look at you go! You got over 400G total from them. That'll teach em".format(number))
    player.xp += 200
    player.quest = None
    player.completed.append("Mess with Goblins")
    sleep(1)
    return True


# TODO: redo this gay battle its no fun.
def beat_the_dev(player):  # fight is somewhat broke nibba
    dev = Enemy("Heckin-doggo", 9999999, 1, 50000)
    sleep(2)
    print("\n-Heh...")
    sleep(3)
    print("-You think you can really clap me, eh?")
    sleep(3)
    print("-I created this world. You are but another player object. Watch this.")
    sleep(3)
    print("[!] Your Health and Max Health have dropped to 1!")
    oldhealth = player.health
    oldmax = player.max_health
    oldweapon = player.weapon
    player.health = 1
    player.max_health = 1
    sleep(1)
    print("[!] You feel a noticeable lack of weapon...")
    player.weapon = "Fists"
    sleep(2)
    if "UNKOWN" in player.inventory:
        player.weapon = "UNKOWN"
        print("")
        print("[!] Equipped weapon.ERROR: Weapon Does not Exist!")
    print("Let's fight, if that's what you're here for. :)")
    result = battle(player, [dev])
    if result == "Lost":
        print("-Did you really think that was a good idea?  I didn't.")
        sleep(0.5)
        print("-Here's your stats back, by the way.")
        print("[!] You feel whole and weighted again! Although you really didn't need those extra pounds back...")
        player.health = oldhealth
        player.max_health = oldmax
        player.weapon = oldweapon
        return False
    elif result == "Won":
        print("-Holy frick how did you manage to do that?!?!")
        sleep(1)
        print("-Do, do you have some unknown powers?")
        sleep(1)
        print("-WAIT!!")
        sleep(3)
        print("-Do you... do you have the powers of UNKOWN?")
        sleep(2)
        print("-I thought I sealed those powers away in the title screen."
              "Apparently, I didn't do it that great, since here we are.")
        sleep(3)
        print("-I'll give you 50000 more XP and 100,000G not to tell anyone about it, deal?")
        deal = input("(y/n) \n>>>").lower().strip()
        if deal.find("ye") != -1 or deal == "y":
            player.money += 100000
            player.xp += 50000
            player.inventory.pop("UNKOWN")
            player.completed.append("Beat up the Developer")
            print("-Cool, also I completed the mission for ya.")
            print("-See ya later my guy")
            return True
        else:
            print("-Well sucks to be you, I have the UNKOWN now. You need to pay attention to your pockets pal.")
            print("[!] Everything in you inventory is missing! Maybe if you left now, you could retrieve your save.")
            sleep(1)
            print(
                "-Wait, WHAT?! Don't leave the game! DONT! IM GONNA SAVE IT RIGHT NOW. NO MONEY OR ANYTHING. ILL DELETE YOU!!!")
            print("[!] The game froze. Now's your chance!")
            sleep(5)
            print("I'll...")
            sleep(3)
            print("...dab...on...")
            sleep(7)
            print("...YOUUUUUU!!@!!!23123#Fveqwy3543g?%%%% player.name!!!@313323")
            sleep(1)
            print("[!] PLAYER {} NOT FOUND. COMMENCING FILE REMOVAL.".format(player.name))
            player.weapon = "Fists"
            player.money = 0
            player.health = 0
            player.xp = -1
            player.level = ": None!"
            player.quest = "do nothing. You don't exist."
            player.inventory = {"There's Nothing Here...": "You should just make a new save pal."}
            data.save(player)
            player.name = "DELETED"
            print("----{GAME SAVED}----")
            sleep(1)
            print("----{WORLD DELETED}----")


# Easter Egg Battle. Unobtainable via normal means.
def ryans_battle(player):
    pheonix = Enemy("Pheonix", 1000000, 10000, 5000)  # health, damage, xp, "Lost" "Won"
    status = battle(player, [pheonix])
    if status == "Lost":
        print("-hahahahahahahahaha loser")
    else:
        print("-ahhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh noooo")
        player.completed.append("Ryan's Battle")
        player.quest = None
        sleep(1)


def defeat_ryan(player):
    ryan = Ryan()

    status = battle(player, [ryan])
    if status == "Lost":
        print("You were eaten.")
    elif status == "Won":
        print("The smell of burnt popcorn fades away. \nYou notice a small round object on the ground.")
        player.inventory.update({"BeyBlade": 1})
        sleep(3)
        print("You have acquired the Beyblade!")
        player.quest = None
        player.completed.append("Defeat Ryan")
    else:
        print("The air is noticeably lighter.")