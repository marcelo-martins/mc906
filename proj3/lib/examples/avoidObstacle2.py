
import sys, time
sys.path.insert(0, '../src')
from robot import Robot
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import numpy as np
import matplotlib.pyplot as plt

def calcular(a_direcao, frente, esquerda, direita, direcao):
	#inputs
	a_direcao.input['distanciaF'] = frente
	a_direcao.input['distanciaE'] = esquerda
	a_direcao.input['distanciaD'] = direita
	a_direcao.input['direcao'] = direcao
	# Crunch the numbers
	a_direcao.compute()
	return (a_direcao.output['velocidadeE'], a_direcao.output['velocidadeD'])


#variaveis fuzzy
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

# regras


rules = []
rules.append(ctrl.Rule(distanciaF['longe'], velocidadeE['positivo']))
rules.append(ctrl.Rule(distanciaF['longe'], velocidadeD['positivo']))

#rules.append(ctrl.Rule(distanciaF['medio'], velocidadeE['positivo']))
#rules.append(ctrl.Rule(distanciaF['medio'], velocidadeD['negativo']))

rules.append(ctrl.Rule(distanciaF['perto'] & distanciaD['medio'], velocidadeE['positivo']))
rules.append(ctrl.Rule(distanciaF['perto']& distanciaD['medio'], velocidadeD['negativo']))

rules.append(ctrl.Rule(distanciaF['perto'] & distanciaE['medio'], velocidadeE['negativo']))
rules.append(ctrl.Rule(distanciaF['perto']& distanciaE['medio'], velocidadeD['positivo']))


rules.append(ctrl.Rule(distanciaD['perto'], velocidadeE['negativo']))
rules.append(ctrl.Rule(distanciaD['perto'], velocidadeD['positivo']))
rules.append(ctrl.Rule(distanciaD['longe'], velocidadeE['positivo']))
rules.append(ctrl.Rule(distanciaD['longe'], velocidadeD['positivo']))

rules.append(ctrl.Rule(distanciaE['perto'], velocidadeE['positivo']))
rules.append(ctrl.Rule(distanciaE['perto'], velocidadeD['negativo']))
rules.append(ctrl.Rule(distanciaE['longe'], velocidadeE['positivo']))
rules.append(ctrl.Rule(distanciaE['longe'], velocidadeD['positivo']))

rules.append(ctrl.Rule(direcao['negativo']& distanciaE['longe'], velocidadeE['negativo']))
rules.append(ctrl.Rule(direcao['negativo']& distanciaE['longe'], velocidadeD['positivo']))
rules.append(ctrl.Rule(direcao['positivo']& distanciaD['longe'], velocidadeE['positivo']))
rules.append(ctrl.Rule(direcao['positivo']& distanciaD['longe'], velocidadeD['negativo']))

# control
direcao_ctrl = ctrl.ControlSystem(rules)
a_direcao = ctrl.ControlSystemSimulation(direcao_ctrl)
target = -0
robot = Robot()
while (True):
	lim = 5
	robot.set_velocity(0,0)
	#ler sensores da direita, esquerda e frente
	ultrassonic = robot.read_ultrassonic_sensors()
	ang = robot.get_current_orientation()[2]/0.0174533
	print ("angulo: "+ str(ang))

	ang = ang-target
	ang = (ang/180)*5 + 5
	frente = ultrassonic[3]
	frente1 = ultrassonic[4]

	direita = ultrassonic[6]
	direita1 = direita

	esquerda = ultrassonic[1]
	esquerda1 = esquerda

	if (frente1 < frente):
		frente = frente1
	if (frente > lim):
		frente = 10
	else:
		frente = 10*(frente/lim)

	if (direita1 < direita):
		direita = direita1
	if (direita > lim):
		direita = 10
	else:
		direita = 10*(direita/lim)

	if (esquerda1 < esquerda):
		esquerda = esquerda1
	if (esquerda > lim):
		esquerda = 10
	else:
		esquerda = 10*(esquerda/lim)

	#calcular a direcao
	direction = calcular(a_direcao, frente,esquerda,direita, ang)
	velEsq = direction[0]
	velEsq -= 5
	velDir = direction[1]
	velDir -= 5
	#altera velocidade
	robot.set_left_velocity(velEsq)
	robot.set_right_velocity(velDir)
	#sleep
	time.sleep(0.1)
