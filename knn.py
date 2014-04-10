import random
import time
import math


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
    probability=[]

    decay=1

    combined=positive+negative

    combination_constant=[combination_calc(k,len(positive)),combination_calc(k,len(negative))]

    for i in range(k):

        decay*=(gamma**combined[i])

    positive_theta=len(positive)/k

    negative_theta=len(negative)/k

    #The below "probability.append" creates probability for positive points and stores it in probability[0]. The forumala can be found in my uploaded document
    probability.append((positive_theta)**len(positive) * (1-positive_theta)**len(negative) *combination_constant[0]*decay)

    #The below "probability.append" creates probability for negative points and stores it in probability[1]. The forumala can be found in my uploaded document
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

    for p_class in classtype:

        total_weight=0

        #points_dict actually has a list containing distances between neighbours of specific class and query box. 
        for distance in points_dict[p_class]:

            if p_class not in weight_dict.keys():

                weight_dict[p_class]=[]

            weight_dict[p_class].append(sigmoid(-distance))

            total_weight+=sigmoid(-distance)

        weight_dict[p_class].append(total_weight)

        total_weight_list.append([total_weight,p_class])

        total_weight_list2.append(total_weight)

    max_weight=max(total_weight_list)

    # if there is only 1 maximum weight, we select that class which has this weight as the dominant class 
    if total_weight_list2.count(max_weight[0])==1:

        dominant_class=max_weight[1]

    #in case if we have multiple equal maximum weights, we randomnly choose a dominant weight
    else:

        max_weight_classes=[]

        for x,y in total_weight_list:

            if x==max_weight[0]:

                max_weight_classes.append(y)

        dominant_class=random.choice(max_weight_classes)

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

    for p_class in point_class:

        classtype[p_class]=[]

        for point in points:

            if point[1]==p_class:

                classtype[p_class].append(point[:2])

        probability[p_class]=len(classtype[p_class])/total_frequency
    

    for index in range(total_class):
        
        if index==0:

            probability_boundary[point_class[index]]=[0,probability[point_class[index]]]

        elif index==total_class-1 :
            
            probability_boundary[point_class[index]]=[1-probability[point_class[index]],1]

        else:

            previous_right_boundary=probability_boundary[point_class[index-1]][1]

            probability_boundary[point_class[index]]=[previous_right_boundary,probability[point_class[index]]+previous_right_boundary]



    r1 = random.SystemRandom()

    for i in range(size):

        rand_no=0

        for j in range(times):

            rand_no+=(1*r1.uniform(0,1))

        mean_rand=rand_no/times

        for p_class in point_class:

            if probability_boundary[p_class][0]<mean_rand and probability_boundary[p_class][1]>=mean_rand:

                if p_class not in sampled_dict.keys():

                    sampled_dict[p_class]=[]

                sampled_dict[p_class].append(distance)

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


    for key in keys: 

        positive=[]

        negative=[]
        #spoints contain sampled points

        spoints=[]


        if len(KNN[key])>k: #In case our KNN has more points than kpoints and we need to create fake samples

            distance=KNN[key][-1][0] #We take into account the last k_point in the list as we also know that it has greatest distance from the query box
            #and actually find other points of its distance and remove those points and send them to sampler. I have discussed about it in my document. 

            index=-1

            for i in KNN[key]:
                
                index+=1

                if i[0]==distance:

                    first_half=KNN[key][ :index]

                    second_half=KNN[key][index:-1]

                    second_half+=[KNN[key][-1]]

                    break

            for point in first_half:

                if point_dictionary[tuple(point[1])]==[1]:

                    positive.append(point[0])

                if point_dictionary[tuple(point[1])]==[0]:

                    negative.append(point[0])



            for point in second_half:

                if point_dictionary[tuple(point[1])]==[1]:
    
                    spoints.append([point[0],1])
    
                if point_dictionary[tuple(point[1])]==[0]:
    
                    spoints.append([point[0],0])

            spoints_dict={} #should contain the dictionary that will be returned by the sampler

            spoints_dict=sampler(3,k-len(first_half),spoints,[0,1])

            if 1 in spoints_dict.keys():
    
                positive+=spoints_dict[1]
    
            if 0 in spoints_dict.keys():
    
                negative+=spoints_dict[0]


            if flag==0:

                probability=binomial_distribution(k,positive,negative,gamma)
    
                KNN_probability[key]=[{0:[probability[1]],1:[probability[0]]},max(probability[0],probability[1])]

            elif flag==1:
    
                _dict = {}
    
                if len(positive) > 0:
    
                    _dict[1]=positive
    
                if len(negative) > 0:
    
                    _dict[0]=negative
    
                #Here weight is a list which contains a weight dictionary and a dominant class(the class that has the greatest cumulative weight)
    
                weight=weight_assigner(_dict,list(_dict.keys()))

                KNN_weights[key]=weight


        if len(KNN[key])<=k:
        

            for point in KNN[key]:
                
                if point_dictionary[tuple(point[1])]==[1]:
    
                    positive.append(point[0])
    
                if point_dictionary[tuple(point[1])]==[0]:
    
                    negative.append(point[0])


            if flag==0:

                probability=binomial_distribution(len(KNN[key]),positive,negative,gamma)
    
                KNN_probability[key]=[{0:[probability[1]],1:[probability[0]]},max(probability[0],probability[1])]

            elif flag==1:
    
                _dict = {}
    
                if len(positive) > 0:
    
                    _dict[1]=positive
    
                if len(negative) > 0:
    
                    _dict[0]=negative
    
                #Here weight is a list containing a weight dictionary and dominant class

                weight=weight_assigner(_dict,list(_dict.keys()))

                KNN_weights[key]=weight
                

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

        if len(class_dictionary[tuple(i[1])])!=0:
    
            knn_points.append(i)

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
    
    todo=[]
    
    to_visit=[]
    
    for box in grid_dictionary.keys():
    
        if len(grid_dictionary[box])==0:
    
            todo.append(box)

    for box in todo:
    
        present_k=0
    
        counter=0
    
        boundary=[]
    
        to_visit=[]
    
        prev_visit=[box]
    
        k_points=[]       
        

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

            for point in to_visit:

                prev_visit.append(point)

                dist.append([manhattan_distance(point,box),point])


            to_visit=[]

            k_points+=k_search(k-present_k,dist,grid_dictionary)

            present_k=len(k_points)

        
        KNN[tuple(box)]=k_points

    if flag==0:

        KNN_probability=Probabilistic_KNN(k,KNN,grid_dictionary,gamma,0)
       
        return KNN_probability
        
    if flag==1:

        KNN_weights=Probabilistic_KNN(k,KNN,grid_dictionary,gamma,1)
       
        return KNN_weights

    


