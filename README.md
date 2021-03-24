# The Pill Bot
<center>
  <img width="200" alt="pill icon" src="https://raw.githubusercontent.com/Ricky-MY/The-Pill-Bot/main/bot/assets/pngtree_pillcartoon.png">
</center>

## Table of Contents
1. [Overview](#overview)
2. [Key-Features](#key-features)
2. [Explanation](#) 
3. [Installation](#)

### Overview
-------------
**The Pill Bot**, otherwise known as *~~The Lion Bot~~* is a **[discord.py](https://github.com/Rapptz/discord.py)** bot that supports a large variety of commands and functions.

### Key Features
* Made easy to understand / analyze
* Statically Typed
* Utilizies Standard Libs
* SnekBox / Eval

### Explaination
A in-depth documentation of all the `modules`, `commands` and `concepts` with examples contained in the **extensions** folder.
<details>
<summary>Modules</summary>
<div>

**1. [Admin](https://github.com/Ricky-MY/The-Pill-Bot/tree/main/bot/extensions/admin)**
<br>
&nbsp;&nbsp;&nbsp;&nbsp;i. Handles cog IO(insert-outcast)<br>
&nbsp;&nbsp;&nbsp;&nbsp;ii. Error catching. Majority of the how it does the job has high subjectivity to a specific module. This is done to improve responses.

**2. [Advance/Meta](https://github.com/Ricky-MY/The-Pill-Bot/tree/main/bot/extensions/advance)**
<br>
&nbsp;&nbsp;&nbsp;&nbsp;i. Contains advance modules such as `eval` and `docs`(docs is still in the working). The eval command is implemented with **[snekbox](https://github.com/python-discord/snekbox)** to achieve a secure way of executing code.

**3. [Games/Fun](https://github.com/Ricky-MY/The-Pill-Bot/tree/main/bot/extensions/games)**
<br>
&nbsp;&nbsp;&nbsp;&nbsp;i. This module holds a variety of games such as, `connect four`, `slots` and so on...

**4. [Miscellaneous](https://github.com/Ricky-MY/The-Pill-Bot/tree/main/bot/extensions/misc)**
<br>
&nbsp;&nbsp;&nbsp;&nbsp;i. Code for procedural(sorta) generating help command.
<br>
&nbsp;&nbsp;&nbsp;&nbsp;ii. Last but not least global and local tags.

**5. [Moderation](https://github.com/Ricky-MY/The-Pill-Bot/tree/main/bot/extensions/moderation)**
<br>
&nbsp;&nbsp;&nbsp;&nbsp;i. Presumably, the moderation module contains all the commands related to server moderation, namely; `mute`, `silent`, `ban`, `quara`, `kick` and so on... 

**6. [Utilities](https://github.com/Ricky-MY/The-Pill-Bot/tree/main/bot/extensions/utils)**
<br>
&nbsp;&nbsp;&nbsp;&nbsp;i. Contains the cog that allows user to fetch source code of a given command through discord.
<br>
&nbsp;&nbsp;&nbsp;&nbsp;ii. Contains embed threading (making a discord embed through a command).
</div>
</details>
<br>

<details>
<summary>Commands</summary>
<div>

---
**Moderation Commands**
| Usage|Explaination|  
| -----| ----------
|`p!mutesetup `|Prepares the server for a mute role that strips away send message access from the user.|
|`p!permanentmute <member>`|Permanently restrict send message access from the user. |
|`p!mute <member> [time=10m]`|Temporarily restrict send message access from a user for a set amount of time. |
|`p!selfmute [time=10m]`|Restrict send message access for yourself server-wide. |
|`p!unmute <member>`|Removes an active mute from a user whether it be permanent or temporary.|
|`p!ban <member> [reason=Unspecified]`|Places a permanent ban on a user.|
|`p!silent `|Removes texting access from everyone on the channel invoked in.|
|`p!unban <id_> [reason=Unspecified]`|Lifts an active ban on a user.|
|`p!clear [amount=5] [user]`|Removes a certain amount of messages from the channel of which the command is used in. |
|`p!kick <member> [reason=Unspecified]`|Removes a user from the server. Beware that the user can still re-join, |
|`p!unsilent `|Reverts channel silencing, thus giving back texting access to everyone for the channel invoked in.|

---
**Utility Commands**
| Usage|Explaination|
| -----| ----------
|`p!thread <channel> <color> <properties>`||
|`p!prefix `||
|`p!code <command>`|Reveals the source code of a command. Source code relating administrative modules or anti-nuke modules are prohibited from visibility.|

---
**Admin Commands**
| Usage|Explaination|
| -----| ----------
|`p!debug `|Enables debug mode that adjusts raise_norm to redirect tracebacks from the console |

---
**Advance Commands**
| Usage|Explaination|
| -----| ----------
|`p!allcommands `||
|`p!eval <code>`|Runs python code provided in a sandbox and returns the value. |

---
**Games Commands**
| Usage|Explaination|
| -----| ----------
|`p!rickroll [member]`|Sends a trustable looking link or a gif that later unveils to be a rickroll. Caution: this may cause massive emotional damage towards the victim.|        
|`p!8ball <text>`|Basic 8 ball command that answers your question with answers ranging from an astounding yes to an absolute no.|
|`p!connectfour <opponent>`|Connect four is a game of vertical checkers with whoever succeeds to place down 4 straight ellipses wins.|
|`p!joke `|Sends a random joke|
|`p!latency `|Shows bot's latency to the discord server|
|`p!poop `|Pooping publicly in random places. Caution; can lead to an immediate arrests for indecent exposure|
|`p!slap [member]`|Slaps a user. If no user is mentioned, a random user is picked.|
|`p!hug [member]`|Hugs a user. If no user is mentioned, it will hug a random user.|
|`p!diceroll [sides=6]`|A dice roll. The dice has 6 sides by default but you can still pass in sides as an argument|
|`p!selfban [reason=Unspecified reason]`|Fake ban or a self ban that does not ban the user in actuality.|
|`p!kiss <member>`|Kisses a user. If no user is mentioned, it will kiss a random user, ouch! That might be a bit awkward.|

---
**Miscellaneous Commands**
| Usage|Explaination|
| -----| ----------
|`p!invite `|Gets the invite link for the support server of the bot.|
|`p!gtag <name>`||
|`p!addrole <name> [hex_colour_code=#000000] [hoist=False]`|Creates a role with basic permissions and a specifiable name, color and hoist choices.|
|`p!delrole [roles]...`|Remove roles in bulk.|
|`p!avatar [member]`|Retrieves the avatar of a user.|
|`p!migrate <ini_id> <end_id>`||
|`p!userinfo [member]`||
|`p!membercounter <channel>`||
|`p!help [module]`|Main help command that shows you an index of all the modules and their respective help command.|

</div>
</details>