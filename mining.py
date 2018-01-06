import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import random
import time

import normaleval as ne

gift_pref = pd.read_csv('child_wishlist_v2.csv',header=None).drop(0, 1).values
child_pref = pd.read_csv('gift_goodkids_v2.csv',header=None).drop(0, 1).values

effective_swap_count = 0

def triple_check_and_swap(first,pred,gift_pref,child_pref,num,normalized_child_happiness,normalized_gift_happiness):

	global effective_swap_count
	total_child_happiness = normalized_child_happiness
	total_gift_happiness = normalized_gift_happiness
	
	second=random.randrange(45001,1000000)
	count=0
	index=second+1
	#child_id=pred[first][0]
	gift_id=pred[second][1]
	index_list=[]
	index_list.append(second)

	initial_child_happiness = 0
	initial_gift_happiness = 0
	after_child_happiness = 0
	after_gift_happiness = 0

	while(count<num-1 and index<1000000):
		if pred[index][1]==gift_id:
			index_list.append(index)
			count+=1
		index+=1

	if count<num-1:
		return pred,total_child_happiness,total_gift_happiness
		
	child_id=pred[first][0]
	gift_id=pred[first][1]
	child_happiness = ( ne.n_gift_pref - np.where(gift_pref[child_id]==gift_id)[0]) * ne.ratio_child_happiness
	if not child_happiness:
		child_happiness = -1

	gift_happiness = ( ne.n_child_pref - np.where(child_pref[gift_id]==child_id)[0]) * ne.ratio_gift_happiness
	if not gift_happiness:
		gift_happiness = -1

	initial_child_happiness += child_happiness*num
	initial_gift_happiness += gift_happiness*num

	for ind in index_list:
		child_id=pred[ind][0]
		gift_id=pred[ind][1]
		child_happiness = ( ne.n_gift_pref - np.where(gift_pref[child_id]==gift_id)[0]) * ne.ratio_child_happiness
		if not child_happiness:
			child_happiness = -1

		gift_happiness = ( ne.n_child_pref - np.where(child_pref[gift_id]==child_id)[0]) * ne.ratio_gift_happiness
		if not gift_happiness:
			gift_happiness = -1

		initial_child_happiness += child_happiness
		initial_gift_happiness += gift_happiness

	child_id=pred[first][0]
	gift_id=pred[second][1]
	child_happiness = ( ne.n_gift_pref - np.where(gift_pref[child_id]==gift_id)[0]) * ne.ratio_child_happiness
	if not child_happiness:
		child_happiness = -1

	gift_happiness = ( ne.n_child_pref - np.where(child_pref[gift_id]==child_id)[0]) * ne.ratio_gift_happiness
	if not gift_happiness:
		gift_happiness = -1

	after_child_happiness += child_happiness*num
	after_gift_happiness += gift_happiness*num

	for ind in index_list:
		child_id=pred[ind][0]
		gift_id=pred[first][1]
		child_happiness = ( ne.n_gift_pref - np.where(gift_pref[child_id]==gift_id)[0]) * ne.ratio_child_happiness
		if not child_happiness:
			child_happiness = -1

		gift_happiness = ( ne.n_child_pref - np.where(child_pref[gift_id]==child_id)[0]) * ne.ratio_gift_happiness
		if not gift_happiness:
			gift_happiness = -1

		after_child_happiness += child_happiness
		after_gift_happiness += gift_happiness
		
		
	
	
	if (total_child_happiness + after_child_happiness/2000 - initial_child_happiness/2000)**3  + (total_gift_happiness +after_gift_happiness/2000 - initial_gift_happiness/2000)**3  >  total_child_happiness**3 + total_gift_happiness**3:
	#if after_happiness> initial_happiness:
		
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
		
		
		total_child_happiness += ( after_child_happiness/2000 - initial_child_happiness/2000 )
		total_gift_happiness += ( after_gift_happiness/2000 - initial_gift_happiness/2000 )
		
		effective_swap_count += 1
	
	return pred,total_child_happiness,total_gift_happiness

