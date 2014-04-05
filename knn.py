import random
import time
import math


sigmoid=lambda x:(2 / (1 + math.exp(-x)))

def factorial(f):
    result=1
    for i in range(f):
        result*=(i+1)
    return result

def combination_calc(n,r):
    combination=(factorial(n)/(factorial(n-r)*factorial(r)))
    return combination

def binomial_distribution(k,positive,negative,gamma):
    probability=[]
    decay=1
    combined=positive+negative
    combination_constant=[combination_calc(k,len(positive)),combination_calc(k,len(negative))]
    # print(len(combined))
    for i in range(k):
        decay*=(gamma**combined[i])
    positive_theta=len(positive)/k
    negative_theta=len(negative)/k
    print(decay,positive_theta,negative_theta)
    probability.append((positive_theta)**len(positive) * (1-positive_theta)**len(negative) *combination_constant[0]*decay)
    probability.append((negative_theta)**len(negative) * (1-negative_theta)**len(positive) *combination_constant[1]*decay)
    return probability

def weight_assigner(points_dict,classtype):
    """
    returns a list [weight_dict,dominant_class]
    total_weight_list=[[total weight, class_type].....]
    total_weight_list2=[total_weight.......]
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
        total_weight_list.append([total_weight,[i]])
        total_weight_list2.append(total_weight)

    max_weight=max(total_weight_list)
    if total_weight_list2.count(max_weight[0])==1:
        dominant_class=max_weight[1]
    else:
        max_weight_classes=[]
        for x,y in total_weight_list:
            if x==max_weight[0]:
                max_weight_classes.append(y)

        dominant_class=random.choice(max_weight_classes)

    return [weight_dict,dominant_class]
    

def sampler(times,size,points,point_class):
    """
    points=[distance, coordinates, classtype]
    probability dictionary is used to record the probabilities of each classes
    This returns a sampled_dict that contains a list of occurences of each class represented with distance
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
    flag 1 means to use weighted KNN. flag 0 means to use probabilistic binomial KNN
    """
    keys=KNN.keys()
    positive=[]
    negative=[]
    spoints=[]
    KNN_weights={}

    for key in keys: 
        # print(len(KNN[key]))
        if len(KNN[key])>k: #In case our KNN has more points than kpoints and we need to create fake samples
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
            # print(spoints_dict)
            if 1 in spoints_dict.keys():
                positive+=spoints_dict[1]
            if 0 in spoints_dict.keys():
                negative+=spoints_dict[0]

            # print(positive,negative)
            if flag==0:
                probability=binomial_distribution(k,positive,negative,gamma)
                KNN[key].append(probability)
            elif flag==1:
                temp=weight_assigner({1:positive,0:negative},[0,1])
                KNN[key].append([temp])

        if len(KNN[key])<=k:

            for i in KNN[key]:
                if point_dictionary[tuple(i[1])]==[1]:
                    positive.append(i[0])
                if point_dictionary[tuple(i[1])]==[0]:
                    negative.append(i[0])

            if flag==0:
                probability=binomial_distribution(len(KNN[key]),positive,negative,gamma)
                KNN[key].append(probability)
            elif flag==1:
                _dict = {}
                if len(positive) > 0:
                    _dict[1]=positive
                if len(negative) > 0:
                    _dict[0]=negative
                temp=weight_assigner(_dict,list(_dict.keys()))
                KNN[key].append([temp])

    return KNN





def k_search(k,point_list,class_dictionary):
    """
    returns a list of KNN points
    """
    
    knn_points=[]
    for i in point_list:
        if len(class_dictionary[tuple(i[1])])!=0:
            knn_points.append(i)

    return knn_points
            


def manhattan_distance(point1,point2):
    print(point1)
    p1 = point1[0]-point2[0]
    p2 = point1[1]-point2[1]
    return abs(p1)+abs(p2)



def k_nearest_neighbour(grid_dictionary,k,size,gamma=0.9,flag=1):
    """
    This function assigns k nearest neighbours to each empty box and returns a dictionary containing the nearsest neighbours for all the empty boxes
    """
    KNN={}
    move_up=(0,-1) 
    move_down=(0,1) 
    move_left=(-1,0) 
    move_right=(1,0)
    present_k=0
    todo=[]
    #visited=[]
    k_points=[]
    for box in grid_dictionary.keys():
        if len(grid_dictionary[box])==0:
            todo.append(box)
    for box in todo:
        counter=0
        boundary=[]
        up=[]
        down=[]
        
        while(present_k<k):
            counter+=1
            up_updated=False
            down_updated=False
            
            if len(up)!=0 and up[1]>0: #make sure there is an up coordinate and also that up hasnt reached the upper horizontal border
                
                if up[0]<size[0]:#make sure that up is not touching the right vertical border

                    boundary.append([up[0]+move_right[0],up[1]])

                if up[0]>1:#make sure that up is not touching the left border

                    boundary.append([up[0]+move_left[0],up[1]])

                up=[up[0],up[1]+move_up[1]]
                up_updated=True

            if len(down)!=0 and down[1]<size[1]:

                if down[0]<size[0]:#make sure that down is not touching the right vertical border

                    boundary.append([down[0]+move_right[0],down[1]])

                if down[1]>1:

                    boundary.append([down[0]+move_left[0],down[1]])

                down=[down[0],down[1]+move_down[1]]
                down_updated=True

            if len(boundary)!=0:
                boundary_clone=boundary[:]
                for i in boundary_clone:
                    temp=boundary.pop(boundary.index(i))
                    if temp[0]>box[0] and temp[0]<size[0]:
                        temp[0]+=move_right[0]
                        boundary.append(temp)
                    elif temp[0]<box[0] and temp[0]>1:
                        temp[0]+=move_left[0]
                        boundary.append(temp)

            if counter==1:
                up.append(box[0])
                up.append(box[1]+move_up[1])
                up_updated=True

                down.append(box[0])
                down.append(box[1]+move_down[1])
                down_updated=True

                boundary.append([box[0]+move_left[0],box[1]])
                boundary.append([box[0]+move_right[0],box[1]])

            if len(boundary)==0 and up_updated==False and down_updated==False:
                break
            dist=[[manhattan_distance(point,box),point] for point in boundary+[up]+[down]]
            k_points+=k_search(k-present_k,dist,grid_dictionary)
            present_k+=len(k_points)
        
            
        KNN[tuple(box)]=k_points
    if flag==0:

        KNN=Probabilistic_KNN(k,KNN,grid_dictionary,gamma,0)
        
    if flag==1:

        KNN=Probabilistic_KNN(k,KNN,grid_dictionary,gamma,1)

    return KNN


'''
#if __name__=='__main__':
    # point_dict={(2,2):[1],(1,3):[0],(2,4):[],(3,3):[],(4,4):[]}
    # point_dict={(2,2):[1],(1,3):[0],(2,4):[1],(3,3):[1],(4,4):[0]}

grid_dictionary={(4,2):[0],(5,3):[],(4,3):[1],(3,3):[],(6,4):[],(5,4):[],(4,4):[],(3,4):[],(2,4):[0],(5,5):[0],(4,5):[0],(3,5):[1],(4,6):[0]}
positive=[[1,(4,3)],[2,(3,5)]]
negative=[[1,(4,5)],[2,(4,6)],[2,(5,5)],[2,(4,2)],[2,(2,4)]]
# print(k_search(1,points,point_dict))
# print(factorial(5))
# print(combination_calc(96,3))
# #print("|{}|".)
# print(binomial_distribution(7,[[1],[3],[4]],[[1],[2],[5],[6]],0.9))
# print(sampler(3,3,points,[0,1]))
KNN={(4,4):[[1,(4,3)],[2,(3,5)],[2,(4,6)],[2,(5,5)],[2,(4,2)],[2,(2,4)]]}
# print(KNN)
points_dict={0:[1,2,2,3],1:[1,1,1,2]}
# print(Probabilistic_KNN(7,KNN,grid_dictionary,0.9))
# print(sigmoid(0.458))
temp=weight_assigner(points_dict,[0,1])
#print(temp[0],temp[1])
#print(sigmoid(-1))
        
'''
