import sys, time
sys.path.insert(0, '../src')
from robot import Robot
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import numpy as np

def calcular(a_direcao, frente, esquerda, direita):
	#inputs
	a_direcao.input['distanciaF'] = frente
	#a_direcao.input['distanciaT'] = 3
	#a_direcao.input['distanciaE'] = esquerda
	a_direcao.input['distanciaD'] = direita
	# Crunch the numbers
	a_direcao.compute()
	return (a_direcao.output['direcao'], a_direcao.output['velocidade'])


#variaveis fuzzy
direcao = ctrl.Consequent(np.arange(0, 11, 1), 'direcao')
velocidade = ctrl.Consequent(np.arange(0, 11, 1), 'velocidade')
distanciaF = ctrl.Antecedent(np.arange(0,11,1), 'distanciaF')
distanciaD = ctrl.Antecedent(np.arange(0,11,1), 'distanciaD')
#distanciaE = ctrl.Antecedent(np.arange(0,11,1), 'distanciaE')

"""
v_perto = [0, 0, 2, 5]
v_medio = [3, 4, 6, 7]
v_longe = [5, 8, 10,10]
"""

v_mp = [0,0,3]
v_p = [0,3,5]
v_m = [0,5,10]
v_l = [5,8,10]
v_ml = [8,10,10]


distanciaF['mperto'] = fuzz.trimf(distanciaF.universe, v_mp)
distanciaF['perto'] = fuzz.trimf(distanciaF.universe, v_p)
distanciaF['medio'] = fuzz.trimf(distanciaF.universe, v_m)
distanciaF['longe'] = fuzz.trimf(distanciaF.universe, v_ml)

distanciaD['mperto'] = fuzz.trimf(distanciaD.universe, v_mp)
distanciaD['perto'] = fuzz.trimf(distanciaD.universe, v_p)
distanciaD['medio'] = fuzz.trimf(distanciaD.universe, v_m)
distanciaD['longe'] = fuzz.trimf(distanciaD.universe, v_ml)

#distanciaE['perto'] = fuzz.trapmf(distanciaE.universe, v_perto)
#distanciaE['medio'] = fuzz.trapmf(distanciaE.universe, v_medio)
#distanciaE['longe'] = fuzz.trapmf(distanciaE.universe, v_longe)




#names = ['perto','medio','longe']
#distanciaF.automf(names=names)
#distanciaD.automf(names=names)
#names = ['esquerda', 'frente', 'direita']
#direcao.automf(names=names)
direcao['W'] = fuzz.trimf(direcao.universe, v_mp)
direcao['NW'] = fuzz.trimf(direcao.universe, v_p)
direcao['N'] = fuzz.trimf(direcao.universe, v_m)
direcao['NE'] = fuzz.trimf(direcao.universe, v_l)
direcao['L'] = fuzz.trimf(direcao.universe, v_ml)

names = ['zero', 'slow', 'fast']
velocidade.automf(names=names)

# regras

rule1 = ctrl.Rule(distanciaF['longe'], velocidade['fast'])
rule2 = ctrl.Rule(distanciaF['medio'], velocidade['slow'])
rule3 = ctrl.Rule(distanciaF['perto'], velocidade['slow'])
rule4 = ctrl.Rule(distanciaF['mperto'], velocidade['zero'])
rule5 = ctrl.Rule(distanciaF['longe'] & distanciaD['perto'], velocidade['slow'])
rule6 = ctrl.Rule(distanciaF['longe'] & distanciaD['mperto'], velocidade['zero'])

rule7 = ctrl.Rule(distanciaF['longe']& distanciaD['longe'], direcao['NE'])
rule8 = ctrl.Rule(distanciaF['longe']& distanciaD['medio'], direcao['N'])
rule9 = ctrl.Rule(distanciaF['longe']& distanciaD['perto'], direcao['NW'])
rule10 = ctrl.Rule(distanciaF['longe']& distanciaD['mperto'], direcao['W'])

rule11 = ctrl.Rule(distanciaF['medio'], direcao['NW'])
rule12 = ctrl.Rule(distanciaF['perto'], direcao['W'])
rule13 = ctrl.Rule(distanciaF['mperto'], direcao['W'])



"""

rule4 = ctrl.Rule(distanciaF['perto'] & distanciaD['perto'], direcao['esquerda'])
rule6 = ctrl.Rule(distanciaF['perto'] & distanciaD['longe'], direcao['esquerda'])
rule7 = ctrl.Rule(distanciaF['perto'] & distanciaD['medio'], direcao['esquerda'])
rule11 = ctrl.Rule(distanciaF['medio'], direcao['esquerda'])



rule5 = ctrl.Rule(distanciaF['longe'] & distanciaD['longe'], direcao['direita'])


rule9 = ctrl.Rule(distanciaF['longe'] & distanciaD['perto'], direcao['esquerda'])

rule1 = ctrl.Rule(distanciaF['perto'], velocidade['zero'])
rule2 = ctrl.Rule(distanciaF['medio'], velocidade['slow'])
rule3 = ctrl.Rule(distanciaF['longe'], velocidade['fast'])
rule12 = ctrl.Rule(distanciaF['longe'] & distanciaD['perto'], velocidade['slow'])


rule10 = ctrl.Rule(distanciaD['perto'], direcao['frente'])
rule8 = ctrl.Rule(distanciaD['medio'], direcao['frente'])
"""




# control
direcao_ctrl = ctrl.ControlSystem([rule1,rule2,rule3,rule4,rule5,rule6,rule7,rule8,rule9,rule10,rule11,rule12,rule13])
a_direcao = ctrl.ControlSystemSimulation(direcao_ctrl)


robot = Robot()
while (True):
	lim = 5
	robot.set_velocity(0,0)
	#ler sensores da direita, esquerda e frente
	ultrassonic = robot.read_ultrassonic_sensors()
	frente = ultrassonic[3]
	direita = ultrassonic[7]
	direita1 = ultrassonic[6]
	esquerda = ultrassonic[0]

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


	if (esquerda > lim):
		esquerda = 10
	else:
		esquerda = 10*(esquerda/lim)

	#calcular a direcao
	direction = calcular(a_direcao, frente, esquerda,direita)

	print('fr/dir :'+ str(frente )+' '+ str(direita))

	angulo = direction[0]
	angulo -= 5
	speed = direction[1]
	#altera velocidade
	robot.set_velocity(speed*0.05, -angulo*0.25)
	print((angulo, speed))
	#sleep
	time.sleep(0.1)

"""



for i in range(10):

	






    robot.set_left_velocity(10.0) #rad/s
    robot.set_right_velocity(10.0)
    time.sleep(10) #Go foward for 10 seconds!

    robot.stop()
    time.sleep(0.5) #Stop for half second

   
    time.sleep(1) #Turning left for 1 second

    robot.stop()
    time.sleep(0.5) #Stop for half second

    robot.set_velocity(0.5, -0.1)
    time.sleep(5) #Moving forward and to the right for 5 seconds

    robot.stop()
    time.sleep(0.5) #Stop for half second

    robot.set_velocity(-0.1, -0.1)
    time.sleep(5) #Moving backwards and to the right for 5 seconds

    robot.stop()
    time.sleep(0.5) #Stop for half second
"""