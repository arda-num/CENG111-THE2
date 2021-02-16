# Arda Numanoglu METU 

import math
import random
from evaluator import *    

def new_move():
	
	status = new_infection_status()
	global current_universal_state
	coordinate = status[1]
	movements = new_moveof_individuals
	new_universal_state = list()

	lst = list()
	for stat in status[0]: #status control
		if(stat[2] == "infected"):
			lst.append(stat[3])   #appending the index of new_infected individual

	i = 0
	while i < number_of_individuals:
		if( current_universal_state[i][0] == tuple(coordinate[i]) ): # if an individual did not move this statement is True
			if(i in lst):
				new_universal_state.append([tuple(coordinate[i]),current_universal_state[i][1],current_universal_state[i][2],"infected"])
			else:
				new_universal_state.append([tuple(coordinate[i]),current_universal_state[i][1],current_universal_state[i][2],current_universal_state[i][3]])
		else:

			if(i in lst):
				new_universal_state.append([tuple(coordinate[i]),movements[i],current_universal_state[i][2],"infected"])
			else:
				new_universal_state.append([tuple(coordinate[i]),movements[i],current_universal_state[i][2],current_universal_state[i][3]])

		i += 1
		
	current_universal_state = new_universal_state # saves the new universal state
	
	return new_universal_state # returns [(x,y), last_move, mask_status, infection_status]


	
	

def move_decision_maker(): # a function which determines the next move of the individuals and put them on a list
	global new_moveof_individuals
	lstmove = list()
	for indiv in current_universal_state:
		lstmove += [indiv[1]]
		
	i = 0
	lst = list()
	probabilities = [prob[0],prob[1],prob[2],prob[3],prob[4],prob[3],prob[2],prob[1]]
	while i < number_of_individuals :
		

		if(lstmove[i] == 0):
			movements = [0,1,2,3,4,5,6,7]
			lst += random.choices(movements, weights= probabilities, k=1) # returns LIST!
			
		elif(lstmove[i] == 1):
			movements = [1,2,3,4,5,6,7,0]
			lst += random.choices(movements, weights= probabilities, k=1)
			
		elif(lstmove[i] == 2):
			movements = [2,3,4,5,6,7,0,1]
			lst += random.choices(movements, weights= probabilities, k=1)
			
		elif(lstmove[i] == 3):
			movements = [3,4,5,6,7,0,1,2]
			lst += random.choices(movements, weights= probabilities, k=1)
			
		elif(lstmove[i] == 4):
			movements = [4,5,6,7,0,1,2,3]
			lst += random.choices(movements, weights= probabilities, k=1)
			
		elif(lstmove[i] == 5):
			movements = [5,6,7,0,1,2,3,4]
			lst += random.choices(movements, weights= probabilities, k=1)
			
		elif(lstmove[i] == 6):
			movements = [6,7,0,1,2,3,4,5]
			lst += random.choices(movements, weights= probabilities, k=1)

		elif(lstmove[i] == 7):
			movements = [7,0,1,2,3,4,5,6]
			lst += random.choices(movements, weights= probabilities, k=1)	

		i += 1
	new_moveof_individuals = lst	
	return lst # returns [x,x,x,x,x,x,x,...] x is a number between 0-7 which represent the intended moves of individuals



def infection_probability():  # compares the individuals distance and choose the ones who have a chance to get infected.
	
	lstof_coordinates = new_coordinates()
	listof_probabilities = list()
	i = 0
	counter1 = -1
	counter2 = 0
	for indiv1 in lstof_coordinates:
		i += 1
		counter1 += 1
		listof_probabilities_per_indiv = list()
		for indiv2 in lstof_coordinates[i:]:
			counter2 += 1
			
			distance = math.sqrt( (indiv2[1]-indiv1[1])**2 + (indiv2[0]-indiv1[0])**2 )
			if( distance <=  D): 
				listof_probabilities += [[counter1,counter2,min(1,K/(distance**2))]]  	
		counter2 = 0	
	return listof_probabilities,lstof_coordinates # returns the interactions which may cause contamination and convey the coordinates taken from new_coordinates() as it is. For instance, [[index1,index2-index1,possibility],...],[[x0,y0],[x1,y1],[x2,y2],...]



