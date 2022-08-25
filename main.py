import datetime
import time
import pytz
import random
import discord
from discord.ext import tasks, commands
import json
import aiohttp
import requests

import credentials
import chatResponses
import onMessage
import rolls
import nsfw as _nsfw
import stringHelpers
import chatBot

import requests
from bs4 import BeautifulSoup

import sqlite3
from sqlite3 import Error

import dateutil.relativedelta as REL

from google.cloud import translate_v2 as translate
from google.oauth2 import service_account

from types import SimpleNamespace

import numpy as np

intents = discord.Intents().default()
intents.members = True
intents.guilds = True
bot = commands.Bot(command_prefix = ('Goblin ', 'goblin ', 'gobbo ', 'Gobbo ','b ', 'B ', 'Boblin ', 'boblin ', 'joblin ', 'Joblin ', 'biblin ', 'Biblin '), intents = intents)
thoughts = chatBot.loadWisdom()

translateCredentials = service_account.Credentials.from_service_account_file('./thegoblin-key.json')
translate_client = translate.Client(credentials=translateCredentials)

class GuildConfigs:
	def __init__(self, guildName, guildID, nsfw, blacklistedSearchTerms, blacklistedCommands):
		self.guildName = guildName
		self.guildID = guildID
		self.nsfw = nsfw
		self.blacklistedSearchTerms = blacklistedSearchTerms
		self.blacklistedCommands = blacklistedCommands

def create_connection(db_file):
	""" Create a database connection to a SQLite database"""
	conn = None
	
	try:
		conn = sqlite3.connect(db_file)
		print(sqlite3.version)
	except Error as e:
		print(e)

	return conn

conn = create_connection("./remind.db")

def insert_reminder(conn, task):
	sql = ''' INSERT INTO remind(author, channel, task, time, done) VALUES(?,?,?,?,?)'''
	cur = conn.cursor()
	cur.execute(sql, task)
	conn.commit()

	return cur.lastrowid

guildConfsList = []

def load_conf():
	f = open('guilds.json', 'r')
	a = json.load(f, object_hook=lambda d: SimpleNamespace(**d))
	
	for g in a.guilds:
		guildConf = GuildConfigs(g.guild_name, g.guild_id, g.nsfw, g.blacklisted_search_terms, g.blacklisted_commands)
		guildConfsList.append(guildConf)

load_conf()

def save_conf(saveString):
	with open('guilds.json', 'r+') as f:
		file_data = json.load(f)
		file_data["guilds"].append(saveString)
		f.seek(0)
		json.dump(file_data, f, indent=4)

def save_conf_all():
	with open('guilds.json', 'w') as f:
		emptyDict = {
			"guilds": []
		}
		json.dump(emptyDict, f, indent= 4)
	
	with open('guilds.json', 'r+') as f:
		file_data = json.load(f)
		for confs in guildConfsList:
			appendDict = {
				"guild_name": confs.guildName,
				"guild_id": confs.guildID,
				"nsfw": confs.nsfw,
				"blacklisted_search_terms": confs.blacklistedSearchTerms,
				"blacklisted_commands": confs.blacklistedCommands
			}

			file_data["guilds"].append(appendDict)
			f.seek(0)
			json.dump(file_data, f, indent = 4)

def create_default_conf(guildName, guildID):
	stringData = {
		"guild_name": guildName,
		"guild_id": guildID,
		"nsfw": False,
		"blacklisted_search_terms": [""],
		"blacklisted_commands": []
	}

	guildConf = GuildConfigs(guildName, guildID, False, [""], [])
	guildConfsList.append(guildConf)

	save_conf(stringData)

def check_guilds_conf(guilds):
	for g in guilds:
		f = 0
		for i in guildConfsList:
			if g.id == i.guildID:
				f = 1
				break
		
		##DO NOT ASK ME WHY THIS HACK WORKS
		if f == 1:
			continue

		guildConf = GuildConfigs(g.name, g.id, False, [""], [])
		guildConfsList.append(guildConf)

		saveString = {
			"guild_name": g.name,
			"guild_id": g.id,
			"nsfw": False,
			"blacklisted_search_terms": [""],
			"blacklisted_commands": []
		}

		save_conf(saveString)

@bot.event
async def on_ready():
	print('Logged in as')
	print(bot.user.name)
	print(bot.user.id)
	print('--------')
	check_guilds_conf(bot.guilds)
	myLoop.start()

@bot.event
async def on_guild_join(guild):
	create_default_conf(guild.name, guild.id)

