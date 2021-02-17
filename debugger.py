import pyautogui, time

# The Lion Bot Debugger
# Author - Ricky

f = open("all_commands.txt", 'r')
time.sleep(1)
print ("3")
time.sleep(1)
print ("2")
time.sleep(1)
print ("1")
for word in f:
	pyautogui.typewrite(word)
	pyautogui.press("enter")
	time.sleep(2)
  
  
def get_prefix(client, message):
	with open('prefixes.json', 'r') as f:
		prefixes = load(f)
	try:
		return commands.when_mentioned_or(prefixes[str(message.guild.id)])(client, message)
	except KeyError:
		with open('prefixes.json', 'r') as f:
			prefixes = load(f)
		prefixes[str(message.guild.id)] = "/"
		with open('prefixes.json', 'w') as f:
			dump(prefixes, f, indent=4)
		return commands.when_mentioned_or(prefixes[str(message.guild.id)])(client, message)
