# gym.py

import gym
from gym import spaces
import numpy as np

from game.game_logic import GameLogic
from game.player import Player
from game.table import Community_Cards

class PokerEnv(gym.Env):
    def __init__(self):
        super(PokerEnv, self).__init__()

        self.game = GameLogic()
        self.action_space = spaces.Discrete(4)  # Fold, Check/Call, Bet/Raise
        self.observation_space = spaces.Dict({
            'game_state': spaces.Discrete(4), # Represents the stage of the game (pre-flop, flop, turn, river)
            'player_hand': spaces.MultiDiscrete([[[2, 14], [1, 4]], [[2, 14], [1, 4]]]),  # Rank and suit of each card in the hand
            'hand_strength': spaces.Box(low=0, high=np.inf, shape=(1,)),  # Hand strength overall
            'hand_strength_2_cards': spaces.Box(low=0, high=np.inf, shape=(1,)),  # Hand strength with 2 cards
            'hand_strength_5_cards': spaces.Box(low=0, high=np.inf, shape=(1,)),  # Hand strength with 5 cards (flop)
            'hand_strength_6_cards': spaces.Box(low=0, high=np.inf, shape=(1,)),  # Hand strength with 6 cards (turn)
            'hand_strength_7_cards': spaces.Box(low=0, high=np.inf, shape=(1,)),  # Hand strength with 7 cards (river)
            'flop_cards': spaces.MultiDiscrete([[[2, 14], [1, 4]], [[2, 14], [1, 4]], [[2, 14], [1, 4]]]),  # Rank and suit of each flop card
            'turn_card': spaces.MultiDiscrete([[2, 14], [1, 4]]),  # Rank and suit of the turn card
            'river_card': spaces.MultiDiscrete([[2, 14], [1, 4]]),  # Rank and suit of the river card
            'betting_info': spaces.Box(low=0, high=np.inf, shape=(3,)),  # Current bet, pot size, number of players
            'player_info': spaces.MultiDiscrete([np.inf, np.inf, np.inf]),  # Chip count, current bet, and in-play status for each player
            })

    def reset(self):
        self.game = GameLogic()  # Reset the game for a new episode
        # Return initial observation
        return np.array([0])

    def step(self, action):
        # Execute the action in the game
        # Update the game state, player actions, etc.

        done = self.game.game_over 
        round_over = self.game.round_over
        reward = 1.0 if done else 0.0

        # Return the current observation, reward, and additional information
        return np.array([0]), reward, done, {}
    
    def get_player_observations(self):
        # Define how to get the observation for each player
        player_observations = []
        for player in self.game.players:
            player_observations.append('player_hand': {player.hand[0], player.hand[1]},
                                       'hand_strength': player.hand_strength,
                                       ) 
        return player_observations
    
    def _get_observation(self):
        # Define how to get the observation for the agent
        if 'game_state' in self.observation_space.spaces == 0:
            return {self.game.game_state, self.player}
        pass

    def render(self, mode='human'):
        # Implement a rendering method
        pass

    def close(self):
        pass