@bot.event
async def on_message(message):	
	if(onMessage.checkGarfield(message.content)):
		await message.channel.send("nuthin")

	if 'ss13' in message.content and not message.author.bot:
		decider = random.randint(0,4)
		if(decider == 1):
			await message.channel.send(onMessage.mockery(message.content))

	decider = random.randint(1, 10000)
	if(decider == 69) and not message.author.bot: 
		await message.channel.send(onMessage.mockery(message.content))
	
	await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, error, *args):
	if isinstance(error, commands.errors.NSFWChannelRequired):
		await ctx.send("dis izzent a NSFW channel!")
	else:
		await ctx.send(random.choice(chatResponses.errors))

@bot.command()
async def roll(ctx, *args):
	args = stringHelpers.youMeChecker(args)
	if(len(args) == 0):
		await ctx.send(rolls.d20())
		return
	
	if(args[0][0].isalpha() == 0):
		await ctx.send(embed = rolls.userRoll(args))
	else:
		await ctx.send(rolls.d20Verbose(args))

@bot.command()
async def flip(ctx, *args):
	if(len(args) > 0):
		await ctx.send(rolls.flipMulti(int(args[0])))
		return

	await ctx.send(rolls.flipSingle())

@bot.command()
async def bet(ctx, *args):
	if(len(args) > 0):
		await ctx.send(rolls.betMulti(int(args[0])))
		return
	
	await ctx.send(rolls.betSingle())

@bot.command()
async def bitcoin(ctx):
	url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
	async with aiohttp.ClientSession() as session:  # Async HTTP request
		raw_response = await session.get(url)
		response = await raw_response.text()
		response = json.loads(response)
		await ctx.send("Bitcoinz iz " + response['bpi']['USD']['rate'] + " ameribux")	

@bot.command()
async def wheelchair(ctx):
	await ctx.send("You're and I'd but it's. I it now can." + "send me $30k in crypto and I'll unlock it")
	
@bot.command()
async def nise(ctx):
	await ctx.send("<:mikudesu:230366418821054464>")

@bot.command()
async def postit(ctx):
	await ctx.send(file = discord.File('it.png'))
	
@bot.command()
async def sleepy(ctx):
	await ctx.send(file = discord.File('sleepy.png'))
	
@bot.command(name = 'wakey',
				aliases = ['wakie'])
async def wakey(ctx):
	await ctx.send(file = discord.File('wakey.png'))
	
@bot.command()
async def dare(ctx):
	await ctx.send(file = discord.File('dare.png'))
	
@bot.command(name = 'wagey',
				aliases = ['wagie'])
async def wagey(ctx):
	await ctx.send(file = discord.File('wagey.png'))
	
@bot.command(name='8ball',
                aliases=['eight_ball', 'eightball', '8-ball'])
async def eight_ball(ctx):
	await ctx.send(random.choice(chatResponses.possible_responses) + ", " + ctx.message.author.mention + " " + "<a:fuuuuck:641605864582545429>")

@bot.command(name = 'is', hidden = 'true', aliases = ['have','did','would','does','should','has','cant',"can't",'can','do','are', 'will', 'am', 'art','was','wast','be','if','may','were','what'])
async def _is(ctx, *args):
	args = stringHelpers.youMeChecker(args)
	if(len(args) > 2 and 'or' in args):
		await ctx.send(chatBot.isOptions(args) + ctx.message.author.mention)
	else:
		if(random.randint(0,30) == 25):
			await ctx.send("shut up, " + ctx.message.author.mention)
		else:
			await ctx.send(random.choice(chatResponses.is_responses) + ", " + ctx.message.author.mention)

@bot.command(hidden = 'true')
async def where(ctx, *args):
	ctx.send("dunno yet")

@bot.command(hidden = 'true')
async def say(ctx, *args):
    await ctx.send(stringHelpers.args2str(args))

@bot.command(hidden = 'true', aliases = ['whens', "when's"])
async def when(ctx, *args):
    await ctx.send(random.choice(chatResponses.when_responses))

@bot.command(hidden = 'true')
async def rate(ctx, *args):
	args = stringHelpers.youMeChecker(args)
	args = stringHelpers.args2str(args)
	await ctx.send(random.choice(chatResponses.choice_responses) + " " + args + " is a " + str(random.randint(0,10)) + "/10")

@bot.command()
async def dndalign(ctx, *args):
	args = stringHelpers.youMeChecker(args)
	args = stringHelpers.args2str(args)
	await ctx.send(random.choice(chatResponses.choice_responses) 
		+ " " + args + " is " + random.choice(chatResponses.dndalignments))

