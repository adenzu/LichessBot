from lichessbot.command import Command
from lichessbot.livegames import *
from lichessbot.commands import *
from lichessbot.config import *
from lichessbot.call import *

import discord



bot = discord.Client()


command_list = Command.__subclasses__()



@bot.event
async def on_ready():
	print(f'We have logged in as {bot.user}')
	bot.loop.create_task(update_live_games())

@bot.event
async def on_message(message):

	if message.author == bot.user:
		return

	elif message.content.startswith(COMMAND_PREFIX) and not message.author.bot:
		
		try:
			call = Call(message)

			for cmd in command_list:
				if cmd.enabled and (call.command == cmd.name or call.command in cmd.aliases):
					
					if not cmd.name in ["help", "stop"]:
						await call.channel.trigger_typing()
	
					call.executed = True

					await cmd.call(call)

			if not call.executed:
				await handle_error(message, CommandNotFound)

		except NoCommand:
			await handle_error(message, NoCommand)