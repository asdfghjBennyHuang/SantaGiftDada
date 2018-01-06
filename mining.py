import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import math
from collections import Counter
import random
import time

n_children = 1000000 # n children to give
n_gift_type = 1000 # n types of gifts available
n_gift_quantity = 1000 # each type of gifts are limited to this quantity
n_gift_pref = 100 # number of gifts a child ranks
n_child_pref = 1000 # number of children a gift ranks
twins = math.ceil(0.04 * n_children / 2.) * 2    # 4% of all population, rounded to the closest number
triplets = math.ceil(0.005 * n_children / 3.) * 3    # 0.5% of all population, rounded to the closest number
ratio_gift_happiness = 2
ratio_child_happiness = 2

gift_pref = pd.read_csv('child_wishlist_v2.csv',header=None).drop(0, 1).values
child_pref = pd.read_csv('gift_goodkids_v2.csv',header=None).drop(0, 1).values

effective_swap_count = 0

def lcm(a, b):
	"""Compute the lowest common multiple of a and b"""
	# in case of large numbers, using floor division
	return a * b // math.gcd(a, b)

def avg_normalized_happiness(pred, child_pref, gift_pref):

	# check if number of each gift exceeds n_gift_quantity
	gift_counts = Counter(elem[1] for elem in pred)
	for count in gift_counts.values():
	    assert count <= n_gift_quantity
	            
	# check if triplets have the same gift
	for t1 in np.arange(0,triplets,3):
	    triplet1 = pred[t1]
	    triplet2 = pred[t1+1]
	    triplet3 = pred[t1+2]
	    # print(t1, triplet1, triplet2, triplet3)
	    assert triplet1[1] == triplet2[1] and triplet2[1] == triplet3[1]
	            
	# check if twins have the same gift
	for t1 in np.arange(triplets,triplets+twins,2):
	    twin1 = pred[t1]
	    twin2 = pred[t1+1]
	    # print(t1)
	    assert twin1[1] == twin2[1]

	max_child_happiness = n_gift_pref * ratio_child_happiness
	max_gift_happiness = n_child_pref * ratio_gift_happiness
	total_child_happiness = 0
	total_gift_happiness = np.zeros(n_gift_type)

	for row in pred:
	    child_id = row[0]
	    gift_id = row[1]
	    
	    # check if child_id and gift_id exist
	    assert child_id < n_children
	    assert gift_id < n_gift_type
	    assert child_id >= 0 
	    assert gift_id >= 0
	    child_happiness = (n_gift_pref - np.where(gift_pref[child_id]==gift_id)[0]) * ratio_child_happiness
	    if not child_happiness:
	        child_happiness = -1

	    gift_happiness = ( n_child_pref - np.where(child_pref[gift_id]==child_id)[0]) * ratio_gift_happiness
	    if not gift_happiness:
	        gift_happiness = -1

	    total_child_happiness += child_happiness
	    total_gift_happiness[gift_id] += gift_happiness

	print('normalized child happiness=',float(total_child_happiness)/(float(n_children)*float(max_child_happiness)))
	print('normalized gift happiness=',np.mean(total_gift_happiness) / float(max_gift_happiness*n_gift_quantity))

	# to avoid float rounding error
	# find common denominator
	# NOTE: I used this code to experiment different parameters, so it was necessary to get the multiplier
	# Note: You should hard-code the multipler to speed up, now that the parameters are finalized
	denominator1 = n_children*max_child_happiness
	denominator2 = n_gift_quantity*max_gift_happiness*n_gift_type
	common_denom = lcm(denominator1, denominator2)
	multiplier = common_denom / denominator1

	# # usually denom1 > demon2
	return float(math.pow(total_child_happiness*multiplier,3) + math.pow(np.sum(total_gift_happiness),3)) / float(math.pow(common_denom,3))
	# return math.pow(float(total_child_happiness)/(float(n_children)*float(max_child_happiness)),2) + math.pow(np.mean(total_gift_happiness) / float(max_gift_happiness*n_gift_quantity),2)

