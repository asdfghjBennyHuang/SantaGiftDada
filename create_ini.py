# -*- coding: utf-8 -*-
"""
Created on Sat Jan  6 16:14:20 2018

@author: user
"""

import pandas as pd
import numpy as np
import normaleval as ne
import time

print( 'imported' )

max_num_gift = 1000
to_prefer = 80
child = pd.read_csv("child_wishlist_v2.csv", header=None)

ini = [-1] * len(child)

gift_count = [0] * 1000

t = time.time()

print( 'start creating' )

preference = 1

while preference <= 1000:
	i = 0
	while i <= 5000:
		row = child.iloc[i]
		if gift_count[ row[preference] ] < max_num_gift-2:
			ini[ i ] = row[preference]
			ini[ i+1 ] = row[preference]
			ini[ i+2 ] = row[preference]
			gift_count[ row[preference] ] += 3
		
		i += 3

	print( 'into twins' )

	while i <= 45000:
		row = child.iloc[i]
		if gift_count[ row[preference] ] < max_num_gift-1:
			ini[ i ] = row[preference]
			ini[ i+1 ] = row[preference]
			gift_count[ row[preference] ] += 2
		
		i += 2

	print( 'into single' )

	while i < 1000000:
		row = child.iloc[i]
		if gift_count[ row[preference] ] < max_num_gift:
			ini[ i ] = row[preference]
			gift_count[ row[preference] ] += 1
		
		i += 1

	print( preference )
	preference += 1

t = time.time() - t
print( 'time for giving gift : {}'.format( t ) )

not_filled = len( [ i for i in ini if i == -1 ] )
print( 'number of unfilled slot : {}'.format( not_filled ) )

print( 'start filling empty slots' )

for inx, n in enumerate( ini ):
    if n == -1:
        for g_inx in range( 1, 1001 ):
            if gift_count[g_inx] < max_num_gift:
                ini[inx] = g_inx
                gift_count[g_inx] += 1
                break

not_filled = len( [i for i in ini if i == -1 ] )
print( 'number of unfilled slot : {}'.format( not_filled ) )

print( 'start writing' )

with open( 'init_state_to_80.csv', 'w' ) as fw:
    fw.write( ','.join( (str(i) for i in ini) ) )

table = [ [ inx, int( i ) ] for inx, i in enumerate( ini ) ]

gift_pref = pd.read_csv('child_wishlist_v2.csv',header=None).drop(0, 1).values
child_pref = pd.read_csv('gift_goodkids_v2.csv',header=None).drop(0, 1).values

score, _, _ = ne.avg_normalized_happiness( table, child_pref, gift_pref )
print( 'score : {}', score )
