import math
import config
import tracks
from copy import deepcopy

log = lambda x : math.log(x, 2)


class Node(object) :

	def __init__(self, tracks, leaf=False) :

		self.tracks = tracks
		self.parent = None
		self.right = None
		self.left = None
		self.test = None
		self.y = None
		self.leaf = leaf
		
	
	def classify(self, track) :
		
		if self.leaf :
			return self.y

		if self.test(track) :
			return self.right.classify(track)
		else :
			return self.left.classify(track)


def maketree(tracks) :
	
	result = find_test(tracks)

	# no info gain possible
	if not result :
		return makeleaf(tracks)

	# otherwise create two nodes and recurse
	ig, attr, split_point, left, right = result

	'''
	# get rid of attribute we test on
	for l in left, right :
		for t in l :
			del t.x[attr]
	'''

	node = Node(tracks)
	node.test = lambda t : t.x[attr] > split_point
	node.right = maketree(right)
	node.left = maketree(left)
	node.left.parent = node
	node.right.parent = node

	return node

def makeleaf(tracks) :

	leaf = Node(tracks, True)

        # set the class to be the majority class
        types = [0 for i in range(config.NUM_TYPES)]

        for t in tracks :
		types[t.y] += 1

	m = 0

	for t in types :
		if t > m :
			m = t

	leaf.y = types.index(m)

	return leaf


def prune(tree, test_tracks) :

	'''
Returns (pruned_tree, accuracy)
	'''

	tree = deepcopy(tree)

	while(True) :

		acc_init = eval_tree(tree, test_tracks)
		acc_max = 0
		best_tree = tree
	
		# avoid special case of pruning root
		nodes = [x for x in [tree.left, tree.right] if x]

		# traverse tree, evaluate accuracy of pruning
		while nodes :

			n = nodes.pop(0)

			if n.leaf :
				continue			

			nodes += [x for x in [n.left, n.right] if x]

			leaf = makeleaf(n.tracks)
			leaf.parent = n.parent

			# splice new leaf node into tree
			right = False

			if n.parent.right == n :
				n.parent.right = leaf
				right = True
			else :
				n.parent.left = leaf
		
			acc = eval_tree(tree, test_tracks)

			if acc >= acc_max :
		  		acc_max = acc
                                best_tree = deepcopy(tree)

			
			# restore tree
			if right :
				n.parent.right = n
			else :
				n.parent.left = n

		if acc_max >= acc_init :
			tree = best_tree
		else :
			break


	return tree
	
			
			

def eval_tree(tree, tracks) :

	right = 0
        for t in tracks :
                if tree.classify(t) == t.y :
                        right += 1

        return right / float(len(tracks))				




def find_test(tracks) :

	e_init = entropy(tracks)

	# maybe all tracks are of same class
	if e_init == 0 :
		return None

	best = (0, None, None, None, None)  # max = (info_gain, attr_index, split_point, left, right)

	for i in range(len(tracks[0].x)) :
	
		# sort tracks by that attribute
		ls = sorted(tracks, key=(lambda t : t.x[i]))	
		
		for t in ls[1:] :
			prev = ls[ls.index(t) - 1]

			# if y values differ check information gain of split point
			if prev.y != t.y :
				left = ls[:ls.index(t)]
				right = ls[ls.index(t):]

				info_gain = e_init - ( (len(left) / float(len(tracks))) * entropy(left) + (len(right) / float(len(tracks))) * entropy(right) )

				if info_gain > best[0] :
					best = (info_gain, i, (prev.x[i] + t.x[i]) / 2.0, left, right)

	if best[0] == 0 :
		return None
	else :
		return best
							

def entropy(tracks) :

	'''
dataset is a list of size NUM_TYPES, containing the number of tracks of each type in this dataset
	'''

	dataset = [0 for i in range(config.NUM_TYPES)]

	for t in tracks :
		dataset[t.y] += 1

	n = float(len(tracks))

	e = 0.0

	for i in dataset :

		if (i/n) == 0 :
			continue

		e += (i/n) * log(1/(i/n))

	return e


			
		