@bot.command(hidden = 'true')
async def which(ctx, *args):
	args = stringHelpers.youMeChecker(args)
	await ctx.send(chatBot.which(args))

@bot.command(hidden = 'true')
async def why(ctx, *arg):
    thought = random.choice(thoughts)

    await ctx.send(thought)

@bot.command(hidden = 'true')
async def seconds(ctx, *args):
    num = random.randint(0,60)

    if(num == 0):
        await ctx.send("now")
    else:
        await ctx.send(str(num) + " seconds")

@bot.command(hidden = 'true')
async def minutes(ctx, *args):
	num = random.randint(0,60)

	if(num == 0):
		await ctx.send("now")
	else:
		await ctx.send(str(num) + " minutes")

@bot.command(hidden = 'true')
async def hours(ctx, *args):
	num = random.randint(0,8)

	if(num == 0):
		await ctx.send("now")
	else:
		await ctx.send(str(num) + " hours")

@bot.command(hidden = 'true')
async def days(ctx, *args):
	num = random.randint(0,30)

	if(num == 0):
		await ctx.send("today")
	else:
		await ctx.send(str(num) + " days")

@bot.command(hidden = 'true')
async def weeks(ctx, *args):
	num = random.randint(0,12)

	if(num == 0):
		await ctx.send("this week")
	else:
		await ctx.send(str(num) + " weeks")

@bot.command(hidden = 'true')
async def months(ctx, *args):
	num = random.randint(0,12)

	if(num == 0):
		await ctx.send("this month")
	else:
		await ctx.send(str(num) + " months")

@bot.command(hidden = 'true')
async def years(ctx, *args):
	num = random.randint(0,10)

	if(num == 0):
		await ctx.send("this year")
	else:
		await ctx.send(str(num) + " years")

@bot.command(hidden = 'true', aliases = ['time'])
async def timeTo(ctx, *args):
	if len(args) > 0:
		args = stringHelpers.youMeChecker(args)

	neverCheck = random.randint(1, 100)
	if neverCheck == 100:
		await ctx.send("nevva")
		return

	monthCheck = random.randint(0, 3)
	yearCheck = random.randint(0, 1)

	context = ""

	if len(args) > 0:
		for a in args:
			context += (f" {a}")

	if len(args) > 0 and args[0] == "until":
		string = (f"time{context} iz")
	else:
		string = (f"time until{context} iz")
	
	days = random.randint(1, 30)

	string += (f" {str(days)} day$")

	if monthCheck != 3:
		months = random.randint(1, 11)
		string += (f" {str(months)} munfz")
	
	if yearCheck == 1:
		years = random.randint(1, 10)
		string += (f" and {str(years)} yeers")

	await ctx.send(string)


@bot.command(hidden = 'true', aliases = ['whose', "who's", "who'd","whos"])
async def who(ctx, *args):
	args = stringHelpers.youMeChecker(args)

	dndChannel = bot.get_channel(782795167643336734)
	if(ctx.channel == dndChannel):
		await ctx.send(chatBot.whoDND(ctx))
		return
	
	if(len(args) > 1):
		if(args[1].endswith(',')):
			temp = args[1]
			temp = temp[:-1]
			args[1] = temp

		if(args[0] == 'would' and args[1] == 'win'):
			await ctx.send(chatBot.wouldWin(args))
			return

	if(len(args) > 2):
		if("or" in args):
			await ctx.send(chatBot.isOptions(args))
			return
		
	await ctx.send(chatBot.whoMembers(ctx))


@bot.command(hidden = 'true')
async def smash(ctx, *args):
	if len(args) > 1 and args[0] == 'or' and args[1] == 'pass':
		mes = 'smash' if random.randint(0,1) == 1 else 'pass'
		await ctx.send(mes)

@bot.command()
async def smile(ctx):
	await ctx.send("sod off")

@bot.command()
async def grayscale(ctx):
	await ctx.send("later")

@bot.command()
async def fmk(ctx, *args):
	if(len(args) > 1):
		fmk = [args[0], args[1], args[2]]
		random.shuffle(fmk)
		await ctx.send("gunna frik " + fmk[0] + ", guna marry " + fmk[1] + ", and " + fmk[2] + " gitz killd")

@bot.command()
async def rank(ctx, *args):
	if(len(args) > 1):
		items = []
		for a in args:
			items.append(a)

		random.shuffle(items)

		message = ""
		index = 1
		for i in items:
			if index == 1:
				message += str(index) + ") " + i
			else:
				message += "\n" + str(index) + ") " + i

			index += 1
		
		await ctx.send(message)

