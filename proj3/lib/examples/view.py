
import sys, time
sys.path.insert(0, '../src')
from robot import Robot
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import numpy as np
import matplotlib.pyplot as plt

"""
# avoid obstacle
velocidadeE = ctrl.Consequent(np.arange(0, 11, 1), 'velocidadeE')
velocidadeD = ctrl.Consequent(np.arange(0, 11, 1), 'velocidadeD')
distanciaF = ctrl.Antecedent(np.arange(0,11,1), 'distanciaF')
distanciaD = ctrl.Antecedent(np.arange(0,11,1), 'distanciaD')
distanciaE = ctrl.Antecedent(np.arange(0,11,1), 'distanciaE')
direcao = ctrl.Antecedent(np.arange(0,11,1), 'direcao')

distanciaF['perto'] = fuzz.trapmf(distanciaF.universe, [0,0,4,8])
distanciaF['medio'] = fuzz.trapmf(distanciaF.universe, [0,4,8,10])
distanciaF['longe'] = fuzz.trapmf(distanciaF.universe, [9,10,10,10])

names = ['perto','medio','longe']
distanciaD.automf(names=names)
distanciaE.automf(names=names)
names = ['negativo', 'zero', 'positivo']
velocidadeE.automf(names=names)
velocidadeD.automf(names=names)
direcao.automf(names=names)
"""



"""
#follow wall
velocidade= ctrl.Consequent(np.arange(0, 11, 1), 'velocidade', 'bisector')
direcao = ctrl.Consequent(np.arange(0, 11, 1), 'direcao', 'bisector')
distanciaF = ctrl.Antecedent(np.arange(0,11,1), 'distanciaF')
distanciaD = ctrl.Antecedent(np.arange(0,11,1), 'distanciaD')
angRel = ctrl.Antecedent(np.arange(0,11,1), 'angRel')


distanciaF['perto'] = fuzz.trapmf(distanciaF.universe, [0,0,4,8])
distanciaF['medio'] = fuzz.trapmf(distanciaF.universe, [0,4,8,10])
distanciaF['longe'] = fuzz.trapmf(distanciaF.universe, [9,10,10,10])

#distanciaD['perto'] = fuzz.trapmf(distanciaF.universe, [0,0,4,8])
#distanciaD['medio'] = fuzz.trapmf(distanciaF.universe, [0,4,8,10])
#distanciaD['longe'] = fuzz.trapmf(distanciaF.universe, [9,10,10,10])

names = ['perto','medio','longe']
#distanciaF.automf(names=names)
distanciaD.automf(names=names)
names = ['esquerda', 'frente', 'direita']
direcao.automf(names=names)
names = ['negativo','paralelo','positivo']
angRel.automf(names=names)
names = ['zero', 'slow', 'fast']
velocidade.automf(names=names)

"""




distanciaF.view()
input("Press enter to continue")
