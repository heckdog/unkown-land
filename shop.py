from essentials import add_commas
from time import sleep
from inventory import view_inventory

# the store contents is housed all within this dict

store = {"bread": 20, "Test Item": 200, "Health Potion": 100}
weapon_store = {"Sword": 100, "digional sword": 100000}
start = {"bread": 20, "Test Item": 150, "Health Potion": 100, "Test Food": 40}
topshelf = {"bread": 20, "Longsword": 1000, "Longbow": 950}
ptonio = {"Mini Health Potion": 50, "Health Potion": 90, "Nap Time" : 40}


def shop(player):
    print("\n----{SHOP}----")
    print("-[TOM] Welcome to the Shop! Whatcha lookin' for?")

    if player.level >= 50:
        print("[B]uy [S]ell [L]eave [Q]uest")
    else:
        print("[B]uy [S]ell [L]eave")
    option = input(">>>").strip().lower()

    # Buying
    if option == "b" or option == "buy":
        buy(player, store)
        return "BuySuccess"

    # Selling
    if option == "s" or option == "sell":
        sell(player, store)
        return "SellSuccess"

    # Leave
    elif option == "l" or option == "leave":
        print("-See ya bruv.")
        return "exit"  # later i may add status codes if things get too complex, so heres one of em.

    # Quest Start
    elif (option == "q" or option == "quest") and player.level >=50:
        print("-[TOM] Eh? You want a quest?")
        sleep(1)
        print("-Alright, I've got one. There's been this one guy, he keeps coming in here with tons of money but robs me anyways.")
        sleep(3)
        print("-He comes in, summons buckets of money, buys 1000s of bread, then the money just vanishes!")
        sleep(1.5)
        print("-I'm not sure how this guy does it, but I don't trust him.")
        sleep(1)
        print("-He's up to something for sure, I tell ye. Here's where I last saw the nard, go give him a piece of your mind, will ye?")
        sleep(3)
        choice = input("Accept Quest? (y/n) \n>>>").lower()
        if choice.find("ye") != -1 or choice == "y":
            print("-Thanks a lot mate, I'll be sure to reward ye once yer back.")
            if player.quest:
                print("-Oh, ye already have a quest. '{}'. Come back once ye done that yeh?".format(player.quest))
            else:

                print("-Aight lad, I've updated yer quest log for ye.")
                player.quest = "Beat up the Developer"
        else:
            print("-Aight then lad, come again some other time. I'm sure he's still out and about, robbin me mates' stores or sum'n."
                  "\n-Keep yer eye out tho, who knows where 'eel turn up next, I tell ye.")
            
    elif option == "q" or option == "quest":
        print("-What? Quest? What do you think, this is some kind of game? That's mad, lad.")

    else:
        print("lol not available rn sorry")


def start_store(player):
    print("\n----{START SHOP}----")
    print("-[FERGUS] Aye lad, welcome to me shop.")
    print("[B]uy [S]ell [Q]uest")
    option = input(">>>").lower().strip()
    if option == "b" or option == "buy":
        buy(player, start)
    elif option == "s" or option == "sell":
        sell(player, start, .7)
    elif option == "q" or option == "quest":
        if not player.quest:
            print("-Eh, you want a quest?")
            sleep(1)
            print("-Well since you're new round here, I'll help ye out.")
            sleep(2)
            print("-See, these Goblins have been messing with me since 2 weeks ago. I bet they've got some Gold on em.")
            sleep(2)
            print("-Mess em up til ye got 400G. I've added a mission for ye. Good luck.")
            player.quest = "Mess with Goblins"
        else:
            print("-You've already got a quest lad! {}".format(player.quest))
            print("Want to remove this quest? (y/n)")
            choice = input(">>>").lower().strip()
            if choice == "y" or choice == "yes":
                player.quest = None
                print("Done!")
            else:
                print("Quest not changed.")


def weapon_store(player):
    print("\n----{SHOP}----")
    print("-Oi lad, whatcha be lookin' for?")
    print("[B]uy [S]ell")


def topshelf_store(player):
    print("\n----{SHOP}----")
    if "tall" in player.traits:
        print("-Aye big boi. Come take a look at what I've got for ye today.")
    elif "longboi" in player.traits:
        print("-Aye, it's that new Longboi! Please, come, take a look at what I've got for ye.")
    else:
        print("-Welcome wee one. Come take a look on the stool at what we have in stock.")
    print("[B]uy [S]ell")
    option = input(">>>").lower().strip()
    if option == "b" or option == "buy":
        buy(player, topshelf)
    elif option == "s" or option == "sell":
        if "Longboi" in player.traits:
            sell(player, topshelf, .73)
        else:
            sell(player, topshelf, .69)


def ptonio_store(player):
    print("\n----{PTONIO SHOP}----")
    print("-[PHILO] Howdy! Welcome to Philo's Ptonio Potions!")
    print("[B]uy [S]ell")
    option = input(">>>").lower().strip()
    if option == "b" or option == "buy":
        buy(player, ptonio)
    elif option == "s" or option == "sell":
        sell(player, ptonio, .7)


def buy(player, stock):
    print("-Here's what I've got in stock:")
    print("----------------")
    for item in stock:
        price = stock[item]
        print("{} -- {}G".format(item, add_commas(price)))
    print("----------------")
    print("You have {}G".format(add_commas(player.money)))
    choice = input("What would you like?\n>>>")
    if choice in stock:
        price = stock[choice]
        try:
            amount = int(input("How many?\n>>>"))
        except TypeError:
            amount = 1  # if u dunno how to put numbers u get one deal with it
        total = amount * price

        if total > player.money:  # gotta be sure they can afford it
            print("You can't afford that! You have {}G, this costs {}G".format(add_commas(player.money), add_commas(total)))
            return "NoMoney"

        confirm = input("Buy {} {} for {}G? (y/n)\n>>>".format(amount, choice, total)).lower().strip()
        if confirm == "y" or confirm == "yes":
            player.money += -total
            print("Sold! You now have {}G.".format(add_commas(player.money)))
            if choice in player.inventory:  # if the item already exists in player inventory
                player.inventory[choice] += amount  # set the items amount higher
            else:  # else, if its a new item
                player.inventory.update({choice: amount})  # create it using this method. idk why it has to be this way, otherwise throws KeyError
        else:
            print("-ok then nvm u wont get it smh")
    else:
        print("[!] \"{}\" is not available!".format(choice))


def sell(player, stock, modifier=.75):
    print("-What are you selling?")
    view_inventory(player)
    choice = input(">>>").strip()

    if choice in player.inventory and choice in stock:
        try:
            amount = int(input("How many?\n>>>"))
        except TypeError:
            amount = 1

        if amount > player.inventory[choice]:
            print("Entered too high of a value!")
            return "HighValue"

        base_price = stock[choice] * modifier
        price = int(base_price * amount)
        if amount == 1:
            print("Sell a {} for {}G?".format(choice, base_price))
        else:
            print("Sell {} {}s for {}G? ({}G each)".format(amount, choice, price, base_price))

        confirm = input("(y/n)\n>>>").lower().strip()
        if confirm == "y" or confirm.find("ye") != -1:  # sell confirm
            print("Sold {} {} for {}G!".format(amount, choice, price))
            player.money += price
            player.inventory[choice] += -amount
            return "Sold"

        else:  # cancel
            print("You cancelled the sale.")
            return "Cancel"
    else:
        print("This store doesn't purchase that!")
