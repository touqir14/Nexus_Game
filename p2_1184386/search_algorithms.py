import queue
import knn


def search_helper(cost_path,parent,search_list, KNN_dictionary,Queue):
	"""
	A helper function for dijkstra to update costs of nodes and also to assign the the least cost path to each node that in the search list
	"""

	for element in search_list:

		#if no cost is assigned to a box, then assign a big cost, just like we give an infinity cost at the beginning of dijkstra to every node
		if cost_path.get(element)==None:

			cost_path[element]=[999999,cost_path[parent][1]+[element]]

		#if no weights of negative points(denoted by key of 0) is found in a box, we assign a weight of 0
		if 0 not in KNN_dictionary[element][0].keys():

			cost=0+cost_path[parent][0]

		else:
			#otherwise we add its cost with its parent's cost
			cost=KNN_dictionary[element][0][0][-1]+cost_path[parent][0]

		if cost_path[element][0]>cost:

			cost_path[element][0]=cost

			cost_path[element][1]=cost_path[parent][1]+[element]

		Queue.put([cost_path[element][0],element])


def neighbour_searcher(parent,KNN_dictionary):
	"""
	Looks for neighbours of a query box and if a neighbour exists, then returns it in a list. It looks in four directions , up, down, left , right.

	"""
	neighbours=[]


	if KNN_dictionary.get((parent[0]+1,parent[1]))!=None:

		neighbours.append((parent[0]+1,parent[1]))


	if KNN_dictionary.get((parent[0]-1,parent[1]))!=None:

		neighbours.append((parent[0]-1,parent[1]))


	if KNN_dictionary.get((parent[0],parent[1]+1))!=None:

		neighbours.append((parent[0],parent[1]+1))


	if KNN_dictionary.get((parent[0],parent[1]-1))!=None:

		neighbours.append((parent[0],parent[1]-1))
 

	return neighbours


def search(start, dest, KNN_dictionary):

	cost_path={}
	
	visited=[]

	todo=[]

	Queue=queue.PriorityQueue()

	cost_path[start]=[0,[start]]

	visited.append(start)

	todo=neighbour_searcher(start,KNN_dictionary)

	search_helper(cost_path,start, todo, KNN_dictionary, Queue)

	while dest not in visited:

		if Queue.empty():

			return []

		node=Queue.get()


		if node[1] not in visited:

			visited.append(node[1])

			neighbours=neighbour_searcher(node[1],KNN_dictionary)

			search_helper(cost_path,node[1],neighbours,KNN_dictionary,Queue)

	return cost_path[dest][1]



def estimated_distance(start,dest):
	"""
	calculates euclidean distance
	"""

	distance=(  (start[0]-dest[0])**2 +  (start[1]-dest[1])**2   )**0.5

	return distance



def A_star_chaser(start, dest, gridworld):

	neighbour=neighbour_searcher(start,gridworld)

	Queue=queue.PriorityQueue()

	for point in neighbour:

		Queue.put([estimated_distance(point,dest),point])


	togo=Queue.get()

	return togo[1]