import numpy as np


event_sequence =['Rainy','NotRainy','Rainy','NotRainy','NotRainy']
expected_sequence = ['Rainy','NotRainy','Rainy','NotRainy','Rainy']


# metodo che 
#1) confronta due output : event_sequence (from direct_sampling) e expected_sequence (from max events)
#2) compara le stringhe e ritorna la probabilità del matching

def matching(expected,event):

	percentage = 0

	for i,j in zip(expected,event):
		
		if (i==j):
			percentage += 100			


	percentage_tot = percentage/len(expected)

	print ("LA PERCENTUALE DI MATCHING E' ",percentage_tot,"%")

	if(percentage_tot<=30):
		print("NOT GOOD")
	if(percentage_tot>30) & (percentage_tot<=75):
		print("WE CAN DO BETTER!!!")
	if(percentage_tot>75):
		print("GOOD")
	if(percentage_tot==100):
		print("OPTIMAL")

def example():
    matching(expected_sequence,event_sequence)
example()









