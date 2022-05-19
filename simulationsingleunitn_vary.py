# -*- coding: utf-8 -*-
"""SimulationSingleUnitn-vary.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-O_RxLJqpuSKnAr8HZ5TKvCzLUiJr3EU
"""

import numpy as np
import pickle
import matplotlib.pyplot as plt
import math
import random

def minknapsack_algo(cost,probability,n,D,C):
    outputreal=np.zeros(n)
    small_set_real=[]
    big_set_real=[]
    lst=np.zeros(n)
    for i in range(n):
        x = (C*(1-probability[i])+cost[i])
        # x=probability[i]/cost[i];
        # x = C*probability[i]
        lst[i]=x
    sorted_index = np.argsort(lst)

    small = []
    iSmall=0
    tempSmall=[]
    big = []
    iBig=0
    tempBig=[]
    probSum=0
    checkSmallFirst = 0 # 0 nothing, 1 small set 
    #Finding big and small sets
    for i in sorted_index:
        if(probSum + probability[i]< D):
            bl=True
            tempSmall.append(i)
            probSum = probSum+probability[i]
        else:
            bl=False
            tempBig.append(i)
        if bl==False:
            if(len(tempSmall)!=0):
                small.append(tempSmall)
                iSmall=iSmall+1
            tempSmall=[]
        else:
            if(len(tempBig)!=0):
                big.append(tempBig)
                iBig=iBig+1
            tempBig=[]

    if bl==False:
        if(len(tempBig)!=0):
            big.append(tempBig)
    else:
        if(len(tempSmall)!=0):
            small.append(tempSmall)
    for sm in small:
      for sm_temp in sm :
        outputreal[sm_temp]=1
    
    #finding the set of elements of small and big 
    #s_1 U s_2......U s_k U {i} where i belongs to b_k for which compute function is minimum
    
    sum_cost = 0
    for i in range(n):
      sum_cost = sum_cost + cost[i]
    
    sum2 = 0
    sum3 = 0
    for i in range(n):
         #if(selected_set[i] > 0):
             #sum_prob = sum_prob + probability[i]
         sum2 = sum2 + probability[i]*(1-probability[i])
         sum3 = sum3 + cost[i]*probability[i]
    mini =  C*sum2 + sum3
    #if len of small  set is greater length of big set first consider one element of small set 
    #and iterate over specific index of big set 
    sm_temp=[]
    output_real1=np.zeros(n)
    i=0
    for sm in small: #if small is [[1,2],[4,5]] then sm is [1,2]
      sm_temp=sm_temp+sm#sm_temp will is a list which is collection of all small elements till ith index
      if(i==len(big)):
        break
      for bm in big[i]: # if big is [[1,2],[3,4]] then big[0] is [1,2] and bm is 1
        output_tempo=np.zeros(n)
        output_tempo[bm]=1
        for sm1 in sm_temp:#for all 
          output_tempo[sm1]=1#value of output_tempo[i] is 1 if ith agent is present in selected set
        ans=compute_objective1(cost, probability, n, D, C, output_tempo)#getting compue function value for selected set
        if(mini>ans):#if mini so far greater than ans now obtained change min and real_output
          mini=ans
          output_real1=output_tempo
          small_set_real=[]
          big_set_real=[]
          for sm1 in sm_temp:
            small_set_real.append(sm1)
          big_set_real.append(bm)
      i+=1

    if(len(big)!=0 and len(small)!=0):
      return (mini,output_real1,small_set_real,big_set_real)#return minimum value obtained 

    return (mini,output_real1,small_set_real,big_set_real)#return minimum value obtained

def aaai_algo(cost, probability, n, D, C):
    output = np.zeros(n)
    pot_cost = np.zeros(n)
    for i in range(n):
        pot_cost[i] = C*probability[i] - cost[i]/2
    sorted_index = np.argsort(-pot_cost)
    sum1 = 0
    #print(sorted_index)
    for i in sorted_index:
        if(cost[i]/2 < C*(-sum1+D-1/2)):
            output[i] = 1
            sum1 = sum1 + probability[i]

        val = compute_objective(cost, probability, n, D, C, output)

    return (val,output)

def compute_objective1(cost, probability, n, D, C, selected_set):
     #sum_prob = 0
     sum2 = 0
     sum3 = 0
     for i in range(n):
         if(selected_set[i] > 0):
             #sum_prob = sum_prob + probability[i]
             sum2 = sum2 + probability[i]*(1-probability[i])
             sum3 = sum3 + cost[i]*probability[i]
     obj =  C*sum2 + sum3
     return obj

def compute_objective(cost, probability, n, D, C, selected_set):
     sum_prob = 0
     sum2 = 0
     sum3 = 0
     for i in range(n):
         if(selected_set[i] > 0):
             sum_prob = sum_prob + probability[i]
             sum2 = sum2 + probability[i]*(1-probability[i])
             sum3 = sum3 + cost[i]*probability[i]
     obj =  C*sum2 + sum3 + C*(D-sum_prob)**2
     return obj
   
def optimal(cost, probability, n, D, C):
    sum_cost = 0
    for i in range(n):
      sum_cost = sum_cost + cost[i]
    min_obj = C*(D**2)
    output = np.zeros(n)
    set_result=[]
    for i in range(2**n):
        string = bin(i)[2:].zfill(n)
        arr = [int(x) for x in tuple(string)]
        obj = compute_objective(cost, probability, n, D, C, arr)
        if(obj < min_obj):
            # print("aaaaaaaaa")
            min_obj = obj
            output = arr
    for i in range(n):
      if(output[i]==1):
        set_result.append(i)
    ans=compute_objective(cost, probability, n, D, C,output)
    return (ans,set_result)
    

