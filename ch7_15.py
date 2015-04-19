###############################################################################
# Problem: 7.15, "Fundamentals of Natural Computing"
# Author: Stephanie Athow
# Date: 9 April 2015
# Problem Statement:
#	Implement a RIFS to generate all the fractals whose codes are presented in 
#	Table 7.3. - Stored in Text file: IFS_Codes
###############################################################################

import numpy as np
import random
import matplotlib.pyplot as plt


MAX_POINTS = 10000
DEPTH = 5
XMAX = 100
YMAX = 100

###############################################################################
#							Generate Valid Points
# Creates starting point list for Sierpinski Gasket and Square
# opt: 0 - Sierpinski Gasket
# opt: 1 - Square
###############################################################################
def genValidPoints( pointList, opt ):
	if ( opt == 0 ):
		y = 0
		x = 0

		for i in range ( 0, XMAX ):
			point = ( x, y )
			pointList.append( point )
			x += 1
			
		while ( x > 0 ):
			x += -1
			y += 1
			point = ( x, y )
			pointList.append( point )
			
		for i in range( 0, YMAX ):
			point = (0, y)
			pointList.append( point )
			y += -1
		
	if ( opt == 1 ):
		y = 0
		x = 0
		
		for i in range( 0, XMAX/2 ):
			for j in range( 0, YMAX/2 ):
				point = ( x, y )
				pointList.append( point )
				y += 1
			x += 1
			y = 0
		
		for i in range( XMAX/2, XMAX ):
			for j in range( YMAX/2, YMAX ):
				point = ( x, y )
				pointList.append( point )
				y += 1
			x += 1
			y = YMAX/2
	

###############################################################################
#								Select Transformation
# Using the probability per transformation, selects which transformation is 
#	done. Returns index number
###############################################################################
def selectTransformation( codes, code_num ):
	sum = 0
	function = 0
	max = 3
	prob = random.random()
	#print prob
	
	# NOTE: must change to (0,3) for gasket! otherwise (0,4)
	if ( code_num == 0 ):
		max = 4
	
	else:
		max = 5
		
	for function in range( 0, max ):
		sum = sum + float(codes[code_num][function][6])
		#print 'Sum: ', sum
		if( sum > prob ):
			break
	
	#print 'function: ', function
	return function

###############################################################################
#							Select Valid Point 
###############################################################################
def selectPoint( pointList ):
	length = len( pointList )
	i = random.randint( 0, length )
	return i

###############################################################################
#						Run transformation on Point to DEPTH
# From Appendix B.4.6:
#	w(x1, x2) = ( a*x1 + b*x2 + e, c*x1 + d*x2 + f )
# 		OR
#	w(X) = [ a b, c d] * [ x1, x2] + [ e, f ]
###############################################################################
def runTransformation( pointList, index, function ):
	#print "pointList: ", pointList
	x, y = pointList[ index-1 ]
	xnew, ynew = 0, 0
	a, b, c, d, e, f, p = function
	
	xnew = float(a)*x + float(b)*y + float(e)
	ynew = float(c)*x + float(d)*y + float(f)
	point = ( xnew, ynew )
	return point
		
###############################################################################
#							Read in IFS Codes from file
# Reads in IFS codes from text file
###############################################################################
def readCodes(codes, titles, fractal_count):
	count = -1
	# open file
	f = open( 'IFS_Codes.txt', 'r' )

	for line in f:
		# remove added ''
		line = line.strip( '\'')
		
		# ignore blank lines
		if not line.strip( ):
			pass
			
		# ignore '#'
		elif( line[0] == "#"):
			pass
		
		# save into titles list	
		elif( line[0] == '(' ):
			line = line.rstrip()
			titles.append(line)
			count += 1
			#print count
			#if( count > 1 ):
			codes.append([])
		
		# store into 2d list of codes	
		else:
			line = line.rstrip()
			line = line.split()
			#print line
			codes[count].append(line)		
	
	# close file
	f.close()
	
	#return fractal count
	return count

###############################################################################
#								Plot Image of RFIS
# Plots image of the generated fractal
###############################################################################
def plotImage( pointList, title ):
	length = len( pointList )
	for i in range( 0, length ):
		x, y = pointList[i]
		plt.scatter( x, y, marker="." )
		
	plt.grid( True )
	#plt.show()
	plt.savefig( title + '.png' )
	plt.clf()

###############################################################################
#									Main
###############################################################################
codes = []
titles = []
plist = []
plistnew = []
#pointlists = []
fractal_count = 0
i = 0

# read in codes from text file
fractal_count = readCodes( codes, titles, fractal_count )

# calculate and generate fractal images
for i in range( 0, fractal_count+1 ):
	# gasket and square - need initial list seeded
	if ( i < 2 ):
		genValidPoints( plist, i )
		for j in range( MAX_POINTS ):
			index = selectPoint( plist )
			#print "index: ", index
			for iterations in range( DEPTH ):
				trans_num = selectTransformation( codes, i )
				new_point = runTransformation( plist, index, codes[i][trans_num] )
				plistnew.append( new_point )
			plist = plistnew
			
		plotImage( plist, titles[i] )
		#pointlists.append( plist )
		#pointlists.append( [] )
		#del plist[:]
		#del plistnew[:]
	
	# fern and tree - need inital point seeded
	else:
		plist = [ (0,0) ]
		for j in range( MAX_POINTS ):
			index = selectPoint( plist )
			for iterations in range( DEPTH ):
				trans_num = selectTransformation( codes, i )
				new_point = runTransformation( plist, index, codes[i][trans_num] )
				plist.append(new_point)
		plotImage( plist, titles[i] )
		#pointlists.append( plist )
		#pointlists.append( [] )
	del plist[:]
	del plistnew[:]