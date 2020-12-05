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
  