from Structure import Structure
import numpy as np
from Node import Node
from mef_implementado.Solver import Solver
from math import floor

num1 = 6
num2 = 6

x1 = np.linspace(0, 0.15, num1 + 1)
x2 = np.linspace(0.15, 0.4125 , num2 + 1)
x = np.concatenate((x1, x2[1:]))

q0 = 10 * 10 ** 3
q1 = -2 * q0
q2 = q0
nodes = []

for i in range(len(x)):
    tipo = 'no_comum'
    if i == 0 or i == len(x) - 1:
        tipo = 'apoio_fixo'

    nodes.append(Node(x[i], 0, i + 1, tipo))

estrutura = Structure(nodes)

for i in range(len(x) - 1):
    EA, q = 0, 0
    if i < num1:
        EA = 0.8 * 10 ** 9 * 1000 * 10 ** (-6)
        q = q1
    else:
        EA = 2.7 * 10 ** 9 * 1875 * 10 ** (-6)
        q = q2

    estrutura.computeElement(i + 1, i + 2, i + 1, q, EA)

estrutura.computeCargasExternas(num1+1, forceVector=[-50000, 0])

solver = Solver(estrutura)
F, q, _ = solver.solve()

F = {key: F[key] for key in F.keys() if F[key] != 0.0}
q = {key: q[key] for key in q.keys() if q[key] != 0.0}



# arquivo para exportar os valores determinados
filename = 'resultados_barra.txt'
with open(filename, 'w') as f:
    f.write('Valores de Deslocamento Horizontal \n')
    qValues = list(q.values())
    l = len(qValues)
    f.write(f'u_1 = 0.00 \n')
    for i in range(0, l):
        f.write(f'u_{i+2} = {(qValues[i])} ')
        f.write('\n')

    f.write(f'u_{l+2} = 0.00 \n')

    f.write('Forças nas extremidades \n')
    f.write(str(F['R1']))
    f.write('\n')
    f.write(str(F[f'R{2 * (num1 + num2) + 1}']))

