from essentials import *


def view_inventory(player):
    print("\n----{INVENTORY}----")
    if not player.inventory:  # if nothing exists in the inventory
        print("[*] Nothing!")
    else:
        for item in player.inventory:
            print("[*] {} ({})".format(item, add_commas(player.inventory[item])))


def use_item(player):
    # TODO: maybe make weapons in lowercase too or something with a for loop
    view_inventory(player)
    choice = input("Which item would you like to use? \n>>>").strip()

    # Equipping Weapons
    if (choice in weapons) and (choice in player.inventory):
        equip = input("Equip {}? \n>>>".format(choice)).strip().lower()
        if equip == "y" or equip.find("ye") != -1:
            # Taking the old weapon
            if choice in player.inventory and player.weapon != "Fists":  # if the item already exists in player inventory
                player.inventory[player.weapon] += 1  # put that weapons count up
            elif choice != "Fists":  # anything but nothing. I should really make "Fists" -> None
                player.inventory.update({player.weapon: 1})  # why does this work?
            player.weapon = choice

            print("Equipped {}!").format(choice)

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

    # Other Items
    elif choice in player.inventory:
        use = input("Use {}? It doesn't seem to do anything. \n>>>".format(choice)).strip().lower()
        if use == "y" or use.find("ye") != -1:
            player.inventory[choice] += -1
            print("Used one {}. You feel strangely sad about losing it, as if it wasn't meant to be used up.".format(choice))

    # Empty Check
    if player.inventory[choice] <= 0:
        test = player.inventory.pop(choice, None)  # this gets rid of that option and returns None if an error
        if not test:
            print("You shouldn't see this text. If you do, line 57 under inventory.py went horribly wrong.")



