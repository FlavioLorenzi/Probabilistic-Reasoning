'''
Created on 5 feb 2019

@author: Lorenzi Flavio
'''

from gym.envs.registration import register

register(
    id='myPacman-v0',
    entry_point='gym_foo.envs:myPacManEnv',
)
