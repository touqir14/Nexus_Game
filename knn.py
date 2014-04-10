import random
import time
import math
from dijkstra import search


sigmoid=lambda x:(2 / (1 + math.exp(-x))) #I have added some details about this function in a document

def factorial(f):
    """
    A "f" factorial calculator
    >>> factorial(5)
    120

    >>> factorial(9)
    362880
    """
    result=1
    for i in range(f):
        result*=(i+1)
    return result

def combination_calc(n,r):
    """
    function calculates the combination constant found in the formula of binomial_distribution
    >>> combination_calc(10,4)
    210
    >>> combination_calc(5,3)
    10
    """
    combination=(factorial(n)/(factorial(n-r)*factorial(r)))
    return combination

def binomial_distribution(k,positive,negative,gamma):
    """
    probability[Probability of finding positive, Probability of finding negative]
    i have used gamma to give weights to each point and it is dependent on how far away they are from query point.
    I have also uploaded a document explaining how i use gamma and how i derive decay from it.
    That document also also refers to the formula of binomial_distribution
    """
    # print("positive is {}, negative is {}".format(positive,negative))
    probability=[]
    decay=1
    combined=positive+negative
    combination_constant=[combination_calc(k,len(positive)),combination_calc(k,len(negative))]
    # print(len(combined))
    for i in range(k):
        decay*=(gamma**combined[i])
    positive_theta=len(positive)/k
    negative_theta=len(negative)/k
    # print(decay,positive_theta,negative_theta)
    probability.append((positive_theta)**len(positive) * (1-positive_theta)**len(negative) *combination_constant[0]*decay)
    probability.append((negative_theta)**len(negative) * (1-negative_theta)**len(positive) *combination_constant[1]*decay)
    return probability

def weight_assigner(points_dict,classtype):
    """
    weight_dict has keys as 0(if exists) and 1(if exists) and the values are a list of weights of points and the last value of the list is the sum of the weights.  
    returns a list [weight_dict,dominant_class]
    total_weight_list=[[total weight, class_type].....] contains a list which contains total weight for a class and then next value is the classtype
    total_weight_list2=[total_weight.......] Contains the total combined weights of each class
    """
    
    weight_dict={}
    total_weight_list=[]
    total_weight_list2=[]
    for i in classtype:
        total_weight=0
        for j in points_dict[i]:

            if i not in weight_dict.keys():
                weight_dict[i]=[]

            weight_dict[i].append(sigmoid(-j))
            total_weight+=sigmoid(-j)

        weight_dict[i].append(total_weight)
        total_weight_list.append([total_weight,i])
        total_weight_list2.append(total_weight)

    max_weight=max(total_weight_list)

    # if there is only 1 maximum weight, we select that class which has this weight as the dominant class 
    if total_weight_list2.count(max_weight[0])==1:
        dominant_class=max_weight[1]
        #print(dominant_class)
    #in case if we have multiple equal maximum weights, we randomnly choose a dominant weight
    else:
        max_weight_classes=[]
        for x,y in total_weight_list:
            if x==max_weight[0]:
                max_weight_classes.append(y)

        dominant_class=random.choice(max_weight_classes)
        #print(dominant_class)
    # print (weight_dict)
    return [weight_dict,dominant_class]
    

