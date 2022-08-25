import random
import chatResponses

def isOptions(args):
	options = []
	optionString = ''
	index = 0
	for a in args[1:]:
		if(a == 'or'):
			options.append(optionString)
			index += 1
			optionString = ''
			continue

		if(a.endswith(',')):
			a = a[:-1]
			optionString += a
			options.append(optionString)
			index += 1
			optionString = ''
			continue

		optionString += a + ' '

	options.append(optionString)
	
	return random.choice(options) + ", "

def which(args):
	contextStr = ''
	subjects = ['','']

	contextToggle = 0
	subToggle = 0
	
	for a in args:
		if(a == 'or'):
			subToggle = 1
			continue
	
		if(contextToggle == 1):
			subjects[subToggle] += a + ' '

		if(contextToggle == 0):
			contextStr += a + ' '
			if(a.endswith(',')):
				contextToggle = 1
	
	print(subjects)

	if(random.randint(0,1) == 1):
		message = contextStr + " " + subjects[0] + "iz bedda den " + subjects[1]
	else:
		message = contextStr + " " + subjects[1] + "iz da choice ouba " + subjects[0]
	
	return message

def whoDND(ctx):
	roll = random.randint(1, 100)
	if(roll >= 1 and roll <= 2):
		return random.choice(chatResponses.who_responses_dnd_rare)
	elif(roll >= 3 and roll <= 13):
		return random.choice(chatResponses.who_responses_dnd_uncommon)
	else:
		return random.choice(chatResponses.who_responses_dnd)

def wouldWin(args):
	contextStr = ''
	subjects = ['','']

	contextToggle = 0
	subToggle = 0
	
	for a in args[2:]:
		if(a == 'or'):
			subToggle = 1
			continue

		if(a == 'in'):
			contextToggle = 1
	
		if(contextToggle == 1):
			if(a.endswith(',')):
				contextStr += a + ' '
				contextToggle = 0
			else:
				contextStr += a + ' '
		
		if(contextToggle == 0):
			subjects[subToggle] += a + ' ' 

	if(random.randint(0,1) == 1):
		message = contextStr + " " + subjects[0] + "wud rek " + subjects[1]
	else:
		message = contextStr + " " + subjects[1] + "wud smash " + subjects[0]
	
	return message

def whoMembers(ctx):
	members = ["Da gob", "gobbo", "u", "me"]
	for member in ctx.guild.members:
		if not member.bot and len(member.roles) > 1:
			if member.nick != None:
				members.append(member.nick)
			
			members.append(member.name)
	
	return random.choice(members)

def loadWisdom():
	fname = "./wisdom.txt"
	
	wisdomArray = []

	with open(fname, 'r', encoding='utf-8') as f:
		while 1:
			line = f.readline()
			if not line: break
			wisdomArray.append(line)

	return wisdomArray