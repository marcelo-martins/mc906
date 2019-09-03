from search import *
from notebook import psource, heatmap, gaussian_kernel, show_map, final_path_colors, display_visual, plot_NQueens
import warnings
warnings.filterwarnings("ignore")
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import lines
import numpy as np
from ipywidgets import interact
import ipywidgets as widgets
from IPython.display import display
import time
import math

import resource

globalvar = 0
matriz = np.full((61,61), 0)
for x in range (61):
    matriz[x, 0] = 1
    matriz[x,60] = 1
for y in range (61):
    matriz[0, y] = 1
    matriz[60,y] = 1
for x in range (20,61):
    matriz[x, 20] = 1
for x in range (0,41):
    matriz[x, 40] = 1
#-----------------------------------------------------------------------------------------------------------------------------------
class MyProblem(Problem):

        def __init__(self, initial, goal):
            Problem.__init__(self, initial, goal)

        def actions(self, state):
            x = state[0]
            y = state[1]
            theta = state[2]
            acoes = []

            #teste para ver se andar pra frente pode
            if(theta==1):
                x2=x
                y2=y+1
            elif(theta==3):
                x2=x+1
                y2=y
            elif(theta==5):
                x2=x
                y2=y-1
            elif(theta==7):
                x2=x-1
                y2=y


            if(0<x2<60 and 0<y2<60):
                if((not(x2==20 and 0<=y2<40)) and (not(x2==40 and 20<y2<=60))):
                    acoes.append("anda")

            acoes.append("gira")
            return acoes
        def result(self, state, action):
            global globalvar
            globalvar = globalvar + 1
            estado = [1,1,1]
            theta = state[2]
            if(action == "anda"):
                estado[2] = state[2]
                if(theta == 1):
                    estado[0] = state[0]
                    estado[1] = state[1] + 1
                elif(theta == 3):
                    estado[0] = state[0] + 1
                    estado[1] = state[1]
                elif(theta == 5):
                    estado[0] = state[0]
                    estado[1] = state[1] - 1
                elif(theta == 7):
                    estado[0] = state[0] - 1
                    estado[1] = state[1]

            elif(action == "gira"):
                estado[0] = state[0]
                estado[1] = state[1]
                if(theta == 7):
                    estado[2] = 1
                else:
                    estado[2] = theta+2

            estado2 = (estado[0], estado[1], estado[2])
            matriz[60-estado[1], estado[0]] = 6
            return estado2

        def goal_test(self, state):#ignora o fato de que o robo pode estar girado quando chegar no goal
            xG = self.goal[0]
            yG = self.goal[1]

            global globalvar
            if(state[0] == xG and state[1] == yG):
                print("nós visitados: ", globalvar)
                globalvar = 0
                matriz[60-yG, xG] = 3
                return True
            else:
                return False

        def path_cost(self, c, state1, action, state2):
            return c + 1

        def value(self, state):
            raise NotImplementedError

inicio = time.time()
posI = (10,10,1)
posF = (50,50,3)
robot_problem = MyProblem(posI, posF)

xx = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

a = breadth_first_graph_search(robot_problem)

#a = best_first_graph_search(robot_problem, lambda f : math.sqrt((math.fabs(f.state[0]-posF[0]))**2 + (math.fabs(f.state[1]-posF[1]))**2)) #H1
#a = best_first_graph_search(robot_problem, lambda f : math.fabs(f.state[0] - posF[1])) #H2

yy = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

print("memoria usada", yy-xx)

fim = time.time()
print("tempo final ", fim - inicio)

for no in a.path():
   matriz[60- no.state[1], no.state[0]] = 4

plt.matshow(matriz)
plt.show()
