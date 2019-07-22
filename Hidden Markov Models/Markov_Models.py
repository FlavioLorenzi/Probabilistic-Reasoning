'''
Created on 10 gen 2019

version 2.1

@author: Michele Ciciolla e Flavio Lorenzi
'''

import numpy as np
import random

states = ( 'Rainy' , 'not_Rainy' )

start_probability = {'Rainy': 0.5,
                     'not_Rainy': 0.5}

transition_probability = {
   'Rainy' : {'Rainy': 0.7, 'not_Rainy': 0.3},
   'not_Rainy' : {'Rainy': 0.3, 'not_Rainy': 0.7},
   }

observations = ( 'take_Umbrella', 'not_take_Umbrella' )
 
emission_probability = {
   'Rainy' : {'take_Umbrella': 0.9, 'not_take_Umbrella': 0.1},
   'not_Rainy' : {'take_Umbrella': 0.2, 'not_take_Umbrella': 0.8},
   }


# REFACTORED DATA USED IN FORWARD-BACKWARD algo 
init_p = np.array([0.5, 0.5])
fin_b = np.array([1, 1])
transmat = np.array([[0.7, 0.3],
                    [0.3, 0.7]])
emissionprob = np.array([[0.9, 0.1],
                        [0.2, 0.8]])



def direct_sampling( obs, states, start_p,trans_p, emit_p ):
    
    event_sequence = []
    observation_sequence = [] 
    cont = 0
    
    while True:
        # start probability R = < 0.7 , 0.3 >
        if cont == 0 :
            n = random.uniform( 0, 1 )
            if n <= start_p['Rainy']:
                state = states[0]
            else:
                state = states[1]
        else:
            n = random.uniform( 0, 1 )
            if n <= (trans_p[last_event]).__getitem__('Rainy'): 
                state = 'Rainy'
            else:
                state = 'not_Rainy'
                
        # last event is saved       
        last_event = state
        
        if n <= (emit_p[state]).__getitem__('take_Umbrella'):
            observation = obs[0]
        else:
            observation = obs[1]
        #print( "%s : state is  ( %s ) , observation is ( %s )" % ( cont, state, observation ) )
        
        (event_sequence,observation_sequence) = storage(state,observation,event_sequence,observation_sequence)
        
        cont += 1
        
        if cont == 20:  # 20 iterations is when cont = 21
            break
    
    
    # print("Direct Sampling completed")   
    # print(event_sequence)
    # print(observation_sequence)
    return (observation_sequence,event_sequence)

def storage(state,observation,es,os):
    # inserisce state nella lista es
    # inserisce observation nella lista os
   
    es.append(state)
    os.append(observation)

    return es,os

def forward(observed, transmat, init_p):
    # output list of likely of events
    fwd = []
    # previous forward output 
    f_prev = {}
    # element used in process
    for i in range(0, len(observed)):
        f_curr = {}
        f_curr_not_normalized = {}
        if i==0:
            # initial case
            sens_mod = (check_sens_mod(observed, i))
            f_curr_not_normalized = sens_mod @ transmat @ init_p
            f_curr = normalize(f_curr_not_normalized)
            
        else:
            # other cases
            sens_mod = (check_sens_mod(observed,i))
            f_curr_not_normalized = sens_mod @ transmat @ f_prev
            f_curr = normalize(f_curr_not_normalized)
            
        fwd.append(f_curr)
        f_prev = f_curr
        
    return fwd

def util_forward(observed, transmat, init_p):           
    # method used in upgraded_forward_backward to get last event forward likehood
    # previous forward output 
    f_prev = {}
    # element used in process
    for i in range(0, len(observed)):
        f_curr = {}
        f_curr_not_normalized = {}
        if i==0:
            # initial case
            sens_mod = (check_sens_mod(observed, i))
            f_curr_not_normalized = sens_mod @ transmat @ init_p
            f_curr = normalize(f_curr_not_normalized)
            
        else:
            # other cases
            sens_mod = (check_sens_mod(observed,i))
            f_curr_not_normalized = sens_mod @ transmat @ f_prev
            f_curr = normalize(f_curr_not_normalized)
            
        f_prev = f_curr
        
    return f_prev

def backward(observed, transmat, fin_b):   
    
    observed = list(reversed(observed))
    # output list of likely of events
    bwd = []
    # previous forward output 
    b_prev = {}
    # element used in process
    for i in range(0, len(observed)):
        b_curr = {}
        b_curr_not_normalized = {}
        
        if i==0:
            # initial case
            sens_mod = (check_sens_mod(observed, i))
            b_curr_not_normalized = transmat @ sens_mod @ fin_b
            b_curr = normalize(b_curr_not_normalized)
                
        else:
            # other cases
            sens_mod = (check_sens_mod(observed,i))
            b_curr_not_normalized = transmat @ sens_mod@ b_prev
            b_curr = normalize(b_curr_not_normalized)
                
        # put b_curr inside bwd list
        bwd.append(b_curr)
        b_prev = b_curr
        
    return bwd

def smoothing(fwd,bwd,init_p,fin_b):
    
    bwd = list(reversed(bwd))
    fbwd = []
    
    for i in range(0,len(fwd)+1):
        s_curr = {}
        s_curr_not_normalized = {}
        
        if i==0:
            s_curr_not_normalized = init_p*bwd[i]
            s_curr = normalize(s_curr_not_normalized)
        
        elif i==(len(fwd)):
            s_curr_not_normalized = fwd[(i-1)]*fin_b
            s_curr = normalize(s_curr_not_normalized)
        
        else:
            s_curr_not_normalized = fwd[(i-1)]*bwd[i]
            s_curr = normalize(s_curr_not_normalized)
   
        fbwd.append(s_curr)
        
    return list(fbwd)
  
