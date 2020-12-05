import discord
import json
from discord.ext import commands


class Help(commands.Cog):

	def __init__(self, client):
		self.client = client

	@commands.group(name=str("help"), invoke_without_command=True)
	@commands.guild_only()
	async def help(self, ctx):
		with open('prefixes.json', 'r') as f:
			prefixes = json.load(f)
		current_prefix = str(prefixes[str(ctx.guild.id)])
		embed = discord.Embed(color=discord.Colour.dark_gold())
		fields = [('[Moderation]',
				   f"`{current_prefix}help moderation`\nThe moderation module includes all basic moderation commands, for each command you need the corresponding server permission, for isntance, a person will be able to ban people if they themselves have the ban_members permission for the guild.",
				   False),
				  ('[Miscellaneous]',
				   f"`{current_prefix}help misc`\nA guide to all miscellaneous commands that exists, this includes a wide variety of utilities that can furthermore increase your capability as a server owner.",
				   True),
				  ('[Greeting]',
				   f"`{current_prefix}help greet`[Maintenance]\nA customizable welcoming system that you could use to welcome people",
				   True),
				  ('[MemberCounter]',
				   f"`{current_prefix}help mbc`\nA module that allows you to setup a voice channel as a member counter that changes its name to the amount of members in ur server",
				   True),
				  ('[Tag]',
				   f"`{current_prefix}help tag`\nA module that allows you store text that can be recalled with a name",
				   True),
				  ('[TypeWriter]',
				   f"`{current_prefix}help typewriter`\nA module that allows you create, send, edit and fully customize an embed.",
				   True),
				  ('[Magic]', f"`{current_prefix}help magic`\nMystic arts from harry potter", True)
				  ]
		for name, value, inline in fields:
			embed.add_field(name=name, value=value, inline=inline)
		embed.set_author(name="-=The Lion's Help Menu=-")
		embed.add_field(name='[Levelling]',
						value=f"`{ctx.prefix}help level`[Maintenance]\nA chat levelling system that can be used to allow people to level up corresponding to the messages they send")
		#	embed.add_field(name='[ReactionRole]', value=f"`{ctx.prefix}help rrole`\nA reaction role function that allows you to setup reactionroles for messages")
		await ctx.send(embed=embed)

	@help.command()
	@commands.guild_only()
	async def moderation(self, ctx):
		with open('prefixes.json', 'r') as f:
			prefixes = json.load(f)
		current_prefix = str(prefixes[str(ctx.guild.id)])
		embed = discord.Embed(title='=Moderation Commands=', color=discord.Color.dark_gold())
		fields = [('Kick', f'`{current_prefix}kick (@user) [reason]`'),
				  ('Ban', f'`{current_prefix}ban (@user) [reason]`'),
				  ('UnBan', f'`{current_prefix}unban (@user) [reason]`'),
				  ('Mute', f'`{current_prefix}mute (@user)`'),
				  ('UnMute', f'`{current_prefix}unmute (@user)`')
				  ]
		for name, value in fields:
			embed.add_field(name=name, value=value)
		await ctx.send(embed=embed)

	@help.command()
	@commands.guild_only()
	async def magic(self, ctx):
		fembed = discord.Embed(title="=Grand Warden's Handbook=",
							   description='poop, slap, hug, diceroll, 8ball, ping, gift, rickroll, joke',
							   color=discord.Color.dark_gold())
		await ctx.send(embed=fembed)

	@help.command()
	@commands.guild_only()
	async def misc(self, ctx):
		with open('prefixes.json', 'r') as f:
			prefixes = json.load(f)
		current_prefix = str(prefixes[str(ctx.guild.id)])
		embed = discord.Embed(title='=Miscellaneous Commands=', color=discord.Color.dark_gold())
		fields = [('Users', f'`{current_prefix}members`\nReturns the amount of members in a server'),
				  ('Addrole',
				   f'`{current_prefix}addrole <name> (hex_color_code) (displays_seperately True/False)`\nAdds a role'),
				  ('Giverole', f'`{current_prefix}giverole <member> <role>`\nAssigns a role to the member tagged'),
				  ('Delrole', f'`{current_prefix}delrole (@role)`\nDeletes a role'),
				  ('Avatar', f'`{current_prefix}avatar (@member)`\nReturns the avatar of the member tagged'),
				  ('move', f'`{current_prefix}move (from_vc_id) (to_vc_id)`\nMoves everyone from the voice call of the first ID to the voice call of the second ID.'),
				  ('Prefix', f'`{current_prefix}prefix`\nChecks the current server prefix'),
				  ('Announce', f'`{current_prefix}announce <#channel> <message>`\nAnnounces a text message with a pre-built template.'),
				  ('Announce here', f'`{current_prefix}announce here <#channel> <message>`\nAnnounces a text message with a pre-built template and mentions everyone online.'),
				  ('Announce Everyone', f'`{current_prefix}announce everyone <#channel> <message>`\nAnnounces a text message with a pre-built template and mentions everyone.'),
				  ('Userinformation',
				   f'`{current_prefix}userinfo <member>`\nDisplays the tagged user info, will disaply your info if none is mentioned')
				  ]
		for name, value in fields:
			embed.add_field(name=name, value=value)
		await ctx.send(embed=embed)

	@help.command()
	@commands.guild_only()
	async def aegis(self, ctx):
		with open('prefixes.json', 'r') as f:
			prefixes = json.load(f)
		current_prefix = str(prefixes[str(ctx.guild.id)])
		embed = discord.Embed(title='=Acessing Aegis=', color=discord.Color.dark_gold())
		embed.add_field(name='To access:', value=f'`Execute the "{current_prefix} aegis" command to acess the module`')
		await ctx.send(embed=embed)

	@help.command()
	@commands.guild_only()
	async def greet(self, ctx):
		with open('prefixes.json', 'r') as f:
			prefixes = json.load(f)
		current_prefix = str(prefixes[str(ctx.guild.id)])
		embed = discord.Embed(title="=Greeting System Guide=",
							  description='This system allows you to send customizable welcome messages when a member joins your server!',
							  color=discord.Color.dark_gold())
		fields = [('Setup',
				   f'`{current_prefix}welcome <channel> <hex_color_code> <msg>`\n<channel> : Mention the channel you would like to use for the greeting message\n<msg> : _Type your welcome message here(you can use the special codes from below)_\n<hex-color-code> : _Hex color code for your welcome embed message, use 000000 for default color_'),
				  ('Check', f'`{current_prefix}welcome check`\n Checks what the current preferences for welcome are!'),
				  ('Clear', f'`{current_prefix}welcome clear`\n Clears and disables the greeting system!'),
				  ('Message Limitations',
				   f'_Adding the keywords down below would perform a unique action that allows you to better customize your message!_\n`{{mention}}`: Mentions the new member\n`{{guild}}`: Says the guild name\n`{{user}}`: Says the name of the new member')
				  ]
		for name, value in fields:
			embed.add_field(name=name, value=value)
		await ctx.send(embed=embed)

	@help.command()
	@commands.guild_only()
	async def mbc(self, ctx):
		with open('prefixes.json', 'r') as f:
			prefixes = json.load(f)
		current_prefix = str(prefixes[str(ctx.guild.id)])
		embed = discord.Embed(title='=MemberCounter Guide=', color=discord.Color.dark_gold())
		embed.add_field(name='Setup',
						value=f'`{current_prefix}mbc (VoiceChannelID)`\nThis sets the tagged voice channel into a membercounter that updates its name into the server member count. Use the COPYID function to copy an id of a voice channel and place it in the <VoiceChannelID> argument.')
		embed.add_field(name='Check',
						value=f'`{current_prefix}mbc check`\nShows you what the currently configured channel for member counter is. If none/disabled, it will return as none.')
		await ctx.send(embed=embed)

	@help.command()
	@commands.guild_only()
	async def level(self, ctx):
		with open('prefixes.json', 'r') as f:
			prefixes = json.load(f)
		current_prefix = str(prefixes[str(ctx.guild.id)])
		embed = discord.Embed(title='=Chat Levelling System Guide=', color=discord.Color.dark_gold())
		embed.add_field(name='Rank',
						value=f"`{current_prefix}rank`\nShows you the tagged member's rank in the system, if none is tagged, your rank will be displayed.")
		await ctx.send(embed=embed)

	@help.command()
	@commands.guild_only()
	async def tag(self, ctx):
		with open('prefixes.json', 'r') as f:
			prefixes = json.load(f)
		current_prefix = str(prefixes[str(ctx.guild.id)])
		embed = discord.Embed(title='=Tag Commands=', color=discord.Color.dark_gold())
		embed.add_field(name='Global Tags', value=f'`{current_prefix}gtag <name>`\n This gets the tag with the name from the database.')
		embed.add_field(name='Tags[DISABLED]',
						value=f'`{current_prefix}tag <name>`\n This gets the private tag with the name.\n`{current_prefix}tag add <name> <content>`\n This creates a new tag.\n`{current_prefix}tag remove <name>`\n This removes the private tag with the name.')
		await ctx.send(embed=embed)

	@help.command(aliases=['typewriter', 'typeWriter'])
	@commands.guild_only()
	async def TypeWriter(self, ctx):
		with open('prefixes.json', 'r') as f:
			prefixes = json.load(f)
		current_prefix = str(prefixes[str(ctx.guild.id)])
		embed = discord.Embed(title='=TypeWriter Commands=', color=discord.Color.dark_gold())
		embed.add_field(name='Threading', value=f"`{current_prefix}thread <#channel> <decimal_color_code> <title%description>`\n Creates a customized embed and sends it directly to any specified channel.\n*Use '%' to split title and description*\n *Use '|' to go to new lines.*")
		embed.add_field(name='AdvanceThreading', value=f"`{current_prefix}advThread`\n Creates a customized embed step by step and sends it directly to a finally mentioned channel.")
		
		embed.add_field(name='Preview',
						value=f'`{current_prefix}thread preview <decimal_color_code> <title%description>`\n This works just like the original command but its a preview that sends the embed to the channel the command is used in.')
		embed.add_field(name='Edit',
						value=f'`{current_prefix}thread edit <#channel> <messageID> <decimal_color_code> <title%description>`\n Edits any pre-existing embeds/messages only sent by the bot.')
		embed.add_field(name='Specified Edit',
						value=f'`{current_prefix}thread edit_<target object> <#channel> <messageID> <value>`\n Specifically edits an attribute of any embeds, i.e.color of an embed, description of an embed etc... The input value may vary as the target object changes.')
		
		embed.add_field(name='Announce selectively[CUSTOM]', value= f'`{current_prefix}announce selective <#channel> <message>`\nAnnounces a text message with a pre-built template and mentions everyone with the <@&756865729550090330> role.'),
				  
		await ctx.send(embed=embed)

	@help.command()
	@commands.guild_only()
	async def rrole(self, ctx):
		with open('prefixes.json', 'r') as f:
			prefixes = json.load(f)
		current_prefix = str(prefixes[str(ctx.guild.id)])
		embed = discord.Embed(title='=Reaction Role Guide=', color=discord.Color.dark_gold())
		embed.add_field(name='Setup',
						value=f"`{current_prefix}rrole <#channel> <message_id> <emoji> <@role>`\nThis command allows you to setup reactionroles\n<#channel> : _Mention the channel where the message with reactionrole will be_\n<message_id> : _Insert the message ID of the message you'd like people to react to, to get roles_\n<emoji> : _The emoji people would react with to get the role mentioned_\n<@role> : _The role people would get when reacted with the set emoji_")
		embed.add_field(name='Check',
						value=f'`{current_prefix}rrole check`\n Checks all reaction role objects for your server')
		embed.add_field(name='Clear',
						value=f'`{current_prefix}welcome clear <message_id>`\n Clear all reaction role objects corresponding to the message ID')
		await ctx.send(embed=embed)


def setup(client):
	client.add_cog(Help(client))
	print('Help.cog is loaded')
