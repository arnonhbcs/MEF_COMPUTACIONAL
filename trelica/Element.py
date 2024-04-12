from Node import Node
import numpy as np
from math import sin, cos


class Element:
    """
    Essa classe representa os de una treliça (barras). Seus atributos de instancia são
    os nós que compreendem o elemento, seu comprimento, o ângulo que o elemento forma com o eixo x e a matriz
    de rigidez.
    """
    def __init__(self, A: Node, B: Node):
        self.A = A
        self.B = B

        self.y = B.y - A.y
        self.x = B.x - A.x
        self.L = np.sqrt(self.x**2 + self.y**2)
        E = 200 * 10**9
        A = 900 * 10**(-6)
        EA = E*A
        self.EA = EA

        self.alpha = np.arctan2(self.y, self.x)
        self.setKMatrix(np.zeros(4))
        self.computeKMatrix()

    def getAlpha(self):
        return self.alpha

    def getKMatrix(self):
        return self.K

    def setKMatrix(self, K):
        self.K = K

    def getNodes(self):
        return self.A, self.B

    def computeKMatrix(self):
        c = cos(self.alpha)
        s = sin(self.alpha)
        K = np.array([
            [c ** 2, c * s, -c ** 2, -c * s],
            [c * s, s ** 2, -c * s, -s ** 2],
            [-c ** 2, -c * s, c ** 2, c * s],
            [-c * s, -s ** 2, c * s, s ** 2]
        ])
        K = K * self.EA / self.L
        K = np.round(K, 2)
        self.setKMatrix(K)
