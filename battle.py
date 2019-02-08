from random import randint
import random
from time import sleep
from essentials import weapons
import inventory


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

    not_dead = True

    while not_dead and player.health > 0:

        # check for the whole enemy team being dead.
        for enemy in enemies:
            dead = 0
            if enemy.health <= 0:
                dead += 1
            if dead == len(enemies):
                return "Won"
            not_dead = True

        # TODO: for each enemy, attack
        status = random.choice(enemy.doing)
        choice = input("\n{} {} What do? \n[A]ttack [I]nventory [D]efend [S]pecial [E]scape\n>>>".format(enemy.name, status)).lower().strip()

        #TODO: allow attacking for only one enemy at a time
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

        # todo: redo this and make it not so useless
        # Defending
        elif choice == "d" or choice == "defend":
            # Player Turn
            defended = False
            for i in range(player.defence):
                chance = randint(1, 10)
                if chance == 5:
                    defended = True

            # TODO: make below enemy TURNS
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
        elif choice == "e" or choice == "escape":
            escape_number = randint(1,100)
            if escape_number < 50:
                print("You escaped from the {}".format(enemy.name))
                return "Escaped"

        # Unknown Command
        else:
            print("'{}' not recognized, please try again.".format(choice))
    # End sequence
    # Todo: work with multi xp gain
    if enemy.health <= 0:
        xp_gain = enemy.xp + int((randint(0, enemy.xp)/2))  # Give player Enemy XP + up to 0.5x more
        money_gain = xp_gain * randint(2,3) + randint(1, 10)  # pseudo-random money based on enemy xp.
        print("You have successfully defeated the {}! Gained {} XP and {}G".format(enemy.name, xp_gain, money_gain))
        player.xp += xp_gain
        player.money += money_gain
        player.xp_check()
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