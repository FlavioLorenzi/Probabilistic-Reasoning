'''
Created on 4 feb 2019

@author: Flavio Lorenzi

'''
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging.config
import math
import pkg_resources
import numpy as np
import gym
from gym import error, spaces, utils
from gym.utils import seeding
import random

"""
        The agent takes a step in the environment.
        -------
        Input parameters:
        action : int[0,4]
        -------
        Output parameters:
        ob, reward, episode_over: tuple
            ob (object) :
                an environment-specific object representing your observation of
                the environment.
            reward (float) :
                amount of reward achieved by the previous action. The scale
                varies between environments, but the goal is always to increase
                your total reward.
            episode_over (bool) :
                whether it's time to reset the environment again. Most (but not
                all) tasks are divided up into well-defined episodes, and done
                being True indicates the episode has terminated. (For example,
                perhaps the pole tipped too far, or you lost your last life.)
        -------
            
"""
class myPacManEnv(gym.Env):
    
    metadata = {'render.modes': ['human']}

    """
    Define a simple PacMan-grid environment.
    The environment defines which actions can be taken at which point and
    when the agent receives which reward.
    """
    
    def __init__(self):
        
        self.__version__ = "0.0.1"
        logging.info("myPacManEnv - Version {}".format(self.__version__))

        # Grid dimensions
        self.width = 10
        self.height = 10
        self.walls = myPacManEnv.generate_walls(self)
        
        # Pacman initial position
        self.x = 1
        self.y = 1
        
        # General variables defining the environment
        self.TOTAL_TIME_STEPS = 5
        self.curr_step = 0
        self.reward = 0
        self.is_dead = False 
        # Initial position of Pacman in the 2D World
        
        # Define how many actions the agent can do
        self.action_space = spaces.Discrete(4)
        
        # Define what the observation is like
        self.observation_space = [self.x, self.y, self.is_dead]
        
    def step(self, action):
        
        self.curr_step += 1 
        self._take_action(action)

        reward = self.reward + 1
        
        ob = self._get_state()
        return ob, reward, self.is_dead

    def _get_state(self):
        """Get the observation."""
        ob = [self._getx(), self._gety(), self.is_dead] # self.getX , self.getY , self.getCurrStep
        return ob
    
    def _getx(self):

        """Get the position X."""
        return (self.observation_space[0])
    
    def _gety(self):

        """Get the position Y."""
        return (self.observation_space[1])
    
    def _take_action(self, action):
        
        death = myPacManEnv.check4ghosts(self)

        if death:
            self.is_dead = True
        
        # Calcolo degli step rimanenti
        remaining_steps = ( self.TOTAL_TIME_STEPS - self.curr_step ) 
        time_is_over = (remaining_steps <= 0)
        
        # In caso di time_over Pacman muore
        throw_away = time_is_over and not self.is_dead
        if throw_away:
            self.is_dead = True
        
        ''' 
        calcolo della posizione
        '''
        px = self.x
        py = self.y
        
        if action == 0:
            # RIGHT
            px+=1
        if action == 1:
            # LEFT
            px-=1
        if action == 2:
            # UP
            py+=1
        if action == 3:
            # DOWN
            py-=1
        
        # CONTROLLO BORDI 
        (px,py) = myPacManEnv.check4borders(self,px,py)
        
        if not(myPacManEnv.is_on_wall(self,px,py)):
        # AGGIORNO x,y e observation space se non sono sui muri
            self.x = px
            self.y = py
        
        self.observation_space = [self.x,self.y,self.is_dead] 

    def reset(self):
        print("\nReset")
        """
        Reset the state of the environment and returns 
        the initial observation of the space.
        """
        self.curr_step = 0
        self.is_dead = False
        self.reward = 0.0
        
        self.x = 5
        self.y = 3
        
        # 4 Ghots random position generation
        self.ghost1 = myPacManEnv.generate_ghost(self)
        self.ghost2 = myPacManEnv.generate_ghost(self)
        self.ghost3 = myPacManEnv.generate_ghost(self)
        self.ghost4 = myPacManEnv.generate_ghost(self)
        
        return [self.x,self.y,self.is_dead]
    
    def check4borders(self,x,y):
        
        if ( x >= self.width - 1 ):
            x = 8
            
        if ( x < 1 ):
            x = 1
            
        if ( y >= self.width -1  ):
            y = 8
        
        if ( y < 1 ):
            y = 1
        
        return (x,y)
        
    def generate_ghost(self):
        # Generate ghost in random position
        gx = random.randint(2,7) 
        gy = random.randint(2,7)
        ghost = [gx,gy]
        
        while (not(ghost in self.walls)):
            return ghost
    
    def check4ghosts(self):
        # if Pacman position == ghost position -> death = true
        pos = [self.x,self.y]
        return (    (pos==self.ghost1) or (pos==self.ghost2) or (pos==self.ghost3) or (pos==self.ghost4)  )
    
    def generate_walls(self):
        # walls are generated like sequence of map-points not accessibles like [XXXXX]
        walls = [[4,3],[4,4],[4,5],[6,2],[7,2]]
        return walls
        
    def is_on_wall(self,x,y):
        pos = [x,y]
        # if pos belogs in walls -> return true
        return pos in self.walls




        
