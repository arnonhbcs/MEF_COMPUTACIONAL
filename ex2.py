from Node import Node
from Structure import Structure
from Solver import Solver

# instanciar os nós por meio das coordenadas
# Considera-se o nó 1 como origem
node1 = Node(x=0, y=0, key=1, tipo='apoio_fixo')
node2 = Node(x=10, y=0, key=2, tipo='apoio_livre_vertical')
node3 = Node(x=5, y=8, key=3, tipo='no_comum')
node4 = Node(x=5, y=4, key=4, tipo='no_comum')

nodes = [node1, node2, node3, node4]

# instanciar a Treliça
structure = Structure(nodes)

# instanciar os elementos (Barras)
structure.computeElement(1, 2, key=1)
structure.computeElement(1, 3, key=2)
structure.computeElement(1, 4, key=3)
structure.computeElement(2, 3, key=4)
structure.computeElement(3, 4, key=5)
structure.computeElement(2, 4, key=6)

# Inserir cargas externas
structure.computeCargasExternas(nodeKey=3, forceVector=[20, 30])

# Instanciando o Solver
solver = Solver(structure)
F, q, Fint = solver.solve()



print(F)
print(q)
print(Fint)



