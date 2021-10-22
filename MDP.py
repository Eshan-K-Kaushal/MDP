import os
import sys
sys.setrecursionlimit(1000)

class transportMDP(object):
    def __init__(self, N):
        #N = number of blocks
        self.N = N #N would be set by the user of the program
    def startstate(self):
        return 1 #we are startiing from the state 1, i.e., block 1
    def isEnd(self, state):
        return state == self.N
    def actions(self, state): #actions that can be carried out at any state
        acts = []
        if state+1<=self.N:
            acts.append('walk')
        if state*2<=self.N:
            acts.append('magic_tram')
        return acts
    def transition_reward(self, state, action):
        #this function is going to deal with transition probabilities
        #and it is going to give rewards to all the states
        acts = []
        if action == 'walk':
            acts.append((state+1, 1., -1.)) #when we write 1. it means
        elif action == 'magic_tram':       #it can be a decimal too
            acts.append((state * 2, 0.5, -2.)) #move to next state
            acts.append((state, 0.5, -2.)) #or stay here
        return acts
    def discount(self):
        return 1.
    def states(self):
        return range(1, self.N+1)
        #here it will go from state 1 to state 10
        #the plus 1 is done since the last one is never touched
def valueIteration(mdp):
    v = {}
    for state in mdp.states():
        v[state] = 0
    def Q(state, action):
        return sum(transition_prob*(reward + mdp.discount()*v[newState])
                   for newState, transition_prob, reward in
                   mdp.transition_reward(state, action))
    while True:
        newv = {} #or this going to be the Vi+1
        for state in mdp.states():
            if mdp.isEnd(state):
                newv[state] = 0
            else:
                newv[state] = max(Q(state, action)
                                  for action in mdp.actions(state))
        if max(abs(v[state]-newv[state]) for state in mdp.states()) < 1e-10: #that is, being very very close to 0 (1e-10 means 1^(-10))
            break
        v = newv
        pi = {}
        for state in mdp.states():
            if mdp.isEnd(state):
                pi[state] = 'none' #it is going to be 0 ince it is a terminal state
            else:
                pi[state] = max((Q(state, action), action) for action #this one points us in the direction of the state that has the mas utility
                                in mdp.actions(state))[1]
        os.system('cls')
        print('{:15} {:15} {:15}'.format('s', 'v(s)', 'pi(s)'))
        list1 = []
        for state in mdp.states():
            list1.append(v[state])
            print('{:15} {:15} {:15}'.format(state, v[state], pi[state]))
        print("The max value at a state for optimality is {}".format(max(list1)))
        #print(list1)
        #input() #perhaps value of n here
mdp = transportMDP(10)
print(mdp.actions(3))
print(mdp.transition_reward(3, 'walk'))
print(mdp.transition_reward(3, 'magic_tram'))
print(mdp.transition_reward(1, 'walk'))
valueIteration(mdp)