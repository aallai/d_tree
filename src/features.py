from tree import *
from copy import deepcopy
import config

def subset_search(tracks) :

	'''
Forward selection of feature subsets
	'''		
	
	left = [i for i in range(config.NUM_ATTRIBUTES)]

	# split data in half for validation
	train_tracks = deepcopy(tracks[:len(tracks)/2])
	test_tracks = tracks[len(tracks)/2:]

	# best accuracy reached so far
	acc_max = 0.0	

	while (left) :

		# best feature for this iteration
		best = None
	
		for f in left :
			
			# add feature
			for t in train_tracks :
				t.x.append(tracks[train_tracks.index(t)].x[f])
	
			# train and evaluate tree
			t = maketree(train_tracks)
			t = prune(t, test_tracks)
			acc = eval_tree(t, test_tracks)

			if acc > acc_max :
				acc_max = acc
				best = f 

			# remove feature
			for t in train_tracks :
				t.x.pop()

		if not best :
			# no feature improves accuracy
			break	

		# otherwise add feature to all tracks
		left.remove(best)
		print 'Adding feature ' + str(best)	
		for t in train_tracks :
                                t.x.append(tracks[train_tracks.index(t)].x[best])

	
	t = maketree(train_tracks)
	t = prune(t, test_tracks)
	
	print 'Accuracy -> ' + str(eval_tree(t, test_tracks))

	return t
