from Element import Element
from Node import Node
from typing import List, Tuple
import numpy as np


class Trelica:
    """
    Essa classe representa uma Treliça sujeita a cargas externas constantes. Para utilizá-la,
    definimos quais são os elementos estruturais, as cargas externas às quais esses elementos estão sujeitos
    e as condições de contorno, obtendo a matriz de rigidez da estrutura global.
    """
    def __init__(self, Nodes: List[Node]):
        self.nodes = Nodes
        self.size = 2 * len(Nodes)
        self.elements: List[Element] = []
        self.K = np.zeros((self.size, self.size))
        self.cargasExternas = np.zeros((self.size, 1))
        self.condicoesContorno = []

    def getKMatrix(self):
        return self.K

    def setKMatrix(self, K):
        self.K = K

    def computeElement(self, aKey: int, bKey: int):
        aX, aY, bX, bY = -1, -1, -1, -1

        if aKey > self.size or bKey > self.size:
            print('ERRO: NÓ INVÁLIDO')

        else:
            for node in self.nodes:
                if node.key == aKey:
                    aX, aY, aType = node.x, node.y, node.type
                elif node.key == bKey:
                    bX, bY, bType = node.x, node.y, node.type

            el = Element(
                Node(aX, aY, aKey, aType),
                Node(bX, bY, bKey, bType)
            )
            el.computeKMatrix()

            self.elements.append(el)
            self.computeKMatrix()

    def computeKMatrix(self):
        self.setKMatrix(np.zeros((self.size, self.size)))
        for element in self.elements:
            A, B = element.getNodes()
            aKey, bKey = A.getKey(), B.getKey()
            elementK = element.getKMatrix()

            # submatrizes da matriz de rigidez do elemento
            Ka = elementK[0:2, 0:2]
            Kb = elementK[0:2, 2:]
            Kc = elementK[2:, 0:2]
            Kd = elementK[2:, 2:]

            # somar essas matrizes nos devidos lugares da matriz global
            self.K[2 * aKey - 2:2 * aKey, 2 * aKey - 2:2 * aKey] += Ka
            self.K[2 * aKey - 2:2 * aKey, 2 * bKey - 2:2 * bKey] += Kb
            self.K[2 * bKey - 2:2 * bKey, 2 * aKey - 2:2 * aKey] += Kc
            self.K[2 * bKey - 2:2 * bKey, 2 * bKey - 2:2 * bKey] += Kd

    def computeCargasExternas(self, nodeKey: int, forceVector: List[float]):
        for node in self.nodes:
            if node.key == nodeKey:
                self.cargasExternas[2*nodeKey-2, 0] = forceVector[0]
                self.cargasExternas[2 * nodeKey - 1, 0] = forceVector[1]

    def getCargasExternas(self):
        return self.cargasExternas

    def computeCondContorno(self, nodeKey: int, tipo: str, value=0):
        if tipo == 'Apoio Livre':
            pass
        elif tipo == 'Apoio Fixo':
            pass