def triple_check_and_swap(first,pred,gift_pref,child_pref,num):

	global effective_swap_count

	second=random.randrange(45001,1000000)
	count=0
	index=second+1
	#child_id=pred[first][0]
	gift_id=pred[second][1]
	index_list=[]
	index_list.append(second)

	initial_happiness = 0
	after_happiness = 0

	while(count<num-1 and index<1000000):
		if pred[index][1]==gift_id:
			index_list.append(index)
			count+=1
		index+=1

	if count<num-1:
		return pred
		
	child_id=pred[first][0]
	gift_id=pred[first][1]
	child_happiness = (n_gift_pref - np.where(gift_pref[child_id]==gift_id)[0]) * ratio_child_happiness
	if not child_happiness:
		child_happiness = -1

	gift_happiness = ( n_child_pref - np.where(child_pref[gift_id]==child_id)[0]) * ratio_gift_happiness
	if not gift_happiness:
		gift_happiness = -1

	initial_happiness += ( child_happiness+gift_happiness )

	for ind in index_list:
		child_id=pred[ind][0]
		gift_id=pred[ind][1]
		child_happiness = (n_gift_pref - np.where(gift_pref[child_id]==gift_id)[0]) * ratio_child_happiness
		if not child_happiness:
			child_happiness = -1

		gift_happiness = ( n_child_pref - np.where(child_pref[gift_id]==child_id)[0]) * ratio_gift_happiness
		if not gift_happiness:
			gift_happiness = -1

		initial_happiness += ( child_happiness+gift_happiness )

	child_id=pred[first][0]
	gift_id=pred[second][1]
	child_happiness = (n_gift_pref - np.where(gift_pref[child_id]==gift_id)[0]) * ratio_child_happiness
	if not child_happiness:
		child_happiness = -1

	gift_happiness = ( n_child_pref - np.where(child_pref[gift_id]==child_id)[0]) * ratio_gift_happiness
	if not gift_happiness:
		gift_happiness = -1

	after_happiness += ( child_happiness+gift_happiness )

	for ind in index_list:
		child_id=pred[ind][0]
		gift_id=pred[first][1]
		child_happiness = (n_gift_pref - np.where(gift_pref[child_id]==gift_id)[0]) * ratio_child_happiness
		if not child_happiness:
			child_happiness = -1

		gift_happiness = ( n_child_pref - np.where(child_pref[gift_id]==child_id)[0]) * ratio_gift_happiness
		if not gift_happiness:
			gift_happiness = -1

		after_happiness += ( child_happiness+gift_happiness )

	if after_happiness> initial_happiness:
		temp=pred[first][1]
		
		if num==3:
			if first%3==0:
				pred[first][1]=pred[second][1]
				pred[first+1][1]=pred[second][1]
				pred[first+2][1]=pred[second][1]
			elif first%3==1:
				pred[first][1]=pred[second][1]
				pred[first-1][1]=pred[second][1]
				pred[first+1][1]=pred[second][1]
			else:
				pred[first][1]=pred[second][1]
				pred[first-1][1]=pred[second][1]
				pred[first-2][1]=pred[second][1]
		else:
			if first%2==0:
				pred[first][1]=pred[second][1]
				pred[first-1][1]=pred[second][1]
			else:
				pred[first][1]=pred[second][1]
				pred[first+1][1]=pred[second][1]
		
		for ind in index_list:
			pred[ind][1]=temp
			
		effective_swap_count += 1

	return pred

def data_mining(pred, gift_pref, child_pref):

	global effective_swap_count
	
	effective_swap_count = 0

	#print(avg_normalized_happiness(pred, child_pref, gift_pref))
	for num in range( 0 , 10000000 ):
		first=random.randrange(1,1000000)
		if first<=5000:
			pred=triple_check_and_swap(first,pred,gift_pref,child_pref,3)
		elif first>5000 and first<=45000:
			pred=triple_check_and_swap(first,pred,gift_pref,child_pref,2)
		else:
			initial_happiness = 0
			after_happiness = 0
			second=random.randrange(45001,1000000)
			
			child_id=pred[first][0]
			gift_id=pred[first][1]

			child_happiness = (n_gift_pref - np.where(gift_pref[child_id]==gift_id)[0]) * ratio_child_happiness
			if not child_happiness:
				child_happiness = -1

			gift_happiness = ( n_child_pref - np.where(child_pref[gift_id]==child_id)[0]) * ratio_gift_happiness
			if not gift_happiness:
				gift_happiness = -1

			initial_happiness += ( child_happiness + gift_happiness )

			child_id=pred[second][0]
			gift_id=pred[second][1]

			child_happiness = (n_gift_pref - np.where(gift_pref[child_id]==gift_id)[0]) * ratio_child_happiness
			if not child_happiness:
				child_happiness = -1

			gift_happiness = ( n_child_pref - np.where(child_pref[gift_id]==child_id)[0]) * ratio_gift_happiness
			if not gift_happiness:
				gift_happiness = -1

			initial_happiness += ( child_happiness+gift_happiness )

			child_id=pred[first][0]
			gift_id=pred[second][1]

			child_happiness = (n_gift_pref - np.where(gift_pref[child_id]==gift_id)[0]) * ratio_child_happiness
			if not child_happiness:
			    child_happiness = -1

			gift_happiness = ( n_child_pref - np.where(child_pref[gift_id]==child_id)[0]) * ratio_gift_happiness
			if not gift_happiness:
				gift_happiness = -1

			after_happiness += ( child_happiness+gift_happiness )

			child_id=pred[second][0]
			gift_id=pred[first][1]

			child_happiness = (n_gift_pref - np.where(gift_pref[child_id]==gift_id)[0]) * ratio_child_happiness
			if not child_happiness:
			    child_happiness = -1

			gift_happiness = ( n_child_pref - np.where(child_pref[gift_id]==child_id)[0]) * ratio_gift_happiness
			if not gift_happiness:
			    gift_happiness = -1

			after_happiness += ( child_happiness+gift_happiness )
			if after_happiness> initial_happiness:
				# do swapping
				temp=pred[first][1]
				pred[first][1]=pred[second][1]
				pred[second][1]=temp

				effective_swap_count += 1

	print( 'effective_swap_count : {}'.format( effective_swap_count ) )
	return pred


random_sub = pd.read_csv('sample_submission_random_v2.csv').values.tolist()

print( 'start swapping' )

for big_round in range( 40 ):

	t = time.time()
	random_sub = data_mining(random_sub, gift_pref, child_pref)
	t = time.time() - t
	print( 'time spend on algorithm : {}'.format( t ) )

	t = time.time()
	score = avg_normalized_happiness(random_sub, child_pref, gift_pref)
	print( 'score : {}'.format( score ) )
	t = time.time() - t
	print( 'time spend on evaluating : {}'.format( t ) )

	with open( 'answer_jfjshdlh_{}.csv'.format( big_round ), 'w' ) as fw:
		fw.write( ','.join( ( str(i[1]) for i in random_sub ) ) )
	
	print( '-----------------------' )
