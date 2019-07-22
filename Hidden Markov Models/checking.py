import numpy as np

event_sequence =['Rainy','Rainy','not_Rainy','not_Rainy']	#EXPECTED	#from sampling

fbwd = [[0.647, 0.353], [0.867, 0.133], [0.2, 0.8],[0.3,0.6]]			#from backward



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



def max_events(fbwd):
    generated = []
    for i in range(len(fbwd)):
        
        if (fbwd[i][0]>=fbwd[i][1]):
            generated.append('Rainy')
        else:
            generated.append('not_Rainy')
    return generated
     



def example1():
    max_events(fbwd)
#example1()

def example():
	gen = max_events(fbwd)
	matching(gen,event_sequence)
example()










