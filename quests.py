from random import randint
import random
from time import sleep
from essentials import weapons, talk, settings, choose
import inventory
import data


# below is deprecated
# Enemy = namedtuple("Enemy", "name health max_health damage")


class Enemy:
    def __init__(self, name, health, damage, xp, doing_plus=[], is_boss=False, item_trigger=None, has_special=False):
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

        self.has_special = has_special

    def gain(self, player):
        xp_gain = self.xp + int((randint(0, self.xp) / 2))  # Give player Enemy XP + up to 0.5x more
        money_gain = xp_gain * randint(2, 3) + randint(1, 10)  # pseudo-random money based on enemy xp.
        print("You have successfully defeated the {}! Gained {} XP and {}G".format(self.name, xp_gain, money_gain))
        player.xp += xp_gain
        player.money += money_gain

        if not settings.quickdeath:
            sleep(3)
        else:
            input()

    def special(self, player):
        print("\n----{SPECIAL}----\n")
        print("There's nothing you can do!")


class Boss(Enemy):
    def __init__(self, name, health, damage, xp, doing_plus=[], item_trigger=None, has_special=False):
        Enemy.__init__(self, name, health, damage, xp, doing_plus,
                       is_boss=True, item_trigger=item_trigger, has_special=has_special)
        # its dumb but it works


def battle(player, enemies, boss=False):
    print("\n---{BATTLE START}---")
    try:
        if player.health > 0:
            print("{} joined the battle! ({}/{}HP)".format(player.name, player.health, player.max_health))
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
                player.xp_check()
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

            if target:
                # Player Turn
                dam = weapons[player.weapon]  # returns attack stats
                dam += randint(0, dam)
                # random crits
                if randint(0, 100) <= player.crit_chance:  # a ten percent chance
                    dam += randint(dam * 2, dam * 3)
                    print("[!] CRITICAL HIT!")

                damage(target, dam)
                sleep(1)

                die_messages = ["got yeeted on!",
                                "got RKO'd straight outta nowhere!",
                                "got gamershotted!",
                                "needs an F in the chat.",
                                "= RIP",
                                "is straight up not having a good time!",
                                "is no more.",
                                "just fricken dies.",
                                "turned into dust."]

                if target.health < 0:  # if you killed an enemy
                    print("[!] {} {}".format(target.name, random.choice(die_messages)))  # hee hee funny

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
                if item == None:
                    pass
                elif item == enemy.item_trigger:
                    print("ITEM TRIGGER!")
                    enemy.trigger()

        # Special
        elif choice == "s" or choice == "special":
            print("Perform Special on who?")
            target = select(enemies)
            if target.has_special:
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
            else:
                print("You can't do anything!")

        # Escape # TODO: add ability to disable this option before a battle
        elif choice == "e" or choice == "escape":
            if not boss:
                escape_number = randint(1, 100)
                if escape_number < 50:
                    print("[!] You escaped from {}".format(enemy.name))
                    return "Escaped"
                else:
                    print("[!] You couldn't escape!")
                    for enemy in enemies:
                        print("{} attacked!".format(enemy.name))
                        damage(player, enemy.damage)
                        print()
            else:
                print("You aren't getting out of here...")

        # Unknown Command
        else:
            print("'{}' not recognized, please try again.".format(choice))

    # End sequence
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
                return None
            elif int(target) <= len(enemies) and int(target) >= 0:  # check if its within 0-len of targets
                target = enemies[int(target) - 1]
                check = False
            else:
                print("'{}' isn't valid. Type the number, not the name!".format(target))
        except ValueError:
            print("'{}' isn't valid. Type the number, not the name.".format(target))
    return target


