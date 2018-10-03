from essentials import *


def view_inventory(player):
    print("\n----{INVENTORY}----")
    if not player.inventory:  # if nothing exists in the inventory
        print("[*] Nothing!")
    else:
        for item in player.inventory:
            print("[*] {} ({})".format(item, add_commas(player.inventory[item])))

# tODO: why it make u equip bread

def use_item(player):
    # TODO: maybe make weapons in lowercase too or something with a for loop
    view_inventory(player)
    choice = input("Which item would you like to use? \n>>>").strip()
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

    elif choice in player.inventory:
        use = input("Use {}? \n>>>".format(choice)).strip().lower()
        if use == "y" or use.find("ye") != -1:
            player.inventory[choice] += -1
            print("Used one {}!".format(choice))

