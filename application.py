from discord.ext import commands
import functions

TOKEN = 'NzQzODkyMDcxNzM5MjkzNzA3.XzbReg.qeNyE2r4N5JcRcgpP-8nCV7NjpU'

bot = commands.Bot(command_prefix="-")
players = {}
main_channel = ""
order = []
d = []


@bot.command(name="instructions")
async def instructions(ctx):
    await ctx.send("One Night Werewolf is a hidden role game. There are two teams: the villagers and the werewolves. "
                   "The villagers' goal is to figure out who the werewolves are and kill them. The werewolves' goal"
                   " is to survive by convincing the villagers that they are on their side.\n\nAt the start of each "
                   "'night,' players receive roles indicating their team. Some roles have special night actions, such"
                   " switching other players' cards. Instructions on how to complete these will be sent out on each "
                   "players' turn. After every player has completed their night actions, players have 5 minutes to "
                   "discuss who they believe the werewolf is, before voting on who to kill. If a werewolf is killed, "
                   "the villagers win; otherwise, the werewolves win.")


@bot.command(name="newgame")
async def newgame(ctx):
    await ctx.send("Welcome to One Night Werewolf! Send -join [nickname] to join the game, and send -allin if everyone "
                   " has joined.")


@bot.command(name="join")
async def join(ctx, arg):
    global players
    obj = functions.Player(ctx.author, arg, 0)
    players[obj] = 0


@bot.command(name="allin")
async def allin(ctx):
    global main_channel
    main_channel = ctx.channel
    await ctx.send("If you would like to create a custom deck, enter -select custom. Otherwise, enter -select default.")


@bot.command(name="select")
async def select(ctx, arg):
    global players, d
    if arg == "default":
        if len(players) <= 5:
            d = functions.default_deck(len(players))
            await ctx.send("Deck generated. Type -done to continue.")
        else:
            d = functions.default_deck(5)
            await ctx.send("Your deck currently consists of 3 villagers, 2 werewolves, the seer, the troublemaker, "
                           "and the robber. Type -select [role] to add other roles to your deck (-listroles for "
                           "options)")
    elif arg == "custom":
        await ctx.send("Type -select [role] to add roles to your deck (-listroles for options)")
    else:
        arg = arg.capitalize()
        if arg not in functions.options:
            await ctx.send("Invalid role. Try again.")
        else:
            d.append(functions.Card(arg))
            await ctx.send(f'{arg} added. Type -select [role] to continue adding roles, or -done to begin game.')


@bot.command(name="done")
async def done(ctx):
    global d, order
    functions.deal(players, d)
    order = functions.sort_players(players)
    for n in order:
        msg = f'Your role is {n.get_card()}. '
        msg += functions.instructions(n.get_card().get_name())
        msg += f' Please wait for further instructions--you will receive a message on your turn.'
        await n.get_user().send(msg)
    if players[order[0]] == "Doppelganger":
        msg = "Send -copy [player nickname] to copy their role (-listnames to get a list of all player nicknames)"
    elif players[order[0]] == "Werewolf":
        msg = functions.werewolf(players, d, order[0])
    elif players[order[0]] == "Minion":
        msg = functions.minion(players)
    elif players[order[0]] == "Seer":
        msg = "Send -see [player nickname] to see their card (-listnames to get a list of all player nicknames)"
    elif players[order[0]] == "Mason":
        msg = functions.mason(players, order[0])
    elif players[order[0]] == "Robber":
        msg = "Send -rob [player nickname] to steal their card (-listnames to get a list of all player nicknames)"
    elif players[order[0]] == "Troublemaker":
        msg = "Send -swap [player nickname] [player nickname] to swap two players cards (-listnames to get a list of" \
              " all player nicknames)"
    else:
        msg = "You have no night action."
    await order[0].get_user().send(msg)


