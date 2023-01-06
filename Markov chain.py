import numpy as np
import random
import collections
import math

DEBUG = False
def debug(str):
    if DEBUG:
        print(str)


class Agent:
    def __init__(self, No_states, No_iterations):
        self.numstates_ = No_states
        self.iterations_ = No_iterations

    def states(self, No_states):
        """
        states = []
        for state in range(self.numstates_):
            state = input("Please enter a state")
            states.append(state)
        return states
        """
        return list(np.arange(1, No_states) )

    def transition_(self, No_states, No_interations):
        stateTransitionMetric = []
        prob_of_individual_states = []
        #states = self.states(self.numstates_)
        states = list(np.arange(1, self.numstates_+1))
        debug("states present are")
        debug(states)
        Initial_state_ = int(input("Please enter a initial state"))
        if Initial_state_ not in states:
            print("State not present")
            pass
        else:
            for state in states:
                for iteration in range(self.iterations_):
                    state_picked = self.random(self.numstates_)
                    prob_of_individual_states.append(state_picked)
                frequency = dict(collections.Counter(prob_of_individual_states))        # find the number of occurences of each state
                total = sum(frequency.values(), 0.0)
                frequency = {k: round(v / total, 1) for k, v in frequency.items()}

                debug("The probability of transtions from state {} to other states are {}".format(state, list(frequency.values())))
                debug(frequency)
                debug(list(frequency.values()))
                
                stateTransitionMetric.append(list(frequency.values()))
            print(stateTransitionMetric)    
        self.state_transition(No_states = len(states), initial_state = Initial_state_, STM = stateTransitionMetric )

    def random(self, No_states):
        return random.randint(1, self.numstates_)
    
    def animation(self):
        pass

    def state_transition(self, No_states, initial_state, STM):
        probability_array = []
        initial_Prob_Array = STM[initial_state-1]
        debug("The probability of reaching other states from the given initial states {}".format(initial_Prob_Array))
        for i,v in enumerate(initial_Prob_Array):     
            probability_array.extend([i+1]*int(v*100))
        pass


No_states = int(input("Enter the number of states"))
iterations = int(input("Enter the number of iterations"))

RL = Agent(No_states = No_states, No_iterations = iterations)
RL.transition_(No_states = No_states, No_interations = iterations) 