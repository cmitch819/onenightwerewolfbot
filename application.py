import discord
import functions
import time
import asyncio

TOKEN = 'NzQzODkyMDcxNzM5MjkzNzA3.XzbReg.qeNyE2r4N5JcRcgpP-8nCV7NjpU'

client = discord.Client()
selection_mode = False
game = False
allin = False
vote_mode = False
players = {}
order = []
d = []
main_channel = ""
start_time = 0
temp = {}
voted = []
votes = {}
num_players = 0


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    global game, players, order, d, main_channel, allin, start_time, temp, voted, votes, selection_mode, num_players
    if "-newgame" in message.content:
        game = True
        main_channel = message.channel
    if game:
        if "-newgame" in message.content:
            await message.channel.send("Welcome to One Night Werewolf! Send a message if you'd like to join the game.")
        elif "-allin" in message.content:
            selection_mode = True
            game = False
        elif str(message.author) != "OneNightWerewolfBot#5215" and message.author not in players:
            players[message.author] = 0
            num_players += 1
    if selection_mode:
        if "-allin" in message.content:
            await message.channel.send("Enter -default to use default deck and -custom to create your own deck.")
        elif "-default" in message.content:
            if num_players <= 5:
                d = functions.default_deck(num_players)
                selection_mode = False
                allin = True
            else:
                pass  # function for add cards
        elif "-custom" in message.content:
            pass  # function for add cards
        elif "-done" in message.content:
            selection_mode = False
            allin = True
    if allin and str(message.author) != "OneNightWerewolfBot#5215":
        if "-done" in message.content or "-default" in message.content:
            functions.deal(players, d)
            order = functions.sort_players(players)
            for player in players:
                temp[player] = players[player]
                msg = f'Your role is: {players[player]}. '
                msg += functions.instructions(players[player])
                await player.send(msg)
        if len(order) > 0:
            if temp[order[0]] == "Werewolf":
                msg = functions.werewolf(players, d)
            elif temp[order[0]] == "Minion":
                msg = functions.minion(players)
            elif temp[order[0]] == "Seer":
                msg = "Whose card would you like to see?"
            elif temp[order[0]] == "Robber":
                msg = "Whose card would you like to steal?"
            elif temp[order[0]] == "Troublemaker":
                msg = "Whose cards would you like to swap?"
            else:
                msg = "You have no night action."
            await order[0].send(msg)
            if temp[order[0]] == "Werewolf" or temp[order[0]] == "Villager" or temp[order[0]] == "Minion":
                order.remove(order[0])
        else:
            await main_channel.send("All players have completed their roles. You now have 5 minutes to discuss your "
                                    "suspicions and make a decision.")
        if message.channel.type is discord.ChannelType.private and str(message.author) != "OneNightWerewolfBot#5215":
            if temp[order[0]] == "Seer":
                msg = functions.seer(players, message.content)
            elif temp[order[0]] == "Robber":
                msg = functions.robber(players, message.author, message.content)
            elif temp[order[0]] == "Troublemaker":
                names = str(message.content).split(",")
                for j in range(len(names)):
                    names[j] = names[j].strip()
                msg = functions.troublemaker(players, names[0], names[1])
            else:
                msg = "You have no night action."
            await order[0].send(msg)
            order.remove(order[0])

    elif vote_mode:
        pass
    elif "-vote" in message.content:
        if message.author in voted:
            await message.channel.send("You have already voted.")
        else:
            voted.append(message.author)
            name = message.content[6:]
            if name in votes:
                votes[name] += 1
            else:
                votes[name] = 1
        if len(voted) > len(players):
            kill = ""
            role = ""
            max_votes = 0
            for n in votes:
                if votes[n] > max_votes:
                    kill = n
            for name in players:
                if name.name == kill:
                    role = players[name]
            await message.channel.send(f'You have chosen to kill {kill}. {kill}\'s role was {role}.')
            if role == "Werewolf":
                await message.channel.send(f'Villagers win!')
            else:
                await message.channel.send(f'Werewolves win!')

    print(players)


client.run(TOKEN)
