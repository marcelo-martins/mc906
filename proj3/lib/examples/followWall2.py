import sys, time
sys.path.insert(0, '../src')
from robot import Robot
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import numpy as np

def calcular(a_direcao, frente, direita, ang):
	#inputs
	a_direcao.input['distanciaF'] = frente
	a_direcao.input['distanciaD'] = direita
	a_direcao.input['angRel'] = ang
	# Crunch the numbers
	a_direcao.compute()
	return (a_direcao.output['direcao'], a_direcao.output['velocidade'])


deltaY = 0.0564+0.1603
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

# regras
rules = []

rules.append(ctrl.Rule(distanciaF['longe'], velocidade['fast']))
rules.append(ctrl.Rule(distanciaF['medio'], velocidade['slow']))
rules.append(ctrl.Rule(distanciaF['perto'], velocidade['zero']))

rules.append(ctrl.Rule(distanciaF['medio'], direcao['esquerda']))
rules.append(ctrl.Rule(distanciaF['perto'], direcao['esquerda']))

rules.append(ctrl.Rule(distanciaD['perto'], velocidade['zero']))
rules.append(ctrl.Rule(distanciaD['medio'], velocidade['slow']))
rules.append(ctrl.Rule(distanciaD['longe'], velocidade['fast']))

rules.append(ctrl.Rule(angRel['positivo'], direcao['esquerda']))
rules.append(ctrl.Rule(angRel['negativo'] & distanciaF['longe'], direcao['direita']))
rules.append(ctrl.Rule(angRel['negativo'] & (distanciaF['medio']|distanciaF['perto']), direcao['esquerda']))
#rules.append(ctrl.Rule(angRel['paralelo'], direcao['frente']))

rules.append(ctrl.Rule(distanciaD['medio'],direcao['esquerda']))
rules.append(ctrl.Rule(distanciaD['perto'], direcao['esquerda']))
rules.append(ctrl.Rule(distanciaD['longe'] & distanciaF['longe'], direcao['direita']))

direcao_ctrl = ctrl.ControlSystem(rules)
a_direcao = ctrl.ControlSystemSimulation(direcao_ctrl)


robot = Robot()
while (True):
	lim = 5
	robot.set_velocity(0,0)
	#ler sensores
	ultrassonic = robot.read_ultrassonic_sensors()
	frente = ultrassonic[3]
	frente1 = ultrassonic[2]
	direita = ultrassonic[7]
	direita1 = ultrassonic[6]

	deltaX = direita - direita1
	ang = deltaX/deltaY

	ang_lim = 3
	if (ang > ang_lim):
		ang = ang_lim
	if (ang < -ang_lim):
		ang = -ang_lim
	ang = (ang/ang_lim)*5 + 5

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

	#calcular a direcao
	direction = calcular(a_direcao, frente, direita, ang)

	print('fr/dir :'+ str(frente )+' '+ str(direita))

	angulo = direction[0]
	angulo -= 5
	speed = direction[1]
	#altera velocidade
	robot.set_velocity(speed*0.05, -angulo*0.25)
	print((angulo, speed))
	#sleep
	time.sleep(0.1)
