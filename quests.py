from random import randint
from time import sleep
import inventory
import data

# below is deprecated
# Enemy = namedtuple("Enemy", "name health max_health damage")


class Enemy:
    def __init__(self, name, health, damage, xp):
        self.name = name
        self.health = health
        self.max_health = health
        self.damage = damage
        self.xp = xp


# ENEMIES: Go like Enemy(NAME, HEALTH, DAMAGE, XP)
# evil_turtle = Enemy("Evil Turtle", 30, 5, 10)
dragon = Enemy("Dragon", 8000, 20, 1000)


weapons = {"Sword": 70, "RPG": 5000, "Fists": 10, "Glitch": 123918312, "digional sword": 1000}


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
        choice = input("\nA {} stands in your way. What do? \n[A]ttack [I]nventory [D]efend [S]pecial \n>>>".format(enemy.name)).lower().strip()

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
            inventory.view_inventory(player)

        # Special
        elif choice == "s" or choice == "special":
            print("u aint no special snowflake and this is unfinished lol try again")

        # Unknown Command
        else:
            print("'{}' not recognized, please try again.".format(choice))
    # End sequence
    if enemy.health <= 0:
        xp_gain = enemy.xp + (randint(0, (enemy.xp/2)))  # Give player Enemy XP + up to 0.5x more
        money_gain = xp_gain * randint(2,3) + randint(1, 10)  # pseudo-random money based on enemy xp.
        print("You have successfully defeated the {}! Gained {} XP and {}G".format(enemy.name, xp_gain, money_gain))
        player.xp += xp_gain
        player.money += money_gain
        sleep(1)
        return "Won"
    elif player.health <= 0:
        print("You lost to the {}, which had {} HP left".format(enemy.name, enemy.health))
        return "Lost"
    else:
        print("Unknown Error: You shouldn't be able to see this text.")
        return None


def damage(player, damage):
    hp = player.health
    hp += -damage
    player.health = hp
    print("{} took {} damage! HP: {}/{}".format(player.name, damage, player.health, player.max_health))


def clap_the_dragon(player):
    if player.quest == "Clap the Dragon":
        status = battle(player, dragon)
        if status == "Won":
            player.quest = None
            player.completed += 1
            player.xp += 300


def battle_turtles(player, turtles):
    number = 0
    for turtle in range(turtles):
        number += 1
        evil_turtle = Enemy("Evil Turtle #{}".format(number), 30, 5, 10)
        status = battle(player, evil_turtle)
        if status == "Lost":
            print("You have lost to {} turtles. Kinda sad really.".format(turtles))
            sleep(2)
            return False
        if status == "Broke":
            return False
    print("You beat all {} of the turtles! Good Job!".format(turtles))
    player.quest = None
    player.completed += 1
    player.xp += 100
    sleep(2)
    return True


def beat_the_dev(player):
    dev = Enemy("Heckin-doggo", 9999999, 1, 50000)
    print("-Heh...")
    sleep(3)
    print("-You think you can really clap me, eh?")
    sleep(3)
    print("-I created this world. You are but another player object. Watch this.")
    sleep(1)
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
              "-Apparently, I didn't do it that great, since here we are.")
        sleep(3)
        print("I'll give you 50000 more XP and 10,000G not to tell anyone about it, deal?")
        deal = input("(y/n) \n>>>").lower().strip()
        if deal.find("ye") != -1 or deal == "y":
            print("-Cool, also I completed the mission for ya.")
            print("-See ya later my guy")
            return True
        else:
            print("-Well sucks to be you, I have the UNKOWN now. You need to pay attention to your pockets better.")
            print("[!] Everything in you inventory is missing! Maybe if you left now, you could retrieve your save.")
            sleep(1)
            print("-Wait, WHAT?! Don't leave the game! DONT! IM GONNA SAVE IT RIGHT NOW. NO MONEY OR ANYTHING. ILL DELETE YOU!!!")
            print("[!] The game froze. Now's your chance!")
            sleep(30)
            player.weapon = "Fists"
            player.money = 0
            player.health = 0
            data.corrupt(player, player.name)
            player.name = "DELETED"
            print("----{GAME SAVED}----")
            sleep(1)
            print("----{WORLD DELETED}----")


