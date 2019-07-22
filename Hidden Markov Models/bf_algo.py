
import numpy as np

init_p = np.array([0.5, 0.5])

transmat = np.array([[0.7, 0.3],
                    [0.3, 0.7]])

emissionprob = np.array([[0.9, 0.1],
                        [0.2, 0.8]])

senmod_U = np.array([[0.9 , 0.0],
                    [0.0 , 0.2]])

senmod_NU = np.array([[0.1 , 0.0],
                    [0.0 , 0.8]])

fin_b = np.array([1, 1])

# list [] ,tuple ()
observed = ['take_Umbrella', 'take_Umbrella', 'not_take_Umbrella','take_Umbrella','take_Umbrella']

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
            b_curr_not_normalized = transmat @ sens_mod @ b_prev
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
    
    elem = obs[cont]
    
    if elem == ('take_Umbrella'):
        return senmod_U
    else:
        return senmod_NU
       
def example():
    fwd = forward(observed, transmat, init_p)
    bwd = backward(observed, transmat, fin_b)
    fbwd = smoothing(fwd, bwd, init_p,fin_b)
    print("forward-backward sequence:")
    print(fbwd)
    
example()
