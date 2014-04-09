import queue
import knn

def search_helper(cost_path,parent,search_list, KNN_dictionary,Queue):
	for element in search_list:

		if cost_path.get(element)==None:
			# print(parent)
			cost_path[element]=[999999,cost_path[parent][1]+[element]]
		if 0 not in KNN_dictionary[element][0].keys():
			temp=0+cost_path[parent][0]
		else:
			temp=KNN_dictionary[element][0][0][-1]+cost_path[parent][0]

		if cost_path[element][0]>temp:
			cost_path[element][0]=temp
			cost_path[element][1]=cost_path[parent][1]+[element]
		Queue.put([cost_path[element][0],element])

def search_helper2(cost_path,parent,search_list, KNN_dictionary,Queue):
	for element in search_list:

		if cost_path.get(element)==None:
			# print(parent)
			cost_path[element]=[999999,cost_path[parent][1]+[element]]
		if 0 and 1 not in KNN_dictionary[element][0].keys():
			temp=0+cost_path[parent][0]

		elif 0 in KNN_dictionary[element][0].keys() and 1 not in KNN_dictionary[element][0].keys() :
			temp=cost_path[parent][0]-KNN_dictionary[element][0][0][-1]

		elif 1 in KNN_dictionary[element][0].keys() and 0 not in KNN_dictionary[element][0].keys() :

			temp=cost_path[parent][0]+KNN_dictionary[element][0][1][-1]

		else:

			temp=(KNN_dictionary[element][0][1][-1] - KNN_dictionary[element][0][0][-1])+cost_path[parent][0]

		if cost_path[element][0]<temp:
			cost_path[element][0]=temp
			cost_path[element][1]=cost_path[parent][1]+[element]
		Queue.put([cost_path[element][0],element])


def neighbour_searcher(parent,KNN_dictionary):

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

	# edge={}
	cost_path={}
	visited=[]
	todo=[]
	Queue=queue.PriorityQueue()
	# print(start)
	# if KNN_dictionary[start][0].get(0)==None:
	cost_path[start]=[0,[start]]
	# else:
	# 	cost_path[start]=[KNN_dictionary[start][0][0][-1],[start]]
	# 	cost_path[start]=[KNN_dictionary[start][0][0][-1],[start]]
	visited.append(start)
	todo=neighbour_searcher(start,KNN_dictionary)
	# print("start and todo",start,todo)
	# edges[start]=todo
	search_helper(cost_path,start, todo, KNN_dictionary, Queue)

	while dest not in visited:
		if Queue.empty():
			return []
		node=Queue.get()
		if node[1] not in visited:
			visited.append(node[1])
			temp=neighbour_searcher(node[1],KNN_dictionary)
			search_helper(cost_path,node[1],temp,KNN_dictionary,Queue)

	#print('came')
	return cost_path[dest][1]

def estimated_distance(start,dest):
	distance=(  (start[0]-dest[0])**2 +  (start[1]-dest[1])**2   )**0.5
	return distance

def chaser(start, dest, gridworld):
	neighbour=neighbour_searcher(start,gridworld)
	#estimated_dist={}
	Queue=queue.PriorityQueue()
	for i in neighbour:
#		Queue.put([knn.manhattan_distance(i,dest),i])
		Queue.put([estimated_distance(i,dest),i])

	togo=Queue.get()
	#print(togo)
	return togo[1]