@bot.command()
async def mmr(ctx, *args):
	if(len(args) > 0):
		if(args[0] == 'rb'):
			url = 'https://api.opendota.com/api/players/93577387'
			async with aiohttp.ClientSession() as session: #async HTTP request
				raw_response = await session.get(url)
				response = await raw_response.text()
				response = json.loads(response)
				await ctx.send("MMR is..." + str(response['solo_competitive_rank']))
	else:
		await ctx.send("ur mmr is... .. . . ." + str(random.randint(1, 13000)))


@bot.command()
async def hero(ctx):
	hero = random.randint(0, len(chatResponses.heroes))
	embed = discord.Embed()
	embed.set_author(name = chatResponses.heroes[hero])
	embed.set_image(url = "https://stormforged.moe/heroes/" + chatResponses.heroesURL[hero] + ".png")
	embed.set_footer(text = "do it nerd")

	await ctx.send(embed = embed)
    
@bot.command()
async def agent(ctx):
	agent = random.randint(0, len(chatResponses.agents))
	embed = discord.Embed()
	embed.set_author(name = chatResponses.agents[agent])
	embed.set_image(url = "https://stormforged.moe/agents/" + chatResponses.agents[agent] + ".png")
	embed.set_footer(text = "do it nerd")

	await ctx.send(embed = embed)

@bot.command(aliases = ['thoughts', 'redpill', 'elaborate', 'ponder', 'pontificate'])
async def wisdom(ctx, *args):
	command = ctx.message.content.split(' ', 1)[1]
	if len(args) < 2:
		await ctx.send(command + " on what?")
		return

	thought = ""

	thought = random.choice(thoughts)

	await ctx.send(thought)

@bot.command()
async def image(ctx, *args):
	nsfwFlag = False
	for g in guildConfsList:
		if g.guildID == ctx.guild.id:
			if g.nsfw:
				nsfwFlag = True
			
			if any(word in args for word in g.blacklistedSearchTerms):
				await ctx.send("no")
				return
	
	query = args
	page = random.randint(1, 10)

	page = 1

	start = (page - 1) * 10 + 1

	if nsfwFlag:
		url = f"https://www.googleapis.com/customsearch/v1?key={credentials.API_KEY}&cx={credentials.SEARCH_ENGINE_ID}&searchType=image&safe=off&q={query}&start={start}"
	else:
		url = f"https://www.googleapis.com/customsearch/v1?key={credentials.API_KEY}&cx={credentials.SEARCH_ENGINE_ID}&searchType=image&safe=active&q={query}&start={start}"

	data = requests.get(url).json()
	search_items = data.get("items")

	if not search_items:
		await ctx.send("think i messed up")
		return

	roll = random.randint(0,10)

	badlinks = ["lookaside", "x-raw-image"]

	while 1:
		if roll < 0:
			await ctx.send("got nuffin")
			break

		result = search_items[roll].get("link")
        
        #this logic doesnt quite work
		for link in badlinks:
			if link in result:
				roll -= 1
				continue

		await ctx.send(result)
		break

@tasks.loop(minutes = 1)
async def myLoop():
	'''For leading 0s use - for linux and # for windows'''

	now = datetime.datetime.now().strftime('%Y-%m-%d %-H:%-M')
	cur = conn.cursor()
	cur.execute('SELECT * FROM remind')
	for row in cur:
		if(row[4] == now):
			channel = bot.get_channel(row[2])
			await channel.send('<@' + str(row[1]) + '> hey bro, ' + row[3])

@bot.command(help = 'CORRECT SYNTAX FOR THIS MESS OF A FUNCTION'
	+ '\n goblin remind [Task] / today @ 10:00pm' 
	+ '\n goblin remind [Task] / tomorrow @ 10:00am'
	+ '\n goblin remind [Task] / wednesday @ HH:MMam'
	+ '\n goblin remind [Task] / DD-MM-YYYY @ HH:MMpm'
	+ '\n EITHER DAY OR TIME CAN BE OMITTED')
