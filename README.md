# One Night Werewolf: Discord Bot Edition
Note: V1 is a direct copy, rules-wise, of One Night Werewolf (in that it does only lasts for one night); I will probably add a v2 later that more closely reflects the version my friends play (lasts until all villagers/werewolves are eliminated). 

## Background
The game One Night Werewolf is a hidden role game similar to Mafia. In each round of the game players receive a card with a role on it, assigning them either the werewolves’ or villagers’ team. Some of these cards also have special features, like being able to look at another players card or swap different players' cards. 

My friends loved playing this game in person in our first year of university, but this was obviously complicated by COVID-19 when we could no longer meet in person. To make up for this, I decided to program a bot that would allow us to play a version of the game using the group chat app Discord. It would used text-based commands to randomly assign a role to each player by privately messaging them, giving them clear instructions on how to perform their “role” in a virtual setting. While players discussed who they thought was the werewolf in a voice chat, they would then be able to vote by message in the server, and once every player had voted the bot would announce the winners.

![Screenshot (391)](https://user-images.githubusercontent.com/22796402/184992836-cae4e6e3-1de2-4d2e-b854-09fa62a2983f.png)

Rules and roles are further explained in the code, both when you send the command "-instructions" and when you receive your role directly, so no prior knowledge of One Night Werewolf is required to play using the bot--all you need is an IDE like Pycharm and your own Discord API token, which you can put in a file call "save.txt" to run the bot as is.

## Code

In v1.py, each method represents a bot command that can be sent by a player, preceded by a hyphen (command prefix) so the bot is listening for it. For example, sending the message "-newgame" in a Discord server would start a new game of One Night Werewolf and the bot would send a short message about how to join the game. This file is entirely used to track bot commands, sending messages to players when necessary, so the majority of the actual game functionality is stored in functions.py.

I created objects for both players and cards, mainly so I could override comparison operators and make my code more readable. For cards, this was so that I could ensure that all roles were sent in a specific order by comparing their placement in a defined order list (for example, the Seer needs to go before any roles that involve swapping cards). I also overrode the representation method to make sending messages about roles easier. For players, the comparison operators were used to keep track of how many votes each player had at the end of the game. I also added methods to get/set the card each player had, which was very useful as roles got swapped around. Most importantly, I associated nicknames with each player to allow other players to more easily complete their night actions. 

Each role  has an associated method that allows players to complete their night action in functions.py. Most of the time, this will involve looking at or swapping a specific player's card. The nicknames were useful because a player could actually get a list of all players in the game by nickname (using -listnames) before running their own command to target another player from the list (for example, a Robber would type -rob [nickname]). 

![Screenshot (390)](https://user-images.githubusercontent.com/22796402/184992897-752b16d7-a613-4a2d-b9f4-5af940da4ec0.png)

## Next Steps
Due to its use of global variables to store players, this bot effectively only works for one server at a time (not a problem for my friends and I, but would have to be modified if this were to be released publicly; maybe by using a database). The bot also ends up producing a lot of command messages in the server [image], which can be inconvenient. My friends got around this by creating a channel entirely dedicated to playing the game.
