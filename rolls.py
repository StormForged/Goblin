import random
import discord
import stringHelpers

def d20():
	return "Rolled " + str(random.randint(0,20))

def d20Verbose(args):
	return "Roll " + stringHelpers.args2str(args) + ": " + str(random.randint(0,20))

def integerSequence(array):
	rollText = ""
	for i in array:
		rollText += str(i) + " "
	
	embed = discord.Embed(title = "Integer Sequence")
	embed.add_field(name = "1 - " + str(len(array)) , value = rollText, inline = False)

	return embed

def userRoll(args):
		finalRoll = 0
		reg = args[0].split('+')
		toMultiply = []
		toAdd = []
		fields = []
		values = []
		for r in reg:
			if 'd' in r:
				fields.append(r)
				toMultiply.append(r.split('d'))
			else:
				toAdd.append(r)
		
		for x in range(0, len(toMultiply)):
			totalDice = int(toMultiply[x][0])
			dieSides = int(toMultiply[x][1])
			valuesRolls = ''
			for y in range(0, totalDice):
				roll = random.randint(1, dieSides)
				valuesRolls += str(roll) + "+"
				finalRoll += roll
			valuesRolls = valuesRolls[:-1]
			values.append(valuesRolls)
		
		addString = ''
		for a in toAdd:
			addString += a + '+'
			finalRoll += int(a)
		addString = addString[:-1]

		embed = discord.Embed(title=args[0])
		for x in range(0, len(fields)):
			embed.add_field(name = fields[x], value = values[x], inline= False)
		if(len(toAdd) > 0):
			embed.add_field(name = 'Static', value = addString, inline = False)
		embed.add_field(name = 'Total: ', value = finalRoll, inline = True)
	
		return embed
	
def flipSingle():
	return 'HEADS' if random.randint(0,1) == 1 else 'TAILS'

def flipMulti(count):
	if(count > 5):
		if(count > 10000000):
			count = 10000000
		heads = 0
		tails = 0

		for x in range(0, count):
			if(random.randint(0,1) == 1):
				heads = heads + 1
			else:
				tails = tails + 1

		mes = "HEADS: " + str(heads) + "\nTAILS: " + str(tails)
		return mes
	
	mes = 'HEADS' if random.randint(0,1) == 1 else 'TAILS'
	for x in range(0, count - 1):
		mes += '\nHEADS' if random.randint(0,1) == 1 else '\nTAILS'
	return mes

def betSingle():
	mes = "WIN"
	num = random.randint(0,2)
	if(num == 1):
		mes = "LOSE"
	if(num == 2):
		mes = "DRAW"
	
	return mes

def betMulti(count):
	if(count > 5):
		count = 5
	
	mes = 'WIN' if random.randint(0,1) == 1 else 'LOSE'
	for x in range(0, count - 1):
		mes += '\nWIN' if random.randint(0,1) == 1 else '\nLOSE'

	return mes