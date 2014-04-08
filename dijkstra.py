import queue

def Queue_creator(cost_path,parent,search_list, KNN_dictionary,Queue):
	for i in search_list:

		if cost_path.get(i)==None:
			# print(parent)
			cost_path[i]=[999999,cost_path[parent][1]+[i]]
		if 0 not in KNN_dictionary[i][0][0].keys():
			temp=0+cost_path[parent][0]
		else:
			if 1 in KNN_dictionary[i][0][0].keys():
				temp=KNN_dictionary[i][0][0][1][-1]+cost_path[parent][0]

		if cost_path[i][0]>temp:
			cost_path[i][0]=temp
			cost_path[i][1]=cost_path[parent][1]+[i]
		Queue.put([cost_path[i][0],i])



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

	print('start {}\n{}'.format(start, KNN_dictionary[start]))
	cost_path[start]=[KNN_dictionary[start][0][0][1][-1],[start]]
	visited.append(start)
	todo=neighbour_searcher(start,KNN_dictionary)
	print("start and todo",start,todo)
	# edges[start]=todo
	Queue_creator(cost_path,start, todo, KNN_dictionary, Queue)

	while dest not in visited:
		node=Queue.get()
		if node[1] not in visited:
			visited.append(node[1])
			temp=neighbour_searcher(node[1],KNN_dictionary)
			Queue_creator(cost_path,node[1],temp,KNN_dictionary,Queue)

	return cost_path[dest][1]