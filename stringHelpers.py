def args2str(args):
	string = ''
	for a in args:
		string += a + ' '
	
	string = string[:-1]

	return string

def youMeChecker(args):
	whatever = []
	for a in args:
		if(a == 'your' or a == 'my'):
			a = 'my' if a == 'your' else 'your'
		
		if(a == 'you' or a == 'me'):
			a = 'me' if a == 'you' else 'you'

		whatever.append(a)

	return whatever