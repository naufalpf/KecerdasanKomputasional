import csv
import sys
import math
import numpy
import random
from itertools import combinations

def load_data ():
	with open ('iris.csv') as file:
		dataset = []
		classes = {}
		classList = []
		rows = csv.reader (file, delimiter = ',')
		for row in rows:	
			r = []
			for col in row:
				try:
					r.append (float (col))
				except:
					pass
			dataset.append (r)
			classList.append (row[-1])

			try:
				classes[row[-1]] += 1
			except:
				classes[row[-1]] = 1
		return dataset, classes, classList


def get_random_slice (n):
	a = random.randrange (n)
	b = random.randrange (n)
	while a == b:
		b = random.randrange (n)
	c = random.randrange (n)
	while a == c or b == c:
		c = random.randrange (n)
	print ('slice: ' + str (sorted ([a+1, b+1, c+1])))
	return (sorted ([a, b, c]))


def get_initial_cluster (dataset):
	clusterList = []
	slice = get_random_slice (len (dataset))
	for i in slice:
		clusterList.append (dataset[i]) #dimasukin ke daftar clusternya
	return clusterList


def group_data (distance): #bandingin centroid mana yang paling kecil langsung taro di clusternya
	groups = []
	for i in range (len (distance)):
		groups.append (distance[i].index (min (distance[i])))
	return groups


def assign_to_clusters (dataaset, cluster, distance): #di grup in
	groups = group_data (distance)
	newCluster = []
	for i in range (len (cluster)):
		centroid = []
		for j in range (len (dataset[0])):
			c = []
			for k in range (len (dataset)):
				if groups[k] == i:
					c.append (dataset[k][j])
			centroid.append (numpy.nanmean (c))
		newCluster.append (centroid)
	return newCluster, groups


def calculate_distance (dataset, cluster): #ngitung euclidian
	distance = []
	for i in range (len (dataset)):
		d = []
		for j in range (len (cluster)):
			c = 0
			for k in range (len (dataset[0])):
				c += pow (dataset[i][k] - cluster[j][k], 2)
			d.append (math.sqrt (c))
		distance.append (d)
	return assign_to_clusters (dataset, cluster, distance)


def calculate_accuraccy (classes, classList, groups, clusterList):
	accurracyList = {}

	for i in range (len (groups)):
		try:
			accurracyList[(classList[i], groups[i])] += 1
		except:
			accurracyList[(classList[i], groups[i])] = 1

	acc_total = 0

	# print ()
	# print ('acc_list:')
	print (str (accurracyList))
	# print ('classes: ')
	# print (str (classes))

	for i in range (len (clusterList)):
		for kelas in classes:
			key = (kelas, i)
			if accurracyList.get (key):
				if accurracyList[key] >= classes[kelas] / 2:
					acc_total += accurracyList[key]

	print (acc_total)
	print (len (classList))
	# print ('return: ' + str (acc_total / len (classList)))
	return acc_total / len (classList)


#main
dataset, classes, classList = load_data ()
ncluster = int (input ('Jumlah Cluster: '))
daftar_akurasi = []

for i in range (100):
	clusterList = get_initial_cluster (dataset)

	# sys.stdout.write ('slice: ')
	# print (i)

	while True:
		nextCluster, groups = calculate_distance (dataset, clusterList) #cluster baru buat iterasi 2 dst
		

		for i in range (len (nextCluster)):
			# sys.stdout.write ('Individual: ')
			for j in range (len (groups)):
				if groups[j] == i:
					pass
					# sys.stdout.write (str (j+1) + ' ')
			# print (nextCluster[i])
		# print ()

		# print (clusterList)
		# print (nextCluster)

		for i in range (len (nextCluster)):
			for j in range (len (nextCluster[i])):
				if numpy.isnan (nextCluster[i][j]):
					nextCluster[i][j] = 0

		if (sorted (clusterList) == sorted (nextCluster)):
			break
		clusterList = nextCluster

	akurasi_now = calculate_accuraccy (classes, classList, groups, clusterList)
	daftar_akurasi.append (akurasi_now)
	print (akurasi_now)


	# print ('akurasi sementara:')
  
print ('best_accuraccy: ' + str (max (daftar_akurasi)))

# for cluster in clusterList:
#	print (cluster)
