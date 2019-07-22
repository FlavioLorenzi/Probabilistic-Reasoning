import numpy as np


fbwd = [[0.647, 0.353], [0.867, 0.133], [0.2, 0.8]]

#metodo che confronta le prob del fwbd,prende il più grande e restituisce una stringa in lista 

def max_events(fbwd):
    expected_sequence = []
    for i in range(len(fbwd)):

        #x = max(fbwd[i][0],fbwd[i][1])
        
        if (fbwd[i][0]>fbwd[i][1]):
            expected_sequence.append('Rainy')
        else:
            expected_sequence.append('NotRainy')
    print(expected_sequence)

def example():
    max_events(fbwd)
example()