def data_mining(pred, gift_pref, child_pref,normalized_child_happiness,normalized_gift_happiness):

	global effective_swap_count
	
	effective_swap_count = 0
	
	total_child_happiness=normalized_child_happiness
	total_gift_happiness=normalized_gift_happiness
	
	#print(avg_normalized_happiness(pred, child_pref, gift_pref))
	for num in range( 0 , 1000000 ):
		first=random.randrange(1,1000000)
		if first<=5000:
			pred,total_child_happiness,total_gift_happiness=triple_check_and_swap(first,pred,gift_pref,child_pref,3,total_child_happiness,total_gift_happiness)
		elif first>5000 and first<=45000:
			pred,total_child_happiness,total_gift_happiness=triple_check_and_swap(first,pred,gift_pref,child_pref,2,total_child_happiness,total_gift_happiness)
		else:
			initial_child_happiness = 0
			initial_gift_happiness = 0
			after_child_happiness = 0
			after_gift_happiness = 0
			
			second=random.randrange(45001,1000000)
			
			child_id=pred[first][0]
			gift_id=pred[first][1]

			child_happiness = (ne.n_gift_pref - np.where(gift_pref[child_id]==gift_id)[0]) * ne.ratio_child_happiness
			if not child_happiness:
				child_happiness = -1

			gift_happiness = ( ne.n_child_pref - np.where(child_pref[gift_id]==child_id)[0]) * ne.ratio_gift_happiness
			if not gift_happiness:
				gift_happiness = -1
			initial_child_happiness += child_happiness
			initial_gift_happiness += gift_happiness
			

			child_id=pred[second][0]
			gift_id=pred[second][1]

			child_happiness = (ne.n_gift_pref - np.where(gift_pref[child_id]==gift_id)[0]) * ne.ratio_child_happiness
			if not child_happiness:
				child_happiness = -1

			gift_happiness = ( ne.n_child_pref - np.where(child_pref[gift_id]==child_id)[0]) * ne.ratio_gift_happiness
			if not gift_happiness:
				gift_happiness = -1

			initial_child_happiness += child_happiness
			initial_gift_happiness += gift_happiness

			child_id=pred[first][0]
			gift_id=pred[second][1]

			child_happiness = ( ne.n_gift_pref - np.where(gift_pref[child_id]==gift_id)[0]) * ne.ratio_child_happiness
			if not child_happiness:
			    child_happiness = -1

			gift_happiness = ( ne.n_child_pref - np.where(child_pref[gift_id]==child_id)[0]) * ne.ratio_gift_happiness
			if not gift_happiness:
				gift_happiness = -1

			after_child_happiness += child_happiness
			after_gift_happiness += gift_happiness

			child_id=pred[second][0]
			gift_id=pred[first][1]

			child_happiness = ( ne.n_gift_pref - np.where(gift_pref[child_id]==gift_id)[0]) * ne.ratio_child_happiness
			if not child_happiness:
			    child_happiness = -1

			gift_happiness = ( ne.n_child_pref - np.where(child_pref[gift_id]==child_id)[0]) * ne.ratio_gift_happiness
			if not gift_happiness:
			    gift_happiness = -1

			after_child_happiness += child_happiness
			after_gift_happiness += gift_happiness
			'''
			if after_gift_happiness != -2:
				print('after_gift_happiness: ')
				print(after_gift_happiness)
			if after_child_happiness != -2:
				print('after_child_happiness: ')
				print(after_child_happiness)
			'''
			
			if (total_child_happiness + after_child_happiness/2000 - initial_child_happiness/2000)**3 + \
				(total_gift_happiness +after_gift_happiness/2000 - initial_gift_happiness/2000)**3  > \
				total_gift_happiness**3+total_child_happiness**3:

			#if after_happiness> initial_happiness:

				# do swapping
				temp=pred[first][1]
				pred[first][1]=pred[second][1]
				pred[second][1]=temp
				total_child_happiness = total_child_happiness + after_child_happiness/2000 - initial_child_happiness/2000
				total_gift_happiness = total_gift_happiness + after_gift_happiness/2000 - initial_gift_happiness/2000
				
				effective_swap_count += 1

	print( 'effective_swap_count : {}'.format( effective_swap_count ) )
	return pred

def read_from_dotted_file( filename ):
	with open( filename, 'r' ) as fr:
		table = [ [ inx, int( i ) ] for inx, i in enumerate( fr.read().split(',') ) ]
	
	return table

if __name__ == '__main__':
	# random_sub = pd.read_csv('sample_submission_random_v2.csv').values.tolist()
	random_sub = read_from_dotted_file( 'init_state_3.csv' )

	train_id = int( random.random() * 1000000 )
	
	print( 'start running' )

	for big_round in range( 10 ):

		t = time.time()
		score,normalized_child_happiness,normalized_gift_happiness = ne.avg_normalized_happiness(random_sub, child_pref, gift_pref)
		print( 'score : {}'.format( score ) )
		t = time.time() - t
		print( 'time spend on evaluating : {}'.format( t ) )

		with open( 'answer_{}_{}.csv'.format( train_id, big_round ), 'w' ) as fw:
			fw.write( ','.join( ( str(i[1]) for i in random_sub ) ) )

		print( '-----------------------' )

		t = time.time()
		random_sub = data_mining(random_sub, gift_pref, child_pref,normalized_child_happiness,normalized_gift_happiness)
		t = time.time() - t
		print( 'time spend on algorithm : {}'.format( t ) )


	t = time.time()
	score,normalized_child_happiness,normalized_gift_happiness = ne.avg_normalized_happiness(random_sub, child_pref, gift_pref)
	print( 'score : {}'.format( score ) )
	t = time.time() - t
	print( 'time spend on evaluating : {}'.format( t ) )

	with open( 'answer_{}_final.csv'.format( train_id ), 'w' ) as fw:
		fw.write( ','.join( ( str(i[1]) for i in random_sub ) ) )
	print( '-----------------------' )
