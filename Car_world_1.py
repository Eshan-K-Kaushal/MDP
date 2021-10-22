#code to tell what all states lie ahead on the basis of actions chosen
import sys
import os
sys.setrecursionlimit(10)
class car_world(object):
    #def __init__(self, state, p):
        #self.state = state #the start state
        #self.p = p
    def isEnd(self, state):
        return state == 'overheated'
    def startstate(self):
        return 'cool'
    def discount_factor(self):
        return 0.5
    state1 = ['cool', 'warm', 'overheated']

    def actions_reward(self, state, action):
        acts = []
        if state == 'cool':
            if action == 'slow':
               acts.append(('cool', 1, 1)) #(s',r, t)
            elif action == 'fast':
                acts.append(('warm', 2, 0.5))
                acts.append(('cool', 2, 0.5))
        elif state == 'warm':
            if action == 'slow':
                acts.append(('warm', 1, 0.5))
                acts.append(('cool', 1, 0.5))
            elif action == 'fast':
                acts.append(('overheated', -10, 1))
        elif state == 'overheated':
            print("The car is overheated. It can't move any further")
        return acts

def val_it(car1, state2, action2):
    v = {}
    for state in car1.state1:
        v[state] = 0

    def Q(state, action):
        return sum(pro * (reward + car1.discount_factor()*v[newstate]) #order of elements for has to be in the way you are returning by acts
                   for newstate, reward, pro in car1.actions_reward(state2, action2))
    while True:
        newv = {}

        for state in car1.state1:
            if car1.isEnd(state):
                newv[state] = 0
            else:
                newv[state] = max(Q(state, act) for act in
                                  car1.actions_reward(state2,action2))
        max1 = []
        for state in car1.state1:
            max1.append(abs(v[state] - newv[state]))
        mx = max(max1)
        print("mx=",mx)
        if mx < 1e-10:
            break
        #if max(abs(v[state] - newv[state])) < 1e-10:
        #    break
        v = newv
        pi = {}
        for state in car1.state1:
            if car1.isEnd(state):
                pi[state] = 'none'
            else:
                pi[state] = max((Q(state, act), act) for act in
                car1.actions_reward(state2, action2))[1]

        os.system('cls')
        print('{:15} {:15} {:15}'.format('s', 'v(s)', 'pi(s)'))
        for state in car1.state1:
            print(state, v[state], pi[state])

car1 = car_world()
print(car1.actions_reward('warm', 'fast'))
print(car1.actions_reward('warm', 'slow'))
val_it(car1, 'cool', 'fast')
#in the end the values almost converge