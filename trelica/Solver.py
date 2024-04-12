from Trelica import Trelica
import sympy as sp
import numpy as np


class Solver:
    """
    Essa classe Resolve uma treliça sujeita a cargas externas constantes,
    determinando os deslocamentos de seus nós e os esforços internos de seus elementos.
    Isso é feito pela biblioteca Sympy, que serve para  resolução computacional de problemas matemáticos
    (sistemas lineares, nesse caso).
    """

    def __init__(self, trelica):

        self.trelica = trelica
        self.nodes = trelica.nodes
        self.size = 2 * len(self.trelica.nodes)
        self.K = trelica.getKMatrix()

        self.uCondContorno = np.array([-1] * self.size).reshape(self.size, 1)  # vetor u incompleto
        self.apoiosCondContorno = [None] * self.size  # vetor f incompleto
        self.cargasExternas = trelica.cargasExternas
        self.forcasApoios = [None] * self.size
        self.forcasExternas = [None] * self.size
        self.X = sp.zeros(self.size, 1)

    def setCondicoesContorno(self):
        n = self.size
        self.apoiosCondContorno = sp.Matrix([sp.symbols('R{}'.format(j + 1)) for j in range(n)])
        for node in self.nodes:
            key = node.key
            if node.type == 'apoio_fixo':
                self.uCondContorno[2 * key - 2] = 0
                self.uCondContorno[2 * key - 1] = 0

            if node.type == 'apoio_livre_horizontal':
                self.uCondContorno[2 * key - 2] = 0
                self.apoiosCondContorno[2 * key - 1] = 0
            if node.type == 'apoio_livre_vertical':
                self.uCondContorno[2 * key - 1] = 0
                self.apoiosCondContorno[2 * key - 2] = 0

        for i in range(self.size):
            if self.uCondContorno[i] is None:
                self.uCondContorno[i] = -1

        self.uCondContorno = sp.Matrix(self.uCondContorno)
        for i in range(self.size):
            expr = self.uCondContorno[i]
            if expr.evalf() == -1:
                self.uCondContorno[i] = sp.symbols('q{}'.format(i + 1))
        # self.uCondContorno[1] = -0.005 # caso especial p/ questão da lista

    def setForcasExternas(self):
        cargasExternas = sp.Matrix(self.cargasExternas)
        self.F = cargasExternas + self.apoiosCondContorno

    def solve(self):
        self.setCondicoesContorno()
        self.setForcasExternas()
        K_sp = sp.Matrix(self.K)
        X = self.F - K_sp * self.uCondContorno

        #escolhendo os simbolos de maneira generalizada
        simbolos = []
        for i in range(self.size):
            q = sp.symbols('q{}'.format(i + 1))
            R = sp.symbols('R{}'.format(i + 1))
            simbolos.append(q)
            simbolos.append(R)

        sol = sp.solve(X, simbolos)
        return sol
