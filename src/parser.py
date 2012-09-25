import config
from tracks import Track

def parse(x, y) :

	'''
Returns list of tracks, each entry is a list containing the average of the 25 attributes over the 200 segments.
	''' 
	

	f = open(x, 'r')	
	x = f.read()
	f.close()

	f = open(y, 'r')
	y = f.read()
	f.close()

	x_lines = [i for i in x.split('\n') if i]
	y_lines = [i for i in y.split('\n') if i]

	tracks = [ ]

	for l in x_lines :
		data = [float(x) for x in l.split()]

		# average 25 attributes over 200 segemnts	
		attrs = [ ]
		
		for i in range(config.NUM_ATTRIBUTES) :
			s = 0
			for j in range(config.NUM_SEGMENTS) :
				s += data[i + config.NUM_ATTRIBUTES*j]
	
			attrs.append(s / float(config.NUM_SEGMENTS))
		

		tracks.append(Track(attrs, int(y_lines[x_lines.index(l)])))

	return tracks	
