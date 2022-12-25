import sys
import gym
import gym_game
import numpy as np
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env

# Custom Environment
env = make_vec_env("Pygame-v0")

#to Train
# model = PPO("MlpPolicy", env, verbose=1)
# model.learn(total_timesteps=300000)  # Total number of timesteps for training
# model.save("ppo_custom")  # To save the model in a file

# To load the trained model from the file
model = PPO.load("ppo_custom") 

obs = env.reset()
# take action until the game is completed
while True:
    # Using the model, we will predict the best action
    action, _states = model.predict(obs)
    # The action returns obs, rewards, dones, info
    obs, rewards, dones, info = env.step([action])
    # If car reached the goal or crashed, stop the game
    # if (dones == True):
    #     break
    env.render()
