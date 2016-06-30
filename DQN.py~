# -------------------------
# Project: Deep Q-Learning on Flappy Bird
# Author: Flood Sung
# Date: 2016.3.21
# -------------------------

import cv2
import sys
sys.path.append("game/")
from DQN_NIPS import BrainDQN
import numpy as np

# preprocess raw image to 80*80 gray image
def preprocess(observation):
	observation = cv2.cvtColor(cv2.resize(observation, (80, 80)), cv2.COLOR_BGR2GRAY)
	ret, observation = cv2.threshold(observation,1,255,cv2.THRESH_BINARY)
	return np.reshape(observation,(80,80,1))
def card_old(a,b):
	huase=a%4
	value=a/4+2
	old_image[huase][value][b]=1

def card(a,b):
	huase=a%4
	value=a/4+2
	image_data[huase][value][b]=1
def playFlappyBird(observation,nextObservation,action,reward):
	#return 6
	# Step 1: init BrainDQN
	actions = 3
	brain = BrainDQN(actions)
	# Step 2: init Flappy Bird Game
	#flappyBird = game.GameState()
	# Step 3: play game
	# Step 3.1: obtain init state
	#action0 = np.array([1,0])  # do nothing
	#observation0, reward0, terminal = flappyBird.frame_step(action0)
	#observation0 = cv2.cvtColor(cv2.resize(observation0, (80, 80)), cv2.COLOR_BGR2GRAY)
	#ret, observation0 = cv2.threshold(observation0,1,255,cv2.THRESH_BINARY)
	terminal=0
	brain.setInitState(observation)
	brain.setPerception(nextObservation,action,reward,terminal)
	brain.setInitState(nextObservation)
	action_final = brain.getAction()
	# Step 3.2: run the game
	while 1!= 0:
		action = brain.getAction()

		#nextObservation,reward,terminal = flappyBird.frame_step(action)
		nextObservation = preprocess(nextObservation)
		brain.setPerception(nextObservation,action,reward,terminal)
	return  action_final


def main():
	global image_data,old_image,action,reward
	image_data=np.zeros((17,17,16),int)
	old_image=np.zeros((17,17,16),int)
	#for i in range(0,7):
	#	card_old(int(argv[i]),i)
	#for i in range(7,14):
	#	card(int(argv[i]),i-7)
	#action=int(argv[14])
	#reward=int(argv[15])
	#print reward
	print playFlappyBird()
	#playFlappyBird()

if __name__ == '__main__':
	main(sys.argv[1:])

