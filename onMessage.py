import random

garfield = ["https://store.steampowered.com/bundle/11631/Garfield_Kart__Lasagna_Bundle/",
			"https://store.steampowered.com/app/362930/Garfield_Kart/",
			"https://store.steampowered.com/app/1085510/Garfield_Kart__Furious_Racing/",
			"what are we doing about this",
			"what are we doing about this?",
			"What are we doing about this",
			"What are we doing about this?"]

def checkGarfield(message):
	for g in garfield:
		if(message == g):
			return True

def mockery(message):
	newString = ""
	tempChar = ""
	decider = random.randint(0,20)
	if(decider == 20):
		for c in message:
			rand = random.randint(0,1)
			if(rand == 1):
				tempChar = c.upper()
			
			newString += tempChar
	else:
		for c in message:
			rand = random.randint(0,1)
			if(rand == 1):
				tempChar = c.upper()
			else:
				tempChar = c
		
			newString += tempChar

	return newString