@bot.command(name="next")
async def next_player(ctx):
    global players, order, d, main_channel
    prev = ctx.author
    player_found = False
    for n in order:
        if prev == n.get_user():
            player_found = True
        elif player_found:
            player_found = False
            if players[n] == "Doppelganger":
                players[n] = n.get_card().get_name()
            if players[n] == "Werewolf":
                msg = functions.werewolf(players, d, n)
            elif players[n] == "Minion":
                msg = functions.minion(players)
            elif players[n] == "Seer":
                msg = "Send -see [player nickname] to see their card (-listnames to get a list of all player nicknames)"
            elif players[n] == "Mason":
                msg = functions.mason(players, n)
            elif players[n] == "Robber":
                msg = "Send -rob [player nickname] to steal their card (-listnames to get a list of all player " \
                      "nicknames)"
            elif players[n] == "Troublemaker":
                msg = "Send -swap [player nickname] [player nickname] to swap two players cards (-listnames to get a " \
                      "list of all player nicknames)"
            elif players[n] == "Insomniac":
                msg = functions.insomniac(n)
            elif players[n] == "Drunk":
                msg = functions.drunk(d, n)
            else:
                msg = "You have no night action. Type -next to continue."
            await n.get_user().send(msg)
            break
    if player_found:
        await main_channel.send("All players have completed their roles. You now have 5 minutes to discuss.")


@bot.command(name="copy")
async def copy(ctx, arg):
    global players, d
    player_id = ctx.author
    for n in players:
        if n.get_user() == ctx.author:
            player_id = n
            break
    functions.doppelganger(players, player_id, arg)
    await ctx.send(f'Your new role is {player_id.get_card().get_name()}.')
    if player_id.get_card().get_name() == "Insomniac":
        pass
    elif player_id.get_card().get_name() == "Werewolf":
        await ctx.send(functions.werewolf(players, d, player_id))
    elif player_id.get_card().get_name() == "Minion":
        await ctx.send(functions.minion(players))
    elif player_id.get_card().get_name() == "Seer":
        await ctx.send("Send -see [player nickname] to see their card.")
    elif player_id.get_card().get_name() == "Mason":
        await ctx.send(functions.mason(players, player_id))
    elif player_id.get_card().get_name() == "Robber":
        await ctx.send("Send -rob [player nickname] to steal their card.")
    elif player_id.get_card().get_name() == "Troublemaker":
        await ctx.send("Send -swap [player 1] [player 2] to swap cards.")
    elif player_id.get_card().get_name() == "Drunk":
        await ctx.send(functions.drunk(d, player_id))


@bot.command(name="see")
async def see(ctx, arg):
    global players
    await ctx.send(functions.seer(players, arg))


@bot.command(name="rob")
async def rob(ctx, arg):
    global players
    robber_id = ctx.author
    for n in players:
        if n.get_user() == ctx.author:
            robber_id = n
            break
    await ctx.send(functions.robber(players, robber_id, arg))


@bot.command(name="swap")
async def swap(ctx, arg1, arg2):
    global players
    await ctx.send(functions.troublemaker(players, arg1, arg2))


@bot.command(name="listnames")
async def listnames(ctx):
    global players
    msg = ""
    for n in players:
        msg += f'{n.get_name()}\n'
    await ctx.send(msg)


@bot.command(name="listroles")
async def listroles(ctx):
    msg = "Your options are:\n"
    for n in functions.options:
        msg += f'{n}\n'
    await ctx.send(msg)


@bot.command(name="vote")
async def vote(ctx, arg):
    global players
    all_votes = True
    for n in players:
        if n.get_user() == ctx.author:
            if n.get_vote():
                await ctx.send("You have already voted.")
            else:
                n.vote()
        elif n.get_name() == arg:
            n.add_vote()
            await ctx.send("Voted.")
    for n in players:
        if not n.get_vote():
            all_votes = False
            break
    if all_votes:
        loser = 0
        for n in players:
            if loser == 0:
                loser = n
            elif n > loser:
                loser = n
        await ctx.send(f'You have chosen to kill {loser.get_name()}. Their role was {loser.get_card().get_name()}.')
        if loser.get_card() == "Werewolf":
            await ctx.send("Villagers win!")
        elif loser.get_card() == "Tanner":
            await ctx.send("Tanner wins!")
        else:
            await ctx.send("Werewolves win!")


bot.run(TOKEN)
