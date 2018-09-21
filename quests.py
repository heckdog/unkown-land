from random import randint
from time import sleep

# not good to use here \/
# from collections import namedtuple

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


weapons = {"Sword": 70, "RPG": 5000, "Fists": 10}


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
        choice = input("\nA {} stands in your way. What do? \n[A]ttack [D]efend [S]pecial \n>>>".format(enemy.name)).lower().strip()

        # Attacking
        if choice == "a" or choice == "attack":
            # Player Turn
            dam = weapons[player.weapon]  # returns attack stats
            dam += randint(dam, dam * 3)
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

        # Special
        elif choice == "s" or choice == "special":
            print("u aint no special snowflake and this is unfinished lol try again")

        # Unknown
        else:
            print("'{}' not recognized, please try again.".format(choice))
    if enemy.health <= 0:
        xp_gain = enemy.xp + (randint(0, (enemy.xp/2)))  # Give player Enemy XP + up to 0.5x more
        print("You have successfully defeated the {}! Gained {} XP".format(enemy.name, xp_gain))
        player.xp += xp_gain
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
    for turtle in range(turtles):
        evil_turtle = Enemy("Evil Turtle", 30, 5, 10)
        status = battle(player, evil_turtle)
        if status == "Lost":
            print("You have lost to {} turtles. Kinda sad really.".format(turtles))
            sleep(2)
            return False
        if status == "Broke":
            break
    print("You beat all {} of the turtles! Good Job!".format(turtles))
    player.quest = None
    player.completed += 1
    player.xp += 100
    sleep(2)
    return True


