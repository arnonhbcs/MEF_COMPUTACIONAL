from Node import Node
import numpy as np
from math import sin, cos


class Element:
    """
    Essa classe representa os elementos finitos lineares de uma estrutura. Seus atributos são
    os nós que compreendem o elemento, seu comprimento, o ângulo que o elemento forma com o eixo x e a matriz
    de rigidez.
    """

    def __init__(self, A: Node, B: Node, key: int, q=0, EA=200*900):
        self.F = np.zeros((4, 1))
        self.K = np.zeros((4, 4))
        self.A = A
        self.B = B

        self.y = B.y - A.y
        self.x = B.x - A.x
        self.L = np.sqrt(self.x ** 2 + self.y ** 2)
        self.q = q

        self.EA = EA

        self.alpha = np.arctan2(self.y, self.x)
        self.setKMatrix(np.zeros((4, 4)))
        self.setFMatrix(np.zeros((4, 1)))
        self.computeKMatrix()
        self.computeFMatrix()
        # usado apenas para calcular forças internas
        self.key = key

    def getAlpha(self):
        return self.alpha

    def getKMatrix(self):
        return self.K

    def setKMatrix(self, K):
        self.K = K

    def setFMatrix(self, F):
        self.F = F

    def getNodes(self):
        return self.A, self.B

    def computeKMatrix(self):
        """
        Essa função retorna a matriz de rigidez do elemento estrutural
        :return: np.array
        """
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

    def computeFMatrix(self):
        """
        Retorna o vetor de forças consistentes (se houver)
        :return: np.array
        """
        c = cos(self.alpha)
        s = sin(self.alpha)
        # F = (self.q * self.L / 2) * np.array([[c], [s], [c], [s]])
        F = (self.q * self.L / 2) * np.array([[c], [s], [c], [s]])
        self.setFMatrix(F)

    def getFMatrix(self):
        return self.F