def new_coordinates(): # adjust the new coordinates through the information that takes from move_decision_maker()
	all_coordinates = list()
	
	for elements in current_universal_state:
		all_coordinates += elements[0]
	
	x_coordinates = list()
	y_coordinates = list()
	
	new_list = list()

	i = 0
	while i < (number_of_individuals*2)-1:
		x_coordinates += [all_coordinates[i]]
		i += 2
	k = 1
	while k < number_of_individuals*2:
		y_coordinates += [all_coordinates[k]]
		k += 2
	
	for elem in x_coordinates:
		new_list.append([elem])

	g = 0
	for elem in y_coordinates:
		new_list[g].append(elem)
		g += 1


	l = 0
	
	for movement in move_decision_maker():  #  new coordinates are generated here
		
		if(movement == 0):
			
			if(  ([x_coordinates[l],y_coordinates[l]+1] not in new_list)  and  (0 <= y_coordinates[l]+1 < M)   ): # if the new coordinate is not already taken from smo else OR is not outside of the boundary this statement is TRUE.
																												
				y_coordinates[l] += 1
				
				new_list[l] = [x_coordinates[l],y_coordinates[l]]
			l += 1
			
		elif(movement == 1):
			if(  ([x_coordinates[l]-1,y_coordinates[l]+1] not in new_list)  and  (0 <= x_coordinates[l]-1 < N) and (0 <= y_coordinates[l]+1 < M)   ):
				y_coordinates[l] += 1
				x_coordinates[l] -= 1
				
				new_list[l] = [x_coordinates[l],y_coordinates[l]]
			l += 1
			
		elif(movement == 2):
			if(  ([x_coordinates[l]-1,y_coordinates[l]] not in new_list)  and (0 <= x_coordinates[l]-1 < N)   ):
			
				x_coordinates[l] -= 1
				
				new_list[l] = [x_coordinates[l],y_coordinates[l]]
			l += 1
			
			
		elif(movement == 3):
			if(  ([x_coordinates[l]-1,y_coordinates[l]-1] not in new_list) and (0 <= y_coordinates[l]-1 < M) and (0 <= x_coordinates[l]-1 < N )  ):
				y_coordinates[l] -= 1
				x_coordinates[l] -= 1
				
				new_list[l] = [x_coordinates[l],y_coordinates[l]]
			l += 1
		elif(movement == 4):
			if(  ([x_coordinates[l],y_coordinates[l]-1] not in new_list)  and  (0 <= y_coordinates[l]-1 < M)   ):
				y_coordinates[l] -= 1
				
				new_list[l] = [x_coordinates[l],y_coordinates[l]]
			l += 1
		elif(movement == 5):
			if(  ([x_coordinates[l]+1,y_coordinates[l]-1] not in new_list) and (0 <= y_coordinates[l]-1 < M) and (0 <= x_coordinates[l]+1 < N)   ):
				y_coordinates[l] -= 1
				x_coordinates[l] += 1
				
				new_list[l] = [x_coordinates[l],y_coordinates[l]]
			l += 1
			
		elif(movement == 6):
			if(  ([x_coordinates[l]+1,y_coordinates[l]] not in new_list)  and (0 <= x_coordinates[l]+1 < N)   ):
			
				x_coordinates[l] += 1
				
				new_list[l] = [x_coordinates[l],y_coordinates[l]]
			l += 1
		elif(movement == 7):
			if(  ([x_coordinates[l]+1,y_coordinates[l]+1] not in new_list) and (0 <= y_coordinates[l]+1 < M) and (0 <= x_coordinates[l]+1 < N )  ):
				y_coordinates[l] += 1
				x_coordinates[l] += 1
				new_list[l] = [x_coordinates[l],y_coordinates[l]]
			l += 1
			

		a = 0
		lstof_coordinates = list()
	while a < number_of_individuals:
		lstof_coordinates += [[x_coordinates[a]] + [y_coordinates[a]]]
		a += 1
	
	
	return lstof_coordinates # returns [[x0,y0],[x1,y1],[x2,y2],...]




def new_infection_status(): # adjust the new infection status through the information that takes from infection_probability()
	lst = infection_probability()
	result = list()
	lst2 = ["infected","notinfected"]
	for case in lst[0]:  
		if( current_universal_state[case[0]][3] == "notinfected" and current_universal_state[case[0]+case[1]][3] == "infected" ):
			
			if( current_universal_state[case[0]][2] == "masked" and current_universal_state[case[0]+case[1]][2] == "masked" ):
				result += [case[:2] + random.choices(lst2, weights = [case[2]/LAMBDA**2, 1-case[2]/LAMBDA**2],k=1)+[case[0]]]
			elif( current_universal_state[case[0]][2] == "masked" or current_universal_state[case[0]+case[1]][2] == "masked" ):
				result += [case[:2] + random.choices(lst2, weights = [case[2]/LAMBDA, 1-case[2]/LAMBDA],k=1)+[case[0]]]
			else:
				result += [case[:2] + random.choices(lst2, weights = [case[2], 1-case[2]],k=1)+[case[0]]]
		
		elif( current_universal_state[case[0]][3] == "infected" and current_universal_state[case[0]+case[1]][3] == "notinfected" ):
			
			if( current_universal_state[case[0]][2] == "masked" and current_universal_state[case[0]+case[1]][2] == "masked" ):
				result += [case[:2] + random.choices(lst2, weights = [case[2]/LAMBDA**2, 1-case[2]/LAMBDA**2],k=1)+[case[0]+case[1]]]
			elif( current_universal_state[case[0]][2] == "masked" or current_universal_state[case[0]+case[1]][2] == "masked" ):
				result += [case[:2] + random.choices(lst2, weights = [case[2]/LAMBDA, 1-case[2]/LAMBDA],k=1)+[case[0]+case[1]]]
			else:
				result += [case[:2] + random.choices(lst2, weights = [case[2], 1-case[2]],k=1)+[case[0]+case[1]]]
	return result , lst[1]	# returns the changes in infection and conveys the coordinates. For instance, [[indiv1,indiv2,"infected" or "notinfected",index of the indiv which is affected. ],...],[[x0,y0],[x1,y1],[x2,y2],...]





""" GLOBAL VARIABLES """
current_universal_state = get_data()[6]  # taking the current universal_state from get_data()

constants = get_data()[:6]  # getting the constants seperated from get_data()
M = constants[0]
N = constants[1]
D = constants[2]
K = constants[3]
LAMBDA = constants[4]
mu = constants[5]

number_of_individuals = len(current_universal_state)
new_moveof_individuals = None
prob = [mu/2 ,mu/8 , (1-mu-mu**2)/2 , (mu**2)*2/5 , (mu**2)/5] # setting the colors's associated probabilities

""" Please do not leave any printing function here during the evaluation process ,since it causes different movements. """