def sampler(times,size,points,point_class):
    """
    This is a generic multiclass sampler, used to produce fake samples of each class depending on the probability distribution of each class.
    points=[distance, coordinates, classtype]
    probability dictionary is used to record the probabilities of each classes
    This returns a sampled_dict that contains a list of occurences of each class represented with distance
    This is discussed in detail in my documents.
    """
    distance=points[0][0]
    probability_boundary={}
    probability={}
    total_frequency=len(points)
    classtype={}
    total_class=len(point_class)
    sampled_dict={}
    for i in point_class:
        classtype[i]=[]
        for j in points:
            if j[1]==i:
                classtype[i].append(j[:2])

        probability[i]=len(classtype[i])/total_frequency
    

    for index in range(total_class):
        
        if index==0:
            probability_boundary[point_class[index]]=[0,probability[point_class[index]]]

        elif index==total_class-1 :
            
            probability_boundary[point_class[index]]=[1-probability[point_class[index]],1]

        else:
            previous_right_boundary=probability_boundary[point_class[index-1]][1]
            probability_boundary[point_class[index]]=[previous_right_boundary,probability[point_class[index]]+previous_right_boundary]

    # print("boundary",probability_boundary)
    # print("probability",probability)

    r1 = random.SystemRandom()
    for i in range(size):
        rand_no=0
        for j in range(times):
            # random.seed(random.uniform(0,1000))
            # r1 = random.SystemRandom()
            rand_no+=(1*r1.uniform(0,1))
            # time.sleep(0.05)
        mean_rand=rand_no/times
        # print("mean")
        for k in point_class:
            if probability_boundary[k][0]<mean_rand and probability_boundary[k][1]>=mean_rand:
                if k not in sampled_dict.keys():
                    sampled_dict[k]=[]
                sampled_dict[k].append(distance)
    return sampled_dict

def Probabilistic_KNN(k,KNN,point_dictionary,gamma,flag):
    """
    This function can calculate weights and probability depeinding on the flag that is passed
    flag 1 means to use weighted KNN. flag 0 means to use probabilistic binomial KNN
    This is discussed in detail in my document
    """
    keys=KNN.keys()
    KNN_weights={}
    KNN_probability={}

    # print(list(keys).sort())
    for key in keys: 
        positive=[]
        negative=[]
        spoints=[]
    
        # print('key {}'.format(key))
        if len(KNN[key])>k: #In case our KNN has more points than kpoints and we need to create fake samples
            # print('1st worlde {}'.format(key))
            distance=KNN[key][-1][0]
            index=-1
            for i in KNN[key]:
                
                index+=1
                # print(index)
                if i[0]==distance:
                    first_half=KNN[key][ :index]
                    second_half=KNN[key][index:-1]
                    second_half+=[KNN[key][-1]]
                    break

            for i in first_half:
                if point_dictionary[tuple(i[1])]==[1]:
                    positive.append(i[0])
                if point_dictionary[tuple(i[1])]==[0]:
                    negative.append(i[0])

            # print(second_half,distance,index)

            for i in second_half:
                # print(i)
                if point_dictionary[tuple(i[1])]==[1]:
                    spoints.append([i[0],1])
                if point_dictionary[tuple(i[1])]==[0]:
                    spoints.append([i[0],0])

            spoints_dict={}
            # print(spoints)
            spoints_dict=sampler(3,k-len(first_half),spoints,[0,1])
            # print("first_half {}".format(first_half))
            # print(spoints_dict)
            # print(positive)
            # print(negative)
            if 1 in spoints_dict.keys():
                positive+=spoints_dict[1]
            if 0 in spoints_dict.keys():
                negative+=spoints_dict[0]

            # print(positive)
            # print(negative)

            # print(positive,negative)
            if flag==0:

                probability=binomial_distribution(k,positive,negative,gamma)
                KNN_probability[key]=[{0:[probability[1]],1:[probability[0]]},max(probability[0],probability[1])]

            elif flag==1:
                _dict = {}
                if len(positive) > 0:
                    _dict[1]=positive
                if len(negative) > 0:
                    _dict[0]=negative
                temp=weight_assigner(_dict,list(_dict.keys()))
                # print('temp {}'.format(temp))
                KNN_weights[key]=temp

            # print("k is great")

        if len(KNN[key])<=k:
        

            for i in KNN[key]:
                
                if point_dictionary[tuple(i[1])]==[1]:
                    positive.append(i[0])
                if point_dictionary[tuple(i[1])]==[0]:
                    negative.append(i[0])

            # print(KNN[key])

            if flag==0:

                probability=binomial_distribution(len(KNN[key]),positive,negative,gamma)
                KNN_probability[key]=[{0:[probability[1]],1:[probability[0]]},max(probability[0],probability[1])]

            elif flag==1:
                _dict = {}
                if len(positive) > 0:
                    _dict[1]=positive
                if len(negative) > 0:
                    _dict[0]=negative
                temp=weight_assigner(_dict,list(_dict.keys()))
                # print('temp {}'.format(temp))
                KNN_weights[key]=temp
                # print(temp)
                
                # print("k is less")

    if flag==1:
        return KNN_weights

    if flag==0:
        return KNN_probability