class EvilTurtle(Enemy):
    # THIS IS HOW TO CALL OTHER STATS FROM ENEMY CLASS
    def __init__(self, name):
        Enemy.__init__(self, "EvilTurtle", 30, 5, 10, ["rolls around in its shell.",
                                                       "fails to dab."], has_special=True)
        self.name = name

    def special(self, player):
        print("\n----{SPECIAL}----")
        print("[1] Dab "
              "\n[2] Default Dance")
        choice = input(">>>").strip().lower()
        if choice == "dab" or choice == "d" or choice == "1":
            print("ooh my god you just dabbed on that turtle")
            chance = randint(1, 10)
            if chance > 7:  # just a random chance of dab back
                print("BUT IT DABS BACK OH MY GOD!!!!!")
                damage(player, int(player.health / 4))  # TODO: if something ever breaks, its this int
            else:
                self.health = -9999
        elif choice == "default dance" or choice == "dance" or choice == "dd" or choice == "2":
            print("The Turtle is unfazed by your smooth moves!")
            damage(player, 5)
        else:
            print("I'm just gonna assume you're good cuz '{}' aint a choice my guy.".format(choice))


class PtonioOutlaw(Enemy):
    def __init__(self, name):
        self.name = name
        Enemy.__init__(self, self.name,
                       100, 20, 70,
                       ["seems concerned.",
                        "yeehaws at you.",
                        "shatters an empty potion bottle.",
                        "sneers under his 10-gallon hat."], item_trigger="Nap Time")

    def trigger(self):
        print("-[{}] Heh... that silly... potion... wont stop... me...".format(self.name))
        sleep(4)
        print("[!] {} passed out!".format(self.name))
        self.health = 5
        self.damage = 0
        self.doing = ["is passed out." for i in range(919)]


class Longworm(Enemy):
    def __init__(self):
        self.name = "Longworm"
        Enemy.__init__(self, self.name, 40, 10, 10, [
            "wriggles around.",
            "does some weird squiggly crap.",
            "munches on dirt."])


class Timmy(Enemy):
    def __init__(self):
        self.name = "Little Timmy"
        Enemy.__init__(self, self.name, 50, 5, 5, [
            "cries.",
            "offers you a granola bar.",
            "wants his mama.",
            "trips.",
            "looks suspiciously like an egg."
        ], has_special=True)

    def special(self, player):
        choice = choose("----{SPECIAL}----", "Cry", "Slap")

        if choice == "Cry":
            talk("-[TIMMY] damn dude, here's the money. I didn't really need it that much...")
            self.health = 0
            player.traits.append("crybaby")

        elif choice == "Slap":
            talk("-[TIMMY] OOF *drops money*")
            self.health = 0
            player.metadata.append("slapped Timmy")


class Ryan(Boss):
    has_special = True

    def __init__(self):
        self.name = "Ryan, Consumer of the Cosmos"
        self.damage = 1
        self.health = 10000000
        self.xp = 15000
        Boss.__init__(self, "Ryan, Consumer of the Cosmos", 10000000, 1, 15000, ["craves the finest burnt popcorn.",
                                                                                 "prepares for a feast.",
                                                                                 "revs up his Beyblade."],
                      item_trigger="Burnt Popcorn",
                      has_special=True)

    def special(self, player):
        if "Burnt Popcorn" in player.inventory:
            talk("-[RYAN] *sniff* What is that delectable smell?")
            print("[!] Ryan lost 1000 HP from the smell of your popcorn!")
            self.health += -1000
        else:
            talk("[!] You slap Ryan! He loses 5HP")
            talk("-[RYAN] wtf man")

    def trigger(self):
        talk("-[RYAN] Oh man, I love me some Popcorn! MMMMMMMMMMM *dies*")
        self.health = 0


class Wendt(Boss):
    def __init__(self):
        Boss.__init__(self, "Wendt, Leader of the Longbois",
                      600000, 400, 10434,
                      ["towers above you.",
                       "laughs at your puny height",
                       "casts a long shadow."
                       "creates a tornado via the power of Orange Justice.",
                       "breathes in the clouds.",
                       "stands ominously."],
                      has_special=True)

    def special(self, player):
        print("----{SPECIAL}----")
        print("[Longsword Sweep] [Chat]\n"
              "[Convince] [Orange Justice]")
        choice = input(">>>").strip().lower()

        if choice == "longsword sweep":
            print("[!] CRITICAL HIT!")
            #TODO: FINSIH the boss battle. implement Crider as co-boss




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
        print("[!] You have acquired the Beyblade!")
        player.quest = None
        player.completed.append("Defeat Ryan")
    else:
        print("The air is noticeably lighter.")


