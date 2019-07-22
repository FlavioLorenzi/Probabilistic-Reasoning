'''
Created on 5 feb 2019

@author: Michele Ciciolla
'''

def generate_walls():
        # walls are generated like sequence of map-points not accessibles like [XXXXX]
        walls = [[4,3],[4,4],[4,5],[6,2]]
        pos = [4,5]
        # if pos belogs in walls -> return true
        print(pos in walls)

generate_walls()