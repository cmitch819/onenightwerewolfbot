# One Night Werewolf: Discord Bot Edition
Note: V1 is a direct copy, rules-wise, of One Night Werewolf (in that it does only lasts for one night); I will probably add a v2 later that more closely reflects the version my friends play (lasts until all villagers/werewolves are eliminated). 

The game One Night Werewolf is a hidden role game similar to Mafia. [explain rules further].

[maybe explain what discord is too]

In v1.py, each method represents a bot command that can be sent by a player, preceded by a hyphen (command prefix) so the bot is listening for it. For example, sending the message "-newgame" in a Discord server would start a new game of One Night Werewolf and the bot would send a short message about how to join the game. This file is entirely used to track bot commands, sending messages to players when necessary, so the majority of the actual game functionality is store in functions.py.

I created objects for both players and cards, mainly so I could override comparison operators and make my code more readable. For cards, this was so that I could ensure that all roles were sent in a specific order by comparing their placement in a defined order list (for example, the Seer needs to go before any roles that involve swapping cards, just to make the game a little more interesting and mess with what people know). I also overrode the representation method to make sending messages about roles easier. For players, the comparison operators were used to keep track of how many votes each player had at the end of the game. I also added methods to get/set the card each player had, which was very useful as roles got swapped around. Most importantly, I associated nicknames with each player to allow other players to more easily complete their night actions. 

Each role  has an associated method that allows players to complete their night action in functions.py. Most of the time, this will involve looking at or swapping a specific player's card. The nicknames were useful because a player could actually get a list of all players in the game by nickname (using -listnames) before running their own command to target another player from the list (for example, a Seer would type -see [nickname]). 

[etc etc]

[shortcomings]
Due to its use of global variables to store players, this bot effectively only works for one server at a time (not a problem for my friends and I, but would have to be modified if this were to be released publicly; maybe by using a database). The bot also ends up producing a lot of command messages in the server [image], which can be inconvenient. My friends got around this by creating a channel entirely dedicated to playing the game.
