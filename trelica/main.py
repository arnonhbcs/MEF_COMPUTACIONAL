import math

from Node import Node
from Element import Element
from Trelica import Trelica
import numpy as np
from Solver import Solver
from math import sqrt, copysign

# instanciar os nós por meio das coordenadas
# Considera-se o nó 1 como origem
node1 = Node(0, 0, 1, 'apoio_fixo')
node2 = Node(10, 0, 2, 'liv')
node3 = Node(5, 8, 3, 'no_comum')
node4 = Node(5, 4, 4, 'no_comum')

nodes = [node1, node2, node3, node4]

# instanciar a Treliça
trelica = Trelica(nodes)

# instanciar os elementos (Barras)
trelica.computeElement(1, 2)
trelica.computeElement(1, 3)
trelica.computeElement(1, 4)
trelica.computeElement(2, 3)
trelica.computeElement(3, 4)
trelica.computeElement(2, 4)

# Inserir cargas externas
trelica.computeCargasExternas(3, [20*10**3, 30*10**3])

# Instanciando o Solver
solver = Solver(trelica)
# solver.setCondicoesContorno()
# solver.setForcasExternas()
# print(solver.solve())
print(solver.uCondContorno)

# solution = solver.solve()
#
#
# print(solution)