def normalize(vector):
    # normalize a given vector
    return (np.round(vector/np.sum(vector),3))

def check_sens_mod(obs,cont):
    # cont < obs.lenght
    # return the appropriate sensor model checking obs current element
    
    sens_mod_umb = np.array([[0.9 , 0.0],
                         [0.0 , 0.2]])

    sens_mod_not_umb = np.array([[0.1 , 0.0],
                          [0.0 , 0.8]])
    
    elem = obs[cont]
    
    if elem == ('take_Umbrella'):
        return sens_mod_umb
    else:
        return sens_mod_not_umb



def upgraded_forward_backward(observed,transmat,init_p,fin_b,f_last):
    
    observed = list(reversed(observed))
    
    ufbwd = []
    
    # previous output 
    b_prev = {}
    f_prev = {}
    
    for i in range(0, len(observed)):
        
        b_curr = {}
        b_curr_not_normalized = {}
        f_curr = {}
        f_curr_not_normalized = {}
        u_curr = {}
        u_curr_not_normalized = {}
        
        sens_mod = (check_sens_mod(observed, i))   #per capire la sensor model da utilizzare con iterazione i

        if i==0:
            # initial case
            b_curr = fin_b
            f_curr = f_last
            # getting u value normalized using f_last * <1.0,1.0>
            u_curr_not_normalized = f_last*fin_b
            u_curr = normalize(u_curr_not_normalized)
            
        
                    
        else:
            # other cases
            
            # getting b value normalized
            b_curr_not_normalized = transmat @ sens_mod @ b_prev    
            b_curr = normalize(b_curr_not_normalized)
            
            # getting f value normalized
            f_curr_not_normalized = get_inv(transmat)@ get_inv(sens_mod)@f_prev    
            f_curr = normalize(f_curr_not_normalized)
            
            # getting u values as f * b
            u_curr_not_normalized = f_curr*b_curr
            u_curr = normalize(u_curr_not_normalized)
        



        # upgrading values    
        b_prev = b_curr
        f_prev = f_curr
        
        # put u_curr inside ufbwd list
        ufbwd.append(u_curr)
    
    if i==(len(observed)):
        # final case 
            
        # getting b value normalized
        b_curr_not_normalized = transmat @ sens_mod @ b_prev
        b_curr = normalize(b_curr_not_normalized)

            
        # getting u values as <0.5,0.5> * b
        u_curr_not_normalized = init_p*b_curr
        u_curr = normalize(u_curr_not_normalized)

    ufbwd.append(u_curr)
    return list(reversed(ufbwd))



def get_inv(matrix):
    det = np.linalg.det(matrix)
    m = matrix/det
    output = np.transpose(m)
    return output




def matching(generated,event):

    percentage = 0

    for i,j in zip(generated,event):
        
        if (i==j):
            percentage += 100       

    percentage_tot = percentage/len(event)

    print ("LA PERCENTUALE DI MATCHING TRA GLI EVENTI E' DEL ",percentage_tot,"%")

    if(percentage_tot<=30):
        print("NOT GOOD")
    if(percentage_tot>30) & (percentage_tot<=75):
        print("WE CAN DO BETTER")
    if(percentage_tot>75)& (percentage_tot<100):
        print("GOOD")
    if(percentage_tot==100):
        print("OPTIMAL")

    return percentage_tot




def max_events(fbwd):
    generated = []
    for i in range(len(fbwd)):
        
        if (fbwd[i][0]>=fbwd[i][1]):
            generated.append('Rainy')
        else:
            generated.append('not_Rainy')
    return generated





def hidden_markov_models():  
    (observed,expected_events) = direct_sampling(observations , states, start_probability, transition_probability, emission_probability )

    fwd = forward(observed, transmat, init_p)
    bwd = backward(observed, transmat, fin_b)
    fbwd = smoothing(fwd, bwd, init_p,fin_b)
    
    print("Forward-Backward sequence:")
    print(fbwd)
    print("\nHow good is the estimate comparing with events_sequence from direct sampling?")

    generated = max_events(fbwd)


    percentage = matching(generated,expected_events)
    return percentage

#hidden_markov_models()





def hidden_markov_models_upgrade():
    (observed,expected_events) = direct_sampling(observations , states, start_probability, transition_probability, emission_probability )
    
    f_last = util_forward(observed, transmat, init_p)
    
    ufbwd = upgraded_forward_backward(observed,transmat,init_p,fin_b,f_last)
    
    print("Upgraded Forward-Backward sequence:")
    print(ufbwd)
    print("\nHow good is the estimate comparing with events_sequence from direct sampling?")

    generated = max_events(ufbwd)
    matching(generated,expected_events)

#hidden_markov_models_upgrade()   
    
    
def media(current):

    for i in range(len(current)):
        result = sum(current)/len(current)
    return result



def performance():
    x = []
    for i in range(0,15):
        percentage = hidden_markov_models()
        x.append(percentage)
    perf = media(x)

    print("LA MEDIA PERCENTUALE DI PERFORMANCE DI 15 SEQUENZE DI LUNGHEZZA 20 E' ",perf)

performance()