def k_search(k,point_list,class_dictionary):
    """
    returns a list of KNN points
    It sees if the points in point_list is empty boxes(does not contain any object like food). 
    Any empty boxes found is considered as points of the set of k-points
    """
    
    knn_points=[]
    for i in point_list:
        # print(i)
        if len(class_dictionary[tuple(i[1])])!=0:
            knn_points.append(i)
            # print(i)

    return knn_points
            


def manhattan_distance(point1,point2):
    """
    Calculates manhattan distance between two points
    >>> manhattan_distance((5,4),(6,7))
    4
    """
    p1 = point1[0]-point2[0]
    p2 = point1[1]-point2[1]
    return abs(p1)+abs(p2)



def k_nearest_neighbour_searcher(grid_dictionary,k,size,gamma=0.9,flag=1):
    """
    This function assigns k nearest neighbours to each empty box and returns a dictionary containing the nearsest neighbours for all the empty boxes
    This is discussed in detail in my document
    """
    KNN={}
    KNN_weights={}
    KNN_probability={}
    move_up=(0,-1) 
    move_down=(0,1) 
    move_left=(-1,0) 
    move_right=(1,0)
    present_k=0
    todo=[]
    to_visit=[]
    k_points=[]
    for box in grid_dictionary.keys():
        if len(grid_dictionary[box])==0:
            todo.append(box)
    # print(todo)
    for box in todo:
        counter=0
        boundary=[]
        to_visit=[]
        prev_visit=[box]
        
        
        while(present_k<k):
            counter+=1
                
            for cell in prev_visit:

                if counter==1: #We will only have the query box in the first iteration

                    if box[1]>0: #if no immediate above boundary is there

        
                        to_visit.append([box[0],box[1]+move_up[1]])
                    

                    if box[1]<size[1]: #if no immediate down boundary is there


                        to_visit.append([box[0],box[1]+move_down[1]])


                    if box[0]>0: #if no immediate left boundary is there


                        to_visit.append([box[0]+move_left[0],box[1]])


                    if box[0]<size[0]: #if no immediate right boundary is there


                        to_visit.append([box[0]+move_right[0],box[1]])

                else:


                    if cell[0]==box[0] and cell[1]<box[1]:#if cell is vertically above query box and on same vertical axis line

                        if cell[0]>0: #if no immediate left boundary

                            to_visit.append([cell[0]+move_left[0],cell[1]])

                        if cell[0]<size[0]: #If no immediate right boundary

                            to_visit.append([cell[0]+move_right[0],cell[1]])

                        if cell[1]>0: #if there is no immediate boundary above
                            
                            to_visit.append([cell[0],cell[1]+move_up[1]])

                    elif cell[0]==box[0] and cell[1]>box[1]: #if cell is vertically below query box and on same vertical axis line 

                        if cell[0]>0:#if no immediate left boundary

                            to_visit.append([cell[0]+move_left[0],cell[1]])

                        if cell[0]<size[0]:#If no immediate right boundary

                            to_visit.append([cell[0]+move_right[0],cell[1]])

                        if cell[1]<size[1]: #If there is no immediate boundary below
                            
                            to_visit.append([cell[0],cell[1]+move_down[1]])


                    elif cell[0]>0 and cell[0]<box[0]:#If our cell is on the left side of query box(it can be above or down) and also if the boundary is not 
                    #immediately to its left side 

                        to_visit.append([cell[0]+move_left[0],cell[1]])

                    elif cell[0]<size[0] and cell[0]>box[0]:#If our cell is on the right side of query box(it can be above or down) and also if the boundary is not 
                    #immediately to its right side

                        to_visit.append([cell[0]+move_right[0],cell[1]])

            if len(to_visit)==0: #This will be true in case we assign a k greater than the total number of points

                break

            prev_visit=[]

            dist=[]

            for i in to_visit:

                prev_visit.append(i)

                dist.append([manhattan_distance(i,box),i])


            to_visit=[]

            k_points+=k_search(k-present_k,dist,grid_dictionary)

            present_k=len(k_points)

        
        KNN[tuple(box)]=k_points
    # print('nineteenfour {}'.format(KNN[(19,4)]))
    # print("KNN {}".format(KNN))
    if flag==0:

        KNN_probability=Probabilistic_KNN(k,KNN,grid_dictionary,gamma,0)
        return KNN_probability
        
    if flag==1:

        KNN_weights=Probabilistic_KNN(k,KNN,grid_dictionary,gamma,1)
        print(KNN_weights)
        return KNN_weights

        #print('okay pointses {}'.format(KNN))
    

