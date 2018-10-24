from random import randint
import random
from time import sleep
import inventory
import data

# below is deprecated
# Enemy = namedtuple("Enemy", "name health max_health damage")


class Enemy:
    def __init__(self, name, health, damage, xp, doing_plus=[]):
        self.name = name
        self.health = health
        self.max_health = health
        self.damage = damage
        self.xp = int(xp)  # its an int to prevent other calculations from being floats idk why
        self.doing = ["stands dreamily.",
                      "dances furiously.",
                      "stands in your way.",
                      "looks ripe.",
                      "smells bad.",
                      "stands there... menacingly.",
                      "is 'ez' according to some kid I asked.",
                      "is probably just Gary in a costume.",
                      "eats pant."
                      ]

        for i in range(20):  # makes the other text more rare. change to lower to make special text appear more often.
            self.doing.append("stands in your way.")

        for thing in doing_plus:
            self.doing.append(thing)

        self.has_special = False

    def special(self, player):
        print("\n----{SPECIAL}----\n")
        print("There's nothing you can do!")


class EvilTurtle(Enemy):
    has_special = True  # tells battle program to allow attacks after this


    def special(self, player):
        print("\n----{SPECIAL}----")
        print("[DAB] [DEFAULT DANCE]")
        choice = input(">>>").strip().lower()
        if choice == "dab" or choice == "d":
            print("ooh my god you just dabbed on that turtle")
            chance = randint(1,10)
            if chance > 7: # just a random chance of dab back
                print("BUT IT DABS BACK OH MY GOD!!!!!")
                damage(player, int(player.health/4))  #TODO: if something ever breaks, its this int
            else:
                self.health = -9999
        elif choice == "default dance" or choice == "dance" or choice == "dd":
            print("The Turtle is unfazed by your smooth moves!")
            damage(player, 5)
        else:
            print("I'm just gonna assume you're good cuz '{}' aint a choice my guy.".format(choice))


# ENEMIES: Go like Enemy(NAME, HEALTH, DAMAGE, XP)
# evil_turtle = Enemy("Evil Turtle", 30, 5, 10)
dragon = Enemy("Dragon", 8000, 20, 1000)

weapons = {"Sword": 70, "RPG": 5000, "Fists": 10, "UNKOWN": 123918312, "digional sword": 1000}


def battle(player, enemy):
    print("---{BATTLE START}---")
    try:
        if player.health > 0:
            print("Battle Load successful.")
        else:
            print("ur dead lmao")
    except TypeError:
        print("Battle system currently down, sorry. Go nag the dev about it (For error reporting, its a 'TypeError')")
        return "Broke"
    while enemy.health > 0 and player.health > 0:
        status = random.choice(enemy.doing)
        choice = input("\n{} {} What do? \n[A]ttack [I]nventory [D]efend [S]pecial [E]scape\n>>>".format(enemy.name, status)).lower().strip()

        # Attacking
        if choice == "a" or choice == "attack":
            # Player Turn
            dam = weapons[player.weapon]  # returns attack stats
            dam += randint(0, dam)
            # random crits
            for i in range(3):
                if randint(0,10) == 2:  # a ten percent chance
                    dam += randint(dam * 2, dam * 3)
                    print("CRITICAL HIT!")
            damage(enemy, dam)
            if enemy.health < 0:  # if you won
                break

            # Enemy Turn
            damage(player, enemy.damage + randint(0, enemy.damage))

        # Defending
        elif choice == "d" or choice == "defend":
            # Player Turn
            defended = False
            for i in range(player.defence):
                chance = randint(1, 10)
                if chance == 5:
                    defended = True

            # Enemy Turn
            if defended:
                print("{} managed to defend from the {}.".format(player.name, enemy.name))
            else:
                print("{} failed to defend, and got hit by the {}".format(player.name, enemy.name))
                damage(player, enemy.damage + randint(0, enemy.damage))

        # Inventory
        elif choice == "i" or choice == "inventory":
            inventory.use_item(player)

        # Special
        elif choice == "s" or choice == "special":
            if enemy.has_special:
                enemy.special(player)
                if enemy.health <= 0:  # if enemy dead
                    break  # break just makes it go to win sequence
                damage(player, enemy.damage + randint(0, enemy.damage))  # damage 1-2x base value
            else:
                enemy.special(player)

        # Escape
        elif choice == "e" or "escape":
            escape_number = randint(1,100)
            if escape_number < 50:
                print("You escaped from the {}".format(enemy.name))
                return "Escaped"

        # Unknown Command
        else:
            print("'{}' not recognized, please try again.".format(choice))
    # End sequence
    if enemy.health <= 0:
        xp_gain = enemy.xp + int((randint(0, enemy.xp)/2))  # Give player Enemy XP + up to 0.5x more
        money_gain = xp_gain * randint(2,3) + randint(1, 10)  # pseudo-random money based on enemy xp.
        print("You have successfully defeated the {}! Gained {} XP and {}G".format(enemy.name, xp_gain, money_gain))
        player.xp += xp_gain
        player.money += money_gain
        sleep(1.5)
        return "Won"
    elif player.health <= 0:
        print("You lost to the {}, which had {} HP left".format(enemy.name, enemy.health))
        return "Lost"
    else:
        print("Unknown Error: You shouldn't be able to see this text.")
        return None


def damage(player, dmg):
    hp = player.health
    hp += -dmg
    player.health = hp
    print("{} took {} damage! HP: {}/{}".format(player.name, dmg, player.health, player.max_health))


def clap_the_dragon(player):
    # THIS QUEST IS FAR FROM WORKING
    if player.quest == "Clap the Dragon":
        status = battle(player, dragon)
        if status == "Won":
            player.quest = None
            player.completed.append("Clap the Dragon")
            player.xp += 300


def battle_turtles(player, turtles):
    number = 0
    for turtle in range(turtles):
        number += 1
        evil_turtle = EvilTurtle("Evil Turtle #{}".format(number), 30, 5, 10)
        status = battle(player, evil_turtle)
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
        goblin = Enemy("Goblin #{}".format(number), 100, 15, 50)  # change the last value to make this chalenge harder or easier
        status = battle(player, goblin)
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
    result = battle(player, dev)
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
            print("-Wait, WHAT?! Don't leave the game! DONT! IM GONNA SAVE IT RIGHT NOW. NO MONEY OR ANYTHING. ILL DELETE YOU!!!")
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


