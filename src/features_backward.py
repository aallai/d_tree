from tree import *
from copy import deepcopy
import config

def subset_search(tracks) :

	'''
Forward selection of feature subsets
	'''		

	# split data in half for validation
	offset = len(tracks)/2
	train_tracks = deepcopy(tracks[:offset])
	test_tracks = deepcopy(tracks[offset:])

	# best accuracy reached so far
	acc_max = eval_tree(prune(maketree(train_tracks), test_tracks), test_tracks)	

	# while we have features left
	while (train_tracks[0].x) :

		# best feature to remove for this iteration
		best = None
	
		for f in xrange(len(train_tracks[0].x)) :
			
			# remove feature
			f_train = [ ]		
			f_test = [ ]
			for t in train_tracks :
				f_train.append(t.x.pop(f))

			for t in test_tracks :
				f_test.append(t.x.pop(f))
	
			# train and evaluate tree
			print 'Evaluating feature ' + str(f)
	
			acc = eval_tree(prune(maketree(train_tracks), test_tracks), test_tracks)

			if acc > acc_max :
				acc_max = acc
				best = f 

			# restore feature
			for t in train_tracks :
				t.x.insert(f, f_train[train_tracks.index(t)])
			for t in test_tracks :
				t.x.insert(f, f_test[test_tracks.index(t)])

		if not best :
			# no feature improves accuracy
			break	

		print '>>>'
		print 'Removing feature ' + str(best)	
		print '>>>'
		for t in train_tracks :
                                t.x.pop(best)
		for t in test_tracks :
				t.x.pop(best)
	
	t = prune(maketree(train_tracks), test_tracks)

	print 'num features' + str(len(train_tracks[0].x))
	
	print 'Accuracy -> ' + str(eval_tree(t, test_tracks))

	return t
