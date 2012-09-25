#!/usr/bin/python

import config
from parser import *
from features import *
import pickle

def main() :

	tracks = parse(config.ROOT_DIR + '/data/trainx.txt', config.ROOT_DIR + '/data/trainy.csv')

	t = subset_search(tracks) 

	f = open(config.ROOT_DIR + '/data/testy.txt', 'w')

	tracks = parse(config.ROOT_DIR + '/data/testx.txt', config.ROOT_DIR + '/data/dummy_testy.csv')

	for x in tracks :
		f.write(str(t.classify(x)) + '\n')

	f.close()

if __name__ == '__main__' :
	main()
