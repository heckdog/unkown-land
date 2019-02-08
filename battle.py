from random import randint
import random
from time import sleep
from essentials import weapons
import inventory
import quests
from program import Player


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
            status = status.replace("s ", " ")
            choice = input(("\n{} {} What do? "
                           "\n[A]ttack [I]nventory [S]pecial [E]scape\n>>>".format(arrange(names), status))).lower().strip()


        #TODO: allow attacking for only one enemy at a time
        # Attacking
        if choice == "a" or choice == "attack":

            print("\nAttack who? (type 'cancel' to cancel attack)")
            target = select(enemies)
            # Player Turn
            dam = weapons[player.weapon]  # returns attack stats
            dam += randint(0, dam)
            # random crits
            for i in range(3):
                if randint(0, player.crit_chance) == 2:  # a ten percent chance
                    dam += randint(dam * 2, dam * 3)
                    print("CRITICAL HIT!")
            damage(target, dam)
            sleep(1)
            if target.health < 0:  # if you killed an enemy
                print("{} died!".format(target.name))

            print() # spacer
            # Enemy Turn
            for enemy in enemies:
                if enemy.health <= 0:
                    enemies.remove(enemy)
                else:
                    print(enemy.name + " attacked!")
                    damage(player, enemy.damage + randint(0, enemy.damage))
                    sleep(1)
                    print()  # just a spacer
                if len(enemies) == 0:
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


if __name__ == '__main__':
    # print(arrange(["Test 1", "Test 2", "Test 3"]))  # passed
    # print(arrange(["Test YEET"]))  # passed
    # print(arrange(["Test", "Test", "Test"]))  # passed
    # print(arrange(["aaaaaaaaaa", "bbbbbbbb", "aaaeee"]))  # passed
    # print(arrange(["sicko mode", "mo bamba"]))  # passed with flying colors
    # print(arrange(["e", "a", "e", "e"]))
    # print(arrange(["goblin", "doblin", "snoblin"]))

    player = Player("Test Player", "Fists", "Test the Game", 100, 10)
    turtle = quests.EvilTurtle("Evil Turtle")
    turtle_2 = quests.EvilTurtle("Turtle 2")

    status = battle(player, [turtle, turtle_2])  # todo: fix this