def defeat_outlaws(player, level=1, amount=3):
    names = ["Jimbob", "Y. Haw", "Cleetus", "Willy", "R. T. Cowboy", "Gideon", "JR", "Clyde", "Don"]
    outlaws = []

    for i in range(amount):
        rand_name = random.choice(names)
        names.pop(names.index(rand_name))
        outlaw = PtonioOutlaw("Outlaw {}".format(rand_name))
        outlaws.append(outlaw)

    status = battle(player, outlaws)
    if status == "Lost":
        print("You got blasted by the Ptonian Outlaws")
        player.health = 1
    elif status == "Won":
        print("You done got {} cowboys! Yeehaw!".format(amount))
        player.completed.append("Defeat the Outlaws")
        player.quest = None
    else:
        print("A sense of yeehaw leaves your body.")


def tutorial_mission(player):
    steve = Enemy("steve", 10, 1, 5, ["is being steve.",
                                      "exists patiently.",
                                      "waits...",
                                      "calls you 'nibba.'"])
    talk("- ready?")
    status = battle(player, [steve])
    if status == "Won":
        talk("- that's what i like to see. here, have some change i found on the ground", 3.1)
        player.money += 14
        print("[!] Gained 14G.")
        sleep(1)
        talk("-oh, lemme heal dem boo boos of yours.", 2)
        print("[!] Your HP has been restored")
        sleep(.5)
        player.health = 100
        player.completed.append("Tutorial")

    elif status == "Lose":
        sleep(1)
        talk("- {}...".format(player.name), 4)
        talk("- that was absolutely retarded. how did you lose? i didn't even try? cmon nibba.", 5)
        talk("- yo ass lucky im a doctor. i might not have a degree but....", 3)
        print("[!] Your HP has been restored.")
        sleep(.5)
        player.health = 100
        talk("- so...")


def defeat_hemlick(player):
    hemlick = PtonioOutlaw("Hemlick")

    status = battle(player, [hemlick])
    if status == "Won":
        sleep(.2)  # this sleep is just to help with continuity
        talk("- Woah there partner, you did it! Yeeehaw!", 3.5)
        player.money += 600
        print("[!] You gained 600G!")
        sleep(.5)
        talk("- That bandit won't be botherin' me no more. Here, this drink's on me.", 4)
        player.health = player.max_health
        print("[!] Your HP was restored!")
        sleep(.5)

        player.completed.append("Teach Hemlick a Lesson")
        player.quest = None

    elif status == "Lose":
        talk("-[HEMLICK] Ain't no finer bandit in Ptonio than I. Get outta here, {}".format(player.name), 3)
    else:
        talk("You decide you don't wanna die today.")


def pest_control(player):
    worms = []
    for i in range(5):
        worms.append(Longworm())

    status = battle(player, worms)

    if status == "Won":
        if "tall" not in player.metadata:
            talk("- Thanks, little one. I shall pay you for your service.", 3)
        elif "Longboi" in player.metadata:
            talk("- Thank you, Longboi {}, for the kind service. Here's your money.".format(player.name), 4)
        else:
            talk("- Thank you my friend. Here is some money for your troubles.", 4)

        print("[!] You got 500G!")
        sleep(.5)
        player.money += 500

        player.completed.append("do Pest Control")
        player.quest = None
    elif status == "Lose":
        talk("dam...", 1.5)
    else:
        talk("Maybe another time...", 2)


def lunchmoney(player):
    kid = Timmy()

    status = battle(player, kid)
    if status == "Won":
        talk("Wow, you just beat up a kid for his lunch money. Wonderful. Great job.", 2.5)
        player.money += 5
        print("[!] You got 5G!")
        player.completed.append("Acquire Lunch Money")
    elif status == "Lose":
        print("damn, a 12 year old beat you up.")
