'''
Created on 5 feb 2019

@author:Flavio Lorenzi
'''
import gym
import gym_foo

'''
PACMAN WORLD is represented like a grid 10x10, Pacman starts at (5,3), 
walls are position-fixed and 4 ghosts spawn randomly at the start

this is an example: https://mega.nz/#!VcVWFIJK!jacLCsUOfp69clriJRRezobtwxN1OeQG0rsbKTM3Ph4

'''
env = gym.make('myPacman-v0')
observation = env.reset()

print("OBSERVATION = [ pacman_x , pacman_y , episode_terminated ]")
print("INITIAL OBSERVATION ( 0 ) = ",observation)
print()

# for i in range(0,10):
# observation = env.reset()
for t in range(5):
    # env.render()
    action = env.action_space.sample()
    observation, reward, done = env.step(action)
    print("CURRENT OBSERVATION (",t+1,") = ",observation)
    
    if done:
        print("\nEpisode finished after {} timesteps".format(t+1))
        break
