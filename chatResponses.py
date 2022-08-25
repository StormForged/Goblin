possible_responses = ['no','no?','thinkin nah','nah mate','dun think so','prob not','dunno','probly','shut up','who cares','prob','ye','yeah','think so','thinkin ye','thnkin yeah','yes']
is_responses = ['yeah dog','YEAH DOG','yee.. nah','probluy ay','...','nup','yup','no','no?','thinkin nah','nah mate','dun think so','prob not','dunno','probly','who cares','prob','ye','yeah','think so','thinkin ye','thnkin yeah','yes']
when_responses = ['soon', 'never', 'aint hapening', 'gotta wait', 'in a bit', 'dunno']
why_responses = []
remind_responses = ['ye', 'ye w.e', 'k', 'after i bum goblina', 'k poofta', 'dun', 'ok poof', 'on it dog', 'yessir', 'ritten down rat'] 
choice_responses = ['thinkin ', 'gonna go with ', '', '', 'deffs ', 'truly', 'gotta be that ', '']
dndalignments = ['nootral gud', 'nootral nootral', 'nootral bad', 'lawful gud', 'lawful nootral', 'lawful bad', 'kayotic gud', 'kayotic nootral', 'kayotic bad guy']
who_responses_dnd = ['Charon', 'Damadeus', 'Corvo', 'Sharon', 'Dumbass', 'Cor:b:o', 'Kizu', 'Ki:b:u', 'Oonix', 'Oo:b:ix']
who_responses_dnd_uncommon = ['Dusty', 'Penance', ':b:usty', ':b:enis']
who_responses_dnd_rare = ['Strahd', 'Nise', 'Vondal', 'Eagle Eyes', 'Steely', 'Pauly', 'Fauly', 'Napoleon', 'The Badger', 'Cyrus', 'Knife-ear', 'Dugg', 'Esher', 'The Abbot', 'Belisarius', 'Jingo', 'NEET', 'Dicksucker', 'Cassatori', 'Argus', 'Rollah', 'Dongo', 'Lilgo', 'Sasuke Plush']
positions = ['under', 'above', 'next to', 'right over near', 'to the left of', 'to the right of', 'behind', 'in front of', 'over by']
places = ['']

heroes = ["Abbadon", "Alchemist", "Ancient Apparition", "Anti Mage", "Arc Warden", "Axe", "Bane", "Batrider",
		"Beastmaster", "Bloodseeker", "Bounty Hunter", "Brewmaster", "Bristleback", "Broodmother", "Centaur Warrunner", "Chaos Knight",
		"Chen", "Clinkz", "Clockwerk", "Crystal Maiden", "Dark Seer", "Dark Willow", "Dazzle", "Death Prophet",
		"Disruptor", "Doom", "Dragon Knight", "Drow Ranger", "Earth Spirit", "Earthshaker", "Elder Titan", "Ember Spirit",
		"Enchantress", "Enigma", "Faceless Void", "Gyrocopter", "Huskar", "Invoker", "Io", "Jakiro",
		"Juggernaut", "Keeper of the Light", "Kunkka", "Legion Commander", "Leshrac", "Lich", "Lifestealer", "Lina",
		"Lion", "Lone Druid", "Luna", "Lycan", "Magnus", "Medusa", "Meepo", "Mirana",
		"Monkey King", "Morphling", "Naga Siren", "Natures Prophet", "Necrophos", "Night Stalker", "Nyx Assassin", "Ogre Magi",
		"Omniknight", "Oracle", "Outworld Devourer", "Pangolier", "Phantom Assassin", "Phantom Lancer", "Phoenix", "Puck",
		"Pudge", "Pugna", "Queen of Pain", "Razor", "Riki", "Rubick", "Sand King", "Shadow Demon",
		"Shadow Fiend", "Shadow Shaman", "Silencer", "Skywrath Mage", "Slardar", "Slark", "Sniper", "Spectre",
		"Spirit Breaker", "Storm Spirit", "Sven", "Techies", "Templar Assassin", "Terrorblade", "Tidehunter", "Timbersaw",
		"Tinker", "Tiny", "Treant Protector", "Troll Warlord", "Tusk", "Underlord", "Undying", "Ursa",
		"Vengeful Spirit", "Venomancer", "Viper", "Visage", "Warlock", "Weaver", "Windranger", "Winter Wyvern",
		"Witch Doctor", "Wraith King", "Zeus", "Mars", "Snapfire", "Hoodwink", "Grimstroke", "Void Spirit"]

heroesURL = ["Abbadon", "Alchemist", "AncientApparition", "AntiMage", "ArcWarden", "Axe", "Bane", "Batrider",
		"Beastmaster", "Bloodseeker", "BountyHunter", "Brewmaster", "Bristleback", "Broodmother", "CentaurWarrunner", "ChaosKnight",
		"Chen", "Clinkz", "Clockwerk", "CrystalMaiden", "DarkSeer", "DarkWillow", "Dazzle", "DeathProphet",
		"Disruptor", "Doom", "DragonKnight", "DrowRanger", "EarthSpirit", "Earthshaker", "ElderTitan", "EmberSpirit",
		"Enchantress", "Enigma", "FacelessVoid", "Gyrocopter", "Huskar", "Invoker", "Io", "Jakiro",
		"Juggernaut", "KeeperoftheLight", "Kunkka", "LegionCommander", "Leshrac", "Lich", "Lifestealer", "Lina",
		"Lion", "LoneDruid", "Luna", "Lycan", "Magnus", "Medusa", "Meepo", "Mirana",
		"MonkeyKing", "Morphling", "NagaSiren", "NaturesProphet", "Necrophos", "NightStalker", "NyxAssassin", "OgreMagi",
		"Omniknight", "Oracle", "OutworldDevourer", "Pangolier", "PhantomAssassin", "PhantomLancer", "Phoenix", "Puck",
		"Pudge", "Pugna", "QueenofPain", "Razor", "Riki", "Rubick", "SandKing", "ShadowDemon",
		"ShadowFiend", "ShadowShaman", "Silencer", "SkywrathMage", "Slardar", "Slark", "Sniper", "Spectre",
		"SpiritBreaker", "StormSpirit", "Sven", "Techies", "TemplarAssassin", "Terrorblade", "Tidehunter", "Timbersaw",
		"Tinker", "Tiny", "TreantProtector", "TrollWarlord", "Tusk", "Underlord", "Undying", "Ursa",
		"VengefulSpirit", "Venomancer", "Viper", "Visage", "Warlock", "Weaver", "Windranger", "WinterWyvern",
		"WitchDoctor", "WraithKing", "Zeus", "Mars", "Snapfire", "Hoodwink", "Grimstroke", "Void_Spirit"]

errors = ['dunno dat wun', 'dumb?', 'try agen', 'stop datz rong', 'cmon']

agents = ['Brimstone', 'Viper', 'Omen', 'Killjoy', 'Cypher', 'Sova', 'Sage', 'Phoenix', 'Jett', 'Reyna', 'Raze', 'Breach', 'Skye', 'Yoru', 'Astra', 'KAYO', 'Chamber', 'Neon', 'Fade']