async def remind(ctx, *args):
	#Get arguments and divvy it all up
	task_str = ''
	task_day = ''
	task_day_arg = ''
	task_time = ''
	task_time_arg = ''
	toggle = 0
	for a in args:
		if(a == "/"):
			toggle = 1
			continue

		if(a == "@"):
			toggle = 2
			continue

		if(toggle == 0):
			task_str += a + ' '

		if(toggle == 1):
			task_day_arg = a
		
		if(toggle == 2):
			task_time_arg = a

	task_day_arg = task_day_arg.lower()
	task_time = task_time.lower()

	#Process day portion
	if task_day_arg:
		if(task_day_arg[:1].isdigit()):
			#Might seem a tad redundant but its just to make sure the input is correct 
			timeStruct = time.strptime(task_day_arg, '%d-%m-%Y')
			task_day = str(timeStruct.tm_year) + "-" + str(timeStruct.tm_mon) + "-" + str(timeStruct.tm_mday)
		elif(task_day_arg == 'tomorrow'):
			task_day = datetime.date.today() + datetime.timedelta(days = 1)
		elif(task_day_arg == 'today'):
			task_day = datetime.date.today()
		else:
			today = datetime.date.today()
			weekday_as_int = time.strptime(task_day_arg, "%A").tm_wday

			rd = REL.relativedelta(days=1, weekday=weekday_as_int)
			task_day = today + rd
	else:
		task_day = datetime.date.today()

	#Process time
	if task_time_arg:
		#check if am/pm is present
		if(task_time_arg[-2:] == 'pm' or task_time_arg[-2:] == 'am'):
			timeStruct = time.strptime(task_time_arg, '%I:%M%p')
		else:
			timeStruct = time.strptime(task_time_arg, '%H:%M')

		task_time = str(timeStruct.tm_hour) + ":" + str(timeStruct.tm_min)
	else:
		task_time = str(time.localtime().tm_hour + 2) + ":0"

	task_datetime = str(task_day) + " " + str(task_time) 

	insert_task = (ctx.author.id, ctx.channel.id, task_str, task_datetime,0)
	insert_reminder(conn, insert_task)

	await ctx.send(random.choice(chatResponses.remind_responses))

@remind.error
async def remind_error(ctx, error):
	await ctx.send('friked it')

@bot.command()
async def translate(ctx, *args):
	translateString = ""

	for a in args:
		translateString += a + " "

	result = translate_client.translate(translateString, target_language="en")

	await ctx.send(result["translatedText"])

@bot.command(hidden = 'true')
async def blacklistCommand(ctx, *args):
	await ctx.send("soon")

@bot.command()
@commands.has_permissions(administrator = True)
async def toggle(ctx, *args):
#Currently bugged
	if(args[0]) == "nsfw":
		for g in guildConfsList:
			if g.guildID == ctx.guild.id:
				g.nsfw = not g.nsfw
				save_conf_all()
				if g.nsfw:
					await ctx.send("nsfw gobbo here")
				elif not g.nsfw:
					await ctx.send("sayf 4 werk")
					
@bot.command()
async def intseq(ctx, *args):
	if len(args) < 1:
		await ctx.send("need numbahz")
		return

	if int(args[0]) > 250:
		await ctx.send("gonna need 2 use integer.org king")
		return
	
	array = np.arange(1, int(args[0]) + 1, 1 )
	random.shuffle(array)
	await ctx.send(embed = rolls.integerSequence(array))

@bot.command(aliases = ["love"])
async def compatability(ctx, *args):
	if len(args) < 2:
		await ctx.send("wut")
		return

	context = ""
	for a in args:
		context += a + " "

	emoji = ""
	compat = random.randint(0, 100)

	if compat == 100:
		emoji = ":sparkling_heart:"
	elif compat >= 75 and compat < 100:
		emoji = ":revolving_hearts:"
	elif compat >= 50 and compat < 75:
		emoji = ":heart:"
	elif compat >= 25 and compat < 50:
		emoji = ":white_heart:"
	else:
		emoji = ":broken_heart:"
	
	compat = str(compat) + "%"

	if 'between' in context:
		string = "The compatability %s is %s %s"%(context, compat, emoji)
	else:
		string = "The compatability between %s is %s %s"%(context, compat, emoji)	

	await ctx.send(string)

@bot.command()
async def gim(ctx, *args):
	team = stringHelpers.args2str(args)
	team = ('+').join(team.split(' '))
	url = "https://secure.runescape.com/m=hiscore_oldschool_ironman/group-ironman/?groupName=" + team

	page = requests.get(url)

	soup = BeautifulSoup(page.content, "html.parser")

	results = soup.find(id="Group Ironman HiScores")

	job_elements = results.find_all("tr", class_ = "uc-scroll__table-row uc-scroll__table-row--type-highlight")

	if(job_elements):
		name_element = ""
		rank_element = ""

		for job_element in job_elements:
			name_element = job_element.find("a", class_ = "uc-scroll__link").text
			rank_element = job_element.find("td", class_= "uc-scroll__table-cell").text

		await ctx.send(name_element + " is ranked: " + rank_element)
	else:
		await ctx.send("didnt find em")

bot.run(credentials.TOKEN)