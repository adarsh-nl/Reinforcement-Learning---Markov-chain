import numpy as np
import random
import collections
import math
import networkx as nx
from networkx.drawing.nx_agraph import to_agraph
import imageio
from PIL import Image, GifImagePlugin

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
        Agent_state_transition_list = []
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
                #frequency = {k: round(v / total, 1) for k, v in frequency.items()}
                frequency = {k: v / total for k, v in frequency.items()}

                debug("The probability of transtions from state {} to other states are {}".format(state, list(frequency.values())))
                debug(frequency)
                debug(list(frequency.values()))
                
                stateTransitionMetric.append(list(frequency.values()))
            debug(stateTransitionMetric)

        no_transitions = int(input("Please enter number of transitions the Agent should take"))    
        return (self.state_transition(initial_state = Initial_state_, STM = stateTransitionMetric, no_transitions = no_transitions, Agent_state_transition_list= Agent_state_transition_list))
        

    def random(self, No_states):
        return random.randint(1, No_states)
    
    def animation(self, agent_transition_list, metric, Nsteps):
        debug("Agent transition list: {}".format(agent_transition_list))
        debug("Metric: {}".format(metric))
        #Sampling the markov chain over 100 steps
        N_steps= Nsteps
        node_ind=0
        node_sel=[node_ind]
        for i in range(N_steps):
            temp_ni=np.random.choice(3,p=metric[node_ind])
            node_sel.append(temp_ni)
            node_ind=temp_ni
        #Setting up network
        G = nx.MultiDiGraph()
        [G.add_node(s,style='filled',fillcolor='white',shape='circle',fixedsize='true',width=0.5) for s in agent_transition_list]

        labels={}
        edge_labels={}

        for i, origin_state in enumerate(agent_transition_list):
            for j, destination_state in enumerate(agent_transition_list):
                try:
                    rate = metric[i][j]
                except:
                    rate = metric[len(metric[0])-1][len(metric[0])-1]
                if rate > 0:
                    G.add_edge(origin_state, destination_state, weight=rate, label="{:.02f}".format(rate),len=2)

        #Setting up node color for each iteration     
        for k in range(N_steps):
            for i,n in enumerate(G.nodes(data=True)):
                if i==node_sel[k]:
                    n[1]['fillcolor']='blue'
                else:
                    n[1]['fillcolor']='white'
                
            A = to_agraph(G)
            A.layout()
            A.draw('net_'+str(k)+'.png')
            A.render()
        #Create gif with imageio
        images = []
        filenames=['net_'+str(k)+'.png' for k in range(N_steps)]
        for filename in filenames:
            images.append(imageio.imread(filename))
        imageio.mimsave('markov_chain.gif', images,fps=3)
        return
    
    def sub_func_state_transition_probability(self, STM, current_state):
        return STM[current_state-1]

    def probability_array(self, ind_prob):
        probability_Array = []
        for i,v in enumerate(ind_prob):     
            probability_Array.extend([i+1]*int(v*100))
        return probability_Array

    def state_transition(self, initial_state, STM, no_transitions, Agent_state_transition_list):
        Current_Agent_state = initial_state
        #Agent_state_transition_list.append(Current_Agent_state)
        ind_prob = self.sub_func_state_transition_probability(STM, initial_state)
        debug("Individual probability from State Transition Function is {}".format(ind_prob))
        probabilityArray = self.probability_array(ind_prob)
        debug("The probability of reaching other states from the given initial states {}\n and length of the array is: {}".format(probabilityArray, len(probabilityArray)))
        #for transition in range(no_transitions):
        if no_transitions == 0:
            self.animation(Agent_state_transition_list, STM, no_transitions)
            debug("Agent transition list: {}".format(Agent_state_transition_list))
            return Current_Agent_state
        else:
            idx = self.random(100)
            debug("Random Index is: {}".format(idx))
            #Agent_state_transition_list.append((Current_Agent_state,probabilityArray[idx]))
            try:
                Agent_state_transition_list.append((Current_Agent_state,probabilityArray[idx]))
                Current_Agent_state = probabilityArray[idx]
            except:
                Agent_state_transition_list.append((Current_Agent_state,probabilityArray[len(probabilityArray)-1]))
                Current_Agent_state = probabilityArray[len(probabilityArray)-1]
            return self.state_transition(initial_state = Current_Agent_state, STM = STM, no_transitions = no_transitions-1, Agent_state_transition_list = Agent_state_transition_list )


No_states = int(input("Enter the number of states"))
iterations = int(input("Enter the number of iterations"))

RL = Agent(No_states = No_states, No_iterations = iterations)
finalState = RL.transition_(No_states = No_states, No_interations = iterations)
print("Final state after transitions is: {}\nThe agent transitioned states are: {}".format(finalState))