#===============================================================================
# 
# if __name__=='__main__':
#     # # point_dict={(2,2):[1],(1,3):[0],(2,4):[],(3,3):[],(4,4):[]}
#     # # point_dict={(2,2):[1],(1,3):[0],(2,4):[1],(3,3):[1],(4,4):[0]}
# 
#     # grid_dictionary={(4,2):[0],(5,3):[],(4,3):[1],(3,3):[],(6,4):[],(5,4):[],(4,4):[],(3,4):[],(2,4):[0],(5,5):[0],(4,5):[0],(3,5):[1],(4,6):[0]}
#     # positive=[[1,(4,3)],[2,(3,5)]]
#     # negative=[[1,(4,5)],[2,(4,6)],[2,(5,5)],[2,(4,2)],[2,(2,4)]]
#     # # print(k_search(1,points,point_dict))
#     # # print(factorial(5))
#     # # print(combination_calc(96,3))
#     # # #print("|{}|".)
#     # # print(binomial_distribution(7,[[1],[3],[4]],[[1],[2],[5],[6]],0.9))
#     # # print(sampler(3,3,points,[0,1]))
#     # KNN={(4,4):[[1,(4,3)],[2,(3,5)],[2,(4,6)],[2,(5,5)],[2,(4,2)],[2,(2,4)]]}
#     # # print(KNN)
#     # points_dict={0:[1,2,2,3],1:[1,1,1,2]}
#     # # print(Probabilistic_KNN(7,KNN,grid_dictionary,0.9))
#     # # print(sigmoid(0.458))
#     # temp=weight_assigner(points_dict,[0,1])
#     # #print(temp[0],temp[1])
#     # #print(sigmoid(-1))
#             
# 
# 
#     dictionary={}
#     for i in range(5):
#         for j in range(5):
#             dictionary[i,j]=[]
# 
#     dictionary[2,0]=[1]
#     dictionary[0,3]=[1]
#     dictionary[1,1]=[1]
#     dictionary[1,3]=[1]
#     dictionary[3,1]=[0]
#     dictionary[3,3]=[1]
#     dictionary[1,4]=[0]
#     dictionary[2,4]=[0]
#     hi=k_nearest_neighbour_searcher(dictionary,5,[4,4],0.9,0)
#     # print(hi)
#     # for i in hi.keys():
#     #     print (i, hi[i][0][0][-1])
# 
#     print(search((0,4),(3,4),hi))
#     print(hi)
#     # print(hi)
#===============================================================================
