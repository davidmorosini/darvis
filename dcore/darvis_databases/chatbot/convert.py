

import os

path = os.path.join('.', 'teste.txt')

with open(path) as c:
	l = c.readline()

	while(l):
		li = ((l.split('\n'))[0]).split('\t')
		com = '\"'
		for i in range(1, len(li)):
			com = com + li[i]
			if(i+1 != len(li)):
				com = com + ' '
			
		com = com + '\",\"' + li[0] + '\",'

		print(com)
		l = c.readline()