num_samples = int(input("number of samples"))
#D = float(input("Demand shortage"))
C = float(input("Cost for buying electricity"))
c_max = float(input("max cost of the customer"))
avg_ratioyx = np.zeros(4)
worst_ratioyx = np.zeros(4)

avg_ratiozx = np.zeros(4)
worst_ratiozx = np.zeros(4)

num_agents = [500, 1000, 1500, 2000]

index = 0
maxwa = 0
avg_y = np.zeros(4)
worst_y = np.zeros(4)

avg_x = np.zeros(4)
worst_x = np.zeros(4)

avg_z = np.zeros(4)
worst_z = np.zeros(4)
for n in num_agents:
    for samples in range(num_samples):
        # print(n,samples)
        D = random.randint(2, math.ceil(n/4))
        # D = (n/4)*np.random.rand()
        cost = c_max*np.random.rand(n,1)
        probability = np.random.rand(n,1)
        # (output,ans,selected_set_by_myalgo)=my_algo(cost,probability,n,D,C)
        # print("The set returned by papers algorithm:")
        # print(selected_set_by_myalgo);

        sum_prob = 0
        for p in probability:
          sum_prob += p
        
        y=0
        if sum_prob<D:
          output_set_minknapsack = np.ones(n)
          y=compute_objective(cost, probability, n, D, C, output_set_minknapsack)
          print("aka....................................................................................")
        else:
          (y,output_set_minknapsack,smallset,bigset)=minknapsack_algo(cost, probability, n, D, C)# take return as the minimum value obtained 
        
        # (x,optimal_set_output)=optimal(cost, probability, n, D, C)

        (z,aaai_set_output)=aaai_algo(cost, probability, n, D, C)

        sum_prob_y = 0
        for i in range(n):
          if output_set_minknapsack[i] >0:
            sum_prob_y+=probability[i]

        # sum_prob_x = 0
        # for i in optimal_set_output:
        #   sum_prob_x+=probability[i]

        # print('sum_prob_optimal - D')
        # print(sum_prob_x-D)
        print('sum_prob_minknapsack - D')
        print(sum_prob_y-D)

        # ratioyx = y/x
        # ratiozx = z/x
        # print("y:")
        # print(y)
        # print("x:")
        # print(x)
        print("The selected set by my algorithm ")
        print(output_set_minknapsack)
        # print("The selected set by optimal algorithm ")
        # print(optimal_set_output)
        
        # avg_ratioyx[index] = avg_ratioyx[index] + ratioyx
        # avg_ratiozx[index] = avg_ratiozx[index] + ratiozx

        avg_y[index] = avg_y[index] + y
        # avg_x[index] = avg_x[index] + x
        avg_z[index] = avg_z[index] + z        


        # if ratioyx > worst_ratioyx[index]:
        #     worst_ratioyx[index] = ratioyx
        # if ratiozx > worst_ratiozx[index]:
        #     worst_ratiozx[index] = ratiozx
        if y > worst_y[index]:
            worst_y[index] = y
        # if x > worst_x[index]:
        #     worst_x[index] = x
        if z > worst_z[index]:
            worst_z[index] = z
    index = index+1
# avg_ratioyx = avg_ratioyx/num_samples
# avg_ratiozx = avg_ratiozx/num_samples
# avg_x = avg_x/num_samples
avg_y = avg_y/num_samples
avg_z = avg_z/num_samples
pickle_out = open("worst_minknapsack_offline.pickle","wb")
pickle_out1 = open("worst_GLS_offline.pickle","wb")
pickle.dump(worst_y, pickle_out)
pickle.dump(worst_z, pickle_out1)

# plt.plot(num_agents,avg_x,'g', label='optimal algorithm') #optimal
# plt.plot(num_agents,worst_x,'y', label='worst_x') 

# plt.plot(num_agents,avg_y,'c', label='minknapsack') #minknapsack
plt.plot(num_agents,worst_y,'r', label='minknapsack')

# plt.plot(num_agents,avg_z,'k', label='GLS algorithm') #aaai
plt.plot(num_agents,worst_z,'b', label='GLS algorithm')

plt.legend(loc='upper left')
plt.xlabel('Number of agents')
plt.ylabel('Loss function value')
plt.savefig('offline_comparisonVaryNLoss.png')
plt.show()

# a=np.array([1,2,3])
# b=a
# a[0]=2
# print(b)
# a=np.zeros(3)
# print(b)

# # plt.plot(num_agents,avg_ratioyx,'c', label='avg_ratio(min-knapsack)') #minknapsack
# plt.plot(num_agents,worst_ratioyx,'m', label='worst_ratio(min-knapsack)')

# # plt.plot(num_agents,avg_ratiozx,'k', label='avg_ratio(GLS)') #aaai
# plt.plot(num_agents,worst_ratiozx,'b', label='worst_ratio(GLS)')

# plt.legend(loc='upper left')
# plt.xlabel('Number of agents')
# plt.ylabel('Ratio with optimal algorithm')
# plt.savefig('offline_comparisonVaryNRatio.png')
# plt.show()