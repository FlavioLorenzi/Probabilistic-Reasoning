'''
version 1.02

Created on 22 gen 2019

@author: Boston Dynamics $$$ FlaMik corporation

'''

#1) HHM

import numpy as np
import random

states = ( 'Rainy' , 'not_Rainy' )
 
last_event = 'Rainy'

observations = ( 'take_Umbrella', 'not_take_Umbrella' )
 
start_probability = {'Rainy': 0.5,
                     'not_Rainy': 0.5}
 
transition_probability = {
   'Rainy' : {'Rainy': 0.7, 'not_Rainy': 0.3},
   'not_Rainy' : {'Rainy': 0.3, 'not_Rainy': 0.7},
   }
 
emission_probability = {
   'Rainy' : {'take_Umbrella': 0.9, 'not_take_Umbrella': 0.1},
   'not_Rainy' : {'take_Umbrella': 0.2, 'not_take_Umbrella': 0.8},
   }





#2)DIRECT SAMPLING ON HMM

def direct_sampling( obs, states, start_p,trans_p, emit_p ):
    
    event_sequence = []
    observation_sequence = []
    cont = 0
    
    while True:
        
        # start probability R = < 0.5 , 0.5 >
        
        
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
        
        
        n = random.uniform( 0, 1 )
        if n <= (emit_p[state]).__getitem__('take_Umbrella'):
            observation = obs[0]
        else:
            observation = obs[1]
        
       
        (event_sequence,observation_sequence) = storage(cont,state,observation,event_sequence,observation_sequence)
        
        cont += 1
        
        
        if cont == 20:  # todo 20 iterations 
            break
        
    print("Event Sequence:  ",event_sequence)
    print("Observation Sequence:  ",observation_sequence)
    print("Tables are updated")
    
    #return last_event,observation_sequence

def storage(cont,state,observation,es,os):          #metodo che aggiorna la nostra "tabella"
  
    es.append(state)
    os.append(observation)

    return es,os




def example():  
    direct_sampling( 
        observations,
        states,
        start_probability,
        transition_probability,
        emission_probability )

example()
