import numpy as np
import sympy as sp

class LeastSquaresApproximator():
    def __init__(self,) -> None:
        pass

    def innerProduct(self, upperLimit: int, lowerLimit: int, 
                     funcA, funcB, funcW) -> any:
        x = sp.Symbol("x")
        func = funcA*funcB*funcW
        product = sp.integrate(func, (x, upperLimit, lowerLimit)).evalf()
        return product
        
    def evaluate(self, func: str, upperLimit: int, lowerLimit: int, 
                 funcW: str|int=1, basis: list[str]|int=1):
        try:
            for index, funcB in enumerate(basis):
                basis[index] = sp.sympify(funcB)
            func = sp.sympify(func)
            funcW = sp.sympify(funcW)
        except sp.SympifyError as e:
            raise ValueError(e.args[0])
        matrixA, matrixB = [], []
        for line in range(len(basis)):
            matrixA.append([])
            product = self.innerProduct(upperLimit, lowerLimit, func, basis[line], funcW)
            matrixB.append([product])
            for col in range(len(basis)):
                product = self.innerProduct(upperLimit, lowerLimit, basis[col], basis[line], funcW)
                matrixA[line].append(product)
        matrixA, matrixB = np.array(matrixA), np.array(matrixB)
        result = np.linalg.solve(matrixA, matrixB)
        aproxFunc = result[0]*basis[0]
        for index in range(1, len(basis)):
            aproxFunc = aproxFunc + result[index]*basis[index]
        return aproxFunc


if __name__ == "__main__":
    app = LeastSquaresApproximator()
    aproxFunc = app.evaluate("sin(x)", -1, 1, basis=["1", "x", "x**2"])
    print(aproxFunc)