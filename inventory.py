from essentials import *


def view_inventory(player):
    print("\n----{INVENTORY}----")
    if not player.inventory:  # if nothing exists in the inventory
        print("[*] Nothing!")
    else:
        for item in player.inventory:
            print("[*] {} ({})".format(item, add_commas(player.inventory[item])))


def use_item(player, battle=False):
    # TODO: maybe make weapons in lowercase too or something with a for loop
    #view_inventory(player)
    choice = select(player.inventory)

    # Equipping Weapons
    if (choice in weapons) and (choice in player.inventory):  # valid weapon and does exist on player
        equip = input("Equip {}? \n>>>".format(choice)).strip().lower()  # ask to be sure
        if equip == "y" or equip.find("ye") != -1:  # if yes
            # Taking the old weapon
            # if choice in player.inventory and player.weapon != "Fists":  # if the item already exists in player inventory
            #     player.inventory[player.weapon] += 1  # put that weapons count up
            if player.weapon != "Fists":
                player.inventory.update({player.weapon: 1})  # why does this work?
            player.weapon = choice
            player.inventory[choice] -= 1  # REMOVE THE OBJECT FROM INVENTORY BC ITS NOW IN WEAPON SLOT.

            print("Equipped {}!".format(choice))

    # Using Healing Items
    elif (choice in health_items) and (choice in player.inventory):
        if player.health < player.max_health:
            use = input("Use {}? (y/n)\n>>>".format(choice)).strip().lower()
            if use == "y" or use.find("ye") != -1:
                player.inventory[choice] += -1  # take that item away by one
                player.health += health_items[choice]  # add the health value of the item to player
                if player.health > player.max_health:
                    player.health = player.max_health  # sets the health to max if it went over
                print("Healed {}. You now have {}/{} HP.".format(health_items[choice], player.health, player.max_health))
        else:
            print("You are already at max health!")

    # Quest Items
    elif choice in quest_items and choice in player.inventory:
        if battle:
            use = input("Use the {}? (y/n)\n>>>".format(choice)).strip().lower()
            if use == "y" or use.find("ye") != -1:
                player.inventory[choice] += -1
        else:
            print("You shouldn't use that now.")

    # Other Items
    elif choice in player.inventory:
        use = input("Use {}? It doesn't seem to do anything. \n>>>".format(choice)).strip().lower()
        if use == "y" or use.find("ye") != -1:
            player.inventory[choice] += -1  # removes the object
            print("Used one {}. You feel strangely sad about losing it, as if it wasn't meant to be used up.".format(choice))

    # get rid of fists cuz they gay
    if "Fists" in player.inventory:
        player.inventory["Fists"] = 0

    # Empty Check
    try:
        if player.inventory[choice] <= 0:
            test = player.inventory.pop(choice, None)  # this gets rid of that option and returns None if an error
            if test:  # if error is reported.
                print("You shouldn't see this text. If you do, line 68 under inventory.py went horribly wrong.")
    except KeyError:
        if choice:  # this just prevents a visual error if select() cancelled.
            print("{} isn't in your inventory!".format(choice))
    return choice


def select(inventory):
    check = True
    inv_list = list(inventory.keys())
    while check:
        print("Use which item? (type 'cancel' to cancel)")
        for item in inventory:
            print("[{}] {} ({})".format(inv_list.index(item) + 1, item, inventory[item]))

        target = input(">>>").strip()

        if target in inv_list:
            return target
        else:
            try:
                if target.lower() == "cancel":
                    return None
                elif int(target) <= len(inventory) and int(target) > 0:  # check if its within 0-len of targets
                    target = inv_list[int(target) - 1]
                    check = False
                else:
                    print("'{}' isn't valid.\n".format(target))
            except ValueError:
                print("'{}' isn't a valid item.\n".format(target))
    return target



