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

        if len(enemies) == 1:
            choice = input("\n{} {} What do? "
                           "\n[A]ttack [I]nventory [S]pecial [E]scape\n>>>".format(enemy.name, status)).lower().strip()
        else:
            names = []
            for enemy in enemies:
                names.append(enemy.name)
            status = status.replace("s ", " ")  # a grammar thing
            choice = input(("\n{} {} What do? "
                           "\n[A]ttack [I]nventory [S]pecial [E]scape\n>>>".format(arrange(names), status))).lower().strip()



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

        # # todo: redo this and make it not so useless
        # # Defending
        # elif choice == "d" or choice == "defend":
        #     # Player Turn
        #     defended = False
        #     for i in range(player.defence):
        #         chance = randint(1, 10)
        #         if chance == 5:
        #             defended = True
        #
        #     # TODO: make below enemy TURNS
        #     # Enemy Turn
        #     if defended:
        #         print("{} managed to defend from the {}.".format(player.name, enemy.name))
        #     else:
        #         print("{} failed to defend, and got hit by the {}".format(player.name, enemy.name))
        #         damage(player, enemy.damage + randint(0, enemy.damage))


        # Inventory
        elif choice == "i" or choice == "inventory":
            inventory.use_item(player)

        # Special
        elif choice == "s" or choice == "special":
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
            escape_number = randint(1,100)
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
        player.money = player.money*.75
        return "Lost"
    else:
        print("Unknown Error: You shouldn't be able to see this text unless the laws of math suddenly changed.")
        return None


def damage(player, dmg):
    hp = player.health
    hp += -dmg
    player.health = hp
    print("{} took {} damage! HP: {}/{}".format(player.name, dmg, player.health, player.max_health))